#!/usr/bin/env python3
from pathlib import Path
import re

HTML = Path("/Users/liujiawei/Desktop/night-four-assets/night-four-the-turn.html")
html = HTML.read_text(encoding="utf-8")

# Lyric size/spacing: smaller font, tighter line distance, and adaptive fit for long lines.
html = html.replace(
"""function makeWavyLyric(text, color, waveAmp, wavePeriod, phaseOff) {
  const fontSize = 66;
  const W = 4096, H = 320;
  const c = makeCanvas(W, H);
  const ctx = c.getContext('2d');
  ctx.font = 'italic ' + fontSize + 'px "Cormorant Garamond", "EB Garamond", serif';
  ctx.fillStyle = color;
  ctx.globalAlpha = 0.82;
  ctx.textBaseline = 'middle';

  const totalTextW = ctx.measureText(text).width;
  let startX = (W - totalTextW) / 2;
  const midY = H / 2;""",
"""function makeWavyLyric(text, color, waveAmp, wavePeriod, phaseOff) {
  const baseFontSize = 58;
  const W = 4096, H = 300;
  const c = makeCanvas(W, H);
  const ctx = c.getContext('2d');
  let fontSize = baseFontSize;
  ctx.font = 'italic ' + fontSize + 'px "Cormorant Garamond", "EB Garamond", serif';
  const maxTextW = W * 0.88;
  const measuredW = ctx.measureText(text).width;
  if (measuredW > maxTextW) {
    fontSize = Math.max(44, Math.floor(baseFontSize * maxTextW / measuredW));
    ctx.font = 'italic ' + fontSize + 'px "Cormorant Garamond", "EB Garamond", serif';
  }
  ctx.fillStyle = color;
  ctx.globalAlpha = 0.82;
  ctx.textBaseline = 'middle';

  const totalTextW = ctx.measureText(text).width;
  let startX = (W - totalTextW) / 2;
  const midY = H / 2;""")

html = html.replace(
    "ctx.font = 'italic 66px \"Cormorant Garamond\", \"EB Garamond\", serif';",
    "ctx.font = 'italic 58px \"Cormorant Garamond\", \"EB Garamond\", serif';",
)
html = html.replace("const widthScale = 0.28 + Math.min(text.length, 12) * 0.028;", "const widthScale = 0.24 + Math.min(text.length, 12) * 0.024;")
html = html.replace("sp.scale.set(widthScale, 0.10, 1);", "sp.scale.set(widthScale, 0.085, 1);")
html = html.replace("const baseY = ROOF_Y + 0.11 - li * 0.28;", "const baseY = ROOF_Y + 0.08 - li * 0.22;")
html = html.replace("const startY = ROOF_Y + 0.11 - lineIdx * 0.28;", "const startY = ROOF_Y + 0.08 - lineIdx * 0.22;")
html = html.replace("sp.scale.set(6.0, 0.40, 1);", "sp.scale.set(5.9, 0.34, 1);")
html = html.replace("const amp = 28 + (li % 3) * 8;", "const amp = 18 + (li % 3) * 6;")

old_calls = re.search(r"addDecoSprite\('kitchen_4'[\s\S]*?addCCDOverlay\(\);", html)
if not old_calls:
    raise SystemExit("Could not find decorative sprite placement block")

new_config = """// ------------------------------------------------------------
// Editable sticker layout
// ------------------------------------------------------------
// You can fine-tune every transparent PNG sticker here.
// key   = file name without .png, e.g. kitchen/4.png => "kitchen_4"
// x/z   = left-right / depth inside the room quadrant (small changes like 0.05 matter)
// y     = vertical height. -0.8 near floor, 0.0 mid wall, 0.45 hanging/upper wall
// s     = visual size. Increase/decrease in small steps, e.g. 0.05
// order = draw layer. Higher numbers appear in front of lower numbers.
// label = only for your reference; it does not affect rendering.
const DECOR_LAYOUT = {
  kitchen: [
    { key: 'kitchen_4', label: 'cream fridge, back right', x: 1.72, z: 0.56, y: -0.43, s: 0.74, order: -1 },
    { key: 'kitchen_6', label: 'wood shelf behind couple', x: 0.78, z: 1.52, y: -0.42, s: 0.55, order: 1 },
    { key: 'kitchen_3', label: 'yellow kettle front left', x: 0.12, z: 1.78, y: -0.76, s: 0.42, order: 3 },
    { key: 'kitchen_5', label: 'scale front right', x: 1.42, z: 1.62, y: -0.80, s: 0.36, order: 4 },
    { key: 'kitchen_1', label: 'succulents mid left', x: 0.24, z: 0.58, y: -0.70, s: 0.46, order: 5 },
    { key: 'kitchen_2', label: 'fan upper right wall', x: 1.86, z: 1.22, y: 0.10, s: 0.40, order: 2 },
  ],
  rooftop: [
    { key: 'rooftop_5', label: 'yellow chair left', x: -1.70, z: 0.84, y: -0.50, s: 0.66, order: 0 },
    { key: 'rooftop_6', label: 'mint table front', x: -0.68, z: 1.88, y: -0.82, s: 0.44, order: 4 },
    { key: 'rooftop_2', label: 'record player front right', x: -1.22, z: 1.58, y: -0.68, s: 0.46, order: 5 },
    { key: 'rooftop_1', label: 'blue suitcases mid', x: -0.24, z: 0.72, y: -0.64, s: 0.50, order: 2 },
    { key: 'rooftop_3', label: 'photo box upper corner', x: -1.88, z: 1.58, y: -0.28, s: 0.34, order: 6 },
    { key: 'rooftop_4', label: 'laptop mid wall', x: -0.42, z: 0.34, y: -0.42, s: 0.46, order: 3 },
  ],
  karaoke: [
    { key: 'karaoke_1', label: 'guitar upper wall', x: -0.24, z: -0.48, y: 0.02, s: 0.66, order: 3 },
    { key: 'karaoke_5', label: 'leather chair left back', x: -1.72, z: -0.50, y: -0.56, s: 0.58, order: 1 },
    { key: 'karaoke_2', label: 'vinyl pile front', x: -0.46, z: -1.72, y: -0.76, s: 0.48, order: 5 },
    { key: 'karaoke_4', label: 'cassette front right', x: -1.38, z: -1.66, y: -0.80, s: 0.34, order: 6 },
  ],
  couch: [
    { key: 'couch_1', label: 'hanging plant upper left', x: 0.30, z: -0.42, y: 0.44, s: 0.58, order: 6 },
    { key: 'couch_5', label: 'dresser back right', x: 1.72, z: -0.62, y: -0.50, s: 0.58, order: 0 },
    { key: 'couch_3', label: 'bench mid/front', x: 0.62, z: -1.52, y: -0.58, s: 0.60, order: 3 },
    { key: 'couch_6', label: 'chess front right', x: 1.28, z: -1.76, y: -0.78, s: 0.42, order: 5 },
    { key: 'couch_2', label: 'coffee front left', x: 0.12, z: -1.12, y: -0.76, s: 0.34, order: 7 },
    { key: 'couch_4', label: 'room key floating front', x: 1.78, z: -1.28, y: -0.20, s: 0.26, order: 8 },
  ],
};

Object.entries(DECOR_LAYOUT).forEach(([roomId, items]) => {
  const room = ROOMS.find((r) => r.id === roomId);
  items.forEach((item) => {
    addDecoSprite(item.key, room, roomId, item.x, item.z, item.y, item.s, item.order);
  });
});
addCCDOverlay();"""

html = html[:old_calls.start()] + new_config + html[old_calls.end():]

HTML.write_text(html, encoding="utf-8")
print("Updated lyrics sizing and converted stickers to DECOR_LAYOUT config")
