"""Running a rule in a child process (REQ-7.6.1).

Not sandboxing (REQ-3.10) — a different job entirely: Python cannot
safely kill a runaway thread, and an infinite loop in generated code
must not take the server down. The child streams one message per tick;
the parent owns the wall clock and kills the child when a tick fails to
arrive in time, recording the run as `too_slow`.

The child receives rule SOURCE, not a class, and loads it itself. That
keeps every message picklable, which lets us use the spawn start method
— forking a multi-threaded FastAPI worker risks deadlock.

The child also self-times each tick, so a tick that finishes late (but
finishes) reports `too_slow` deterministically without the parent's axe.
"""

import multiprocessing
import resource
import traceback

from asr.engine.declaration import Declaration
from asr.engine.run import RunResult, assemble_result, run_rule


class RuleCrashed(Exception):
    """The rule raised while running. Stage C treats this as a
    rejection; the message carries the child's traceback text.
    """


def run_in_child(
    source: str,
    declaration: Declaration,
    seed: int,
    width: int,
    height: int,
    max_ticks: int,
    tick_timeout_seconds: float,
    memory_limit_mb: int,
) -> RunResult:
    """Execute a run in a killable child process and stream it back."""
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
