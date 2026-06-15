"""
Print Lab Wraps — Homepage Poster Generator
Produces a 2400 × 3600 px (24×36 in @ 100 dpi) poster mockup.
"""

from PIL import Image, ImageDraw, ImageFont
import math, os, sys

# ── Canvas ──────────────────────────────────────────────────────────────
W, H = 2400, 3600
img  = Image.new("RGB", (W, H), "#000000")
d    = ImageDraw.Draw(img)

# ── Brand Palette ────────────────────────────────────────────────────────
BLACK    = "#000000"
DARK     = "#0d0d0d"
DARK2    = "#111111"
DARK3    = "#1a1a1a"
RED      = "#E31837"
RED_DARK = "#C0122D"
WHITE    = "#FFFFFF"
GRAY4    = "#9a9a9a"
GRAY6    = "#555555"
GRAY8    = "#2a2a2a"

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ── Font loader (system fallback) ────────────────────────────────────────
def fnt(size, bold=False):
    try:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
            else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
        for p in paths:
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    except Exception:
        pass
    return ImageFont.load_default()

F_BLACK   = fnt(120, bold=True)
F_HERO    = fnt(100, bold=True)
F_H1      = fnt(80,  bold=True)
F_H2      = fnt(60,  bold=True)
F_H3      = fnt(44,  bold=True)
F_H4      = fnt(34,  bold=True)
F_LABEL   = fnt(22,  bold=True)
F_BODY    = fnt(26)
F_SM      = fnt(22)
F_XS      = fnt(18,  bold=True)
F_NAV     = fnt(20,  bold=True)
F_BTN     = fnt(24,  bold=True)

# ── Helpers ──────────────────────────────────────────────────────────────
def rect(x, y, w, h, fill, radius=0):
    if radius:
        d.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=fill)
    else:
        d.rectangle([x, y, x+w, y+h], fill=fill)

def text(t, x, y, font, fill=WHITE, anchor="la"):
    d.text((x, y), t, font=font, fill=fill, anchor=anchor)

def centered_text(t, y, font, fill=WHITE, width=W):
    bb = d.textbbox((0, 0), t, font=font)
    tw = bb[2] - bb[0]
    d.text(((width - tw) // 2, y), t, font=font, fill=fill)

def label_tag(t, x, y):
    """Red uppercase label with leading bar."""
    bw = d.textlength(t, font=F_LABEL) + 24
    rect(x, y, 6, 26, RED)
    text(t, x + 20, y, F_LABEL, fill=RED)

def btn(label, x, y, bw=380, primary=True):
    bg = RED if primary else "#1a1a1a"
    border = RED if primary else "#555"
    rect(x, y, bw, 72, bg, radius=6)
    if not primary:
        d.rounded_rectangle([x, y, x+bw, y+72], radius=6, outline=border, width=2)
    bb = d.textbbox((0,0), label, font=F_BTN)
    tw = bb[2]-bb[0]
    text(label, x + (bw-tw)//2, y + 22, F_BTN, fill=WHITE)

def divider_line(y, color=GRAY8):
    d.line([(0, y), (W, y)], fill=color, width=1)

def star_row(x, y, n=5, size=28):
    for i in range(n):
        d.polygon([
            (x+i*36+size//2, y),
            (x+i*36+size//2+4, y+10),
            (x+i*36+size, y+10),
            (x+i*36+size//2+7, y+17),
            (x+i*36+size//2+10, y+28),
            (x+i*36+size//2, y+22),
            (x+i*36+size//2-10, y+28),
            (x+i*36+size//2-7, y+17),
            (x+i*36, y+10),
            (x+i*36+size//2-4, y+10),
        ], fill=RED)

def check(x, y):
    d.line([(x, y+8), (x+8, y+16), (x+20, y)], fill=RED, width=3)

# ── SECTION 1: HEADER ────────────────────────────────────────────────────
rect(0, 0, W, 100, DARK2)
# Red left accent bar
rect(0, 0, 6, 100, RED)
# Logo
text("PrintLab", 60, 18, fnt(34, bold=True), fill=WHITE)
text("Wraps ★", 60, 54, fnt(28, bold=True), fill=RED)
# Nav links
nav_items = ["SERVICES", "ABOUT", "CAREERS", "CONTACT", "OUR WORK"]
nx = 680
for item in nav_items:
    text(item, nx, 40, F_NAV, fill=GRAY4)
    nx += d.textlength(item, font=F_NAV) + 50
# CTAs
rect(W-480, 20, 210, 60, "#1a1a1a", radius=4)
d.rounded_rectangle([W-480, 20, W-270, 80], radius=4, outline="#555", width=2)
text("Call Us", W-480+60, 35, F_BTN, fill=WHITE)
rect(W-240, 20, 210, 60, RED, radius=4)
text("Get Estimate", W-240+18, 35, F_BTN, fill=WHITE)

# ── SECTION 2: HERO ──────────────────────────────────────────────────────
HERO_H = 920
rect(0, 100, W, HERO_H, DARK)

# Red accent bar (left edge)
rect(0, 100, 6, HERO_H, RED)

# Dark gradient overlay with diagonal lines
for i in range(0, W+H, 80):
    d.line([(i, 100), (i-H, 100+HERO_H)], fill=(227, 24, 55, 6), width=1)

# Silhouette vehicle shape (decorative)
veh_x, veh_y = 1400, 380
# truck body
d.rounded_rectangle([veh_x, veh_y+80, veh_x+820, veh_y+280], radius=12,
                    fill=hex2rgb("#1a0505"), outline=hex2rgb("#2d0a0a"), width=2)
d.rounded_rectangle([veh_x+20, veh_y+20, veh_x+340, veh_y+100], radius=8,
                    fill=hex2rgb("#1a0505"), outline=hex2rgb("#2d0a0a"), width=2)
d.ellipse([veh_x+80, veh_y+260, veh_x+180, veh_y+360], fill=GRAY8, outline="#333", width=3)
d.ellipse([veh_x+610, veh_y+260, veh_x+710, veh_y+360], fill=GRAY8, outline="#333", width=3)
# Red stripe on truck
rect(veh_x, veh_y+140, 820, 16, RED)
# Glow behind truck
for r in range(5, 0, -1):
    d.ellipse([veh_x+300-r*20, veh_y+200-r*10, veh_x+520+r*20, veh_y+300+r*10],
              outline=(227, 24, 55, 15*r), width=1)

# Hero badge
rect(100, 160, 380, 40, hex2rgb("#1a0000"), radius=4)
rect(100, 160, 4, 40, RED)
text("PREMIUM VEHICLE WRAPS & SIGNAGE", 112, 170, F_XS, fill=RED)

# Main headline
text("MAKE YOUR", 100, 225, F_BLACK, fill=WHITE)
text("BRAND MOVE.", 100, 340, F_BLACK, fill=RED)
outline_font = fnt(100, bold=True)
# Outline text: draw border passes then dark fill to simulate outline
for ox in range(-3, 4):
    for oy in range(-3, 4):
        if ox or oy:
            d.text((100+ox, 455+oy), "DOMINATE ROADS.", font=outline_font, fill=GRAY4)
d.text((100, 455), "DOMINATE ROADS.", font=outline_font, fill=BLACK)

# Subheadline
sub = "Industry-leading vehicle wraps, commercial signage,"
sub2 = "and building graphics — installed by certified craftsmen."
text(sub,  100, 595, F_BODY, fill=GRAY4)
text(sub2, 100, 632, F_BODY, fill=GRAY4)

# CTA buttons
btn("GET PROJECT ESTIMATE", 100, 700, bw=420, primary=True)
btn("CALL US TODAY", 550, 700, bw=320, primary=False)

# Trust bar
trust_items = ["★ 5-Star Rated", "✓ Certified Installers", "⚡ Fast Turnaround", "◆ 3M & Avery Films"]
tx = 100
for ti in trust_items:
    tw = d.textlength(ti, font=F_SM)
    text(ti, tx, 820, F_SM, fill=hex2rgb("#aaaaaa"))
    tx += tw + 60

# ── SECTION 3: VEHICLE WRAPS FOCUS ───────────────────────────────────────
SEC2_Y = 1020
SEC2_H = 480
rect(0, SEC2_Y, W, SEC2_H, hex2rgb(DARK2))
divider_line(SEC2_Y)

# Left content
label_tag("VEHICLE WRAPS", 100, SEC2_Y + 50)
text("TURN EVERY MILE", 100, SEC2_Y + 100, F_H2, fill=WHITE)
text("INTO MARKETING.", 100, SEC2_Y + 175, F_H2, fill=RED)

body_lines = [
    "From single vehicles to full commercial fleets — we transform",
    "your transportation into powerful moving billboards that generate",
    "thousands of impressions daily.",
]
for i, line in enumerate(body_lines):
    text(line, 100, SEC2_Y + 280 + i*35, F_SM, fill=GRAY4)

btn("COMMERCIAL WRAPS", 100, SEC2_Y + 390, bw=360, primary=True)
btn("ALL SERVICES", 490, SEC2_Y + 390, bw=280, primary=False)

# Right: two image cards
cx = 1250
for ci, (label, bg1, bg2) in enumerate([
    ("Commercial Fleet Wraps", "#1a0505", "#2d0808"),
    ("Recreational Vehicle Wraps", "#0a0a1a", "#1a1a2d"),
]):
    cx_pos = cx + ci * 590
    rect(cx_pos, SEC2_Y + 40, 560, 380, hex2rgb(bg1), radius=8)
    # Gradient-like overlay
    for gi in range(20):
        alpha_fill = hex2rgb(bg2)
        rect(cx_pos, SEC2_Y + 40 + gi*19, 560, 19, alpha_fill)
    # Card label
    rect(cx_pos, SEC2_Y + 360, 560, 60, hex2rgb("#00000099" if "#" in "#000" else "#000000"), radius=8)
    text("COMMERCIAL" if ci==0 else "RECREATIONAL", cx_pos+16, SEC2_Y + 368, F_XS, fill=RED)
    text(label, cx_pos+16, SEC2_Y + 390, fnt(24, bold=True), fill=WHITE)

# ── SECTION 4: SERVICES ──────────────────────────────────────────────────
SEC3_Y = 1500
SEC3_H = 520
rect(0, SEC3_Y, W, SEC3_H, hex2rgb(BLACK))
divider_line(SEC3_Y)

centered_text("WHAT WE DO", SEC3_Y + 40, F_LABEL, fill=RED)
centered_text("FULL-SERVICE VISUAL BRANDING", SEC3_Y + 80, F_H2, fill=WHITE)

services = [
    ("Commercial\nVehicle Wraps", "Fleet branding\nfor any vehicle"),
    ("Vehicle\nWraps", "Personal cars,\ntrucks & SUVs"),
    ("Signage\n& Prints", "Banners, window\ngraphics & more"),
    ("Buildings\n& Facilities", "Wall murals,\narchitectural wraps"),
    ("Other\nOfferings", "Boats, trailers,\nspecialty projects"),
]
sw = (W - 200) // 5 - 20
sx = 100
for title, desc in services:
    rect(sx, SEC3_Y + 170, sw, 300, hex2rgb(DARK2), radius=8)
    d.rounded_rectangle([sx, SEC3_Y+170, sx+sw, SEC3_Y+470], radius=8,
                        outline=hex2rgb(GRAY8), width=1)
    # Icon circle
    rect(sx + sw//2 - 35, SEC3_Y + 200, 70, 70, hex2rgb("#1a0000"), radius=8)
    d.rounded_rectangle([sx+sw//2-35, SEC3_Y+200, sx+sw//2+35, SEC3_Y+270],
                        radius=8, outline=hex2rgb("#3d0010"), width=1)
    d.ellipse([sx+sw//2-14, SEC3_Y+221, sx+sw//2+14, SEC3_Y+249], outline=RED, width=2)
    # Title
    for li, line in enumerate(title.split("\n")):
        lw = d.textlength(line, font=F_H4)
        d.text((sx + (sw-lw)//2, SEC3_Y + 288 + li*40), line, font=F_H4, fill=WHITE)
    # Desc
    for li, line in enumerate(desc.split("\n")):
        lw = d.textlength(line, font=F_SM)
        d.text((sx + (sw-lw)//2, SEC3_Y + 382 + li*30), line, font=F_SM, fill=GRAY4)
    # Arrow
    lw = d.textlength("Learn More →", font=F_XS)
    d.text((sx + (sw-lw)//2, SEC3_Y + 444), "Learn More →", font=F_XS, fill=RED)
    sx += sw + 20

# ── SECTION 5: WHY PRINT LAB WRAPS ───────────────────────────────────────
SEC4_Y = 2020
SEC4_H = 380
rect(0, SEC4_Y, W, SEC4_H, hex2rgb(DARK2))
divider_line(SEC4_Y)

centered_text("WHY CHOOSE US", SEC4_Y + 40, F_LABEL, fill=RED)
centered_text("THE PRINT LAB DIFFERENCE", SEC4_Y + 80, F_H2, fill=WHITE)

stats = [("10+", "Years Experience"), ("2,500+", "Projects Completed"),
         ("98%", "Customer Satisfaction"), ("3", "Material Partners"), ("15+", "Certified Installers")]
sw2 = (W - 200) // 5
sx2 = 100
for num, lbl in stats:
    # cell
    rect(sx2, SEC4_Y+165, sw2-4, 175, hex2rgb(DARK3), radius=0)
    d.rectangle([sx2, SEC4_Y+165, sx2+sw2-4, SEC4_Y+340], outline=hex2rgb(GRAY8), width=1)
    nw = d.textlength(num, font=F_H2)
    d.text((sx2 + (sw2-nw)//2 - 2, SEC4_Y+180), num, font=F_H2, fill=RED)
    lw = d.textlength(lbl, font=F_SM)
    d.text((sx2 + (sw2-lw)//2 - 2, SEC4_Y+270), lbl, font=F_SM, fill=GRAY4)
    sx2 += sw2

# ── SECTION 6: OUR WORK PREVIEW ──────────────────────────────────────────
SEC5_Y = 2400
SEC5_H = 440
rect(0, SEC5_Y, W, SEC5_H, hex2rgb(BLACK))
divider_line(SEC5_Y)

label_tag("PORTFOLIO", 100, SEC5_Y + 40)
text("OUR WORK SPEAKS.", 100, SEC5_Y + 88, F_H2, fill=WHITE)
btn("VIEW FULL PORTFOLIO →", W-500, SEC5_Y + 88, bw=360, primary=False)

port_colors = [("#2d0808","#1a0505"), ("#050520","#0a0a1a"), ("#052005","#0a1a05")]
port_labels = ["Commercial Fleet", "Color Change", "Retail Signage"]
pw = (W - 260) // 3
px = 100
for i, ((c1,c2), lbl) in enumerate(zip(port_colors, port_labels)):
    if i == 0: ph, pys = 300, SEC5_Y + 170  # tall first card
    else:       ph, pys = 145, SEC5_Y + 170 + (i-1)*155
    rect(px if i==0 else px+pw+30+(i-1)*(pw+30)//1,
         pys, pw, ph, hex2rgb(c1), radius=8)
    lbl_x = px if i==0 else px+pw+30
    lbl_y = pys
    # Gradient overlay bottom
    rect(lbl_x, lbl_y+ph-50, pw, 50, hex2rgb("#000000"), radius=0)
    text(lbl, lbl_x+16, lbl_y+ph-38, F_SM, fill=hex2rgb("#cccccc"))

# Correct layout: large left, two stacked right
rect(100, SEC5_Y+170, pw, 300, hex2rgb("#1a0505"), radius=8)
text("Commercial Fleet", 116, SEC5_Y+430, F_SM, fill=GRAY4)
rect(100+pw+30, SEC5_Y+170, pw, 140, hex2rgb("#050520"), radius=8)
text("Color Change", 116+pw+30, SEC5_Y+290, F_SM, fill=GRAY4)
rect(100+pw+30, SEC5_Y+330, pw, 140, hex2rgb("#052005"), radius=8)
text("Retail Signage", 116+pw+30, SEC5_Y+450, F_SM, fill=GRAY4)
rect(100+2*(pw+30), SEC5_Y+170, pw, 300, hex2rgb("#1a1005"), radius=8)
text("Building Wrap", 116+2*(pw+30), SEC5_Y+430, F_SM, fill=GRAY4)

# ── SECTION 7: PROCESS ───────────────────────────────────────────────────
SEC6_Y = 2840
SEC6_H = 380
rect(0, SEC6_Y, W, SEC6_H, hex2rgb(DARK2))
divider_line(SEC6_Y)

centered_text("HOW IT WORKS", SEC6_Y + 36, F_LABEL, fill=RED)
centered_text("WE MAKE THIS EASY.", SEC6_Y + 76, F_H2, fill=WHITE)

steps = [("01", "Discovery", "Consult, goals,\nvehicle types, timeline."),
         ("02", "Design",     "Detailed mockups\nto exact dimensions."),
         ("03", "Production", "Printed on premium\ncast vinyl film."),
         ("04", "Installation","Certified installers,\nclimate-controlled.")]

sw3 = (W - 200) // 4
sx3 = 100
for num, title, desc in steps:
    # Connector line
    if sx3 > 100:
        d.line([(sx3-sw3+80, SEC6_Y+188), (sx3+40, SEC6_Y+188)], fill=RED, width=2)
    # Circle
    cx3, cy3, cr = sx3 + 40, SEC6_Y + 188, 46
    d.ellipse([cx3-cr, cy3-cr, cx3+cr, cy3+cr], fill=RED)
    d.ellipse([cx3-cr-6, cy3-cr-6, cx3+cr+6, cy3+cr+6],
              outline=hex2rgb("#E3183733"), width=0)
    nw = d.textlength(num, font=F_H4)
    d.text((cx3 - nw//2, cy3 - 22), num, font=F_H4, fill=WHITE)
    # Title
    tw = d.textlength(title, font=F_H3)
    d.text((sx3 + 40 - tw//2, SEC6_Y + 252), title, font=F_H3, fill=WHITE)
    # Desc
    for li, line in enumerate(desc.split("\n")):
        lw2 = d.textlength(line, font=F_SM)
        d.text((sx3 + 40 - lw2//2, SEC6_Y + 302 + li*30), line, font=F_SM, fill=GRAY4)
    sx3 += sw3

# ── SECTION 8: FINAL CTA ─────────────────────────────────────────────────
SEC7_Y = 3220
SEC7_H = 380
# Background with diagonal lines
rect(0, SEC7_Y, W, SEC7_H, hex2rgb(DARK))
for i in range(0, W + SEC7_H, 80):
    d.line([(i, SEC7_Y), (i - SEC7_H, SEC7_Y + SEC7_H)],
           fill=(227, 24, 55, 18), width=1)
divider_line(SEC7_Y)

# Red gradient glow center
for r in range(8, 0, -1):
    d.ellipse([W//2-r*80, SEC7_Y+SEC7_H//2-r*40,
               W//2+r*80, SEC7_Y+SEC7_H//2+r*40],
              outline=(227, 24, 55, 8*r), width=1)

centered_text("READY TO START?", SEC7_Y + 50, F_LABEL, fill=RED)
centered_text("LET'S BUILD SOMETHING", SEC7_Y + 95, F_H1, fill=WHITE)
centered_text("EXTRAORDINARY.", SEC7_Y + 180, F_H1, fill=RED)

centered_text("Get your free project estimate today.", SEC7_Y + 278, F_BODY, fill=GRAY4)

btn_w, gap = 400, 24
total = btn_w*2 + gap
bx = (W - total) // 2
btn("GET FREE ESTIMATE", bx, SEC7_Y + 316, bw=btn_w, primary=True)
btn("CALL (555) PLW-WRAP", bx+btn_w+gap, SEC7_Y + 316, bw=btn_w, primary=False)

# Star row + social proof
star_row(W//2 - 90, SEC7_Y + 412)
centered_text("5.0 Google Rating  •  200+ Reviews  •  10+ Years  •  2,500+ Projects", SEC7_Y + 458, F_XS, fill=GRAY4)

# ── FOOTER ───────────────────────────────────────────────────────────────
FOOT_Y = H - 100
rect(0, FOOT_Y, W, 100, hex2rgb(DARK2))
divider_line(FOOT_Y)
text("PrintLab", 100, FOOT_Y + 14, fnt(30, bold=True), fill=WHITE)
text("Wraps ★", 100, FOOT_Y + 48, fnt(24, bold=True), fill=RED)
centered_text("© 2025 Print Lab Wraps  •  All Rights Reserved  •  Terms  •  Privacy", FOOT_Y + 40, F_XS, fill=GRAY6)
text("(555) PLW-WRAP  |  info@printlabwraps.com  |  printlabwraps.com", W-100, FOOT_Y + 40, F_XS, fill=GRAY4, anchor="ra")

# ── WATERMARK / BRANDING STRIP ───────────────────────────────────────────
# thin red strip at very top
rect(0, 0, W, 4, RED)

# ── SAVE ─────────────────────────────────────────────────────────────────
out = "/home/user/https-github.com-nextlevelbuilder-ui-ux-pro-max-skill/printlabwraps/PrintLabWraps_Homepage_Poster.png"
img.save(out, "PNG", optimize=True)
print(f"Saved: {out}  ({W}×{H}px)")
