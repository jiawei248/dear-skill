#!/usr/bin/env python3
"""
Build script: Regenerates the night-four-the-turn.html with:
1. Longer lyrics (2 per room)
2. Adjusted fonts
3. Title repositioned
4. PNG cutout scene images replacing JPG
5. Room decoration sprites with floating animation
6. Karaoke CCD frame overlay on couple photo
"""

import base64, os, re

DIR = os.path.dirname(os.path.abspath(__file__))

def b64(filename):
    path = os.path.join(DIR, filename)
    with open(path, 'rb') as f:
        data = f.read()
    ext = os.path.splitext(filename)[1].lower()
    mime = 'image/png' if ext == '.png' else 'image/jpeg'
    return f'data:{mime};base64,' + base64.b64encode(data).decode()

# Read existing HTML
with open(os.path.join(DIR, 'night-four-the-turn.html'), 'r') as f:
    html = f.read()

# ============================================================
# 1. Replace lyrics with longer 2-line versions
# ============================================================
old_kitchen_lyrics = """    lyrics: [
      'in the kitchen with the radio low, I want to kiss your eyes open',
      "you sang my name like a song, I don't wanna talk about anything",
      'I just wanna be next to you and watch you while you sleep'
    ],"""

new_kitchen_lyrics = """    lyrics: [
      'in the kitchen with the radio low, I want to kiss your eyes open, you sang my name like a song',
      "I don't wanna talk about anything, I just wanna be next to you and watch you while you sleep"
    ],"""

old_rooftop_lyrics = """    lyrics: [
      'can I be close to you, ooh-oh, can I be close to you',
      "in the morning when I wake, I'll wrap my arms around you",
      "and know that it's forever, I'll bloom, I'll bloom for you"
    ],"""

new_rooftop_lyrics = """    lyrics: [
      "can I be close to you, ooh-oh, can I be close to you, in the morning when I wake",
      "I'll wrap my arms around you and know that it's forever, I'll bloom, I'll bloom for you"
    ],"""

old_karaoke_lyrics = """    lyrics: [
      'I know I\\'m funny haha, you make it easy to just be',
      'I like it when you laugh at me, singing: 2 / 10 — joy: immeasurable',
      'we were dying, laughing, this is all I wanted'
    ],"""

new_karaoke_lyrics = """    lyrics: [
      "I know I'm funny haha, you make it easy to just be, I like it when you laugh at me",
      "singing: 2 / 10 — joy: immeasurable, we were dying laughing, this is all I wanted"
    ],"""

old_couch_lyrics = """    lyrics: [
      'fall back into place, tender is the night',
      'falling through the atmosphere, it was just you and me',
      'what makes this fragile world go round, were we just dust on a breeze'
    ],"""

new_couch_lyrics = """    lyrics: [
      'fall back into place, tender is the night, falling through the atmosphere',
      'it was just you and me, what makes this fragile world go round, were we just dust on a breeze'
    ],"""

html = html.replace(old_kitchen_lyrics, new_kitchen_lyrics)
html = html.replace(old_rooftop_lyrics, new_rooftop_lyrics)
html = html.replace(old_karaoke_lyrics, new_karaoke_lyrics)
html = html.replace(old_couch_lyrics, new_couch_lyrics)

# ============================================================
# 2. Adjust font sizes
# ============================================================
# Sentence lyrics: reduce from 78 to 66
html = html.replace(
    "const fontSize = 78;\n  const W = 4096, H = 360;",
    "const fontSize = 66;\n  const W = 4096, H = 320;"
)
# Falling word sprite: match at 66
html = html.replace(
    "ctx.font = 'italic 72px \"Cormorant Garamond\", \"EB Garamond\", serif';",
    "ctx.font = 'italic 66px \"Cormorant Garamond\", \"EB Garamond\", serif';"
)
# Sprite scale for ceiling lyrics: wider for longer text, slightly less tall
html = html.replace(
    "sp.scale.set(5.2, 0.46, 1);",
    "sp.scale.set(6.0, 0.40, 1);"
)
# Spacing between lyrics lines (now only 2 lines)
html = html.replace(
    "const baseY = ROOF_Y - 0.05 - li * 0.35;",
    "const baseY = ROOF_Y + 0.15 - li * 0.42;"
)

# ============================================================
# 3. Move title higher
# ============================================================
html = html.replace(
    ".hud-top { top: 0px; text-align: center; }",
    ".hud-top { top: -8px; text-align: center; }"
)
html = html.replace(
    "font-size: 44px; font-weight: 400;",
    "font-size: 40px; font-weight: 400;"
)

# ============================================================
# 4. Replace scene images with PNG cutouts
# ============================================================
scene_files = {
    'scene_kitchen': 'scene_kitchen.png',
    'scene_rooftop': 'scene_rooftop.png',
    'scene_rooftop_2': 'scene_rooftop_2.png',
    'scene_karaoke_1': 'scene_karaoke_1.png',
    'scene_karaoke_2': 'scene_karaoke_2.png',
    'scene_couch': 'scene_couch.png',
}

for key, filename in scene_files.items():
    old_pattern = f'"{key}": "data:image/jpeg;base64,'
    new_data = b64(filename)
    # Find and replace the entire data URI line for this key
    start = html.find(old_pattern)
    if start == -1:
        print(f"WARNING: Could not find {key} in HTML")
        continue
    # Find the end of this data URI (next unescaped quote after the base64 data)
    data_start = start + len(f'"{key}": "')
    end = html.find('"', data_start)
    if end == -1:
        print(f"WARNING: Could not find end of {key} data URI")
        continue
    html = html[:data_start] + new_data + html[end:]

# ============================================================
# 5 & 6. Add decorative items and CCD frame
# ============================================================
# Build base64 for all decoration images
deco_data = {}
for room in ['kitchen', 'rooftop', 'karaoke', 'couch']:
    room_dir = os.path.join(DIR, room)
    if os.path.isdir(room_dir):
        files = sorted([f for f in os.listdir(room_dir) if f.endswith('.png')])
        for f in files:
            key = f"{room}_{os.path.splitext(f)[0]}"
            deco_data[key] = b64(os.path.join(room, f))

# Generate the decoration sprite code
# Layout: each item placed within its room's quadrant with different positions
# Kitchen items: succulents, fan, kettle, fridge, scale, shelf
# Rooftop items: suitcases, turntable, photo box, laptop, lawn chair, mint table
# Karaoke items: guitar, vinyl records, CCD camera (overlay), cassette, armchair
# Couch items: hanging plant, coffee, bench, hotel key, dresser, chess

DECO_LAYOUT = {
    'kitchen': [
        # (file_idx, x_offset, z_offset, y, scale, description)
        (1, -0.6, 0.3, -0.82, 0.32, 'succulents'),
        (2, 0.7, 0.55, -0.55, 0.28, 'fan'),
        (3, -0.3, 0.75, -0.72, 0.26, 'kettle'),
        (4, 1.5, 0.4, -0.35, 0.55, 'fridge'),
        (5, 0.2, 1.5, -0.75, 0.24, 'scale'),
        (6, -1.1, 0.9, -0.45, 0.38, 'shelf'),
    ],
    'rooftop': [
        (1, 0.5, -0.3, -0.62, 0.36, 'suitcases'),
        (2, -0.6, 0.45, -0.70, 0.30, 'turntable'),
        (3, 0.1, 1.2, -0.78, 0.22, 'photo_box'),
        (4, -1.2, 0.7, -0.60, 0.34, 'laptop'),
        (5, 1.1, 0.9, -0.50, 0.42, 'lawn_chair'),
        (6, -0.3, 1.5, -0.80, 0.24, 'mint_table'),
    ],
    'karaoke': [
        (1, 0.8, 0.2, -0.45, 0.48, 'guitar'),
        (2, -0.5, 0.6, -0.72, 0.30, 'vinyl_records'),
        # 3 = CCD camera frame (handled specially)
        (4, 0.3, 1.3, -0.78, 0.24, 'cassette'),
        (5, 1.3, 0.7, -0.55, 0.40, 'armchair'),
    ],
    'couch': [
        (1, -0.4, 0.2, 0.30, 0.40, 'hanging_plant'),
        (2, 0.6, 0.9, -0.78, 0.22, 'coffee'),
        (3, -1.0, 0.6, -0.50, 0.45, 'bench'),
        (4, 0.2, 1.4, -0.60, 0.16, 'hotel_key'),
        (5, 1.3, 0.35, -0.52, 0.40, 'dresser'),
        (6, -0.6, 1.3, -0.75, 0.28, 'chess'),
    ],
}

# Room quadrant multipliers
ROOM_QX = {'kitchen': 1, 'rooftop': -1, 'karaoke': -1, 'couch': 1}
ROOM_QZ = {'kitchen': 1, 'rooftop': 1, 'karaoke': -1, 'couch': -1}
ROOM_IDX = {'kitchen': 0, 'rooftop': 1, 'karaoke': 2, 'couch': 3}

# Build the image data object entries
deco_data_entries = []
for key, data_uri in deco_data.items():
    deco_data_entries.append(f'  "{key}": "{data_uri}"')

deco_data_js = "const DECO_IMAGES = {\n" + ",\n".join(deco_data_entries) + "\n};\n"

# Build the sprite placement code
deco_sprite_code = """
// ============================================================
// DECORATIVE ITEMS — transparent PNG props per room
// ============================================================
""" + deco_data_js + """
const decoSprites = [];

function addDecoSprite(key, room, roomId, x, z, y, s) {
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
    sp.position.set(x, y, z);
    const scaleY = s;
    const scaleX = s * aspect;
    sp.scale.set(scaleX, scaleY, 1);
    scene.add(sp);
    decoSprites.push({
      sprite: sp, room, baseX: x, baseY: y, baseZ: z,
      phase: Math.random() * Math.PI * 2,
      freqX: 0.3 + Math.random() * 0.4,
      freqY: 0.4 + Math.random() * 0.3,
      ampX: 0.008 + Math.random() * 0.012,
      ampY: 0.006 + Math.random() * 0.010,
    });
  };
  img.src = DECO_IMAGES[key];
}

// --- CCD Camera frame overlay on karaoke scene ---
function addCCDOverlay() {
  const ccdKey = 'karaoke_3';
  const coupleKey = 'scene_karaoke_2';
  const room = ROOMS[2];
  const qx = -1, qz = -1;
  // Position the CCD frame and couple photo at the same location
  const cx = qx * 1.55, cz = qz * 1.35, cy = -0.3;
  
  // First add the couple photo (behind)
  const coupleImg = new Image();
  coupleImg.onload = () => {
    const c = document.createElement('canvas');
    const aspect = coupleImg.width / coupleImg.height;
    c.width = 512; c.height = Math.round(512 / aspect);
    const ctx = c.getContext('2d');
    ctx.drawImage(coupleImg, 0, 0, c.width, c.height);
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    const mat = new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.0, depthWrite: false });
    const sp = new THREE.Sprite(mat);
    sp.position.set(cx, cy, cz);
    const s = 0.58;
    sp.scale.set(s * aspect, s, 1);
    sp.renderOrder = 1;
    scene.add(sp);
    decoSprites.push({ sprite: sp, room, baseX: cx, baseY: cy, baseZ: cz,
      phase: 0.5, freqX: 0.25, freqY: 0.35, ampX: 0.006, ampY: 0.005 });
  };
  coupleImg.src = WALL_TEXTURES[coupleKey] || DECO_IMAGES[coupleKey] || '';
  
  // Then add the CCD frame (in front, slightly larger)
  const ccdImg = new Image();
  ccdImg.onload = () => {
    const c = document.createElement('canvas');
    const aspect = ccdImg.width / ccdImg.height;
    c.width = 512; c.height = Math.round(512 / aspect);
    const ctx = c.getContext('2d');
    ctx.drawImage(ccdImg, 0, 0, c.width, c.height);
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    const mat = new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.0, depthWrite: false });
    const sp = new THREE.Sprite(mat);
    sp.position.set(cx, cy, cz - 0.01);
    const s = 0.72;
    sp.scale.set(s * aspect, s, 1);
    sp.renderOrder = 2;
    scene.add(sp);
    decoSprites.push({ sprite: sp, room, baseX: cx, baseY: cy, baseZ: cz - 0.01,
      phase: 0.5, freqX: 0.25, freqY: 0.35, ampX: 0.006, ampY: 0.005 });
  };
  ccdImg.src = DECO_IMAGES[ccdKey];
}

"""

# Build placement calls
placement_calls = []
for room_name, items in DECO_LAYOUT.items():
    qx = ROOM_QX[room_name]
    qz = ROOM_QZ[room_name]
    ridx = ROOM_IDX[room_name]
    for (file_idx, xoff, zoff, y, s, desc) in items:
        key = f"{room_name}_{file_idx}"
        x = qx * xoff
        z = qz * zoff
        placement_calls.append(f"addDecoSprite('{key}', ROOMS[{ridx}], '{room_name}', {x:.2f}, {z:.2f}, {y}, {s});")

deco_sprite_code += "\n".join(placement_calls)
deco_sprite_code += "\naddCCDOverlay();\n"

# Now add animation code for deco sprites in the animation loop
deco_anim_code = """
  // decorative items: gentle float + fade based on active room
  for (const d of decoSprites) {
    const isActive = d.room === activeRoom;
    const targetOpacity = isActive ? 0.95 : 0.30;
    d.sprite.material.opacity += (targetOpacity - d.sprite.material.opacity) * Math.min(1, dt * 2.8);
    const t = now * 0.001;
    d.sprite.position.x = d.baseX + Math.sin(t * d.freqX + d.phase) * d.ampX;
    d.sprite.position.y = d.baseY + Math.sin(t * d.freqY + d.phase * 1.3) * d.ampY;
  }
"""

# Insert the deco sprite code after the playerSprites section
insert_marker = "// ------------------------------------------------------------\n// LYRICS SYSTEM"
html = html.replace(insert_marker, deco_sprite_code + "\n" + insert_marker)

# Insert animation code after the playerSprites animation
anim_marker = "  // lyric sentences: only visible in active room, gentle wave motion"
html = html.replace(anim_marker, deco_anim_code + "\n  " + anim_marker)

# Also need to reference WALL_TEXTURES for the CCD overlay (it uses scene_karaoke_2)
# The existing code has a WALL_TEXTURES object, let's check if it's already named that
# Actually looking at the code, the images are in an object - let me find its name
wall_tex_marker = "const WALL_TEXTURES = {"
if wall_tex_marker not in html:
    # Try the other format
    wall_tex_search = re.search(r'const\s+(\w+)\s*=\s*\{\s*"couch_right"', html)
    if wall_tex_search:
        var_name = wall_tex_search.group(1)
        # Replace the reference in addCCDOverlay
        html = html.replace("WALL_TEXTURES[coupleKey]", f"{var_name}[coupleKey]")
    else:
        # Find the object that contains scene images
        scene_tex_search = re.search(r'const\s+(\w+)\s*=\s*\{[^}]*"scene_kitchen"', html, re.DOTALL)
        if scene_tex_search:
            var_name = scene_tex_search.group(1)
            html = html.replace("WALL_TEXTURES[coupleKey]", f"{var_name}[coupleKey]")

# ============================================================
# Write output
# ============================================================
output_path = os.path.join(DIR, 'night-four-the-turn.html')
with open(output_path, 'w') as f:
    f.write(html)

print(f"Done! Output: {output_path}")
print(f"File size: {os.path.getsize(output_path) / 1024 / 1024:.1f} MB")
