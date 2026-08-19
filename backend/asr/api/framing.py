"""The grid wire format (REQ-11.5, REQ-11.5.1).

Grid payloads are packed binary, never nested JSON arrays — twenty
million JSON integers per property per run is not a viable transport
for 30fps playback. The exact framing is specified so both ends cannot
invent incompatible protocols:

    bytes 0..3   uint32, little-endian: byte length of the JSON header
    bytes 4..N   UTF-8 JSON header
    bytes N..    payload region: C-order array blocks at stated offsets
"""

import json
import struct

import numpy as np


def frame_grids(first_tick: int, last_tick: int, stacks: dict) -> bytes:
    """Pack {property name: (ticks, height, width) array stack} for the
    inclusive tick range. Each property is one contiguous C-order block
    covering every tick in the range.
    """
    entries = []
    chunks = []
    offset = 0
    shape = None
    for name in sorted(stacks):
        stack = np.ascontiguousarray(stacks[name])
        shape = list(stack.shape[1:])
        raw = stack.tobytes()
        entries.append(
            {
                "name": name,
                "dtype": stack.dtype.name,
                "offset": offset,
                "length": len(raw),
            }
        )
        chunks.append(raw)
        offset += len(raw)
    header = json.dumps(
        {"ticks": [first_tick, last_tick], "shape": shape, "properties": entries},
        separators=(",", ":"),
    ).encode("utf-8")
    return struct.pack("<I", len(header)) + header + b"".join(chunks)
