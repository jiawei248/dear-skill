#!/usr/bin/env python3
from pathlib import Path

HTML = Path(__file__).resolve().parent / "night-four-the-turn.html"
html = HTML.read_text(encoding="utf-8")

# Make configured PNG-based sprites behave like 2D layers: order wins over depth.
html = html.replace(
    "new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.96 })",
    "new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.96, depthTest: false, depthWrite: false })",
)
html = html.replace(
    "new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.0, depthWrite: false })",
    "new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0.0, depthTest: false, depthWrite: false })",
)

# Ceiling sentence lyrics should also not be unexpectedly clipped by other transparent layers.
html = html.replace(
    "new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0, depthWrite: false })",
    "new THREE.SpriteMaterial({ map: t, transparent: true, opacity: 0, depthTest: false, depthWrite: false })",
)

# Falling lyric words: same visual size as ceiling lyric text, always above PNGs.
html = html.replace(
"""  const sp = new THREE.Sprite(new THREE.SpriteMaterial({
    map: tex(makeWordSprite(text, color)),
    transparent: true,
    opacity: 0.0,
    depthWrite: false,
  }));
  const widthScale = 0.24 + Math.min(text.length, 12) * 0.024;
  sp.scale.set(widthScale, 0.085, 1);""",
"""  const sp = new THREE.Sprite(new THREE.SpriteMaterial({
    map: tex(makeWordSprite(text, color)),
    transparent: true,
    opacity: 0.0,
    depthTest: false,
    depthWrite: false,
  }));
  const widthScale = 0.34 + Math.min(text.length, 12) * 0.035;
  sp.scale.set(widthScale, 0.18, 1);
  sp.renderOrder = 100;""")

HTML.write_text(html, encoding="utf-8")
print("Updated sprite depth behavior and falling lyric layer/size")
