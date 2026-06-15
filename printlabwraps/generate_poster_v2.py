"""
Print Lab Wraps — Premium Homepage Mockup v2
2560 × 4800 px poster. Simulates the elevated design:
photography blocks, glassmorphism pills, animated elements,
overlapping image stack, marquee strip, service card grid, etc.
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageColor
import math, os, random

# ── Canvas ──────────────────────────────────────────────────────────────
W, H = 2560, 4800
canvas = Image.new("RGB", (W, H), "#000000")
d = ImageDraw.Draw(canvas)

# ── Palette ─────────────────────────────────────────────────────────────
BLACK   = (0,   0,   0)
DARK    = (13,  13,  13)
DARK2   = (17,  17,  17)
DARK3   = (26,  26,  26)
RED     = (227, 24,  55)
RED_D   = (160, 8,   30)
RED_A   = (227, 24,  55, 30)
WHITE   = (255, 255, 255)
W70     = (255, 255, 255, 178)
W40     = (255, 255, 255, 102)
W10     = (255, 255, 255, 26)
GRAY4   = (154, 154, 154)
GRAY6   = (85,  85,  85)
GRAY8   = (42,  42,  42)

def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ── Fonts ────────────────────────────────────────────────────────────────
FONT_PATHS_BOLD = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]
FONT_PATHS_REG = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
]
def fnt(size, bold=False):
    paths = FONT_PATHS_BOLD if bold else FONT_PATHS_REG
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

F900_120 = fnt(120, True)
F900_100 = fnt(100, True)
F900_86  = fnt(86,  True)
F900_72  = fnt(72,  True)
F900_60  = fnt(60,  True)
F700_48  = fnt(48,  True)
F700_40  = fnt(40,  True)
F700_36  = fnt(36,  True)
F700_30  = fnt(30,  True)
F700_26  = fnt(26,  True)
F700_22  = fnt(22,  True)
F700_18  = fnt(18,  True)
F400_30  = fnt(30,  False)
F400_26  = fnt(26,  False)
F400_22  = fnt(22,  False)
F400_18  = fnt(18,  False)

# ── Drawing helpers ──────────────────────────────────────────────────────
def fill(x, y, w, h, color, r=0):
    if r:
        d.rounded_rectangle([x, y, x+w, y+h], radius=r, fill=color)
    else:
        d.rectangle([x, y, x+w, y+h], fill=color)

def outline_rect(x, y, w, h, color, r=0, lw=2):
    if r:
        d.rounded_rectangle([x, y, x+w, y+h], radius=r, outline=color, width=lw)
    else:
        d.rectangle([x, y, x+w, y+h], outline=color, width=lw)

def tx(text, x, y, font, color=WHITE, anchor="lt"):
    d.text((x, y), text, font=font, fill=color, anchor=anchor)

def ctxt(text, y, font, color=WHITE, w=W):
    bb = d.textbbox((0,0), text, font=font)
    tw = bb[2]-bb[0]
    d.text(((w-tw)//2, y), text, font=font, fill=color)

def tw(text, font):
    bb = d.textbbox((0,0), text, font=font)
    return bb[2]-bb[0]

def hline(y, color=GRAY8, lw=1):
    d.line([(0, y), (W, y)], fill=color, width=lw)

def vline(x, y1, y2, color, lw=1):
    d.line([(x, y1), (x, y2)], fill=color, width=lw)

# ── Gradient fill (vertical) ─────────────────────────────────────────────
def vgradient(x, y, w, h, c1, c2):
    for i in range(h):
        t = i / max(h-1, 1)
        r = int(c1[0] + (c2[0]-c1[0])*t)
        g = int(c1[1] + (c2[1]-c1[1])*t)
        b = int(c1[2] + (c2[2]-c1[2])*t)
        d.line([(x, y+i), (x+w, y+i)], fill=(r,g,b))

def hgradient(x, y, w, h, c1, c2):
    for i in range(w):
        t = i / max(w-1, 1)
        r = int(c1[0] + (c2[0]-c1[0])*t)
        g = int(c1[1] + (c2[1]-c1[1])*t)
        b = int(c1[2] + (c2[2]-c1[2])*t)
        d.line([(x+i, y), (x+i, y+h)], fill=(r,g,b))

# ── Photo simulation (rich gradient + lines mimicking photography) ────────
def photo_block(x, y, w, h, palette, label="", r=0, overlay=True):
    """Simulate a photographic block with rich gradients and structure."""
    c1, c2, c3 = palette
    # Base gradient
    img_block = Image.new("RGB", (w, h), c1)
    db = ImageDraw.Draw(img_block)
    # Multi-stop gradient
    third = h // 3
    for i in range(third):
        t = i / max(third-1,1)
        rc = tuple(int(c1[j] + (c2[j]-c1[j])*t) for j in range(3))
        db.line([(0,i),(w,i)], fill=rc)
    for i in range(third, h):
        t = (i-third) / max(h-third-1,1)
        rc = tuple(int(c2[j] + (c3[j]-c2[j])*t) for j in range(3))
        db.line([(0,i),(w,i)], fill=rc)
    # Add diagonal structure lines (simulate vehicle surfaces)
    for i in range(0, w+h, 120):
        db.line([(i,0),(i-h,h)], fill=tuple(min(255,c+18) for c in c2), width=1)
    # Noise
    px = img_block.load()
    for _ in range(w*h//8):
        nx, ny = random.randint(0,w-1), random.randint(0,h-1)
        v = random.randint(-18, 18)
        p = px[nx,ny]
        px[nx,ny] = tuple(max(0,min(255,p[j]+v)) for j in range(3))
    # Overlay gradient
    if overlay:
        ov = Image.new("RGBA", (w,h), (0,0,0,0))
        dov = ImageDraw.Draw(ov)
        for i in range(h//2):
            a = int(180 * (i/(h//2)))
            dov.line([(0,h-1-i),(w,h-1-i)], fill=(0,0,0,a))
        for i in range(w//3):
            a = int(120 * (i/(w//3)))
            dov.line([(i,0),(i,h)], fill=(0,0,0,a))
        img_block = Image.alpha_composite(img_block.convert("RGBA"), ov).convert("RGB")
    # Paste
    if r:
        mask = Image.new("L", (w,h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0,0,w,h], radius=r, fill=255)
        canvas.paste(img_block, (x,y), mask)
    else:
        canvas.paste(img_block, (x,y))
    # Label
    if label:
        tx(label, x+24, y+h-52, F700_26, GRAY4)

def star(x, y, size=20, color=RED):
    pts = []
    for i in range(10):
        angle = math.pi/2 + i*math.pi/5
        r2 = size if i%2==0 else size*0.45
        pts.append((x+math.cos(angle)*r2, y+math.sin(angle)*r2))
    d.polygon(pts, fill=color)

def stars_row(x, y, n=5, size=18):
    for i in range(n): star(x+i*44, y, size)

def check_icon(x, y, size=20):
    d.line([(x,y+size//2),(x+size//3,y+size),(x+size,y)], fill=RED, width=3)

def red_pill(x, y, text_str, font=F700_18):
    p = 20
    tw_ = tw(text_str, font)
    fill(x, y, tw_+p*2+20, 44, (30, 4, 8), r=22)
    outline_rect(x, y, tw_+p*2+20, 44, (80, 15, 25), r=22, lw=1)
    # dot
    d.ellipse([x+p, y+16, x+p+12, y+28], fill=RED)
    tx(text_str, x+p+20, y+12, font, WHITE)

def label_tag(t, x, y):
    """Small red eyebrow label."""
    fill(x, y, 6, 24, RED)
    tx(t, x+18, y, F700_18, RED)

def btn_draw(label, x, y, w_, primary=True, h_=68, r=6):
    if primary:
        fill(x, y, w_, h_, RED, r)
        # subtle highlight
        fill(x, y, w_, h_//3, (255,255,255,18), r)
        tw_ = tw(label, F700_26)
        tx(label, x+(w_-tw_)//2, y+(h_-30)//2, F700_26, WHITE)
    else:
        fill(x, y, w_, h_, (25,25,25), r)
        outline_rect(x, y, w_, h_, (80,80,80), r, lw=2)
        tw_ = tw(label, F700_26)
        tx(label, x+(w_-tw_)//2, y+(h_-30)//2, F700_26, WHITE)

def section_divider(y):
    d.line([(0,y),(W,y)], fill=(255,255,255,20), width=1)

# ════════════════════════════════════════════════════════════════════════
# START DRAWING
# ════════════════════════════════════════════════════════════════════════

# ── 1. HERO SECTION ──────────────────────────────────────────────────────
HERO_Y = 0
HERO_H = 1400

# Hero photography background
photo_block(0, HERO_Y, W, HERO_H,
    palette=((8,4,2),(28,14,10),(6,2,2)),
    overlay=False)

# Add hero photo-like vehicle silhouette area (right side lit)
hgradient(W//2, HERO_Y, W//2, HERO_H,
    (50, 18, 12), (10, 4, 4))

# Dark overlay (left side readable)
ov = Image.new("RGBA", (W, HERO_H), (0,0,0,0))
dov = ImageDraw.Draw(ov)
for i in range(W):
    t = i/W
    a = int(220 * max(0, 1 - t*1.6))
    dov.line([(i,0),(i,HERO_H)], fill=(0,0,0,a))
# Simpler overlay approach
for i in range(W):
    t = max(0, 1 - (i/W)*1.5)
    a = int(200*t)
    if a > 0:
        d.line([(i,HERO_Y),(i,HERO_Y+HERO_H)], fill=(0,0,0,a) if False else (
            max(0, int(8-8*(1-t))), max(0,int(4-4*(1-t))), max(0,int(2-2*(1-t)))))

# Actually just draw left dark gradient properly
fill(0, HERO_Y, W//2, HERO_H, BLACK)
for i in range(W//2, W):
    t = (i-W//2)/(W//2)
    darkness = int(200*(1-t*0.7))
    d.line([(i,HERO_Y),(i,HERO_Y+HERO_H)], fill=(0,0,0))

# Re-draw the hero photo area on right
photo_block(W//2 - 100, HERO_Y, W//2+100, HERO_H,
    palette=((35,12,8),(18,6,4),(8,2,2)), overlay=False)
# Blend left edge of photo
for i in range(300):
    t = i/300
    a = int(255*(1-t))
    d.line([(W//2-100+i, HERO_Y),(W//2-100+i, HERO_Y+HERO_H)],
           fill=(0,0,0))

# Vehicle shape silhouette (right side)
vx, vy = 1450, HERO_Y+420
# Truck/van body
d.rounded_rectangle([vx, vy+100, vx+900, vy+380], radius=16,
                    fill=(45,15,10), outline=(80,25,15), width=2)
d.rounded_rectangle([vx+30, vy+30, vx+380, vy+120], radius=12,
                    fill=(45,15,10), outline=(70,22,12), width=2)
# Windows
d.rounded_rectangle([vx+50, vy+50, vx+360, vy+110], radius=6,
                    fill=(25,35,45), outline=(40,55,70), width=1)
d.rounded_rectangle([vx+410, vy+120, vx+890, vy+280], radius=4,
                    fill=(20,30,40), outline=(35,50,65), width=1)
# Red stripe
fill(vx, vy+175, 900, 18, RED)
# Wheels
d.ellipse([vx+80, vy+340, vx+210, vy+470], fill=(20,20,20), outline=(50,50,50), width=3)
d.ellipse([vx+120, vy+380, vx+170, vy+430], fill=(40,40,40))
d.ellipse([vx+680, vy+340, vx+810, vy+470], fill=(20,20,20), outline=(50,50,50), width=3)
d.ellipse([vx+720, vy+380, vx+770, vy+430], fill=(40,40,40))
# Glow beneath truck
for r2 in range(6,0,-1):
    d.ellipse([vx+200-r2*30, vy+430, vx+700+r2*30, vy+470+r2*4],
              outline=(227,24,55,12*r2), width=2)

# Grid lines over hero (subtle)
for gx in range(0, W, 80):
    d.line([(gx, HERO_Y),(gx, HERO_Y+HERO_H)], fill=(227,24,55,8))
for gy in range(0, HERO_H, 80):
    d.line([(0, HERO_Y+gy),(W, HERO_Y+gy)], fill=(227,24,55,6))

# Left red accent bar
fill(0, HERO_Y, 6, HERO_H, RED)

# ── Header bar ──
fill(0, 0, W, 88, (0,0,0,0))  # transparent header area
# Logo
tx("PrintLab", 80, 20, F700_36, WHITE)
tx("Wraps ★", 80, 56, F700_30, RED)
# Nav
nav = ["SERVICES","ABOUT","CAREERS","CONTACT","OUR WORK"]
nx_ = 700
for n in nav:
    tx(n, nx_, 35, F700_22, (180,180,180))
    nx_ += tw(n, F700_22) + 64
# Header CTAs
fill(W-520, 20, 200, 52, (25,25,25), r=6)
outline_rect(W-520, 20, 200, 52, (80,80,80), r=6, lw=1)
ctxt_offset = (200 - tw("Call Us", F700_22))//2
tx("Call Us", W-520+ctxt_offset, 34, F700_22, WHITE)
fill(W-300, 20, 220, 52, RED, r=6)
ctxt_offset2 = (220 - tw("Get Estimate", F700_22))//2
tx("Get Estimate", W-300+ctxt_offset2, 34, F700_22, WHITE)

# ── Eyebrow ──
fill(80, 160, 6, 28, RED)
tx("PREMIUM VEHICLE WRAPS & SIGNAGE", 100, 163, F700_18, RED)

# ── Hero Headline ──
ty = 220
tx("MAKE YOUR",   80, ty,     F900_120, WHITE)
tx("BRAND MOVE.", 80, ty+128, F900_120, RED)
# Outline text (draw white border then black fill)
outline_text = "DOMINATE."
for ox in range(-3,4):
    for oy in range(-3,4):
        if ox or oy:
            d.text((80+ox, ty+260+oy), outline_text, font=F900_100, fill=(70,70,70))
d.text((80, ty+260), outline_text, font=F900_100, fill=BLACK)

# ── Subheadline ──
sub_lines = [
    "Industry-leading vehicle wraps, commercial signage,",
    "and building graphics — certified craftsmen who take",
    "pride in every single detail.",
]
sy = ty + 400
for line in sub_lines:
    tx(line, 80, sy, F400_30, (160,160,160))
    sy += 40

# ── CTAs ──
btn_draw("GET PROJECT ESTIMATE", 80, 620, 460, primary=True, h_=76)
btn_draw("CALL US TODAY", 566, 620, 300, primary=False, h_=76)

# ── Trust Pills ──
pills = ["★ 5-Star Rated","✓ Certified Installers","⚡ Fast Turnaround","◆ 3M & Avery Certified"]
px_ = 80
pill_y = 730
for pill in pills:
    pw_ = tw(pill, F700_18) + 48
    fill(px_, pill_y, pw_, 48, (255,255,255,12), r=24)
    outline_rect(px_, pill_y, pw_, 48, (255,255,255,30), r=24, lw=1)
    tx(pill, px_+24, pill_y+14, F700_18, (180,180,180))
    px_ += pw_ + 20

# ── Scroll indicator ──
vline(86, 860, 940, (227,24,55,180), lw=2)
tx("SCROLL", 78, 948, F700_18, (80,80,80))

# ── Hero counters (bottom right) ──
counters = [("2,500+","Projects Done"),("10+","Years Exp."),("98%","Satisfaction")]
cx_ = W - 280
cy_ = HERO_H - 300
for num, lbl in counters:
    tx(num, cx_, cy_, F900_60, WHITE)
    tx(lbl, cx_, cy_+68, F700_22, (80,80,80))
    cy_ += 145

# ── Red brand strip ─────────────────────────────────────────────────────
STRIP_Y = HERO_H
STRIP_H = 80
fill(0, STRIP_Y, W, STRIP_H, RED)
strip_items = ["Commercial Fleet Wraps","Color Change Wraps","Signage & Prints",
               "Building Graphics","Certified Installers","3M Preferred","Avery Dennison",
               "Commercial Fleet Wraps","Color Change Wraps","Signage & Prints"]
sx_ = 60
for item in strip_items:
    tx(item, sx_, STRIP_Y+26, F700_26, WHITE)
    sx_ += tw(item, F700_26) + 20
    tx("★", sx_, STRIP_Y+26, F700_22, (255,255,255,140))
    sx_ += 40

# ── 2. VEHICLE WRAPS FOCUS ────────────────────────────────────────────────
WF_Y = STRIP_Y + STRIP_H
WF_H = 760
fill(0, WF_Y, W, WF_H, DARK2)
section_divider(WF_Y)

PAD = 100
SPLIT = (W-PAD*2)//2

# Left content
label_tag("VEHICLE WRAPS", PAD, WF_Y+70)
tx("TURN EVERY MILE", PAD, WF_Y+115, F900_86, WHITE)
tx("INTO MARKETING.", PAD, WF_Y+210, F900_86, RED)

body = ["From single vehicles to full commercial fleets —",
        "we transform your transportation into powerful",
        "moving billboards that generate thousands of",
        "impressions every single day."]
by_ = WF_Y+330
for line in body:
    tx(line, PAD, by_, F400_26, (150,150,150))
    by_ += 36

# Benefits
benefits = [
    ("★", "70,000+ Daily Impressions", "Most cost-effective advertising per dollar."),
    ("◆", "Paint Protection Included",  "Premium cast vinyl shields factory paint."),
    ("◉", "5–7 Year Lifespan",          "UV-resistant laminate ensures lasting vibrancy."),
]
bfy_ = WF_Y+510
for icon, title, desc in benefits:
    fill(PAD, bfy_, SPLIT-80, 90, (255,255,255,10), r=8)
    outline_rect(PAD, bfy_, SPLIT-80, 90, (255,255,255,18), r=8, lw=1)
    fill(PAD+16, bfy_+16, 52, 52, (227,24,55,30), r=6)
    tx(icon, PAD+24, bfy_+20, F700_26, RED)
    tx(title, PAD+86, bfy_+16, F700_26, WHITE)
    tx(desc,  PAD+86, bfy_+50, F400_22, (130,130,130))
    bfy_ += 104

# Buttons
btn_draw("COMMERCIAL WRAPS", PAD, WF_Y+WF_H-100, 380, primary=True)
btn_draw("ALL SERVICES",    PAD+400, WF_Y+WF_H-100, 260, primary=False)

# Right: Image stack
IMG_X = PAD + SPLIT + 80
IMG_Y = WF_Y + 60
IMG_W = W - IMG_X - PAD
IMG_H = int(IMG_W * 0.75)

# Main image
photo_block(IMG_X, IMG_Y, IMG_W, IMG_H,
    palette=((18,6,4),(45,20,12),(8,3,2)), label="Commercial Fleet Wraps", r=14)

# Accent image (overlapping bottom-right)
ACC_W = int(IMG_W * 0.52)
ACC_H = int(ACC_W * 0.75)
photo_block(IMG_X+IMG_W-ACC_W+24, IMG_Y+IMG_H-ACC_H+24, ACC_W, ACC_H,
    palette=((4,12,24),(10,30,55),(3,8,18)), label="City Fleet", r=12)
outline_rect(IMG_X+IMG_W-ACC_W+24, IMG_Y+IMG_H-ACC_H+24, ACC_W, ACC_H,
             DARK2, r=12, lw=6)

# Stat badge (top-left of image)
fill(IMG_X-30, IMG_Y+40, 200, 110, RED, r=12)
tx("70k+", IMG_X-18, IMG_Y+52, F900_60, WHITE)
tx("DAILY IMPRESSIONS", IMG_X-18, IMG_Y+118, F700_18, (255,255,255,200))

# ── 3. SERVICES GRID ────────────────────────────────────────────────────
SVC_Y = WF_Y + WF_H
SVC_H = 680
fill(0, SVC_Y, W, SVC_H, BLACK)
section_divider(SVC_Y)

fill(0, SVC_Y, W, SVC_H, BLACK)
# Radial glow at bottom
for r_ in range(12, 0, -1):
    d.ellipse([W//2-r_*120, SVC_Y+SVC_H-r_*80,
               W//2+r_*120, SVC_Y+SVC_H+r_*20],
              fill=tuple(int(c*r_/12) for c in (8,1,3)))

ctxt("WHAT WE DO", SVC_Y+60, F700_22, RED)
ctxt("FULL-SERVICE VISUAL BRANDING", SVC_Y+100, F900_72, WHITE)

services = [
    ("Commercial\nVehicle Wraps", "Fleet branding for vans,\ntrucks, trailers & more."),
    ("Vehicle\nWraps",            "Personal cars, trucks,\nSUVs & specialty vehicles."),
    ("Signage\n& Prints",         "Banners, window graphics,\nlarge-format printing."),
    ("Buildings\n& Facilities",   "Wall murals, architectural\nwraps & wayfinding."),
    ("Other\nOfferings",          "Boats, trailers, golf carts\n& specialty projects."),
]
n_svc = len(services)
card_w = (W - PAD*2 - (n_svc-1)) // n_svc
svc_card_y = SVC_Y + 210
svc_h = SVC_H - 280
scx = PAD
for i, (title, desc) in enumerate(services):
    # Card
    fill(scx, svc_card_y, card_w, svc_h, DARK2)
    outline_rect(scx, svc_card_y, card_w, svc_h, (50,50,50), lw=1)
    # Red bottom bar
    fill(scx, svc_card_y+svc_h-4, card_w, 4, RED)
    # Icon
    icon_x = scx + 36
    icon_y = svc_card_y + 40
    fill(icon_x, icon_y, 72, 72, (227,24,55,25), r=10)
    outline_rect(icon_x, icon_y, 72, 72, (227,24,55,60), r=10, lw=1)
    star(icon_x+36, icon_y+36, 16, RED)
    # Title
    ty_ = svc_card_y + 140
    for line in title.split("\n"):
        tx(line, scx+36, ty_, F700_36, WHITE)
        ty_ += 44
    # Desc
    ty_ += 8
    for line in desc.split("\n"):
        tx(line, scx+36, ty_, F400_22, (120,120,120))
        ty_ += 30
    # Arrow
    tx("Learn More →", scx+36, svc_card_y+svc_h-56, F700_22, RED)
    scx += card_w + 1

# ── 4. STATS / WHY US ───────────────────────────────────────────────────
STAT_Y = SVC_Y + SVC_H
STAT_H = 740
fill(0, STAT_Y, W, STAT_H, DARK2)
section_divider(STAT_Y)

# Glow left
for r_ in range(10,0,-1):
    d.ellipse([-r_*80, STAT_Y+STAT_H//2-r_*60,
               r_*80,  STAT_Y+STAT_H//2+r_*60],
              fill=tuple(int(c*r_/10) for c in (8,1,2)))

# Left: label + heading + stats grid
label_tag("WHY CHOOSE US", PAD, STAT_Y+60)
tx("THE PRINT LAB", PAD, STAT_Y+106, F900_86, WHITE)
tx("DIFFERENCE.", PAD, STAT_Y+200, F900_86, RED)

sg_y = STAT_Y + 340
sg_w = SPLIT - 60
sg_h = STAT_H - 400
cell_w = sg_w//2
cell_h = sg_h//2

stat_data = [("10+","Years in Business"),("2,500+","Projects Completed"),
             ("98%","Satisfaction",""),("15+","Certified Installers")]
for i, item in enumerate(stat_data):
    cx_ = PAD + (i%2)*cell_w
    cy_ = sg_y + (i//2)*cell_h
    fill(cx_, cy_, cell_w-2, cell_h-2, DARK3)
    outline_rect(cx_, cy_, cell_w-2, cell_h-2, (50,50,50), lw=1)
    # Ghost number
    ghost = item[0]
    tx(ghost, cx_+cell_w-tw(ghost, F900_100)-16, cy_+cell_h-90, F900_100, (255,255,255,8))
    tx(item[0], cx_+36, cy_+40, F900_72, WHITE)
    tx(item[1], cx_+36, cy_+cell_h-60, F700_22, (100,100,100))

# Right: trust points
tp_x = PAD + SPLIT + 80
tp_y = STAT_Y + 60
tp_w = W - tp_x - PAD
trust_pts = [
    ("✓", "3M & Avery Certified",
     "We use only manufacturer-certified cast films backed by\nmulti-year warranties on every project."),
    ("✎", "In-House Design Team",
     "Our designers create graphics that stop traffic and\ndrive measurable results for your brand."),
    ("◉", "On-Time, Every Time",
     "Fleet downtime is minimized with our streamlined\nworkflow and climate-controlled facility."),
]
for icon, title, desc in trust_pts:
    fill(tp_x, tp_y, tp_w, 170, (255,255,255,12), r=10)
    outline_rect(tp_x, tp_y, tp_w, 170, (255,255,255,20), r=10, lw=1)
    fill(tp_x+24, tp_y+24, 64, 64, (227,24,55,25), r=8)
    tx(icon, tp_x+36, tp_y+30, F700_36, RED)
    tx(title, tp_x+110, tp_y+28, F700_30, WHITE)
    dy_ = tp_y+70
    for line in desc.split("\n"):
        tx(line, tp_x+110, dy_, F400_22, (110,110,110))
        dy_ += 32
    tp_y += 190

# ── 5. PORTFOLIO PREVIEW ─────────────────────────────────────────────────
PORT_Y = STAT_Y + STAT_H
PORT_H = 900
fill(0, PORT_Y, W, PORT_H, BLACK)
section_divider(PORT_Y)

label_tag("PORTFOLIO", PAD, PORT_Y+60)
tx("OUR WORK SPEAKS.", PAD, PORT_Y+105, F900_86, WHITE)
btn_draw("VIEW FULL PORTFOLIO →", W-560, PORT_Y+118, 420, primary=False, h_=60)

# Portfolio grid: large left + 4 right
GRID_Y = PORT_Y+230
GRID_H = PORT_H - 290
LARGE_W = int((W - PAD*2)*0.45)
SMALL_W = (W - PAD*2 - LARGE_W - 12)//2
SMALL_H = (GRID_H - 8) // 2

palettes = [
    ((40,10,6),(20,5,3),(8,2,2)),   # large
    ((6,8,40),(4,5,24),(2,2,12)),   # top-mid
    ((6,30,12),(3,18,6),(2,8,3)),   # top-right
    ((30,20,4),(18,12,2),(8,5,2)),  # bot-mid
    ((20,4,30),(12,2,18),(6,2,8)),  # bot-right
]
labels = ["Commercial Fleet","Color Change","Retail Signage","Building Wrap","Specialty Wrap"]
cats   = ["COMMERCIAL WRAPS","VEHICLE WRAPS","SIGNAGE","BUILDINGS","OTHER"]

photo_block(PAD, GRID_Y, LARGE_W, GRID_H, palettes[0], r=10, overlay=True)
tx(cats[0],   PAD+24, GRID_Y+GRID_H-80, F700_18, RED)
tx(labels[0], PAD+24, GRID_Y+GRID_H-52, F700_30, WHITE)

gx2 = PAD + LARGE_W + 12
photo_block(gx2,              GRID_Y,            SMALL_W, SMALL_H, palettes[1], r=10)
photo_block(gx2+SMALL_W+8,   GRID_Y,            SMALL_W, SMALL_H, palettes[2], r=10)
photo_block(gx2,              GRID_Y+SMALL_H+8, SMALL_W, SMALL_H, palettes[3], r=10)
photo_block(gx2+SMALL_W+8,   GRID_Y+SMALL_H+8, SMALL_W, SMALL_H, palettes[4], r=10)

for i in range(4):
    gx3 = gx2 + (i%2)*(SMALL_W+8)
    gy3 = GRID_Y + (i//2)*(SMALL_H+8)
    tx(cats[i+1],   gx3+20, gy3+SMALL_H-68, F700_18, RED)
    tx(labels[i+1], gx3+20, gy3+SMALL_H-42, F700_26, WHITE)

# ── 6. PROCESS ──────────────────────────────────────────────────────────
PROC_Y = PORT_Y + PORT_H
PROC_H = 660
fill(0, PROC_Y, W, PROC_H, DARK2)
section_divider(PROC_Y)

# Glow right
for r_ in range(10,0,-1):
    d.ellipse([W-r_*80, PROC_Y+PROC_H//2-r_*60,
               W+r_*80, PROC_Y+PROC_H//2+r_*60],
              fill=tuple(int(c*r_/10) for c in (8,1,2)))

ctxt("HOW IT WORKS", PROC_Y+55, F700_22, RED)
ctxt("WE MAKE THIS EASY.", PROC_Y+96, F900_86, WHITE)

steps = [("01","Discovery","Consult on brand goals,\nvehicle types, fleet size\nand project timeline."),
         ("02","Design",   "Designers create scaled\nvehicle mockups for\nreview and approval."),
         ("03","Production","Printed on premium\ncast vinyl with\nUV-resistant laminate."),
         ("04","Installation","Certified installers apply\nwraps in our climate-\ncontrolled facility.")]
step_w = (W - PAD*2)//4
proc_y = PROC_Y + 240
cx_ = PAD

# Connector line
connector_y = proc_y + 44
d.line([(PAD+80, connector_y),(W-PAD-80, connector_y)], fill=RED, width=2)

for i, (num, title, desc) in enumerate(steps):
    # Circle
    fill(cx_ + step_w//2 - 52, proc_y, 104, 104, DARK2)
    d.ellipse([cx_+step_w//2-52, proc_y, cx_+step_w//2+52, proc_y+104],
              fill=RED, outline=RED, width=0)
    d.ellipse([cx_+step_w//2-58, proc_y-6, cx_+step_w//2+58, proc_y+110],
              outline=(227,24,55,60), width=0)
    tw_num = tw(num, F700_36)
    tx(num, cx_+step_w//2-tw_num//2, proc_y+32, F700_36, WHITE)
    # Ghost number
    tx(num, cx_+12, proc_y-20, F900_100, (227,24,55,18))
    # Title
    tw_t = tw(title, F700_36)
    tx(title, cx_+step_w//2-tw_t//2, proc_y+130, F700_36, WHITE)
    # Desc
    dy_ = proc_y+182
    for line in desc.split("\n"):
        tw_d = tw(line, F400_22)
        tx(line, cx_+step_w//2-tw_d//2, dy_, F400_22, (110,110,110))
        dy_ += 30
    cx_ += step_w

# ── 7. FAQ PREVIEW ──────────────────────────────────────────────────────
FAQ_Y = PROC_Y + PROC_H
FAQ_H = 560
fill(0, FAQ_Y, W, FAQ_H, BLACK)
section_divider(FAQ_Y)

# Two-column layout
fc_w = (W - PAD*2 - 120) // 3

label_tag("FAQ", PAD, FAQ_Y+60)
tx("COMMON", PAD, FAQ_Y+105, F900_86, WHITE)
tx("QUESTIONS.", PAD, FAQ_Y+200, F900_86, RED)
btn_draw("VIEW ALL FAQs", PAD, FAQ_Y+FAQ_H-110, 340, primary=True)

faqs = [
    ("How long does a vehicle wrap last?",
     "Professionally installed wraps using premium cast vinyl last 5–7 years."),
    ("Will a wrap damage my vehicle's paint?",
     "No — wraps actually protect factory paint. Removable without damage."),
    ("How long does installation take?",
     "Full wraps: 1–3 days. Partial wraps & spot graphics: often same-day."),
    ("Do you offer design services?",
     "Yes — our in-house design team creates custom graphics from scratch."),
]
faq_x = PAD + fc_w + 120
fq_y = FAQ_Y + 60
for q, a in faqs:
    fill(faq_x, fq_y, W-faq_x-PAD, 2, (255,255,255,20))
    fq_y += 18
    tx(q, faq_x, fq_y, F700_26, WHITE)
    tx(a, faq_x, fq_y+36, F400_22, (100,100,100))
    # Plus icon
    tx("+", W-PAD-40, fq_y, F700_36, RED)
    fq_y += 110

fill(faq_x, fq_y, W-faq_x-PAD, 2, (255,255,255,20))

# ── 8. FINAL CTA ────────────────────────────────────────────────────────
CTA_Y = FAQ_Y + FAQ_H
CTA_H = 560
fill(0, CTA_Y, W, CTA_H, BLACK)
section_divider(CTA_Y)

# Animated mesh glow
for r_ in range(16,0,-1):
    cx_g = W//2
    cy_g = CTA_Y + CTA_H//2
    d.ellipse([cx_g-r_*100, cy_g-r_*60, cx_g+r_*100, cy_g+r_*60],
              fill=tuple(int(c*r_/16) for c in (12,1,4)))

# Diagonal lines
for i in range(0, W+CTA_H, 90):
    d.line([(i, CTA_Y),(i-CTA_H, CTA_Y+CTA_H)], fill=(227,24,55,16), width=1)

label_tag_cta_w = tw("READY TO START?", F700_22)
fill(W//2-label_tag_cta_w//2-18, CTA_Y+50, label_tag_cta_w+36, 4, RED)
ctxt("READY TO START?", CTA_Y+52, F700_22, RED)
ctxt("LET'S BUILD SOMETHING", CTA_Y+100, F900_100, WHITE)
ctxt("BOLD.", CTA_Y+206, F900_100, RED)

sub_cta = "Get your free project estimate today. Our team is ready to bring"
sub_cta2 = "your brand to life — on every road, every day."
ctxt(sub_cta,  CTA_Y+330, F400_30, (130,130,130))
ctxt(sub_cta2, CTA_Y+368, F400_30, (130,130,130))

btn_draw("GET FREE ESTIMATE",    W//2-420, CTA_Y+430, 400, primary=True,  h_=76)
btn_draw("CALL (555) PLW-WRAP",  W//2+20,  CTA_Y+430, 400, primary=False, h_=76)

# Social proof row
proof_items = [("5.0","Google Rating"),("200+","5-Star Reviews"),("10+","Years in Business"),("2,500+","Projects Done")]
pr_total = len(proof_items)*220 + (len(proof_items)-1)*60
pr_x = (W-pr_total)//2
pr_y = CTA_Y+530
fill(0, pr_y-20, W, 2, (255,255,255,15))
stars_row(pr_x, pr_y+10)
for i, (num, lbl) in enumerate(proof_items):
    if i > 0:
        vline(pr_x+i*280+120, pr_y, pr_y+70, (80,80,80), lw=1)
    tw_n = tw(num, F900_60)
    tx(num, pr_x+i*280+(180-tw_n)//2, pr_y+10, F900_60, RED if i==0 else WHITE)
    tw_l = tw(lbl, F700_18)
    tx(lbl, pr_x+i*280+(180-tw_l)//2, pr_y+78, F700_18, (80,80,80))

# ── FOOTER ──────────────────────────────────────────────────────────────
FOOT_Y = CTA_Y + CTA_H
FOOT_H = 220
fill(0, FOOT_Y, W, FOOT_H, DARK2)
fill(0, FOOT_Y, W, 2, (255,255,255,15))
fill(0, FOOT_Y, 5, FOOT_H, RED)

tx("PrintLab", PAD, FOOT_Y+32, F700_36, WHITE)
tx("Wraps ★",  PAD, FOOT_Y+76, F700_30, RED)

cols = [
    ("Browse",["Home","About","Contact","Our Work"]),
    ("Services",["Commercial Wraps","Vehicle Wraps","Signage & Prints","Buildings & Facilities"]),
    ("Resources",["FAQs","Careers","Reviews"]),
    ("Contact",["(555) PLW-WRAP","info@printlabwraps.com","123 Wrap Drive","Mon–Fri 8am–5pm"]),
]
fx_ = 500
for col_title, col_items in cols:
    tx(col_title.upper(), fx_, FOOT_Y+30, F700_22, WHITE)
    fy_ = FOOT_Y+64
    for item in col_items:
        tx(item, fx_, fy_, F400_22, (90,90,90))
        fy_ += 32
    fx_ += (W-500-PAD)//4

fill(0, FOOT_Y+FOOT_H-40, W, 1, (255,255,255,10))
tx("© 2025 Print Lab Wraps. All rights reserved.", PAD, FOOT_Y+FOOT_H-30, F400_18, (60,60,60))
tx("Disclaimer  •  Terms of Use  •  Privacy Policy", W-PAD, FOOT_Y+FOOT_H-30, F400_18, (60,60,60), anchor="rt")

# ── GRAIN OVERLAY ────────────────────────────────────────────────────────
print("Adding grain overlay...")
grain = Image.new("L", (W, FOOT_Y+FOOT_H), 128)
gp = grain.load()
for gy_ in range(FOOT_Y+FOOT_H):
    for gx_ in range(0, W, 4):
        v = random.randint(110,146)
        gp[gx_,gy_] = v
        if gx_+1 < W: gp[gx_+1,gy_] = v
        if gx_+2 < W: gp[gx_+2,gy_] = v
        if gx_+3 < W: gp[gx_+3,gy_] = v

# Blend grain at low opacity
grain_rgb = Image.merge("RGB", [grain,grain,grain])
canvas_final = Image.blend(canvas.crop([0,0,W,FOOT_Y+FOOT_H]), grain_rgb, 0.022)
canvas.paste(canvas_final, (0,0))

# ── FINAL CANVAS SIZE ────────────────────────────────────────────────────
final_h = FOOT_Y + FOOT_H
canvas_crop = canvas.crop([0, 0, W, final_h])

# ── SAVE ─────────────────────────────────────────────────────────────────
out = "/home/user/https-github.com-nextlevelbuilder-ui-ux-pro-max-skill/printlabwraps/PrintLabWraps_Homepage_Mockup_v2.png"
canvas_crop.save(out, "PNG", optimize=True)
print(f"Saved: {out}  ({W}×{final_h}px)")
