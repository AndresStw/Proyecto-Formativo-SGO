#!/usr/bin/env python3
"""Create an animated GIF of repository commit counts by contributor."""

import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

INPUT = sys.argv[1] if len(sys.argv) > 1 else "contributors.json"
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else "stats/contributors.gif"
WIDTH = 960
ROW_HEIGHT = 62
TOP = 142
BOTTOM = 38
FRAMES = 24

with open(INPUT, encoding="utf-8") as source:
    contributors = json.load(source)

contributors = [
    item for item in contributors
    if item.get("login") and item.get("type") != "Bot"
]
contributors.sort(key=lambda item: item.get("contributions", 0), reverse=True)
contributors = contributors[:10]

os.makedirs(os.path.dirname(OUTPUT) or ".", exist_ok=True)

try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 27)
    label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)
    count_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 17)
except OSError:
    title_font = ImageFont.load_default()
    label_font = ImageFont.load_default()
    count_font = ImageFont.load_default()

height = TOP + max(len(contributors), 1) * ROW_HEIGHT + BOTTOM
max_count = max((item.get("contributions", 0) for item in contributors), default=1) or 1
bar_x = 300
bar_width = WIDTH - bar_x - 120
frames = []

for frame_index in range(FRAMES):
    image = Image.new("RGB", (WIDTH, height), "#0b1020")
    draw = ImageDraw.Draw(image)

    # Subtle blue-purple header gradient.
    for y in range(TOP):
        ratio = y / max(TOP - 1, 1)
        color = (
            int(18 + 16 * ratio),
            int(27 + 8 * ratio),
            int(55 + 35 * ratio),
        )
        draw.line((0, y, WIDTH, y), fill=color)

    draw.text((34, 28), "COMMITS POR COLABORADOR", font=title_font, fill="#f4f7ff")
    draw.text((36, 76), "Proyecto Formativo SGO  ·  datos de GitHub", font=label_font, fill="#b8c5e0")
    draw.rounded_rectangle((WIDTH - 176, 30, WIDTH - 34, 68), radius=18, fill="#23345f")
    draw.ellipse((WIDTH - 157, 44, WIDTH - 145, 56), fill="#54e0b5")
    draw.text((WIDTH - 135, 39), "ACTUALIZADO", font=label_font, fill="#d9e5ff")

    progress = frame_index / max(FRAMES - 1, 1)
    ease = 1 - (1 - progress) ** 3

    for index, item in enumerate(contributors):
        y = TOP + index * ROW_HEIGHT
        login = item["login"]
        count = int(item.get("contributions", 0))
        # Stagger the bar animation slightly by contributor row.
        local_progress = min(max((ease * 1.18) - index * 0.035, 0), 1)
        draw.text((36, y + 13), login[:24], font=label_font, fill="#edf2ff")
        draw.rounded_rectangle((bar_x, y + 15, bar_x + bar_width, y + 43), radius=12, fill="#202b46")
        current_width = max(2, int(bar_width * count / max_count * local_progress))
        draw.rounded_rectangle((bar_x, y + 15, bar_x + current_width, y + 43), radius=12, fill="#65a7ff")
        shown_count = int(count * local_progress)
        draw.text((bar_x + bar_width + 18, y + 17), str(shown_count), font=count_font, fill="#ffffff")

    frames.append(image)

frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=85,
    loop=0,
    optimize=True,
)
print(f"Generated {OUTPUT} with {len(contributors)} contributors")
