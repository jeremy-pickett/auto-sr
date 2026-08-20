# Contract Enforcement

*Part 3 of the ASR deep-dive series. Subsystem: `backend/asr/contract/` — the restricted execution namespace, the Stage C validation pipeline, and the child-process runner that together turn a language model's Python output into something the harness can trust enough to run.*

## A note on terminology, up front

This document deliberately never calls any of this a "sandbox," except in this paragraph, which exists to explain why. The project's own `CLAUDE.md` states the rule plainly: "Generated code runs in a child process with memory rlimit and per-tick wall-clock kill, inside a restricted namespace (allowlisted builtins and NumPy surface — this is contract enforcement, never call it a sandbox)." The requirements spec backs this with two explicit lines: REQ-3.8 says "Sandboxing of generated code is out of scope. The host is assumed hardened," and REQ-3.10 says "The restricted execution namespace (REQ-7.9) is language-contract enforcement, not a security boundary. Do not describe it as a sandbox." REQ-16.8 repeats the exclusion in the out-of-scope list. The `namespace.py` module docstring says it a third way: "This is contract enforcement, not security (REQ-3.10, REQ-16.8) — full NumPy includes file access and the ordinary builtins include `open`, `eval`, `exec`, and `getattr`; keeping them out keeps a generated rule inside the language the experiment is defined over."

The distinction matters because it changes what the system is trying to do. A sandbox assumes a hostile actor and tries to survive deliberate attack — that's explicitly not this project's problem; the host machine is assumed already hardened, and a single-user local app isn't defending against its own operator. What this subsystem actually does is closer to a strict type system or a linter with teeth: it keeps every generated rule inside a small, well-defined language — vectorized NumPy operations over `Cells` objects, with no imports, no unbounded loops, no mutable instance state — so that (a) two rules can be compared apples-to-apples, (b) the harness's assumptions about determinism and read/write discipline actually hold, and (c) an accidental infinite loop or runaway allocation in generated code can be caught and killed without an attacker in the picture at all. Every mechanism below — the builtins dict, the NumPy proxy, the AST walker, the memory rlimit, the wall-clock kill — exists to enforce that language contract, not to resist adversarial code.

---

## 1. The restricted namespace

The whole of the restricted namespace lives in `backend/asr/contract/namespace.py` (63 lines) plus `backend/asr/contract/load.py` (44 lines), which assembles it into the dict that generated source actually executes inside.

### 1.1 Approved builtins

`namespace.py:16-17`:

```python
# REQ-7.9.1 — the whole approved builtin list.
APPROVED_BUILTINS = ("len", "range", "min", "max", "abs", "int", "float", "bool")
```

That's the entire list — eight names. Compare this to CPython's ordinary `builtins` module, which exposes on the order of 150 names including `open`, `eval`, `exec`, `getattr`, `setattr`, `__import__`, `compile`, `input`, `globals`, `vars`, and every exception type. None of that is reachable from generated rule code. `load.py:53-63` builds the actual `__builtins__` dict handed to `exec`:

```python
def restricted_builtins() -> dict:
    """The explicit __builtins__ dict for executing rule source.

    __build_class__ is the interpreter's own machinery for the `class`
    statement — without it `class Rule:` cannot execute at all. It is
    not exposed to rule logic; the static validator rejects any dunder
    reference in rule source.
    """
    allowed = {name: getattr(_python_builtins, name) for name in APPROVED_BUILTINS}
    allowed["__build_class__"] = _python_builtins.__build_class__
    return allowed
```

The one addition beyond the eight approved names, `__build_class__`, isn't a loophole — it's the interpreter's own internal hook for evaluating a `class` statement at all, not something rule code can call directly (the AST static checks reject any dunder reference outright, covered in §3). Without it, `exec(compile("class Rule: ..."))` simply cannot run; Python needs it to build any class object, generated or not.

What's conspicuously absent: `open` (no file access), `eval`/`exec`/`compile` (no code generation from strings), `getattr`/`setattr`/`hasattr`/`delattr` (no dynamic attribute access that could reach past the `Cells` wrapper or Python object internals), `__import__` (no imports — reinforced separately by the AST check on `ast.Import`/`ast.ImportFrom`), `input` (no stdin), `print` (no need — the harness reads return values, not stdout), `globals`/`locals`/`vars` (no namespace introspection), `super` (no class hierarchies — `Rule` has no allowed base class anyway), and `type` (no ad hoc class construction outside the one `class Rule:` statement the AST structure check already requires). If a generated rule needs a capability that isn't `len`, `range`, `min`, `max`, `abs`, `int`, `float`, or `bool`, it has to reach for it through the NumPy proxy or the pre-bound spatial helpers instead — there's no back door through the builtins.

### 1.2 The approved NumPy surface

`namespace.py:19-33`:

```python
# REQ-7.9.2 — the whole approved NumPy surface.
APPROVED_NUMPY_FUNCTIONS = (
    "zeros", "ones", "full", "zeros_like", "ones_like", "full_like",
    "where", "minimum", "maximum", "clip", "abs", "sign", "mod",
    "floor_divide", "logical_and", "logical_or", "logical_not",
    "logical_xor", "sum", "count_nonzero",
)
APPROVED_NUMPY_DTYPES = ("uint8", "uint16", "int32", "float32", "bool_")

# Array methods generated code may call (REQ-7.9.2). Arrays are real
# ndarrays, so this list is enforced by the static validator, not here.
APPROVED_ARRAY_METHODS = ("astype", "copy", "sum")

# np.random is deliberately absent (REQ-7.9.4): randomness reaches
# generated code only through the Dice facade, only in make_start.
```

Twenty functions, five dtypes, three array methods. This is enough to build array construction (`zeros`/`ones`/`full`/the `_like` variants), elementwise selection and clamping (`where`, `minimum`, `maximum`, `clip`), arithmetic-adjacent primitives (`abs`, `sign`, `mod`, `floor_divide`), boolean combination (`logical_and`/`_or`/`_not`/`_xor`), and aggregation (`sum`, `count_nonzero`) — everything a vectorized cellular-automaton `step` needs to compute a next grid from a current one and its neighbors. What it deliberately withholds: `np.random` (the comment is explicit — REQ-7.9.4, "Randomness reaches generated code only through the `Dice` facade, and only in `make_start`," per REQ-7.4.1 — no other source of nondeterminism can slip into `step`); linear algebra (`np.dot`, `np.matmul`, anything from `np.linalg`); reductions that could break vectorization discipline or leak information a rule shouldn't have, like `np.argmax`/`np.argsort`/`np.unique`; I/O (`np.load`/`np.save`/`np.genfromtxt` — full NumPy's file access is exactly the kind of full-language surface REQ-7.9's docstring calls out as a reason to restrict it); and reshape/broadcast trickery (`np.reshape`, `np.tile`, fancy indexing helpers) that could let a rule dodge the fixed grid shape.

The proxy object that actually enforces this at runtime is `ApprovedNumpy`:

```python
class ApprovedNumpy:
    """Only the approved names respond; everything else raises the
    ordinary AttributeError a missing name would.
    """

    __slots__ = ()

    def __repr__(self):
        return "<approved numpy surface (spec section 7.9)>"


for _name in APPROVED_NUMPY_FUNCTIONS + APPROVED_NUMPY_DTYPES:
    setattr(ApprovedNumpy, _name, staticmethod(getattr(np, _name)))

approved_numpy = ApprovedNumpy()
```

This is a genuinely minimal design: rather than writing an `__getattr__` allowlist-check, the module simply never sets any attribute on the class except the 25 approved names, using `__slots__ = ()` to prevent even instance-level attribute assignment. `np.argmax` accessed as `np.argmax` on this object doesn't get intercepted and rejected with a custom message — it just isn't there, so Python raises the same plain `AttributeError` it would for any missing name. `load.py:23` binds this single shared instance into every rule's namespace as the name `np`, so from inside generated code, `np` *is* `approved_numpy`, never the real `numpy` module.

Because `ApprovedNumpy` only forwards attribute access — it does not intercept method calls on the arrays those functions return — the array-method restriction (`astype`, `copy`, `sum` only) can't be enforced by the proxy object at all: a real `ndarray` responds to dozens of methods (`.reshape()`, `.tolist()`, `.argmax()`, `.tobytes()`, …) regardless of how it was constructed. That's why the comment on `APPROVED_ARRAY_METHODS` says "enforced by the static validator, not here" — this is one of the few restrictions that has no runtime enforcement point and depends entirely on the AST walker in `validator.py` catching every `.method()` call statically before the code ever executes (see §3.5).

### 1.3 What full access would let a generated rule do

The docstring names the two riskiest things directly: "full NumPy includes file access and the ordinary builtins include `open`, `eval`, `exec`, and `getattr`." Concretely, if the namespace exposed the real `numpy` module and the real `builtins`, a generated `step` method — remember, this is LLM-authored code, running on every tick of every run — could call `open(path, "w")` to write anywhere the process's file permissions allow, `np.load`/`np.save` to read or write files via NumPy's own I/O layer, `eval`/`exec` to run arbitrary strings as code (including strings assembled at runtime, defeating any static check entirely), `getattr(obj, name_from_a_variable)` to reach attributes the static AST walker can't see because the name isn't a literal in the source, or `__import__("os")` to reach the entire standard library, including subprocess spawning and network sockets. None of this requires malice from the model — it only requires the model reaching for the tool that happens to solve the problem in front of it, the way any LLM asked to "write Python" will reach for `open()` if given the chance. Restricting the namespace to eight builtins and twenty NumPy functions makes those tools simply not exist for the rule to reach for, which is a much stronger guarantee than hoping the model doesn't.

### 1.4 Governance: additions require a REQ identifier

`namespace.py:8-9`: "Additions to either list are a spec change requiring a new REQ identifier (REQ-7.9.3)." `CLAUDE.md` repeats this as a project-wide hard rule: "Additions to the `Dice` surface or the approved builtins/NumPy lists are spec changes requiring new REQ identifiers, not implementation decisions." REQ-7.9.3 in the spec states it as tersely as the code comment does.

The implication is structural, not procedural. Because Stage A's coverage map and Stage B's prompt template both describe the *current* approved surface to the model (see `templates.approved_numpy_surface()`, referenced from `pipeline.py:481`), and because the validator's static checks (§3) hard-code the same lists, widening either list is not a config change or a bugfix — it changes what class of rule the generator is even capable of producing, which changes the shape of the whole rule-space the coverage map is trying to describe. Treating it as a spec change (a new `REQ-` identifier, a line in `documents/asr-requirements-v3.md`, presumably a rationale entry in the spec's §2 decision log) keeps that shift auditable and deliberate rather than something that drifts in through an unreviewed PR that "just adds `np.argsort`, what's the harm." It also means a future maintainer — or a future instance of Claude working on this repo — cannot patch in a new NumPy function to unblock one stuck generation attempt without going through the same governance the original 20 went through.

---

## 2. Stage C validation pipeline — the seven steps in order

REQ-7.8 lists seven checks every generated rule passes before entering the library as `ok`. Steps 1–3 (structure, static, declaration match) live in `backend/asr/contract/validator.py`, called through the single entry point `validate_source`. Steps 4–7 (load, trial run, reproducibility, repair) are orchestrated by `backend/asr/generation/pipeline.py`, which calls `validate_source` first and then drives the remaining steps itself. `validator.py:1-8` frames the whole thing:

> "Every rejection carries the failing check by name plus the specific error text — that pair is what the repair prompt gets (REQ-10.4) and what the rejections table records (REQ-7.11)."

The single top-level function, `validator.py:53-67`:

```python
def validate_source(source: str, declared: dict, simplicity_limit: int) -> None:
    """Run structure, static, and declaration-match checks in order
    (REQ-7.8 steps 1–3). Raises Rejection on the first failure.

    `declared` is what Stage A declared, as plain values: kinds,
    neighbors, reach, uses, reads, modifiers, semantic_slots, assign.
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as bad:
        raise Rejection("structure", f"the source does not parse: {bad}") from None
    rule = _check_structure(tree)
    constants = _read_constants(rule)
    _check_static(rule, constants, simplicity_limit)
    _check_declaration_match(constants, declared)
```

Every failure raises `Rejection`, a small dataclass exception that carries exactly the two pieces of information the rest of the system needs:

```python
@dataclass
class Rejection(Exception):
    """One failed validation check: the check's name and the specific
    error, exactly what repair and the rejections table need.
    """

    failed_check: str
    message: str

    def __str__(self):
        return f"{self.failed_check}: {self.message}"
```

`validate_source` short-circuits on the first failure — a rule that fails structure never reaches the static checks, and one that fails static checks never reaches declaration match. This is deliberate ordering: each stage assumes the previous stage's invariants hold. The static checks, for instance, walk `rule.body` looking for `ast.FunctionDef` nodes named `step` and `make_start` — that lookup only makes sense once structure has already confirmed exactly one `class Rule:` with exactly those methods exists.

### Step 1 — Structure (`_check_structure`, `validator.py:73-127`)

This confirms the module is *shaped* like a rule at all, before anything about its content is inspected: exactly one top-level `class Rule:`, no base classes, no decorators, no metaclass, and a class body containing only the nine declared constants and the three required methods.

```python
def _check_structure(tree: ast.Module) -> ast.ClassDef:
    """Exactly one top-level `class Rule:` with no bases, decorators,
    or metaclass; a class body of approved constants and the three
    methods (REQ-7.1).
    """
    statements = [
        node for node in tree.body
        if not _is_docstring(node)
    ]
    if len(statements) != 1 or not isinstance(statements[0], ast.ClassDef):
        raise Rejection(
            "structure",
            "the module must contain exactly one top-level class definition "
            "and nothing else",
        )
    rule = statements[0]
    if rule.name != "Rule":
        raise Rejection("structure", f"the class must be named Rule, not {rule.name}")
    if rule.bases or rule.keywords or rule.decorator_list:
        raise Rejection(
            "structure", "Rule may not have base classes, decorators, or a metaclass"
        )

    seen_methods = []
    for node in rule.body:
        if _is_docstring(node):
            continue
        if isinstance(node, ast.FunctionDef):
            if node.name not in REQUIRED_METHODS:
                raise Rejection(
                    "structure",
                    f"unexpected method {node.name!r}; only "
                    f"{REQUIRED_METHODS} are allowed",
                )
            if node.decorator_list:
                raise Rejection("structure", f"{node.name} may not have decorators")
            seen_methods.append(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if not isinstance(target, ast.Name) or target.id not in DECLARED_CONSTANTS:
                    raise Rejection(
                        "structure",
                        "class-body assignments are limited to the declared "
                        f"constants {DECLARED_CONSTANTS}",
                    )
        else:
            raise Rejection(
                "structure",
                f"unexpected statement in the class body: {ast.dump(node)[:80]}",
            )
    missing = [name for name in REQUIRED_METHODS if name not in seen_methods]
    if missing:
        raise Rejection("structure", f"Rule is missing methods: {missing}")
    return rule
```

`REQUIRED_METHODS = ("__init__", "make_start", "step")` and `DECLARED_CONSTANTS = ("KINDS", "NEIGHBORS", "REACH", "USES", "READS", "MODIFIERS", "SEMANTIC_SLOTS", "ASSIGN", "SUGGESTED_DISPLAY")` (`validator.py:22-26`). Anything that isn't a docstring, a `FunctionDef` named one of the three required methods, or an `Assign`/`AnnAssign` targeting one of the nine declared constants is rejected outright — including any top-level statement outside the class at all. The repo's own test suite (`tests/test_validator.py:115-119`) checks exactly this with `source = "x = 1\n" + inspect.getsource(life.Rule)` — a single stray module-level statement in front of an otherwise-perfect rule fails structure.

A realistic failure at this stage: a model that decides to define a small helper function alongside the class —

```python
def _neighbor_sum(cells):
    ...

class Rule:
    ...
```

— fails immediately, because `_check_structure` requires the module body (after stripping docstrings) to contain *exactly one statement*, and that statement must be the `ClassDef`. There is no allowance for helper functions, even pure ones; every capability a rule needs has to come from the pre-bound namespace (§1) or be inlined into `step`/`make_start` directly.

### Step 2 — Static checks (`_check_static`, `validator.py:166-275`)

Covered in full depth in §3 below, since the task calls it out separately. In outline, this is an `ast.walk` over the whole class body checking, in order: no imports; no `while` loops; `for` loops only over a literal-bounded `range` or literal tuple/list; no underscore attribute access; no dunder names; every touched property (core, derived, or modifier) is declared in the matching list; every `np.` attribute access is on the approved surface; no write targets a derived/modifier/slot array; every `look`/`move` call uses literal, in-neighborhood offsets and permitted headings; `self.dice` and any `self` assignment are banned inside `step`; the simplicity-limit node count; and every non-`np`/`self` method call is one of `astype`, `copy`, `sum`, `chance`, `integers`, or `choice`.

### Step 3 — Declaration match (`_check_declaration_match`, `validator.py:426-455`)

Covered in §4 below.

### Step 4 — Load check

This step lives in the generation pipeline, not the validator module, because it needs a fully-built `Declaration` (which supplies the bound spatial helpers and semantic-slot constants) rather than just the raw declared values structure/static/match work from. `pipeline.py:527-533`:

```python
        # Step 4: load into the restricted namespace.
        try:
            load_rule_class(source, declaration)
        except Exception:
            raise Rejection(
                "load", traceback.format_exc(limit=1).strip()[-500:]
            ) from None
```

`load_rule_class` (`load.py:37-44`) is the same function the child process uses to actually run the rule for real (§5) — the load check literally does the load a production run would do, just without executing anything beyond class-body evaluation:

```python
def load_rule_class(source: str, declaration: Declaration):
    """Execute rule source in its namespace and hand back the class."""
    namespace = build_namespace(declaration)
    exec(compile(source, "<rule>", "exec"), namespace)  # noqa: S102 - the whole product
    rule_class = namespace.get("Rule")
    if rule_class is None:
        raise ValueError("the source did not define a class named Rule")
    return rule_class
```

`build_namespace` (`load.py:18-34`) is what assembles the dict `exec` runs against — `__builtins__` from `restricted_builtins()`, `np` bound to `approved_numpy`, `make_cells`, `HEADING`, the spatial helpers from `bind_helpers(declaration.neighbors, declaration.reach)`, and one enum-like class per semantic slot (built dynamically so a slot named `"mood"` with values `["calm", "restless"]` becomes a class `MOOD` in the namespace with `MOOD.calm == 0`, `MOOD.restless == 1`, per REQ-5.2.1's requirement that slot values are named constants, never bare strings).

This step catches exceptions raised purely by *executing the class body and its method definitions* — not by running `step` or `make_start` — since `exec` on a `class` statement evaluates default arguments, decorators (already banned), and any class-body expression, but does not call `__init__`, `make_start`, or `step`. A realistic failure here: a rule whose `SEMANTIC_SLOTS` declares a slot the code then references as, say, `MODE.fast` when the slot was actually named `speed` (so the namespace only defines `SPEED`, not `MODE`) — this passes structure and static checks (both operate purely syntactically, with no knowledge of what names actually exist in the namespace) but raises `NameError: name 'MODE' is not defined` the moment `exec` tries to evaluate the class body, which step 4 catches and reports as a `"load"` rejection.

### Step 5 — Trial run

`pipeline.py:551-572`, `_trial_run`:

```python
def _trial_run(source, declaration, width, height):
    try:
        result = run_in_child(
            source, declaration, TRIAL_SEED, width, height, TRIAL_TICKS,
            settings.tick_timeout_seconds, settings.run_memory_limit_mb,
        )
    except RuleCrashed as crashed:
        raise Rejection("trial_run", str(crashed)[-800:]) from None
    if result.stopped_because == "too_slow":
        raise Rejection(
            "trial_run",
            f"a tick exceeded the {settings.tick_timeout_seconds}s budget",
        )
    for record in result.ticks:
        top = int(record.arrays["kind"].max())
        if top >= declaration.kinds:
            raise Rejection(
                "trial_run",
                f"kind {top} at tick {record.tick} is outside the declared "
                f"range 0..{declaration.kinds - 1}",
            )
    return result
```

`TRIAL_TICKS = 10` and `TRIAL_SEED = 12345` (`pipeline.py:30-31`). Per REQ-7.8 step 5 and REQ-7.6.1, this runs at the **full configured grid size** (`width`/`height` default to `settings.grid_width`/`grid_height`, 200×200), not a cheap small grid — the spec's rationale, stated directly in REQ-7.6.1: "Ten ticks at 200×200 is nearly free vectorized and catches a timeout directly rather than inferring it from the AST." This is the step that actually executes `make_start` and `step` for the first time, inside the child process described in §5, and it's where several classes of runtime-only failure surface: an exception raised by `step` itself (caught as `RuleCrashed`, wrapped as a `"trial_run"` rejection), a hung or slow tick (`stopped_because == "too_slow"`, which the child process's own wall-clock kill produces — see §5), or a kind value outside the declared `KINDS` range, checked explicitly here by inspecting `record.arrays["kind"].max()` against `declaration.kinds` on every one of the ten ticks.

REQ-7.5 ("`step` must not modify the grid it receives") is also enforced here, but not by an explicit check in `_trial_run` — it's enforced structurally, by `run.py`'s `_freeze` function marking every array in the grid `write=False` before handing it to `step` (`run.py:105-114`). A rule that tries an in-place mutation gets a `ValueError` from NumPy itself at the moment of the write, which propagates up as an uncaught exception inside the child and surfaces as a `RuleCrashed`, caught by `_trial_run` and reported as `"trial_run"`. The project's own bad-rule fixture for this, `tests/bad_rules/mutates_input.py`, demonstrates it concretely:

```python
    def step(self, cells):
        grid = cells.kind
        grid[0, 0] = 1
        return make_cells(grid.copy())
```

This slips past every static check by design (nothing about `grid[0, 0] = 1` is syntactically distinguishable from a legitimate local mutation of a freshly-copied array), and the corresponding test (`tests/test_validator.py:66-79`) confirms it's caught at trial run with a message containing "read-only" — exactly what NumPy's `setflags(write=False)` protection produces.

### Step 6 — Reproducibility check

`pipeline.py:536-545`, inside `_validate`:

```python
        # Step 5: trial run at full grid size, ten ticks, fixed seed,
        # in the child process (REQ-7.6.1).
        first = _trial_run(source, declaration, width, height)
        # Step 6: reproducibility — same seed, identical fingerprints.
        second = _trial_run(source, declaration, width, height)
        first_prints = [record.state_fingerprint for record in first.ticks]
        second_prints = [record.state_fingerprint for record in second.ticks]
        if first_prints != second_prints:
            raise Rejection(
                "reproducibility",
                "two runs from the same seed produced different states",
            )
```

The trial run executes twice, both times seeded with the same fixed `TRIAL_SEED`, and the two runs' per-tick `state_fingerprint` sequences (the computational fingerprint described in `CLAUDE.md`'s state-model summary — "all future-relevant state... exact bytes, floats never quantized") must match exactly. As REQ-7.8 step 6 itself notes: "This does not catch order-dependent random draws — a fixed-order loop reproduces perfectly. REQ-7.4.1 handles that class statically." In other words, a rule that draws randomness in a fixed sequence every tick (which the static `self.dice`-in-`step` check already forbids entirely, since `step` cannot touch `self.dice` at all) would reproduce fine and this check wouldn't catch it — that whole failure mode is closed off earlier, statically, rather than here. What this check *does* catch is nondeterminism from other sources — for example a rule that (hypothetically, since the approved surface doesn't offer an obvious way to do this) depended on Python's dict/set iteration order, or on floating-point operation order that could vary run to run for reasons outside the rule's own declared randomness. It's a safety net behind the static determinism guarantee, not a substitute for it.

### Step 7 — One repair attempt

Covered in §6.

---

## 3. The AST static checks in detail

`_check_static` (`validator.py:166-275`) is the single largest function in the module and the one doing the most distinct kinds of scanning. It receives the parsed `rule` `ClassDef`, the already-extracted `constants` dict (`KINDS`, `NEIGHBORS`, `REACH`, `USES`, `READS`, `MODIFIERS`, `SEMANTIC_SLOTS`, etc., as plain Python literals from step 1), and the configured `simplicity_limit` (default 40, from `SIMPLICITY_LIMIT` in settings). It runs several independent `ast.walk(rule)` passes, each looking for one category of violation.

### 3.1 Imports, `while`, and malformed `for`

```python
    for node in ast.walk(rule):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise Rejection("static", "imports are not allowed (REQ-7.2)")
        if isinstance(node, ast.While):
            raise Rejection("static", "while loops are banned outright (REQ-7.6.1)")
        if isinstance(node, ast.For):
            _check_for_loop(node)
        if isinstance(node, ast.Attribute):
            if node.attr.startswith("_"):
                raise Rejection(
                    "static",
                    f"underscore attribute access ({node.attr!r}) is not allowed",
                )
        if isinstance(node, ast.Name) and node.id.startswith("__"):
            raise Rejection("static", f"the name {node.id!r} is not allowed")
```

Any `ast.Import` or `ast.ImportFrom` node anywhere in the class body is an unconditional rejection — REQ-7.2's "no imports" is enforced with zero exceptions, not even for standard-library modules that would seem harmless. `ast.While` is banned *outright*, with no conditions under which a `while` loop is acceptable — the rationale in REQ-7.6.1 is direct: "Vectorized rules have no legitimate use for it," and separately, "`while True: pass` is one node," meaning the simplicity-limit node count (§3.4) cannot bound runtime the way it bounds structural complexity, so `while` has to be excluded categorically rather than counted. `tests/bad_rules/while_loop.py` is exactly this:

```python
    def step(self, cells):
        total = 0
        while total < 3:
            total = total + 1
        return make_cells(cells.kind.copy())
```

— rejected immediately, regardless of the fact that this particular loop obviously terminates; the ban is on the construct, not a runtime analysis of whether it happens to halt.

Every attribute access whose name starts with `_` is rejected, and every bare name starting with `__` is rejected. This closes off `Cells`'s private surface (`_arrays`, `_set`, `_has`, `_names`, `_shape` — all underscore-prefixed by design in `engine/cells.py:34,65-75`, specifically so this static check keeps them out of reach) as well as any attempt to reach Python's own dunder machinery (`__class__`, `__dict__`, `__globals__`, `__subclasses__`, and the like — the classic routes by which sandboxed-Python escapes are built in other systems, closed here not by runtime interception but by simply never letting the name appear in the source at all).

### 3.2 The bounded-`for` check

```python
def _check_for_loop(node: ast.For) -> None:
    """for loops only over range(n) with literal n <= 8, or a literal
    tuple or list — never a grid dimension (REQ-7.6.1).
    """
    iterated = node.iter
    if isinstance(iterated, ast.Call) and isinstance(iterated.func, ast.Name):
        if iterated.func.id == "range" and len(iterated.args) == 1:
            bound = iterated.args[0]
            if isinstance(bound, ast.Constant) and isinstance(bound.value, int):
                if bound.value <= 8:
                    return
                raise Rejection(
                    "static", f"range({bound.value}) exceeds the literal limit of 8"
                )
        raise Rejection(
            "static",
            "for loops may only iterate range(n) with a literal n <= 8, "
            "or a literal tuple or list (REQ-7.6.1)",
        )
    if isinstance(iterated, (ast.Tuple, ast.List)):
        for element in iterated.elts:
            if not isinstance(element, (ast.Constant, ast.Attribute)):
                raise Rejection(
                    "static", "loop tuples/lists must hold literal values"
                )
        return
    raise Rejection(
        "static",
        "for loops may only iterate range(n) with a literal n <= 8, or a "
        "literal tuple or list — never a grid dimension (REQ-7.6.1)",
    )
```

This is where REQ-7.6.1's "runtime limit is a separate mechanism" bites hardest: `for row in range(len(cells.kind)):` would be indistinguishable from a bounded loop *by node count* — it's a single `ast.For` — but its actual iteration count scales with the grid's height, which at production grid size (200) is far more expensive than the intent of a small fixed-count loop, and worse, is exactly the kind of construct that would let a rule accidentally reintroduce cell-by-cell iteration into what's supposed to be a vectorized system. `_check_for_loop` closes this by requiring the loop bound to be a *literal* integer no greater than 8, or iteration over a literal tuple/list (each element itself a `Constant` or `Attribute`, e.g. iterating over `(HEADING.n, HEADING.e, HEADING.s, HEADING.w)`). `tests/bad_rules/for_over_grid.py` demonstrates the rejected case directly:

```python
    def step(self, cells):
        fresh = cells.kind.copy()
        for row in range(len(cells.kind)):
            fresh = fresh
        return make_cells(fresh)
```

`len(cells.kind)` is a `Call`, not a `Constant`, so the `isinstance(bound, ast.Constant)` check fails and the function falls through to the final `raise Rejection(...)` — rejected as `"static"` regardless of what the loop body does, because the loop bound itself is disqualifying.

### 3.3 Property-read discipline

```python
    # Property discipline over the whole class: reads must be declared.
    for node in ast.walk(rule):
        for prop in _properties_touched(node):
            _check_property_read(prop, uses, reads, modifiers)
```

`_properties_touched` (`validator.py:311-336`) recognizes three ways a property name can appear: a direct attribute access (`cells.age`, but not `self.KINDS` or `np.something`, both explicitly excluded), a literal string second argument to one of the spatial helper functions (`PROPERTY_HELPERS = ("look", "move", "count_neighbors", "sum_neighbors")` — e.g. `look(cells, "age", -1, 0)`), or a keyword argument to `make_cells` (e.g. `make_cells(kind, energy=...)`). `_check_property_read` then classifies the name against three known sets — `OPTIONAL_CORE_PROPERTIES` (`energy`, `heading`, `memory`, from `engine/cells.py:15-19`) must be listed in `USES`; `DERIVED_PROPERTIES` (`age`, `changed_last_tick`, from `engine/cells.py:22-25`) must be listed in `READS`; and any name in `MODIFIER_CATALOG` (`weight`, `stubbornness`, `rate`, from `engine/modifiers.py:29+`) must be listed in `MODIFIERS`:

```python
def _check_property_read(prop, uses, reads, modifiers) -> None:
    if prop in OPTIONAL_CORE_PROPERTIES and prop not in uses:
        raise Rejection(
            "static", f"core property {prop!r} is not declared in USES"
        )
    if prop in DERIVED_PROPERTIES and prop not in reads:
        raise Rejection(
            "static", f"derived property {prop!r} is not declared in READS (REQ-7.7)"
        )
    if prop in MODIFIER_CATALOG and prop not in modifiers:
        raise Rejection(
            "static", f"modifier {prop!r} is not declared in MODIFIERS"
        )
```

`tests/bad_rules/undeclared_reads.py` is the canonical example: `READS = []` in the constants, but `step` contains `old = cells.age > 3` — `age` is a derived property, present in `DERIVED_PROPERTIES`, and absent from the (empty) `reads` list, so `_check_property_read` raises immediately.

### 3.4 The approved NumPy surface, enforced statically

```python
    # The approved surface: np.<name> and array methods (REQ-7.9.2).
    for node in ast.walk(rule):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == "np":
                approved = APPROVED_NUMPY_FUNCTIONS + APPROVED_NUMPY_DTYPES
                if node.attr not in approved:
                    raise Rejection(
                        "static",
                        f"np.{node.attr} is outside the approved NumPy surface "
                        "(REQ-7.9.2)",
                    )
```

This is a belt-and-suspenders check on top of the `ApprovedNumpy` proxy from §1.2 — the proxy would already raise `AttributeError` at runtime for `np.argmax`, but the static check catches it before any execution happens at all, which matters because it lets the *load check* (step 4) and the *trial run* (step 5) fail earlier and with a more specific message than a generic runtime `AttributeError` would give. `tests/test_validator.py:131-141` verifies this directly by taking the `life` fixture and substituting `count_neighbors(cells, "kind", 1)` with `np.argmax(cells.kind)`, then asserting the rejection's `failed_check == "static"` and that `"argmax"` appears in the message.

### 3.5 Writes to read-only arrays

```python
    # Writes: no assignment may target a derived, modifier, or slot
    # array (REQ-7.7) — as an attribute or through a subscript on one.
    protected = set(DERIVED_PROPERTIES) | set(MODIFIER_CATALOG) | set(slot_names)
    for node in ast.walk(rule):
        for target in _assignment_targets(node):
            named = _attribute_behind(target)
            if named is not None and named.attr in protected:
                raise Rejection(
                    "static",
                    f"{named.attr!r} is read-only to rule code (REQ-7.7)",
                )
```

`_assignment_targets` (`validator.py:354-359`) normalizes `ast.Assign`, `ast.AugAssign`, and `ast.AnnAssign` down to their target node(s); `_attribute_behind` (`validator.py:362-369`) unwraps any chain of subscripts to find the underlying `Attribute` — so `cells.age = v`, `cells.age[mask] = v`, and `cells.age += v` are all recognized as writes to `.age` regardless of subscripting. Any of those targeting a name in `DERIVED_PROPERTIES`, `MODIFIER_CATALOG`, or the rule's own `SEMANTIC_SLOTS` keys is rejected. `tests/bad_rules/writes_age.py` (`cells.age += 1`) and `writes_modifier.py` (`cells.weight += 1`) are the two hand-written fixtures for this; both are caught here, statically, before either array's actual read-only-ness (enforced separately at the `Cells` level via `__setattr__` raising `AttributeError` per `cells.py:56-60`, and the frozen-array mechanism from `run.py`) would even come into play.

### 3.6 Spatial helper discipline: `look` and `move`

```python
    # Spatial helper calls: literal offsets inside the declared
    # neighborhood; moves along permitted headings only (REQ-6.2.2).
    for node in ast.walk(rule):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "look":
                _check_look_call(node, offsets, constants)
            elif node.func.id == "move":
                _check_move_call(node, move_headings, constants)
```

with:

```python
def _check_look_call(node: ast.Call, offsets: set, constants: dict) -> None:
    if len(node.args) != 4:
        raise Rejection("static", "look takes (cells, prop, down, right)")
    down = _literal_int(node.args[2])
    right = _literal_int(node.args[3])
    if down is None or right is None:
        raise Rejection(
            "static", "look offsets must be literal integers (REQ-6.2.2)"
        )
    if (down, right) not in offsets:
        raise Rejection(
            "static",
            f"look offset ({down}, {right}) is outside the declared "
            f"{constants['NEIGHBORS']} neighborhood at reach {constants['REACH']}",
        )
```

`offsets` here is the full set of `(down, right)` pairs computed by `neighbor_offsets(constants["NEIGHBORS"], constants["REACH"])` (`engine/geometry.py:55+`) before the walk even starts (`validator.py:172`). `_literal_int` only accepts an `ast.Constant` int, or a unary-minus applied to one — no variable, no computed expression, can supply a `look` offset. `tests/bad_rules/computed_offset.py` demonstrates exactly the case that's meant to catch: `down = 1; near = look(cells, "kind", down, 0)` — `down` here is an `ast.Name`, not a literal, so `_literal_int` returns `None` and the call is rejected, even though the *value* it would resolve to (`1`) is perfectly legal; the point is that a static AST check can't evaluate variables, so requiring literals is what makes the whole in-neighborhood check possible at all. `tests/bad_rules/look_outside.py` shows the complementary failure — `look(cells, "kind", 2, 0)` under `REACH = 1`, a literal offset that's syntactically fine but numerically outside the declared neighborhood.

`_check_move_call` (`validator.py:402-420`) does the analogous thing for `move`, requiring the direction argument to be a literal `HEADING.<name>` attribute access and checking that heading against `allowed_move_headings(constants["NEIGHBORS"])` — `plus_4` permits only the four cardinal headings, `all_8` all eight. `tests/bad_rules/diagonal_move.py` is `NEIGHBORS = "plus_4"` with `move(cells, "kind", HEADING.ne)` — `ne` is a valid `HEADING` member but not one of the four cardinal directions `plus_4` allows, so it's rejected.

### 3.7 `step`-only invariants: determinism and no self-mutation

```python
    # step-only rules (REQ-7.4, REQ-7.4.1, REQ-7.6).
    step = methods["step"]
    for node in ast.walk(step):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == "self" and node.attr == "dice":
                raise Rejection(
                    "static", "self.dice may appear only in make_start (REQ-7.4.1)"
                )
        for target in _assignment_targets(node):
            named = _attribute_behind(target)
            if (
                named is not None
                and isinstance(named.value, ast.Name)
                and named.value.id == "self"
            ):
                raise Rejection(
                    "static", "step may not assign to self (REQ-7.4)"
                )
```

This walk is scoped to *only* the `step` method's subtree (`step = methods["step"]`, then `ast.walk(step)`), unlike every other check in this function which walks the whole class. Two things are forbidden inside `step` specifically: any reference to `self.dice` (REQ-7.4.1's core determinism guarantee — randomness is permitted only in `make_start`, never in `step`, closing off the ambiguity the spec calls out where "the same grid at two ticks has different futures because the RNG advanced"), and any assignment that ultimately targets `self.<anything>` (REQ-7.4's "no mutable state on the `Rule` instance"). `tests/bad_rules/dice_in_step.py` (`noise = self.dice.chance(0.5)` inside `step`) and `assigns_self.py` (`self.remembered = cells.kind` inside `step`) are the two corresponding fixtures.

### 3.8 The simplicity limit

```python
    counted = sum(
        isinstance(node, COUNTED_NODES) for node in ast.walk(step)
    )
    if counted > simplicity_limit:
        raise Rejection(
            "static",
            f"step has {counted} branch/loop/comprehension nodes; the "
            f"simplicity limit is {simplicity_limit} (REQ-7.6)",
        )
```

`COUNTED_NODES = (ast.If, ast.IfExp, ast.For, ast.While, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)` (`validator.py:30-33`) — note `ast.While` is in this list even though it's already unconditionally banned above; the two checks are independent and either alone would catch a `while`. `simplicity_limit` defaults to 40 (`SIMPLICITY_LIMIT` in `config.py:54`). REQ-7.6's rationale, from the spec's decision table: "Complexity must emerge from iteration, not rule richness. Unconstrained, the generator writes elaborate machines and the Rule 110 surprise never appears" — the limit exists to keep individual rules simple so that any interesting emergent behavior comes from the cellular automaton running many ticks, not from the single-tick rule itself being an elaborate program. `tests/bad_rules/too_complex.py` is the direct test of the boundary: 41 repeated `if width_is_never_zero: total = total + 1` statements, each contributing one `ast.If` to the count, pushing the total past the 40-node limit.

### 3.9 Approved array methods, checked statically

```python
    # Array methods anywhere: astype, copy, sum only — any other method
    # call on a non-np, non-self object is off the approved surface.
    for node in ast.walk(rule):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            owner = node.func.value
            if isinstance(owner, ast.Name) and owner.id in ("np", "self"):
                continue
            if node.func.attr not in APPROVED_ARRAY_METHODS + ("chance", "integers", "choice"):
                raise Rejection(
                    "static",
                    f"method .{node.func.attr}() is outside the approved "
                    "array surface (REQ-7.9.2)",
                )
```

This is where `APPROVED_ARRAY_METHODS = ("astype", "copy", "sum")` from §1.2 actually gets enforced — as noted there, `ApprovedNumpy` has no way to intercept a method call on the ndarray *values* its own functions return, so this static walk is the only enforcement point. It skips calls whose receiver is literally the name `np` or `self` (since `np.<function>(...)` calls and `self.dice.<method>(...)` calls are governed by the other checks), and for everything else — meaning any `.method()` call on what's presumably a `cells.<property>` array or an intermediate NumPy array — requires the method name be one of `astype`, `copy`, `sum`, or one of the three `Dice` facade methods `chance`, `integers`, `choice` (permitted here because `self.dice.chance(...)` etc. resolve to `owner.id == "self"`... actually the comment clarifies these are included for calls like `dice.chance(...)` where `dice` isn't literally named `self` inside a helper expression, keeping the `Dice` facade's own vocabulary available). A rule that calls, say, `cells.kind.argmax()` fails here regardless of what the earlier `np.<attr>` check would have caught, since `argmax` is neither an approved array method nor a `Dice` method.

---

## 4. Declaration match

`_check_declaration_match` (`validator.py:426-455`) is step 3 of REQ-7.8 and the shortest of the three functions `validate_source` runs, but it closes a distinct and important gap: everything above confirms the *implementation* is well-formed and internally consistent with its own declared constants (e.g., "if `READS` says `[]`, don't read `age`"). This check instead confirms the implementation's declared constants match what **Stage A separately declared** before Stage B ever saw the prompt — i.e., that Stage B didn't quietly rewrite the experiment Stage A proposed.

```python
def _check_declaration_match(constants: dict, declared: dict) -> None:
    """The implementation's constants must exactly match what Stage A
    declared — a mismatch means the implementation silently rewrote the
    experiment (REQ-7.8 step 3). READS included.
    """
    pairs = (
        ("KINDS", "kinds"),
        ("NEIGHBORS", "neighbors"),
        ("REACH", "reach"),
        ("USES", "uses"),
        ("READS", "reads"),
        ("MODIFIERS", "modifiers"),
        ("SEMANTIC_SLOTS", "semantic_slots"),
        ("ASSIGN", "assign"),
    )
    for constant_name, declared_name in pairs:
        implemented = constants.get(constant_name)
        wanted = declared.get(declared_name)
        if constant_name in ("USES", "READS", "MODIFIERS"):
            implemented = list(implemented or [])
            wanted = list(wanted or [])
        elif constant_name in ("SEMANTIC_SLOTS", "ASSIGN"):
            implemented = dict(implemented or {})
            wanted = dict(wanted or {})
        if implemented != wanted:
            raise Rejection(
                "declaration_match",
                f"{constant_name} is {implemented!r} but Stage A declared "
                f"{wanted!r}",
            )
```

`constants` here is the dict of plain Python literal values `_read_constants` extracted from the class body's `Assign`/`AnnAssign` statements (step 1). `declared` is the corresponding dict of values Stage A's JSON proposal actually specified, threaded in from `pipeline.py:_validate` (`pipeline.py:514-523`), which builds it directly from `proposal["kinds"]`, `proposal["neighbors"]`, etc. — the same JSON object the model returned from the Stage A prompt, before Stage B (a second, separate model call) wrote any implementation code at all.

Eight pairs are checked; `SUGGESTED_DISPLAY` is deliberately excluded from this list (it's advisory metadata per REQ-7.1.1 — "it never affects any fingerprint" — so it isn't held to exact-match discipline). List-typed fields (`USES`, `READS`, `MODIFIERS`) are normalized through `list(... or [])` before comparison so that Stage A omitting a key and Stage B implementing it as an empty list compare equal rather than falsely mismatching on `None` vs `[]`; dict-typed fields (`SEMANTIC_SLOTS`, `ASSIGN`) get the same treatment via `dict(... or {})`.

`tests/test_validator.py:82-92` demonstrates this directly and specifically calls out `READS` as the field this check is most likely to catch silently: a source file (`tests/bad_rules/declaration_mismatch.py`) declares `READS = ["age"]` and does in fact read `cells.age` in `step` — perfectly self-consistent, and it passes `validate_source` when checked against its own honest declaration. But the test then constructs a `declared` dict with `reads=[]` (simulating a Stage A proposal that never mentioned reading `age` at all) and re-validates the same source against that mismatched declaration — this time it fails with `failed_check == "declaration_match"` and a message containing `"READS"`. The scenario this guards against: Stage B, given some latitude in how it implements a rule, adds a capability (reading the age of a cell to decide its next state) that Stage A's English description and structured proposal never called for. Without this check, that rule would enter the library as a faithful implementation of a coverage-map slot it doesn't actually occupy — corrupting the very coverage accounting (REQ-8.1, REQ-8.5, REQ-8.6) the whole generation loop depends on to know what's already been tried.

---

## 5. The child-process runner

`backend/asr/contract/child.py` (136 lines) is the mechanism referred to throughout `CLAUDE.md` as "a child process with memory rlimit and per-tick wall-clock kill." Its own module docstring states the design rationale plainly:

> "Not sandboxing (REQ-3.10) — a different job entirely: Python cannot safely kill a runaway thread, and an infinite loop in generated code must not take the server down. The child streams one message per tick; the parent owns the wall clock and kills the child when a tick fails to arrive in time, recording the run as `too_slow`."

### 5.1 How the process is spawned

```python
def run_in_child(
    source: str,
    declaration: Declaration,
    seed: int,
    width: int,
    height: int,
    max_ticks: int,
    tick_timeout_seconds: float,
    memory_limit_mb: int,
    on_tick=None,
) -> RunResult:
    """Execute a run in a killable child process and stream it back.
    `on_tick` (parent-side) receives each TickRecord as it arrives —
    the generation stream's progress feed."""
    context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    child = context.Process(
        target=_child_main,
        args=(
            sender,
            source,
            declaration,
            seed,
            width,
            height,
            max_ticks,
            tick_timeout_seconds,
            memory_limit_mb,
        ),
        daemon=True,
    )
    child.start()
    sender.close()
```

Two design choices are called out in the module docstring and worth stating explicitly. First, `multiprocessing.get_context("spawn")` rather than the default fork-based context: "the child receives rule SOURCE, not a class, and loads it itself. That keeps every message picklable, which lets us use the spawn start method — forking a multi-threaded FastAPI worker risks deadlock." Fork duplicates the parent's entire memory space including whatever locks other threads happen to hold at that instant, which is unsafe under a multi-threaded server like FastAPI's uvicorn workers; spawn starts a genuinely fresh interpreter and only ships across what's explicitly passed. Second, the parent passes `source` (a string) and `declaration` (a picklable dataclass) across the process boundary, not a live `Rule` class object — a class object holding references to compiled code and closures over the restricted namespace wouldn't survive pickling cleanly across a spawn boundary anyway, and shipping source text is what lets the child rebuild the exact same restricted-namespace load the trial run and Stage C both depend on.

The transport is a `multiprocessing.Pipe(duplex=False)` — a one-directional OS pipe wrapped in Python's pickling `Connection` protocol, not shared memory and not a socket. The parent holds the read end (`receiver`); the child (through `sender`, passed as an argument) writes to it. Immediately after starting the child, the parent closes its own copy of `sender` (`sender.close()`) — standard pipe hygiene, ensuring the parent's read loop sees EOF/closure signals correctly once the child exits, rather than the pipe staying artificially "open" because the parent also held a writable handle to it.

### 5.2 The memory rlimit

`_child_main` (`child.py:100-136`) is the function that actually runs inside the spawned child process, and the very first thing it does — before importing anything else, before touching the rule source at all — is set the memory limit:

```python
def _child_main(
    sender,
    source,
    declaration,
    seed,
    width,
    height,
    max_ticks,
    tick_timeout_seconds,
    memory_limit_mb,
):
    limit = memory_limit_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    try:
        from asr.contract.load import load_rule_class
        ...
```

`resource.setrlimit(resource.RLIMIT_AS, (limit, limit))` sets both the soft and hard limits on `RLIMIT_AS` — the process's total virtual address-space size — to `memory_limit_mb * 1024 * 1024` bytes. `memory_limit_mb` comes from `settings.run_memory_limit_mb`, defaulting to 2048 MB (`RUN_MEMORY_LIMIT_MB` in `config.py:53`). Once set, any attempt by the process — whether by the rule's own NumPy allocations or the interpreter's normal bookkeeping — to grow its address space past that ceiling causes the allocation to fail at the OS level (typically surfacing in Python as a `MemoryError`), which is exactly the kind of accidental-runaway-allocation failure a generated rule with, say, an off-by-one in an array-construction call could trigger. Setting both soft and hard limits to the same value (rather than leaving headroom between them) means the child process can't raise its own limit back up even if it tried — though again, per the terminology note in §0, this isn't framed as resisting a deliberately hostile rule trying to escape the limit; it's a blunt, reliable backstop against an accidental multi-gigabyte allocation eating the host.

### 5.3 The per-tick wall-clock kill

This mechanism spans both sides of the pipe. On the child side, `run_rule` (called from inside `_child_main`, via the `on_tick` callback) sends one message per completed tick as soon as it's computed:

```python
        result = run_rule(
            rule_class,
            declaration,
            seed,
            width,
            height,
            max_ticks,
            tick_timeout_seconds,
            on_tick=lambda record: sender.send(("tick", record)),
        )
```

The parent's read loop is where the actual timeout enforcement happens:

```python
    ticks = []
    # The first message covers interpreter start-up, loading the rule,
    # and building the whole starting grid; be generous once.
    patience = tick_timeout_seconds + 30.0
    try:
        while True:
            if not receiver.poll(patience):
                # The tick never arrived: a hung or endless tick. The
                # parent owns the clock and swings the axe (REQ-7.6.1).
                child.kill()
                child.join()
                if not ticks:
                    raise RuleCrashed(
                        "the run produced no ticks at all before the timeout"
                    )
                return assemble_result(ticks, "too_slow", None)
            kind, payload = receiver.recv()
            if kind == "tick":
                ticks.append(payload)
                if on_tick:
                    on_tick(payload)
                # After tick 0 the per-tick budget applies, plus slack
                # for serialization.
                patience = tick_timeout_seconds + 1.0
            elif kind == "done":
                return assemble_result(ticks, payload["stopped_because"], payload["loop_length"])
            elif kind == "crashed":
                raise RuleCrashed(payload)
    finally:
        receiver.close()
        if child.is_alive():
            child.kill()
        child.join()
```

`receiver.poll(patience)` blocks for up to `patience` seconds waiting for the next message; if nothing arrives in that window, the parent treats it as a hung or endless tick and calls `child.kill()` (SIGKILL, not a graceful terminate — the module docstring's framing is that "Python cannot safely kill a runaway thread," which is exactly why this uses OS-level process termination rather than any in-process signal or cooperative-cancellation mechanism that a genuinely stuck tick — e.g. inside a tight NumPy C loop — might not even be able to observe). Two different patience windows are used: the *first* wait (before any tick has arrived) is `tick_timeout_seconds + 30.0`, generous because it has to cover Python interpreter startup in the freshly-spawned child, loading and `exec`-ing the rule source, and building the entire tick-0 starting grid — none of which is the per-tick budget's concern. Every subsequent wait tightens to `tick_timeout_seconds + 1.0`, the configured per-tick budget (`TICK_TIMEOUT_SECONDS`, default 2.0 seconds, per `config.py:52`) plus one second of slack for pipe serialization overhead. If the timeout fires after at least one tick has already arrived, the run is recorded as `stopped_because="too_slow"` via `assemble_result(ticks, "too_slow", None)` — a real (partial) result with real ticks, not a bare error, which is what lets a rule that behaves fine for a while and then hangs still contribute whatever prefix of ticks it did complete. If the timeout fires before *any* tick arrived (including the generous first-message window), there's no usable partial result at all, and the parent raises `RuleCrashed("the run produced no ticks at all before the timeout")` instead.

The `finally` block is unconditional cleanup: close the parent's read end, and if the child process is somehow still alive at that point (e.g., a `RuleCrashed` was raised mid-loop from a `"crashed"` message, short-circuiting the normal `"done"` exit but leaving the child process itself possibly still finishing up), kill and join it. This guarantees no orphaned child process survives a `run_in_child` call regardless of which of the three exit paths (timeout, done, crashed) was taken.

The project's own test, `tests/test_child.py:31-66`, verifies this end to end with a deliberately pathological rule:

```python
HANGS_FOREVER = """
class Rule:
    KINDS = 2
    NEIGHBORS = "all_8"
    REACH = 1
    ...
    def step(self, cells):
        while True:
            pass
"""


def test_a_hung_tick_is_killed_by_the_parent_and_recorded_too_slow():
    # REQ-15.7: a deliberate endless tick is killed by the parent and
    # recorded as too_slow without taking the server down.
    declaration = Declaration(kinds=2, neighbors="all_8", reach=1)
    started = time.monotonic()
    result = run_in_child(
        HANGS_FOREVER, declaration, seed=1, width=6, height=6,
        max_ticks=10, tick_timeout_seconds=0.3, memory_limit_mb=4096,
    )
    assert result.stopped_because == "too_slow"
    assert result.ticks_run == 0  # only tick 0 completed
    assert time.monotonic() - started < 40  # killed, not waited out
```

Note this test passes raw source text directly to `run_in_child`, bypassing the static AST checks that would reject a `while` loop in production (§3.1) — which is intentional: it's testing the runtime kill mechanism in isolation from the static gate that would normally prevent this exact rule from ever reaching a child process at all. In production, `while True: pass` never gets this far, because `_check_static` rejects it during Stage C step 2, long before any process is spawned. This test exists specifically to prove the second line of defense (the wall-clock kill) also works, independently of whether the first line of defense (the static ban) is doing its job — defense in depth against the same failure mode.

### 5.4 How results and errors cross the process boundary

The transport format is plain Python object pickling over the `multiprocessing.Connection` — `sender.send((kind, payload))` on the child side, `receiver.recv()` on the parent side, where `kind` is one of three string tags (`"tick"`, `"done"`, `"crashed"`) and `payload` is, respectively, a `TickRecord` (a dataclass holding that tick's arrays, fingerprints, and metadata — defined in the engine's run module and constructed fresh each tick by `run_rule`), a small dict `{"stopped_because": ..., "loop_length": ...}`, or a string (a formatted traceback). There is no custom binary framing here — unlike the tick-playback wire format for the frontend, which REQ-11.5.1 requires use dense binary framing rather than JSON, this is an internal, same-machine, same-Python-version IPC channel, so ordinary pickling (which `multiprocessing.Connection` uses internally) is the appropriate choice; it's not a boundary the spec asks to be framed any more explicitly than this.

Error propagation is handled entirely inside `_child_main`'s own `try`/`except`:

```python
    try:
        from asr.contract.load import load_rule_class

        rule_class = load_rule_class(source, declaration)
        result = run_rule(
            rule_class,
            declaration,
            seed,
            width,
            height,
            max_ticks,
            tick_timeout_seconds,
            on_tick=lambda record: sender.send(("tick", record)),
        )
        sender.send(
            ("done", {
                "stopped_because": result.stopped_because,
                "loop_length": result.loop_length,
            })
        )
    except Exception:
        sender.send(("crashed", traceback.format_exc()))
    finally:
        sender.close()
```

Any exception — whether from `load_rule_class` failing to `exec` the source, or from `run_rule` raising while executing `make_start`/`step` — is caught by the blanket `except Exception:`, formatted with `traceback.format_exc()` (the full Python traceback as text, giving the parent something more diagnostically useful than a bare exception message), and sent across the pipe as a `"crashed"` message. On the parent side, `run_in_child` re-raises this as `RuleCrashed(payload)` (`child.py:91-92`) — a dedicated exception type whose module-level docstring states its role plainly: "The rule raised while running. Stage C treats this as a rejection; the message carries the child's traceback text." `tests/test_child.py:69-101` demonstrates this with a rule that returns `cells.deliberately_broken` — an unknown property name that `Cells.__getattr__` (`cells.py:48-54`) turns into an `AttributeError` with a distinctive message — and confirms `"deliberately_broken"` survives intact in the caught `RuleCrashed`'s string representation, i.e., the full traceback text really does make the round trip across the process boundary unmodified.

---

## 6. The repair attempt

REQ-7.8 step 7: "On rejection, return the specific failing check and error text to the model once. If the repair fails, mark `broken`, store the error, stop." This is implemented directly in `pipeline.py:generate_rule`, not in the `contract/` package — the contract package's job is producing a `Rejection` with a precise `failed_check`/`message` pair; what the pipeline does with that pair (retry once, then give up) is generation-orchestration logic that lives alongside the Stage A/B model calls it has to interleave with.

The flow, from `pipeline.py:229-253`:

```python
    emit("validating", {})
    repair_rendered = repair_raw = None
    failure = _validate(source, proposal, declaration, width, height)
    if failure is not None:
        emit("validation_failed", {
            "check": failure.failed_check, "error": failure.message,
        })
        # One repair attempt (REQ-7.8 step 7), told exactly what failed.
        emit("repairing", {})
        repair_rendered = templates.render(
            templates.load_template("repair.txt"),
            {
                "stage_b_prompt": stage_b_prompt,
                "previous_code": source,
                "failed_check": failure.failed_check,
                "error_text": failure.message,
            },
        )
        stage_started = time.perf_counter()
        repair_raw = model_call(repair_rendered)
        note_served("repair")
        log_step("repair (model call)", stage_started)
        source = _extract_source(repair_raw)
        emit("validating", {})
        failure = _validate(source, proposal, declaration, width, height)
```

This is a literal re-prompt of the model — a second, separate call to `model_call` (the same function used for Stage A and Stage B), against a rendered template that combines the *original* Stage B prompt, the *previous, failing* source code, and the exact `failed_check`/`error_text` pair the validator produced. The template itself, `backend/asr/generation/prompts/repair.txt`, is short and direct:

```
{stage_b_prompt}

YOUR PREVIOUS ATTEMPT
{previous_code}

WHAT FAILED
{failed_check}: {error_text}

Fix exactly what failed and return the complete corrected `class Rule:`
definition. Same format as before: no imports, no top-level statements
outside the class, no prose, no markdown fences. This is the only repair
attempt.
```

Note the template restates the *whole* original Stage B prompt (declared properties, the plugin contract, helper signatures, the `Dice` facade description, the approved NumPy surface, the simplicity limit) rather than a bare diff — the model gets the complete context it needs to produce a full corrected rule, plus the specific thing it got wrong, plus an explicit instruction ("This is the only repair attempt") that the template itself communicates to the model, matching the harness's own behavior.

The pipeline's own control flow structurally guarantees this happens at most once: `_validate` is called exactly twice in `generate_rule` — once before the `if failure is not None:` block, and once at the end of that same block, after the repair call. There is no loop, no recursion, no re-entry — the code path from "first validation failed" to "repair produced its own outcome" is linear and runs precisely one repair round trip. Whatever the second `_validate` call returns (a fresh `Rejection`, or `None` for success) is simply what `failure` holds when execution falls out of the `if` block, and everything downstream treats that final value as final — win or lose, that's the only shot.

Full provenance of the repair round-trip is retained regardless of outcome — `repair_rendered` and `repair_raw` are threaded into the `provenance` dict (`pipeline.py:271-272`) alongside the Stage A and Stage B renders/raws, and stored on the rule row (see §7) whether the rule ultimately becomes `ok` or `broken`. If the model was never invoked for repair (first validation passed outright), both fields stay `None`.

---

## 7. What happens to rejections

CLAUDE.md states the governing principle directly: "Broken rules and rejections stay in the library as generator-quality data." REQ-7.8.1 backs this: "Broken rules remain in the library permanently and appear in Stage A context." This subsystem's role in that is producing the `Rejection` (with its `failed_check`/`message` pair) and the `RuleCrashed` traceback that eventually gets persisted — the actual persistence is a storage-subsystem concern, but it's worth tracing the handoff concretely since it's the direct payoff of everything above being this precise about *which* check failed and *why*.

There are three distinct outcomes the pipeline can reach, all still resulting in something durable:

**A rule that fails Stage C validation (after the one repair attempt) becomes `status="broken"`.** `pipeline.py:279-296`:

```python
        rule_id = _store_rule(
            conn, proposal, source, provenance,
            status="broken",
            failed_check=failure.failed_check,
            error_text=failure.message,
            observed_shape=None,
            owner_uid=owner_uid,
            visibility=visibility,
            spark=spark,
        )
        _store_rejection(conn, proposal, failure.failed_check, rule_id)
```

`_store_rule` inserts into the `rules` table via `db.insert_rule` — the same table every `ok` rule lands in, with `status`, `failed_check`, and `error_text` columns (`db.py:38-40`) recording exactly what `Rejection.failed_check`/`.message` said, plus the *entire* generation provenance regardless of outcome: `stage_a_rendered`/`stage_a_raw`, `stage_b_rendered`/`stage_b_raw`, `repair_rendered`/`repair_raw` (`db.py:47-49`), the engine version, prompt-set hash, modifier-catalog hash, and helper version. This is the concrete mechanism behind the spec's claim that even failures carry full provenance (REQ-12.4) — a broken rule's row lets you reconstruct exactly what Stage A proposed, exactly what Stage B wrote (both before and after the repair attempt, if one happened), and exactly which named check rejected it and with what message.

`_store_rejection` (`pipeline.py:615-633`) additionally inserts a row into the dedicated `rejections` table:

```python
def _store_rejection(conn, proposal, failed_check, rule_id=None) -> None:
    """Broken rules keep their description in the rejections corpus
    (REQ-7.11) — the record of what the generator reached for and
    could not build."""
    conn.execute(
        """INSERT INTO rejections(created_at, rule_id, failed_check,
               stage_a_description, concepts_json, requested_shape,
               kinds, neighbors, reach, modifier_in_scope)
           VALUES(?,?,?,?,?,?,?,?,?,?)""",
        (
            db.now(), rule_id, failed_check,
            proposal.get("description"),
            json.dumps(proposal.get("concepts", [])),
            proposal.get("shape"),
            proposal.get("kinds"), proposal.get("neighbors"), proposal.get("reach"),
            (proposal.get("modifiers") or [None])[0],
        ),
    )
    conn.commit()
```

The `rejections` table (`db.py:97-109`) is a lighter-weight, purpose-built record distinct from the full `rules` row — it exists specifically to carry the Stage A *description* (the English-language proposal, before any code existed), its concept tags, requested shape, and geometry declaration, alongside the `failed_check` name, with a nullable `rule_id` foreign key back to the full row when one exists. This is exactly what REQ-7.11 asks for: "the Stage A description, its reasoning, its concept tags, and the failing check are retained." REQ-7.11.1 explains why this matters enough to warrant its own table and its own appearance in future Stage A context: "the simplicity limit rejects longer implementations, and richer English descriptions produce longer implementations. Rejections are therefore systematically biased against semantically rich descriptions, and the corpus under-represents exactly the region the semantic framing exists to explore. The bias is acceptable but must be measurable" — measuring that bias requires the rejected descriptions to actually be retained and queryable, not silently discarded.

**A rule that crashes during its canonical (post-validation) run also becomes `broken`, retroactively.** This is a distinct code path from the Stage C `broken` case above — the rule *passed* Stage C's trial run and reproducibility check, was stored as `status="ok"`, and only failed later, during the full-length canonical run that decides its behavior classification. `pipeline.py:326-336`:

```python
    except RuleCrashed as crashed:
        log_step("canonical run (child process, crashed)", stage_started)
        # It survived ten trial ticks but died in the long run: the
        # rule stays ok-with-history? No — a crash mid-run leaves no
        # usable history, so record the rule as broken after the fact.
        conn.execute(
            "UPDATE rules SET status='broken', failed_check=?, error_text=? WHERE id=?",
            ("canonical_run", str(crashed)[-2000:], rule_id),
        )
        conn.commit()
        _store_rejection(conn, proposal, "canonical_run", rule_id)
```

The comment's phrasing — "the rule stays ok-with-history? No" — makes the design decision explicit: a rule that survives ten trial ticks (Stage C's sample) but crashes partway through a full run (up to `max_ticks`, default 500) doesn't keep whatever partial run history it accumulated as a legitimate `ok` result; since a crash mid-run leaves no complete, trustworthy history to classify or play back, the row is updated in place to `status='broken'` with `failed_check="canonical_run"` (a check name that never appears in Stage C's own vocabulary — `structure`, `static`, `declaration_match`, `load`, `trial_run`, `reproducibility` — precisely because this is a distinct failure surface, the full-length run, not one of the seven Stage C gates), and the same `_store_rejection` call folds it into the rejections corpus exactly like a Stage C failure would.

**A failure in Stage A itself never reaches the `rules` table at all.** `pipeline.py:199-205` and `_record_generation_failure` (`pipeline.py:636-643`) handle this — a `GenerationFailed` (malformed JSON, an invalid proposal, a model safety refusal) is caught before any `Declaration` or source code exists, so there's no rule row to create; only a `rejections` row is inserted, with `rule_id=None` and the raw model response (truncated to 2000 characters) standing in for `stage_a_description`. This is the one outcome this subsystem's contract-enforcement machinery never sees at all — `validate_source`, the child-process runner, and everything in §1–6 only ever run once Stage A has already produced a structurally valid proposal; a Stage A failure short-circuits before any of it is invoked.

Across all three paths, the pattern is the same: the `Rejection`'s `failed_check`/`message` pair (or the `RuleCrashed` traceback text) produced by this subsystem is never discarded — it's threaded straight through into either the `rules` table's `failed_check`/`error_text` columns, the `rejections` table's `failed_check` column, or both, which is what lets "generator-quality data" (CLAUDE.md's phrase) mean something concrete: every documented failure mode above corresponds to a real, queryable row in the permanent library, tagged with exactly which of the seven Stage C gates (or the canonical-run path, or Stage A itself) stopped it.
