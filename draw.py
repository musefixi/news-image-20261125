#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news collage (1024x1024 PNG).

All artwork is drawn with Pillow shapes and text; no external images.
Six panels, each a verified 25 Nov 2026 story, plus a sports strip.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (18, 58, 92)
ORANGE = (240, 120, 40)
TEAL = (20, 130, 120)
CREAM = (246, 240, 224)
INK = (24, 28, 36)
WHITE = (255, 255, 255)

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def centred(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)

def tag(draw, x, y, label, bg, fg=WHITE):
    f = font(BOLD, 19)
    w = draw.textlength(label, font=f) + 26
    draw.rounded_rectangle([x, y, x + w, y + 30], radius=15, fill=bg, outline=WHITE, width=2)
    draw.text((x + 13, y + 4), label, font=f, fill=fg)

def flame(draw, cx, cy, s=1.0):
    # simple orange/yellow flame
    draw.polygon([(cx - 26 * s, cy + 20 * s), (cx - 6 * s, cy - 28 * s),
                  (cx + 8 * s, cy - 6 * s), (cx + 26 * s, cy + 20 * s)],
                 fill=(255, 140, 0))
    draw.ellipse([cx - 12 * s, cy - 6 * s, cx + 12 * s, cy + 20 * s], fill=(255, 210, 40))

def tanker(draw, x, y, w, hull=(40, 48, 60)):
    draw.rectangle([x, y, x + w, y + 26], fill=hull)
    draw.rectangle([x + w * 0.15, y - 22, x + w * 0.35, y], fill=(70, 78, 90))
    draw.rectangle([x + w * 0.55, y - 16, x + w * 0.75, y], fill=(70, 78, 90))
    draw.rectangle([x, y + 26, x + w, y + 30], fill=(200, 60, 40))

def mine(draw, cx, cy, r=14):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(50, 50, 55), outline=(20, 20, 20), width=2)
    for dx, dy in [(-r, 0), (r, 0), (0, -r), (0, r), (-10, -10), (10, -10), (-10, 10), (10, 10)]:
        draw.line([cx + dx * 0.7, cy + dy * 0.7, cx + dx * 1.5, cy + dy * 1.5],
                  fill=(50, 50, 55), width=3)

def stars(draw, x0, y0, x1, y1, n=24):
    import random
    rnd = random.Random(25)
    for _ in range(n):
        sx = rnd.randint(x0 + 6, x1 - 6)
        sy = rnd.randint(y0 + 6, y1 - 6)
        r = rnd.choice([1, 2, 2, 3])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=WHITE)

def panel(draw, x, y, w, pic_h, head_h, tag_label, tag_bg, headline, subline, bg, draw_scene):
    draw.rectangle([x, y, x + w, y + pic_h + head_h], fill=bg, outline=INK, width=3)
    draw_scene(draw, x, y, w, pic_h)
    tag(draw, x + 10, y + 10, tag_label, tag_bg)
    # headline strip
    hy = y + pic_h
    draw.rectangle([x, y + pic_h, x + w, y + pic_h + head_h], fill=CREAM, outline=INK, width=3)
    hf = font(BOLD, 24)
    lines = wrap(draw, headline, hf, w - 24)
    ly = hy + 6
    for ln in lines[:2]:
        centred(draw, x + w / 2, ly, ln, hf, INK)
        ly += 28
    sf = font(REG, 15)
    centred(draw, x + w / 2, hy + head_h - 22, subline, sf, (70, 75, 85))

# --- scenes (each receives the panel's picture area) ---
def scene_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.62], fill=(150, 200, 225))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(28, 90, 150))
    for i in range(4):
        wx = x + 60 + i * 115
        d.arc([wx, y + h * 0.66, wx + 70, y + h * 0.86], 0, 180, fill=WHITE, width=3)
    tanker(d, x + 40, y + 78, 170)
    tanker(d, x + 260, y + 92, 170, hull=(90, 50, 40))
    flame(d, x + 330, y + 62, 0.9)
    d.ellipse([x + 300, y + 18, x + 340, y + 48], fill=(90, 90, 95))
    d.ellipse([x + 330, y + 8, x + 362, y + 34], fill=(110, 110, 115))
    mine(d, x + 110, y + 138, 13)
    mine(d, x + 430, y + 148, 12)

def scene_houthi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 200, 120))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(120, 90, 60))
    # refinery towers
    for tx, th in [(x + 50, 90), (x + 110, 110), (x + 330, 100)]:
        d.rectangle([tx, y + h * 0.72 - th, tx + 42, y + h * 0.72], fill=(70, 70, 78))
        d.rectangle([tx + 12, y + h * 0.72 - th - 22, tx + 30, y + h * 0.72 - th], fill=(50, 50, 58))
    flame(d, x + 250, y + 82, 1.1)
    d.ellipse([x + 215, y + 22, x + 255, y + 52], fill=(90, 90, 95))
    # drone
    dx, dy = x + 380, y + 38
    d.ellipse([dx - 26, dy - 8, dx + 26, dy + 8], fill=(60, 60, 68))
    d.line([dx - 40, dy, dx + 40, dy], fill=(60, 60, 68), width=4)
    d.ellipse([dx - 52, dy - 5, dx - 30, dy + 5], fill=(40, 40, 46))
    d.ellipse([dx + 30, dy - 5, dx + 52, dy + 5], fill=(40, 40, 46))

def scene_huawei(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 24, 30))
    stars(d, x, y, x + w, y + h, 14)
    # chip
    cx, cy = x + w / 2, y + h / 2 + 6
    for i in range(4):
        px = cx - 66 + i * 44
        d.line([px, cy - 78, px, cy - 52], fill=(180, 180, 190), width=4)
        d.line([px, cy + 52, px, cy + 78], fill=(180, 180, 190), width=4)
    d.rounded_rectangle([cx - 78, cy - 52, cx + 78, cy + 52], radius=14, fill=(30, 160, 90), outline=(120, 220, 160), width=3)
    d.rounded_rectangle([cx - 48, cy - 28, cx + 48, cy + 28], radius=8, fill=(16, 90, 55))
    centred(d, cx, cy - 20, "H", font(BOLD, 40), WHITE)
    d.text((x + 18, y + h - 30), "GUILTY", font=font(BOLD, 22), fill=(255, 90, 70))

def scene_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 240, 245))
    # containers
    cols = [(200, 70, 60), (40, 110, 170), (230, 170, 40)]
    for i, c in enumerate(cols):
        bx = x + 46 + i * 130
        d.rectangle([bx, y + 118, bx + 112, y + 158], fill=c)
        for k in range(4):
            d.line([bx + 22 + k * 24, y + 118, bx + 22 + k * 24, y + 158], fill=(255, 255, 255), width=2)
    # rising/falling chart + % badge
    pts = [(x + 50, y + 92), (x + 130, y + 66), (x + 210, y + 78), (x + 300, y + 46), (x + 400, y + 58)]
    d.line(pts, fill=(200, 50, 40), width=5, joint="curve")
    d.polygon([(x + 400, y + 58), (x + 378, y + 44), (x + 382, y + 66)], fill=(200, 50, 40))
    d.ellipse([x + 392, y + 8, x + 472, y + 62], fill=(200, 50, 40), outline=WHITE, width=3)
    centred(d, x + 432, y + 12, "%", font(BOLD, 34), WHITE)

def scene_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 34))
    stars(d, x, y, x + w, y + h, 30)
    # station module
    d.rounded_rectangle([x + 150, y + 66, x + 350, y + 106], radius=20, fill=(190, 195, 205), outline=(120, 125, 135), width=2)
    d.rectangle([x + 60, y + 74, x + 150, y + 98], fill=(40, 90, 200))
    d.rectangle([x + 350, y + 74, x + 440, y + 98], fill=(40, 90, 200))
    d.ellipse([x + 228, y + 76, x + 258, y + 96], fill=(20, 60, 120))
    # capsule docking
    d.rounded_rectangle([x + 210, y + 118, x + 290, y + 148], radius=12, fill=(230, 230, 235), outline=(150, 150, 160), width=2)
    flame(d, x + 250, y + 168, 0.7)
    d.text((x + 20, y + h - 32), "TIANGONG", font=font(BOLD, 20), fill=(150, 200, 255))

def scene_pacific(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(170, 220, 235))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(30, 140, 180))
    for i in range(3):
        wx = x + 60 + i * 140
        d.arc([wx, y + h * 0.60, wx + 80, y + h * 0.82], 0, 180, fill=WHITE, width=3)
    # islands
    d.ellipse([x + 60, y + 92, x + 170, y + 128], fill=(60, 170, 90))
    d.ellipse([x + 300, y + 84, x + 390, y + 116], fill=(60, 170, 90))
    d.polygon([(x + 95, y + 92), (x + 115, y + 58), (x + 135, y + 92)], fill=(40, 140, 75))
    # treaty document + pen
    d.rectangle([x + 180, y + 96, x + 300, y + 158], fill=WHITE, outline=INK, width=2)
    for k in range(3):
        d.line([x + 192, y + 110 + k * 12, x + 288, y + 110 + k * 12], fill=(90, 100, 115), width=3)
    # shield with no-base cross
    d.ellipse([x + 380, y + 96, x + 452, y + 158], fill=(255, 255, 255), outline=INK, width=3)
    d.line([x + 392, y + 112, x + 440, y + 146], fill=(200, 50, 40), width=6)
    d.line([x + 440, y + 112, x + 392, y + 146], fill=(200, 50, 40), width=6)

def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=4)
    # header
    d.rectangle([14, 14, W - 15, 106], fill=NAVY, outline=INK, width=3)
    centred(d, W / 2, 26, "THE WORLD TODAY", font(BOLD, 56), ORANGE)
    # date line
    d.line([14, 148, W - 15, 148], fill=INK, width=3)
    centred(d, W / 2, 114, "WEDNESDAY 25 NOVEMBER 2026", font(BOLD, 30), TEAL)

    panels = [
        ("CONFLICT", (180, 40, 40), "TWO TANKERS HIT MINES",
         "IN THE STRAIT OF HORMUZ", "IRGC: vessels struck mines and caught fire", scene_hormuz, (150, 200, 225)),
        ("MIDDLE EAST", (200, 90, 30), "HOUTHIS STRIKE SAUDI",
         "REFINERY AT RAS TANURA", "Houthis say they attacked the oil refinery", scene_houthi, (250, 200, 120)),
        ("TECH", (20, 130, 90), "HUAWEI FOUND GUILTY",
         "IN U.S. CRIMINAL TRIAL", "Trade-secret theft and bank fraud convictions", scene_huawei, (22, 24, 30)),
        ("ECONOMY", (30, 90, 160), "U.S. PROPOSES NEW",
         "TARIFFS ON 14 PARTNERS", "Aimed at factory overcapacity; China hit hardest", scene_tariffs, (235, 240, 245)),
        ("SPACE", (90, 60, 160), "SHENZHOU-24 DOCKS",
         "AT TIANGONG STATION", "Pakistan's Zeeshan Ali: first foreigner aboard", scene_space, (10, 14, 34)),
        ("PACIFIC", (20, 120, 140), "SOLOMONS SIGN PACT",
         "WITH AUSTRALIA", "Treaty bars any foreign military base on its soil", scene_pacific, (170, 220, 235)),
    ]
    # headline may be two lines: join parts for wrapping
    gx, gy = 14, 156
    col_w, row_h = 492, 248
    pic_h, head_h = 160, 88
    for i, (tag_label, tag_bg, h1, h2, sub, scene, bg) in enumerate(panels):
        x = gx + (i % 2) * (col_w + 12)
        y = gy + (i // 2) * (row_h + 12)
        panel(d, x, y, col_w, pic_h, head_h, tag_label, tag_bg,
              h1 + " " + h2, sub, bg, scene)

    # sports strip
    sy = gy + 3 * row_h + 2 * 12 + 12
    d.rectangle([14, sy, W - 15, sy + 46], fill=NAVY, outline=INK, width=3)
    centred(d, W / 2, sy + 10,
            "SPORT  •  LAKERS BEAT JAZZ — DONCIC 28 PTS  •  SINNER OUT AFTER KNEE SURGERY",
            font(BOLD, 20), WHITE)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
