// Decoder for the grid wire format (REQ-11.5.1):
//   bytes 0..3   uint32 little-endian: byte length of the JSON header
//   bytes 4..N   UTF-8 JSON header
//   bytes N..    payload region: C-order array blocks at stated offsets

const VIEWS = {
  uint8: Uint8Array,
  uint16: Uint16Array,
  int32: Int32Array,
  float32: Float32Array,
  bool: Uint8Array,
}

export function decodeGrids(buffer) {
  const headLength = new DataView(buffer).getUint32(0, true)
  const header = JSON.parse(new TextDecoder().decode(new Uint8Array(buffer, 4, headLength)))
  const payloadStart = 4 + headLength
  const [firstTick, lastTick] = header.ticks
  const [height, width] = header.shape
  const tickCount = lastTick - firstTick + 1
  const properties = {}
  for (const prop of header.properties) {
    const View = VIEWS[prop.dtype]
    if (!View) throw new Error(`unknown dtype ${prop.dtype}`)
    // Slice so each stack owns aligned memory regardless of offset.
    const bytes = buffer.slice(payloadStart + prop.offset, payloadStart + prop.offset + prop.length)
    properties[prop.name] = new View(bytes)
  }
  return { firstTick, lastTick, tickCount, width, height, properties }
}

// One tick's plane from a decoded stack.
export function plane(stack, tickIndex, width, height) {
  const size = width * height
  return stack.subarray(tickIndex * size, (tickIndex + 1) * size)
}
