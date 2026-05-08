#!/usr/bin/env python3
from pathlib import Path

HTML = Path("/Users/liujiawei/Desktop/night-four-assets/night-four-the-turn.html")
html = HTML.read_text(encoding="utf-8")

# Tighten only the two lyric lines. Keep all user-tuned image layouts unchanged.
html = html.replace(
    "const baseY = ROOF_Y + 0.08 - li * 0.22;",
    "const baseY = ROOF_Y + 0.08 - li * 0.18;",
)
html = html.replace(
    "const startY = ROOF_Y + 0.08 - lineIdx * 0.22;",
    "const startY = ROOF_Y + 0.08 - lineIdx * 0.18;",
)

if "const earphoneWires = [];" not in html:
    earphone_code = r"""

// ------------------------------------------------------------
// Editable earphone wire layout
// ------------------------------------------------------------
// Each wire is a curved line from a room player to one person's ear.
// points = [[x,y,z], ...]. First point is near player; last point is near ear.
// Add/move middle points to shape the curve. order controls layer.
const EARPHONE_LINE_LAYOUT = {
  kitchen: [
    { label: 'player to boy ear', points: [[1.82, -0.82, 1.92], [1.55, -0.48, 1.50], [1.32, 0.10, 1.06], [1.18, 0.32, 0.98]], order: 96 },
    { label: 'player to girl ear', points: [[1.82, -0.84, 1.92], [1.28, -0.58, 1.56], [0.96, -0.18, 1.12], [0.82, 0.03, 1.00]], order: 96 },
  ],
  rooftop: [
    { label: 'player to boy ear', points: [[-1.82, -0.96, 1.92], [-1.46, -0.54, 1.55], [-1.08, 0.08, 1.12], [-0.92, 0.28, 1.02]], order: 96 },
    { label: 'player to girl ear', points: [[-1.82, -0.98, 1.92], [-1.18, -0.62, 1.58], [-0.66, -0.18, 1.18], [-0.48, 0.02, 1.04]], order: 96 },
  ],
  karaoke: [
    { label: 'player to boy ear', points: [[-1.82, -1.02, -1.92], [-1.62, -0.60, -1.54], [-1.22, 0.08, -1.12], [-1.04, 0.34, -1.00]], order: 96 },
    { label: 'player to girl ear', points: [[-1.82, -1.04, -1.92], [-1.30, -0.62, -1.54], [-0.76, -0.08, -1.14], [-0.56, 0.14, -1.00]], order: 96 },
  ],
  couch: [
    { label: 'player to boy ear', points: [[1.82, -0.96, -1.92], [1.54, -0.56, -1.54], [1.22, 0.08, -1.12], [1.08, 0.30, -1.00]], order: 96 },
    { label: 'player to girl ear', points: [[1.82, -0.98, -1.92], [1.24, -0.62, -1.56], [0.78, -0.16, -1.12], [0.60, 0.06, -1.00]], order: 96 },
  ],
};

const earphoneWires = [];
function addEarphoneWire(room, cfg) {
  const curve = new THREE.CatmullRomCurve3(cfg.points.map(([x, y, z]) => new THREE.Vector3(x, y, z)));
  const geometry = new THREE.BufferGeometry().setFromPoints(curve.getPoints(48));
  const material = new THREE.LineBasicMaterial({
    color: room.palette.glow || room.palette.accent || '#fff5d4',
    transparent: true,
    opacity: 0,
    linewidth: 1,
    depthTest: false,
    depthWrite: false,
  });
  const line = new THREE.Line(geometry, material);
  line.renderOrder = cfg.order || 96;
  scene.add(line);
  earphoneWires.push({ line, room });
}

Object.entries(EARPHONE_LINE_LAYOUT).forEach(([roomId, wires]) => {
  const room = ROOMS.find((r) => r.id === roomId);
  wires.forEach((wire) => addEarphoneWire(room, wire));
});
"""
    marker = "// ------------------------------------------------------------\n// Editable image layout"
    if marker not in html:
        raise SystemExit("Editable image layout marker not found")
    html = html.replace(marker, earphone_code + "\n" + marker)

if "for (const wire of earphoneWires)" not in html:
    anim_code = r"""
  // earphone wires: only visible in the active room
  for (const wire of earphoneWires) {
    const isActive = wire.room === activeRoom;
    const targetOpacity = isActive ? 0.82 : 0;
    wire.line.material.opacity += (targetOpacity - wire.line.material.opacity) * Math.min(1, dt * 3);
  }
"""
    marker = "  // decorative items: gentle float + fade based on active room"
    if marker not in html:
        raise SystemExit("Decorative animation marker not found")
    html = html.replace(marker, anim_code + "\n" + marker)

HTML.write_text(html, encoding="utf-8")
print("Added earphone wire curves and tightened lyric line spacing")
