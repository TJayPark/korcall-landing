#!/usr/bin/env python3
"""
KORCALL Marketing Video Generator
Generates 3 short-form TikTok/Reels videos for KORCALL Korean tutoring platform.
Uses Pillow for frame rendering and moviepy for video compositing.
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    ImageClip,
    CompositeVideoClip,
    concatenate_videoclips,
    vfx,
)

# === CONFIGURATION ===
WIDTH, HEIGHT = 1080, 1920
FPS = 30
OUTPUT_DIR = os.path.expanduser("~/korcall-landing/videos")
FONT_BOLD = "/tmp/fonts/Pretendard-Bold.otf"
FONT_REGULAR = "/tmp/fonts/Pretendard-Regular.otf"

# Colors
DARK_BG = "#1a1a2e"
DARK_BG2 = "#16213e"
MAGENTA = "#d004d4"
BRIGHT_GREEN = "#39ff14"
NEON_BLUE = "#00d4ff"
PINK = "#ff6b9d"
CORAL = "#ff6b6b"
GOLD = "#ffd700"
WHITE = "#ffffff"
LIGHT_GRAY = "#cccccc"
RED = "#ff3333"
SUBTITLE_BG = "#0f0f23"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def get_font(size, bold=True):
    path = FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(path, size)


def text_bbox_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def make_gradient_bg(color1, color2, width=WIDTH, height=HEIGHT):
    """Create a vertical gradient background."""
    c1 = hex_to_rgb(color1)
    c2 = hex_to_rgb(color2)
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for y in range(height):
        r = int(c1[0] + (c2[0] - c1[0]) * y / height)
        g = int(c1[1] + (c2[1] - c1[1]) * y / height)
        b = int(c1[2] + (c2[2] - c1[2]) * y / height)
        for x in range(width):
            pixels[x, y] = (r, g, b)
    return img


def draw_rounded_rect(draw, xy, fill, radius=20):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def draw_centered_text(draw, y, text, font, fill, img_width=WIDTH, max_width=None):
    """Draw text centered horizontally at given y position.
    If max_width is set, wraps text to fit."""
    if max_width is None:
        max_width = img_width - 200  # padding

    # Simple word wrap
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        tw, _ = text_bbox_size(draw, test_line, font)
        if tw <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    total_height = 0
    line_heights = []
    for line in lines:
        _, lh = text_bbox_size(draw, line, font)
        line_heights.append(lh)
        total_height += lh + 10

    current_y = y
    for i, line in enumerate(lines):
        tw, th = text_bbox_size(draw, line, font)
        x = (img_width - tw) // 2
        draw.text((x, current_y), line, font=font, fill=fill)
        current_y += line_heights[i] + 10


def create_frame(bg_img, elements):
    """Create a frame with text elements drawn on a background.
    elements: list of dicts with keys: y, text, font_size, color, bold, max_width
    """
    img = bg_img.copy()
    draw = ImageDraw.Draw(img)

    for el in elements:
        font = get_font(el.get("font_size", 60), el.get("bold", True))
        fill = el.get("color", WHITE)
        if isinstance(fill, str):
            fill = hex_to_rgb(fill)
        draw_centered_text(
            draw,
            el["y"],
            el["text"],
            font,
            fill,
            max_width=el.get("max_width", WIDTH - 200),
        )

    return np.array(img)


def create_frame_with_badge(bg_img, elements, badge=None):
    """Create frame with optional badge/tag element."""
    img = bg_img.copy()
    draw = ImageDraw.Draw(img)

    if badge:
        bfont = get_font(badge.get("font_size", 36), True)
        tw, th = text_bbox_size(draw, badge["text"], bfont)
        bx = (WIDTH - tw - 40) // 2
        by = badge["y"]
        draw_rounded_rect(
            draw,
            (bx, by, bx + tw + 40, by + th + 20),
            fill=hex_to_rgb(badge.get("bg_color", MAGENTA)),
            radius=15,
        )
        draw.text(
            (bx + 20, by + 10),
            badge["text"],
            font=bfont,
            fill=hex_to_rgb(badge.get("color", WHITE)),
        )

    for el in elements:
        font = get_font(el.get("font_size", 60), el.get("bold", True))
        fill = el.get("color", WHITE)
        if isinstance(fill, str):
            fill = hex_to_rgb(fill)
        draw_centered_text(
            draw,
            el["y"],
            el["text"],
            font,
            fill,
            max_width=el.get("max_width", WIDTH - 200),
        )

    return np.array(img)


def crossfade_clips(clips, fade_duration=0.4):
    """Apply crossfade between clips using moviepy 2.x effects."""
    if len(clips) <= 1:
        return clips[0] if clips else None

    result_clips = []
    for i, clip in enumerate(clips):
        effects = []
        if i > 0:
            effects.append(vfx.CrossFadeIn(fade_duration))
        if i < len(clips) - 1:
            effects.append(vfx.CrossFadeOut(fade_duration))
        if effects:
            clip = clip.with_effects(effects)
        result_clips.append(clip)

    return concatenate_videoclips(result_clips, method="compose")


def build_scene(frame_array, duration):
    """Build a scene clip from a numpy frame array."""
    return ImageClip(frame_array).with_duration(duration)


def add_fade(clip, fade_in=0.3, fade_out=0.3):
    """Add fade in and fade out to a clip using moviepy 2.x effects."""
    effects = []
    if fade_in > 0:
        effects.append(vfx.FadeIn(fade_in))
    if fade_out > 0:
        effects.append(vfx.FadeOut(fade_out))
    if effects:
        return clip.with_effects(effects)
    return clip


# ============================
# VIDEO 1: Korean Phrases K-Drama Taught You WRONG
# ============================
def generate_video1():
    print("Generating Video 1: K-Drama Wrong Phrases...")
    bg = make_gradient_bg(DARK_BG, "#0e0e1a")

    # Screen 1: Hook (0-2s)
    frame1 = create_frame(
        bg,
        [
            {"y": 650, "text": "Korean phrases", "font_size": 80, "color": WHITE},
            {"y": 760, "text": "you learned", "font_size": 80, "color": WHITE},
            {
                "y": 870,
                "text": "WRONG",
                "font_size": 110,
                "color": RED,
                "bold": True,
            },
            {
                "y": 1010,
                "text": "from K-dramas",
                "font_size": 75,
                "color": LIGHT_GRAY,
            },
            {"y": 1150, "text": "😱", "font_size": 120, "color": WHITE},
        ],
    )

    # Screen 2: Oppa (2-6s)
    frame2_bg = make_gradient_bg("#1a1a2e", "#2d1b4e")
    frame2 = create_frame(
        frame2_bg,
        [
            {
                "y": 450,
                "text": "옵빠 (Oppa)",
                "font_size": 90,
                "color": MAGENTA,
                "bold": True,
            },
            {"y": 620, "text": "❌", "font_size": 100, "color": RED},
            {
                "y": 770,
                "text": "You say it to",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
            {
                "y": 850,
                "text": "every Korean guy?",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
            {
                "y": 1020,
                "text": "Only for OLDER guys",
                "font_size": 60,
                "color": BRIGHT_GREEN,
            },
            {
                "y": 1110,
                "text": "you're close with!",
                "font_size": 60,
                "color": BRIGHT_GREEN,
            },
        ],
    )

    # Screen 3: Aigo (6-10s)
    frame3_bg = make_gradient_bg("#1a1a2e", "#1b2e4e")
    frame3 = create_frame(
        frame3_bg,
        [
            {
                "y": 450,
                "text": "아이고 (Aigo)",
                "font_size": 90,
                "color": NEON_BLUE,
                "bold": True,
            },
            {
                "y": 650,
                "text": "It's NOT just",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
            {
                "y": 730,
                "text": "frustration",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
            {
                "y": 900,
                "text": "Koreans say it for",
                "font_size": 60,
                "color": BRIGHT_GREEN,
            },
            {
                "y": 990,
                "text": "EVERYTHING 😂",
                "font_size": 70,
                "color": BRIGHT_GREEN,
                "bold": True,
            },
        ],
    )

    # Screen 4: Daebak (10-14s)
    frame4_bg = make_gradient_bg("#1a1a2e", "#2e1b2e")
    frame4 = create_frame(
        frame4_bg,
        [
            {
                "y": 450,
                "text": "대박 (Daebak)",
                "font_size": 90,
                "color": GOLD,
                "bold": True,
            },
            {
                "y": 650,
                "text": "Textbook: Amazing!",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
            {
                "y": 830,
                "text": "Real life:",
                "font_size": 60,
                "color": WHITE,
            },
            {
                "y": 930,
                "text": "Can mean good",
                "font_size": 65,
                "color": BRIGHT_GREEN,
                "bold": True,
            },
            {
                "y": 1030,
                "text": "OR bad!",
                "font_size": 65,
                "color": RED,
                "bold": True,
            },
        ],
    )

    # Screen 5: CTA tease (14-18s)
    frame5 = create_frame(
        bg,
        [
            {
                "y": 700,
                "text": "Want to learn",
                "font_size": 75,
                "color": WHITE,
            },
            {
                "y": 820,
                "text": "REAL Korean?",
                "font_size": 85,
                "color": MAGENTA,
                "bold": True,
            },
            {
                "y": 1000,
                "text": "From REAL Koreans?",
                "font_size": 70,
                "color": NEON_BLUE,
            },
        ],
    )

    # Screen 6: CTA (18-22s)
    frame6_bg = make_gradient_bg("#0e0e1a", "#1a0a2e")
    frame6 = create_frame(
        frame6_bg,
        [
            {"y": 650, "text": "🔗", "font_size": 120, "color": WHITE},
            {
                "y": 820,
                "text": "KORCALL",
                "font_size": 110,
                "color": MAGENTA,
                "bold": True,
            },
            {
                "y": 990,
                "text": "Real Korean from",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
            {
                "y": 1070,
                "text": "Real Koreans",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
            {
                "y": 1220,
                "text": "Link in bio",
                "font_size": 65,
                "color": BRIGHT_GREEN,
                "bold": True,
            },
        ],
    )

    clips = [
        add_fade(build_scene(frame1, 2.0)),
        add_fade(build_scene(frame2, 4.0)),
        add_fade(build_scene(frame3, 4.0)),
        add_fade(build_scene(frame4, 4.0)),
        add_fade(build_scene(frame5, 4.0)),
        add_fade(build_scene(frame6, 4.0)),
    ]

    final = concatenate_videoclips(clips, method="compose")
    outpath = os.path.join(OUTPUT_DIR, "video1-kdrama-wrong.mp4")
    final.write_videofile(outpath, fps=FPS, codec="libx264", audio=False)
    print(f"Video 1 saved to {outpath}")
    return outpath


# ============================
# VIDEO 2: 5 Korean Words You Already Know from K-pop
# ============================
def generate_video2():
    print("Generating Video 2: K-pop Words You Know...")

    gradient_pairs = [
        ("#1a0a3e", "#0e0e2a"),  # Hook - deep purple
        ("#3e0a2a", "#1a0a1e"),  # Saranghae - pink/red
        ("#0a2e3e", "#0a1a2e"),  # Fighting - blue
        ("#3e2a0a", "#1e1a0a"),  # Oppa - warm
        ("#0a3e2e", "#0a1e1a"),  # Mansae - green
        ("#3e0a3e", "#1e0a1e"),  # Daebak - magenta
        ("#1a0a3e", "#0e0e1a"),  # CTA
    ]

    # Screen 1: Hook
    bg1 = make_gradient_bg(*gradient_pairs[0])
    frame1 = create_frame(
        bg1,
        [
            {
                "y": 700,
                "text": "You already",
                "font_size": 85,
                "color": WHITE,
            },
            {
                "y": 830,
                "text": "speak Korean",
                "font_size": 90,
                "color": MAGENTA,
                "bold": True,
            },
            {"y": 1000, "text": "🤯", "font_size": 140, "color": WHITE},
        ],
    )

    # Screen 2: Saranghae
    bg2 = make_gradient_bg(*gradient_pairs[1])
    frame2 = create_frame(
        bg2,
        [
            {
                "y": 450,
                "text": "사랑해",
                "font_size": 110,
                "color": PINK,
                "bold": True,
            },
            {
                "y": 610,
                "text": "(Saranghae)",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
            {"y": 780, "text": "=", "font_size": 70, "color": WHITE},
            {
                "y": 880,
                "text": '"I love you"',
                "font_size": 70,
                "color": WHITE,
                "bold": True,
            },
            {
                "y": 1050,
                "text": "Every K-pop song",
                "font_size": 50,
                "color": LIGHT_GRAY,
            },
            {
                "y": 1120,
                "text": "ever 💕",
                "font_size": 50,
                "color": LIGHT_GRAY,
            },
        ],
    )

    # Screen 3: Fighting
    bg3 = make_gradient_bg(*gradient_pairs[2])
    frame3 = create_frame(
        bg3,
        [
            {
                "y": 450,
                "text": "화이팅",
                "font_size": 110,
                "color": CORAL,
                "bold": True,
            },
            {
                "y": 610,
                "text": "(Fighting)",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
            {"y": 780, "text": "=", "font_size": 70, "color": WHITE},
            {
                "y": 880,
                "text": '"You got this!"',
                "font_size": 70,
                "color": WHITE,
                "bold": True,
            },
            {
                "y": 1050,
                "text": "What fans yell",
                "font_size": 50,
                "color": LIGHT_GRAY,
            },
            {
                "y": 1120,
                "text": "at concerts 🔥",
                "font_size": 50,
                "color": LIGHT_GRAY,
            },
        ],
    )

    # Screen 4: Oppa
    bg4 = make_gradient_bg(*gradient_pairs[3])
    frame4 = create_frame(
        bg4,
        [
            {
                "y": 450,
                "text": "오빠",
                "font_size": 110,
                "color": GOLD,
                "bold": True,
            },
            {
                "y": 610,
                "text": "(Oppa)",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
            {"y": 780, "text": "=", "font_size": 70, "color": WHITE},
            {
                "y": 870,
                "text": '"Older brother',
                "font_size": 65,
                "color": WHITE,
                "bold": True,
            },
            {
                "y": 960,
                "text": '/ babe"',
                "font_size": 65,
                "color": WHITE,
                "bold": True,
            },
            {
                "y": 1100,
                "text": "Your bias 😍",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
        ],
    )

    # Screen 5: Mansae
    bg5 = make_gradient_bg(*gradient_pairs[4])
    frame5 = create_frame(
        bg5,
        [
            {
                "y": 450,
                "text": "만세",
                "font_size": 110,
                "color": BRIGHT_GREEN,
                "bold": True,
            },
            {
                "y": 610,
                "text": "(Mansae)",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
            {"y": 780, "text": "=", "font_size": 70, "color": WHITE},
            {
                "y": 880,
                "text": '"Hooray!"',
                "font_size": 70,
                "color": WHITE,
                "bold": True,
            },
            {
                "y": 1050,
                "text": "SVT taught us",
                "font_size": 50,
                "color": LIGHT_GRAY,
            },
            {
                "y": 1120,
                "text": "this one 🎵",
                "font_size": 50,
                "color": LIGHT_GRAY,
            },
        ],
    )

    # Screen 6: Daebak
    bg6 = make_gradient_bg(*gradient_pairs[5])
    frame6 = create_frame(
        bg6,
        [
            {
                "y": 450,
                "text": "대박",
                "font_size": 110,
                "color": NEON_BLUE,
                "bold": True,
            },
            {
                "y": 610,
                "text": "(Daebak)",
                "font_size": 55,
                "color": LIGHT_GRAY,
            },
            {"y": 780, "text": "=", "font_size": 70, "color": WHITE},
            {
                "y": 880,
                "text": '"OMG / Amazing"',
                "font_size": 70,
                "color": WHITE,
                "bold": True,
            },
            {
                "y": 1050,
                "text": "Your reaction to",
                "font_size": 50,
                "color": LIGHT_GRAY,
            },
            {
                "y": 1120,
                "text": "every comeback 🤩",
                "font_size": 50,
                "color": LIGHT_GRAY,
            },
        ],
    )

    # Screen 7: CTA
    bg7 = make_gradient_bg(*gradient_pairs[6])
    frame7 = create_frame(
        bg7,
        [
            {
                "y": 600,
                "text": "Want to learn",
                "font_size": 70,
                "color": WHITE,
            },
            {
                "y": 720,
                "text": "100 more?",
                "font_size": 85,
                "color": BRIGHT_GREEN,
                "bold": True,
            },
            {
                "y": 920,
                "text": "KORCALL",
                "font_size": 110,
                "color": MAGENTA,
                "bold": True,
            },
            {
                "y": 1120,
                "text": "Link in bio 🔗",
                "font_size": 60,
                "color": NEON_BLUE,
            },
        ],
    )

    clips = [
        add_fade(build_scene(frame1, 2.5)),
        add_fade(build_scene(frame2, 3.0)),
        add_fade(build_scene(frame3, 3.0)),
        add_fade(build_scene(frame4, 3.0)),
        add_fade(build_scene(frame5, 3.0)),
        add_fade(build_scene(frame6, 3.0)),
        add_fade(build_scene(frame7, 4.5)),
    ]

    final = concatenate_videoclips(clips, method="compose")
    outpath = os.path.join(OUTPUT_DIR, "video2-kpop-words.mp4")
    final.write_videofile(outpath, fps=FPS, codec="libx264", audio=False)
    print(f"Video 2 saved to {outpath}")
    return outpath


# ============================
# VIDEO 3: What Your K-drama Bias ACTUALLY Said
# ============================
def generate_video3():
    print("Generating Video 3: Subtitle Lies...")
    bg = make_gradient_bg(SUBTITLE_BG, "#1a0a1e")

    # Screen 1: Hook
    frame1 = create_frame(
        bg,
        [
            {
                "y": 650,
                "text": "Netflix subtitles",
                "font_size": 80,
                "color": RED,
                "bold": True,
            },
            {
                "y": 790,
                "text": "LIE to you",
                "font_size": 95,
                "color": RED,
                "bold": True,
            },
            {"y": 960, "text": "😤", "font_size": 130, "color": WHITE},
        ],
    )

    # Screen 2: "I like you" vs actual
    def make_split_frame(
        sub_text, actual_korean, actual_romanized, actual_meaning, emoji, bg_pair=None
    ):
        if bg_pair:
            frame_bg = make_gradient_bg(*bg_pair)
        else:
            frame_bg = bg.copy()

        img = frame_bg.copy()
        draw = ImageDraw.Draw(img)

        # Top section: "Subtitle said:"
        label_font = get_font(40, False)
        sub_font = get_font(60, True)
        ko_font = get_font(75, True)
        roman_font = get_font(40, False)
        meaning_font = get_font(50, True)

        # "Subtitle said:" label
        tw, _ = text_bbox_size(draw, "Subtitle said:", label_font)
        draw.text(
            ((WIDTH - tw) // 2, 350),
            "Subtitle said:",
            font=label_font,
            fill=hex_to_rgb(LIGHT_GRAY),
        )

        # Subtitle text with red background
        tw, th = text_bbox_size(draw, f'"{sub_text}"', sub_font)
        rx = (WIDTH - tw - 40) // 2
        ry = 430
        draw_rounded_rect(
            draw, (rx, ry, rx + tw + 40, ry + th + 30), fill=(80, 20, 20), radius=15
        )
        draw.text(
            (rx + 20, ry + 12),
            f'"{sub_text}"',
            font=sub_font,
            fill=hex_to_rgb(WHITE),
        )

        # Divider line
        draw.line(
            [(200, 620), (WIDTH - 200, 620)], fill=hex_to_rgb(MAGENTA), width=3
        )

        # "Actually said:" label
        tw, _ = text_bbox_size(draw, "Actually said:", label_font)
        draw.text(
            ((WIDTH - tw) // 2, 680),
            "Actually said:",
            font=label_font,
            fill=hex_to_rgb(LIGHT_GRAY),
        )

        # Korean text
        tw, _ = text_bbox_size(draw, actual_korean, ko_font)
        draw.text(
            ((WIDTH - tw) // 2, 770),
            actual_korean,
            font=ko_font,
            fill=hex_to_rgb(NEON_BLUE),
        )

        # Romanized
        tw, _ = text_bbox_size(draw, f"({actual_romanized})", roman_font)
        draw.text(
            ((WIDTH - tw) // 2, 890),
            f"({actual_romanized})",
            font=roman_font,
            fill=hex_to_rgb(LIGHT_GRAY),
        )

        # Actual meaning with green bg
        tw, th = text_bbox_size(draw, actual_meaning, meaning_font)
        rx = (WIDTH - tw - 40) // 2
        ry = 1000
        draw_rounded_rect(
            draw, (rx, ry, rx + tw + 40, ry + th + 30), fill=(10, 60, 30), radius=15
        )
        draw.text(
            (rx + 20, ry + 12),
            actual_meaning,
            font=meaning_font,
            fill=hex_to_rgb(BRIGHT_GREEN),
        )

        # Emoji
        emoji_font = get_font(100, True)
        tw, _ = text_bbox_size(draw, emoji, emoji_font)
        draw.text(
            ((WIDTH - tw) // 2, 1180),
            emoji,
            font=emoji_font,
            fill=hex_to_rgb(WHITE),
        )

        return np.array(img)

    frame2 = make_split_frame(
        "I like you",
        "내가 미쳤나봐",
        "Naega michyeonnabwa",
        '"I think I\'ve gone crazy"',
        "Way more dramatic! 😭",
        ("#0f0f23", "#1a0a2e"),
    )

    frame3 = make_split_frame(
        "Let's eat",
        "밥 먹었어?",
        "Bap meogeosseo?",
        '"Have you eaten?"',
        "= I care about you 🥺",
        ("#0f0f23", "#0a1a2e"),
    )

    frame4 = make_split_frame(
        "I'm sorry",
        "잘못했어",
        "Jalmothaesseo",
        '"I did wrong"',
        "Hits different 💔",
        ("#0f0f23", "#1a0a1e"),
    )

    # Screen 5: Learn what they really mean
    frame5_bg = make_gradient_bg("#0f0f23", "#1a0a2e")
    frame5 = create_frame(
        frame5_bg,
        [
            {
                "y": 700,
                "text": "Learn what they",
                "font_size": 75,
                "color": WHITE,
            },
            {
                "y": 830,
                "text": "REALLY mean",
                "font_size": 90,
                "color": NEON_BLUE,
                "bold": True,
            },
        ],
    )

    # Screen 6: CTA
    frame6_bg = make_gradient_bg("#0f0f23", "#1a0a3e")
    frame6 = create_frame(
        frame6_bg,
        [
            {
                "y": 600,
                "text": "KORCALL",
                "font_size": 110,
                "color": MAGENTA,
                "bold": True,
            },
            {
                "y": 780,
                "text": "Real Korean from",
                "font_size": 55,
                "color": WHITE,
            },
            {
                "y": 860,
                "text": "Real Koreans",
                "font_size": 55,
                "color": WHITE,
            },
            {
                "y": 1050,
                "text": "Link in bio 🔗",
                "font_size": 65,
                "color": BRIGHT_GREEN,
                "bold": True,
            },
        ],
    )

    clips = [
        add_fade(build_scene(frame1, 2.5)),
        add_fade(build_scene(frame2, 4.0)),
        add_fade(build_scene(frame3, 4.0)),
        add_fade(build_scene(frame4, 4.0)),
        add_fade(build_scene(frame5, 3.5)),
        add_fade(build_scene(frame6, 4.0)),
    ]

    final = concatenate_videoclips(clips, method="compose")
    outpath = os.path.join(OUTPUT_DIR, "video3-subtitle-lies.mp4")
    final.write_videofile(outpath, fps=FPS, codec="libx264", audio=False)
    print(f"Video 3 saved to {outpath}")
    return outpath


# ============================
# MAIN
# ============================
if __name__ == "__main__":
    print("=" * 60)
    print("KORCALL Video Generator")
    print("=" * 60)

    v1 = generate_video1()
    v2 = generate_video2()
    v3 = generate_video3()

    print("\n" + "=" * 60)
    print("All videos generated!")
    print(f"  1. {v1}")
    print(f"  2. {v2}")
    print(f"  3. {v3}")
    print("=" * 60)
