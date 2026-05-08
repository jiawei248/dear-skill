#!/usr/bin/env python3
import base64
import os
import re

DIR = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(DIR, "night-four-the-turn.html")


def data_uri(rel_path):
    path = os.path.join(DIR, rel_path)
    with open(path, "rb") as f:
        payload = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{payload}"


with open(HTML, "r", encoding="utf-8") as f:
    html = f.read()

# 1) Tighten the two lyric lines and keep falling words attached to the same y.
html = html.replace(
    "const baseY = ROOF_Y + 0.15 - li * 0.42;",
    "const baseY = ROOF_Y + 0.11 - li * 0.28;",
)
html = html.replace(
    "const startY = ROOF_Y + 0.15 - lineIdx * 0.42;",
    "const startY = ROOF_Y + 0.11 - lineIdx * 0.28;",
)

# 2) Rebalance karaoke CCD: bigger camera frame, smaller photo inside.
html = html.replace("const s = 0.58;", "const s = 0.44;", 1)
html = html.replace("const s = 0.72;", "const s = 0.98;", 1)

# 3) Add per-room player image data.
player_images = {
    "kitchen": data_uri("kitchen/player.png"),
    "rooftop": data_uri("rooftop/player.png"),
    "karaoke": data_uri("karaoke/player.png"),
    "couch": data_uri("couch/player.png"),
}
player_js = "const PLAYER_IMAGES = {\n" + ",\n".join(
    f'  "{room}": "{uri}"' for room, uri in player_images.items()
) + "\n};\n"

old_player_block = """const playerSprites = [];
ROOMS.forEach((room, idx) => {
  const t = tex(makePlayerOverlay(room));
  const mat = new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.92 });
  const sp = new THREE.Sprite(mat);
  // Tuck into the FAR outer corner of each quadrant, near the floor (out of sight-line of figures)
  const sx = idx === 0 ?  2.05 : idx === 1 ? -2.05 : idx === 2 ? -2.05 : 2.05;
  const sz = idx === 0 ?  2.05 : idx === 1 ?  2.05 : idx === 2 ? -2.05 : -2.05;
  sp.position.set(sx, -0.85, sz);
  sp.scale.set(0.34, 0.34, 1);
  scene.add(sp);
  playerSprites.push({ sprite: sp, room });
});"""

new_player_block = player_js + """
const playerSprites = [];
const PLAYER_LAYOUT = {
  kitchen: { x:  1.82, z:  1.92, y: -0.84, s: 0.34 },
  rooftop: { x: -1.82, z:  1.92, y: -0.86, s: 0.30 },
  karaoke: { x: -1.82, z: -1.92, y: -0.86, s: 0.32 },
  couch:   { x:  1.82, z: -1.92, y: -0.84, s: 0.34 },
};

ROOMS.forEach((room) => {
  const layout = PLAYER_LAYOUT[room.id];
  const img = new Image();
  img.onload = () => {
    const c = document.createElement('canvas');
    const aspect = img.width / img.height;
    c.width = 512;
    c.height = Math.round(512 / aspect);
    const ctx = c.getContext('2d');
    ctx.drawImage(img, 0, 0, c.width, c.height);
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    const mat = new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.0, depthWrite: false });
    const sp = new THREE.Sprite(mat);
    sp.position.set(layout.x, layout.y, layout.z);
    sp.scale.set(layout.s * aspect, layout.s, 1);
    sp.renderOrder = 3;
    scene.add(sp);
    playerSprites.push({ sprite: sp, room, baseX: layout.x, baseY: layout.y, baseZ: layout.z, phase: Math.random() * Math.PI * 2 });
  };
  img.src = PLAYER_IMAGES[room.id];
});"""

if old_player_block not in html:
    raise SystemExit("Could not find existing player block")
html = html.replace(old_player_block, new_player_block)

# 4) Make decorative props more varied, larger, and layered.
html = html.replace(
    "function addDecoSprite(key, room, roomId, x, z, y, s) {",
    "function addDecoSprite(key, room, roomId, x, z, y, s, order = 0) {",
)
html = html.replace(
    "    sp.position.set(x, y, z);\n    const scaleY = s;",
    "    sp.position.set(x, y, z);\n    sp.renderOrder = order;\n    const scaleY = s;",
)

old_calls = re.search(
    r"addDecoSprite\('kitchen_1'[\s\S]*?addCCDOverlay\(\);",
    html,
)
if not old_calls:
    raise SystemExit("Could not find decorative placement calls")

new_calls = """addDecoSprite('kitchen_4', ROOMS[0], 'kitchen', 1.72, 0.56, -0.43, 0.74, -1);
addDecoSprite('kitchen_6', ROOMS[0], 'kitchen', 0.78, 1.52, -0.42, 0.55, 1);
addDecoSprite('kitchen_3', ROOMS[0], 'kitchen', 0.12, 1.78, -0.76, 0.42, 3);
addDecoSprite('kitchen_5', ROOMS[0], 'kitchen', 1.42, 1.62, -0.80, 0.36, 4);
addDecoSprite('kitchen_1', ROOMS[0], 'kitchen', 0.24, 0.58, -0.70, 0.46, 5);
addDecoSprite('kitchen_2', ROOMS[0], 'kitchen', 1.86, 1.22, 0.10, 0.40, 2);
addDecoSprite('rooftop_5', ROOMS[1], 'rooftop', -1.70, 0.84, -0.50, 0.66, 0);
addDecoSprite('rooftop_6', ROOMS[1], 'rooftop', -0.68, 1.88, -0.82, 0.44, 4);
addDecoSprite('rooftop_2', ROOMS[1], 'rooftop', -1.22, 1.58, -0.68, 0.46, 5);
addDecoSprite('rooftop_1', ROOMS[1], 'rooftop', -0.24, 0.72, -0.64, 0.50, 2);
addDecoSprite('rooftop_3', ROOMS[1], 'rooftop', -1.88, 1.58, -0.28, 0.34, 6);
addDecoSprite('rooftop_4', ROOMS[1], 'rooftop', -0.42, 0.34, -0.42, 0.46, 3);
addDecoSprite('karaoke_1', ROOMS[2], 'karaoke', -0.24, -0.48, 0.02, 0.66, 3);
addDecoSprite('karaoke_5', ROOMS[2], 'karaoke', -1.72, -0.50, -0.56, 0.58, 1);
addDecoSprite('karaoke_2', ROOMS[2], 'karaoke', -0.46, -1.72, -0.76, 0.48, 5);
addDecoSprite('karaoke_4', ROOMS[2], 'karaoke', -1.38, -1.66, -0.80, 0.34, 6);
addDecoSprite('couch_1', ROOMS[3], 'couch', 0.30, -0.42, 0.44, 0.58, 6);
addDecoSprite('couch_5', ROOMS[3], 'couch', 1.72, -0.62, -0.50, 0.58, 0);
addDecoSprite('couch_3', ROOMS[3], 'couch', 0.62, -1.52, -0.58, 0.60, 3);
addDecoSprite('couch_6', ROOMS[3], 'couch', 1.28, -1.76, -0.78, 0.42, 5);
addDecoSprite('couch_2', ROOMS[3], 'couch', 0.12, -1.12, -0.76, 0.34, 7);
addDecoSprite('couch_4', ROOMS[3], 'couch', 1.78, -1.28, -0.20, 0.26, 8);
addCCDOverlay();"""
html = html[: old_calls.start()] + new_calls + html[old_calls.end() :]

# 5) Let the PNG players float very slightly, like the props.
html = html.replace(
    """  // dim non-active room players too
  for (const p of playerSprites) {
    const isActive = p.room === activeRoom;
    const target = isActive ? 0.92 : 0.35;
    p.sprite.material.opacity += (target - p.sprite.material.opacity) * Math.min(1, dt * 2.5);
  }""",
    """  // dim non-active room players too
  for (const p of playerSprites) {
    const isActive = p.room === activeRoom;
    const target = isActive ? 0.96 : 0.35;
    p.sprite.material.opacity += (target - p.sprite.material.opacity) * Math.min(1, dt * 2.5);
    const t = now * 0.001;
    p.sprite.position.x = p.baseX + Math.sin(t * 0.32 + p.phase) * 0.006;
    p.sprite.position.y = p.baseY + Math.sin(t * 0.42 + p.phase) * 0.006;
  }""",
)

with open(HTML, "w", encoding="utf-8") as f:
    f.write(html)

print("Patched night-four-the-turn.html")
