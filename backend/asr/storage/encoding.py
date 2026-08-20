"""Tick payload encoding (REQ-12.5).

A snapshot is written every SNAPSHOT_EVERY ticks. Between snapshots,
each tick stores either a changed-index list (`sparse`) or a raw XOR
against the previous tick (`dense`) — whichever is smaller for that
tick. All payloads are Zstandard-compressed.

Derived arrays are never stored in deltas: `age` changes on nearly
every cell every tick and would make every settled tick dense
(REQ-12.6). `age` IS included in snapshots so reconstruction walks
forward at most one snapshot interval instead of from tick 0
(REQ-12.6.2). `changed_last_tick` is never stored at all — it is the
kind difference of adjacent ticks.
"""

import json
import struct

import numpy as np
import zstandard

# Derived properties, reconstructed rather than stored (REQ-12.6).
NEVER_IN_DELTAS = ("age", "changed_last_tick")
SNAPSHOT_ALSO_KEEPS = ("age",)


def _compressor() -> zstandard.ZstdCompressor:
    # A fresh context per call: ZstdCompressor/ZstdDecompressor are not
    # safe for concurrent use, and route handlers run in a threadpool.
    return zstandard.ZstdCompressor()


def _decompressor() -> zstandard.ZstdDecompressor:
    return zstandard.ZstdDecompressor()


def _frame(header: dict, payload: bytes) -> bytes:
    """Length-prefixed JSON header, then a payload region — the same
    shape as the wire framing (REQ-11.5.1)."""
    head = json.dumps(header, separators=(",", ":")).encode("utf-8")
    return struct.pack("<I", len(head)) + head + payload


def _unframe(blob: bytes):
    (head_length,) = struct.unpack_from("<I", blob, 0)
    header = json.loads(blob[4 : 4 + head_length].decode("utf-8"))
    return header, blob[4 + head_length :]


def _stored_names(arrays: dict, snapshot: bool) -> list:
    names = [n for n in sorted(arrays) if n not in NEVER_IN_DELTAS]
    if snapshot:
        names += [n for n in SNAPSHOT_ALSO_KEEPS if n in arrays]
    return names


def encode_snapshot(arrays: dict) -> bytes:
    """The full grid, every stored property plus age."""
    entries = []
    chunks = []
    offset = 0
    shape = None
    for name in _stored_names(arrays, snapshot=True):
        array = np.ascontiguousarray(arrays[name])
        shape = list(array.shape)
        raw = array.tobytes()
        entries.append(
            {"name": name, "dtype": array.dtype.str, "offset": offset, "length": len(raw)}
        )
        chunks.append(raw)
        offset += len(raw)
    header = {"shape": shape, "arrays": entries}
    return _compressor().compress(_frame(header, b"".join(chunks)))


def encode_delta(previous: dict, current: dict):
    """Difference against the previous tick: whichever of the two delta
    forms is smaller for this tick. Returns (encoding_name, blob).
    """
    sparse = _encode_sparse(previous, current)
    dense = _encode_dense(previous, current)
    if len(sparse) <= len(dense):
        return "sparse", _compressor().compress(sparse)
    return "dense", _compressor().compress(dense)


def _encode_sparse(previous: dict, current: dict) -> bytes:
    """Per property: the flat indices that changed, and their new
    values. A property with no changes is omitted entirely.
    """
    entries = []
    chunks = []
    offset = 0
    shape = None
    for name in _stored_names(current, snapshot=False):
        now = np.ascontiguousarray(current[name])
        before = np.ascontiguousarray(previous[name])
        shape = list(now.shape)
        changed = np.flatnonzero(now.reshape(-1) != before.reshape(-1))
        if changed.size == 0:
            continue
        indices = changed.astype(np.uint32).tobytes()
        values = now.reshape(-1)[changed].tobytes()
        entries.append(
            {
                "name": name,
                "dtype": now.dtype.str,
                "count": int(changed.size),
                "offset": offset,
                "index_length": len(indices),
                "value_length": len(values),
            }
        )
        chunks.append(indices)
        chunks.append(values)
        offset += len(indices) + len(values)
    header = {"kind_of_delta": "sparse", "shape": shape, "arrays": entries}
    return _frame(header, b"".join(chunks))


def _encode_dense(previous: dict, current: dict) -> bytes:
    """Per property: the raw bytes XORed against the previous tick.
    Unchanged regions become zeros, which Zstandard flattens.
    """
    entries = []
    chunks = []
    offset = 0
    shape = None
    for name in _stored_names(current, snapshot=False):
        now = np.ascontiguousarray(current[name])
        before = np.ascontiguousarray(previous[name])
        shape = list(now.shape)
        mixed = np.bitwise_xor(
            np.frombuffer(now.tobytes(), np.uint8),
            np.frombuffer(before.tobytes(), np.uint8),
        ).tobytes()
        entries.append(
            {"name": name, "dtype": now.dtype.str, "offset": offset, "length": len(mixed)}
        )
        chunks.append(mixed)
        offset += len(mixed)
    header = {"kind_of_delta": "dense", "shape": shape, "arrays": entries}
    return _frame(header, b"".join(chunks))


def decode(encoding: str, blob: bytes, previous: dict | None) -> dict:
    """Rebuild one tick's stored arrays. `previous` is the already-
    decoded prior tick for sparse/dense; snapshots stand alone.
    """
    header, payload = _unframe(_decompressor().decompress(blob))
    shape = tuple(header["shape"])
    if encoding == "snapshot":
        arrays = {}
        for entry in header["arrays"]:
            raw = payload[entry["offset"] : entry["offset"] + entry["length"]]
            arrays[entry["name"]] = np.frombuffer(raw, entry["dtype"]).reshape(shape).copy()
        return arrays

    if previous is None:
        raise ValueError(f"a {encoding} tick cannot be decoded without the previous tick")
    arrays = {
        name: array for name, array in previous.items() if name not in NEVER_IN_DELTAS
    }
    if encoding == "sparse":
        for entry in header["arrays"]:
            start = entry["offset"]
            indices = np.frombuffer(
                payload[start : start + entry["index_length"]], np.uint32
            )
            values = np.frombuffer(
                payload[
                    start + entry["index_length"]
                    : start + entry["index_length"] + entry["value_length"]
                ],
                entry["dtype"],
            )
            fresh = arrays[entry["name"]].copy().reshape(-1)
            fresh[indices] = values
            arrays[entry["name"]] = fresh.reshape(shape)
        return arrays
    if encoding == "dense":
        for entry in header["arrays"]:
            raw = payload[entry["offset"] : entry["offset"] + entry["length"]]
            before = arrays[entry["name"]]
            mixed = np.bitwise_xor(
                np.frombuffer(before.tobytes(), np.uint8), np.frombuffer(raw, np.uint8)
            )
            arrays[entry["name"]] = np.frombuffer(
                mixed.tobytes(), entry["dtype"]
            ).reshape(shape)
        return arrays
    raise ValueError(f"unknown payload encoding {encoding!r}")
