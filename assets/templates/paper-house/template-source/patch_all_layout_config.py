#!/usr/bin/env python3
from pathlib import Path
import re

HTML = Path(__file__).resolve().parent / "night-four-the-turn.html"
html = HTML.read_text(encoding="utf-8")

def add_rot_to_object_literals(block: str) -> str:
    # Preserve existing user-tuned x/y/z/s/order values; only append rot when absent.
    def repl(match):
        obj = match.group(0)
        if " rot:" in obj or "\n" in obj:
            return obj
        return obj[:-2] + ", rot: 0 },"
    return re.sub(r"\{ key: '[^']+'[^{}]*? \},", repl, block)

# Add helpers near the editable layout section.
html = html.replace(
"""// ------------------------------------------------------------
// Editable sticker layout
// ------------------------------------------------------------""",
"""function deg(v) { return v * Math.PI / 180; }

// ------------------------------------------------------------
// Editable image layout
// ------------------------------------------------------------""")

html = html.replace(
"""// You can fine-tune every transparent PNG sticker here.
// key   = file name without .png, e.g. kitchen/4.png => "kitchen_4"
// x/z   = left-right / depth inside the room quadrant (small changes like 0.05 matter)
// y     = vertical height. -0.8 near floor, 0.0 mid wall, 0.45 hanging/upper wall
// s     = visual size. Increase/decrease in small steps, e.g. 0.05
// order = draw layer. Higher numbers appear in front of lower numbers.
// label = only for your reference; it does not affect rendering.""",
"""// You can fine-tune every image here.
// key   = image id. For stickers: kitchen/4.png => "kitchen_4"; for figures: "scene_kitchen".
// x/z   = left-right / depth inside the room quadrant (small changes like 0.05 matter)
// y     = vertical height. -0.8 near floor, 0.0 mid wall, 0.45 hanging/upper wall
// s     = visual size. Increase/decrease in small steps, e.g. 0.05
// order = draw layer. Higher numbers appear in front of lower numbers.
// rot   = rotation angle in degrees. Positive rotates clockwise, negative counter-clockwise.
// label = only for your reference; it does not affect rendering.""")

# Add rot: 0 to every existing DECOR_LAYOUT item without changing tuned values.
decor_match = re.search(r"const DECOR_LAYOUT = \{[\s\S]*?\n\};", html)
if not decor_match:
    raise SystemExit("DECOR_LAYOUT not found")
decor_block = add_rot_to_object_literals(decor_match.group(0))
html = html[:decor_match.start()] + decor_block + html[decor_match.end():]

# Replace figure layout with configurable table.
old_scene = re.search(r"const SCENE_LAYOUT = \[[\s\S]*?\];\nSCENE_LAYOUT\.forEach\(cfg => \{[\s\S]*?\n\}\);", html)
if not old_scene:
    raise SystemExit("SCENE_LAYOUT block not found")

new_scene = """const FIGURE_LAYOUT = [
  { room: 'kitchen', key: 'scene_kitchen', label: 'kitchen couple', x: 1.0, z: 1.0, y: -0.18, s: 1.4, order: 10, rot: 0 },
  { room: 'rooftop', key: 'scene_rooftop', label: 'rooftop couple 1', x: -0.85, z: 1.0, y: -0.15, s: 1.5, order: 10, rot: 0 },
  { room: 'rooftop', key: 'scene_rooftop_2', label: 'rooftop couple 2', x: -1.55, z: 1.35, y: -0.3, s: 0.7, order: 11, rot: 0 },
  { room: 'karaoke', key: 'scene_karaoke_1', label: 'karaoke singing couple', x: -0.85, z: -1.0, y: -0.15, s: 1.4, order: 10, rot: 0 },
  { room: 'couch', key: 'scene_couch', label: 'couch couple', x: 1.0, z: -1.0, y: -0.2, s: 1.4, order: 10, rot: 0 },
];

FIGURE_LAYOUT.forEach((cfg) => {
  const room = ROOMS.find((r) => r.id === cfg.room);
  const t = loadWallTex(cfg.key);
  const mat = new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.96 });
  mat.rotation = deg(cfg.rot || 0);
  const sp = new THREE.Sprite(mat);
  sp.position.set(cfg.x, cfg.y, cfg.z);
  sp.scale.set(cfg.s, cfg.s, 1);
  sp.renderOrder = cfg.order || 0;
  scene.add(sp);
  figureSprites.push({ sprite: sp, room });
});"""
html = html[:old_scene.start()] + new_scene + html[old_scene.end():]

# Replace existing PLAYER_LAYOUT with configurable table that includes order/rot/labels.
old_player_layout = re.search(r"const PLAYER_LAYOUT = \{[\s\S]*?\n\};", html)
if not old_player_layout:
    raise SystemExit("PLAYER_LAYOUT block not found")
new_player_layout = """const PLAYER_LAYOUT = {
  kitchen: { label: 'kitchen record player', x:  1.82, z:  1.92, y: -0.84, s: 0.34, order: 20, rot: 0 },
  rooftop: { label: 'rooftop portable player', x: -1.82, z:  1.92, y: -0.86, s: 0.30, order: 20, rot: 0 },
  karaoke: { label: 'karaoke walkman', x: -1.82, z: -1.92, y: -0.86, s: 0.32, order: 20, rot: 0 },
  couch:   { label: 'couch cd player', x:  1.82, z: -1.92, y: -0.84, s: 0.34, order: 20, rot: 0 },
};"""
html = html[:old_player_layout.start()] + new_player_layout + html[old_player_layout.end():]

html = html.replace(
"""    const mat = new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.0, depthWrite: false });
    const sp = new THREE.Sprite(mat);
    sp.position.set(layout.x, layout.y, layout.z);
    sp.scale.set(layout.s * aspect, layout.s, 1);
    sp.renderOrder = 3;""",
"""    const mat = new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.0, depthWrite: false });
    mat.rotation = deg(layout.rot || 0);
    const sp = new THREE.Sprite(mat);
    sp.position.set(layout.x, layout.y, layout.z);
    sp.scale.set(layout.s * aspect, layout.s, 1);
    sp.renderOrder = layout.order || 0;""")

# Make CCD overlay configurable too.
html = html.replace(
"""function addCCDOverlay() {
  const ccdKey = 'karaoke_3';
  const coupleKey = 'scene_karaoke_2';
  const room = ROOMS[2];
  const qx = -1, qz = -1;
  // Position the CCD frame and couple photo at the same location
  const cx = qx * 1.55, cz = qz * 1.35, cy = -0.3;""",
"""const CCD_OVERLAY_LAYOUT = {
  room: 'karaoke',
  photo: { key: 'scene_karaoke_2', label: 'photo inside CCD', x: -1.55, z: -1.35, y: -0.30, s: 0.44, order: 11, rot: 0 },
  frame: { key: 'karaoke_3', label: 'CCD camera frame', x: -1.55, z: -1.36, y: -0.30, s: 0.98, order: 12, rot: 0 },
};

function addCCDOverlay() {
  const ccdKey = CCD_OVERLAY_LAYOUT.frame.key;
  const coupleKey = CCD_OVERLAY_LAYOUT.photo.key;
  const room = ROOMS.find((r) => r.id === CCD_OVERLAY_LAYOUT.room);
  const photo = CCD_OVERLAY_LAYOUT.photo;
  const frame = CCD_OVERLAY_LAYOUT.frame;""")

html = html.replace("sp.position.set(cx, cy, cz);\n    const s = 0.44;\n    sp.scale.set(s * aspect, s, 1);\n    sp.renderOrder = 1;", "sp.position.set(photo.x, photo.y, photo.z);\n    const s = photo.s;\n    mat.rotation = deg(photo.rot || 0);\n    sp.scale.set(s * aspect, s, 1);\n    sp.renderOrder = photo.order || 0;")
html = html.replace("decoSprites.push({ sprite: sp, room, baseX: cx, baseY: cy, baseZ: cz,", "decoSprites.push({ sprite: sp, room, baseX: photo.x, baseY: photo.y, baseZ: photo.z,")
html = html.replace("sp.position.set(cx, cy, cz - 0.01);\n    const s = 0.98;\n    sp.scale.set(s * aspect, s, 1);\n    sp.renderOrder = 2;", "sp.position.set(frame.x, frame.y, frame.z);\n    const s = frame.s;\n    mat.rotation = deg(frame.rot || 0);\n    sp.scale.set(s * aspect, s, 1);\n    sp.renderOrder = frame.order || 0;")
html = html.replace("decoSprites.push({ sprite: sp, room, baseX: cx, baseY: cy, baseZ: cz - 0.01,", "decoSprites.push({ sprite: sp, room, baseX: frame.x, baseY: frame.y, baseZ: frame.z,")

# Add rot support to decor sprite rendering and creation.
html = html.replace("function addDecoSprite(key, room, roomId, x, z, y, s, order = 0) {", "function addDecoSprite(key, room, roomId, x, z, y, s, order = 0, rot = 0) {")
html = html.replace("const mat = new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.0, depthWrite: false });\n    const sp = new THREE.Sprite(mat);\n    sp.position.set(x, y, z);\n    sp.renderOrder = order;", "const mat = new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.0, depthWrite: false });\n    mat.rotation = deg(rot || 0);\n    const sp = new THREE.Sprite(mat);\n    sp.position.set(x, y, z);\n    sp.renderOrder = order;", 1)
html = html.replace("addDecoSprite(item.key, room, roomId, item.x, item.z, item.y, item.s, item.order);", "addDecoSprite(item.key, room, roomId, item.x, item.z, item.y, item.s, item.order, item.rot || 0);")

HTML.write_text(html, encoding="utf-8")
print("Added configurable figure/player/decor/CCD rotation and layout")
