#!/usr/bin/env python3
"""Draw the front page of 22 November 2026 as a single 1024x1024 image.

Every headline below was checked against news reported on Sunday
22 November 2026 (AP, AFP, BBC and others). The script draws a
newspaper front page with Pillow and writes entry.png beside itself.
Run: python3 render_image.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (178, 34, 34)
NAVY = (31, 56, 100)
SLATE = (90, 100, 116)
LIGHT = (233, 227, 213)
BODY = (60, 60, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_icon(draw, kind, box, fg, bg):
    """Draw a small flat pictogram inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=bg)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    s = min(x1 - x0, y1 - y0)
    u = max(2, s // 16)
    if kind == "globe":
        draw.ellipse([cx - 4 * u, cy - 4 * u, cx + 4 * u, cy + 4 * u],
                     outline=fg, width=2 * u)
        draw.ellipse([cx - 2 * u, cy - 4 * u, cx + 2 * u, cy + 4 * u],
                     outline=fg, width=u)
        draw.line([cx - 4 * u, cy, cx + 4 * u, cy], fill=fg, width=u)
    elif kind == "shield":
        draw.polygon([(cx, cy - 4 * u), (cx + 3 * u, cy - 3 * u),
                      (cx + 3 * u, cy), (cx, cy + 4 * u), (cx - 3 * u, cy),
                      (cx - 3 * u, cy - 3 * u)], outline=fg, width=2 * u)
        draw.line([cx - u, cy, cx, cy + u], fill=fg, width=u)
        draw.line([cx, cy + u, cx + 2 * u, cy - 2 * u], fill=fg, width=u)
    elif kind == "factory":
        draw.rectangle([cx - 4 * u, cy, cx + 4 * u, cy + 4 * u], fill=fg)
        draw.rectangle([cx - 4 * u, cy - 3 * u, cx - 2 * u, cy], fill=fg)
        draw.rectangle([cx - u, cy - 4 * u, cx + u, cy], fill=fg)
        for wx in (-2, 0, 2):
            draw.rectangle([cx + wx * u - u // 2, cy + u,
                            cx + wx * u + u // 2, cy + 2 * u], fill=PAPER)
    elif kind == "phone":
        draw.rounded_rectangle([cx - 2 * u, cy - 4 * u, cx + 2 * u, cy + 4 * u],
                               radius=u, outline=fg, width=2 * u)
        draw.line([cx - u, cy - 3 * u, cx + u, cy - 3 * u], fill=fg, width=u)
        draw.ellipse([cx - u // 2, cy + 3 * u - u // 2,
                      cx + u // 2, cy + 3 * u + u // 2], fill=fg)


def draw_card(draw, x, y, w, h, kicker, headline, deck, icon=None,
              head_max=30, deck_max=19, max_head_lines=2, max_deck_lines=2):
    """Draw one story card, shrinking type until it fits inside."""
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    pad = 14
    icon_w = 72 if icon else 0
    tw = w - 2 * pad - icon_w
    kick_size = 16 if w > 400 else 14
    f_kick = font(SANS_B, kick_size)
    draw.text((x + pad, y + pad), kicker, font=f_kick, fill=RED)
    ty = y + pad + kick_size + 9
    hs = head_max
    while hs > 16:
        lines = wrap(draw, headline, font(SERIF, hs), tw)
        if len(lines) <= max_head_lines:
            break
        hs -= 1
    f_head = font(SERIF, hs)
    lines = wrap(draw, headline, f_head, tw)
    for ln in lines:
        draw.text((x + pad, ty), ln, font=f_head, fill=INK)
        ty += hs + 6
    ty += 3
    ds = deck_max
    while ds > 12:
        dlines = wrap(draw, deck, font(SERIF_REG, ds), tw)
        if len(dlines) <= max_deck_lines:
            break
        ds -= 1
    f_deck = font(SERIF_REG, ds)
    dlines = wrap(draw, deck, f_deck, tw)
    # drop deck lines until the block fits the card
    while dlines and ty + len(dlines) * (ds + 6) > y + h - pad:
        dlines = dlines[:-1]
    for ln in dlines:
        draw.text((x + pad, ty), ln, font=f_deck, fill=BODY)
        ty += ds + 6
    if icon:
        draw_icon(draw, icon, (x + w - 66, y + 12, x + w - 12, y + 66),
                  NAVY, LIGHT)


def draw_lead(draw, x, y, w, h):
    """The big lead story: Gulf escalation, with a radar illustration."""
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    pad = 20
    ill_w = 240
    tx, ty = x + pad, y + pad
    tw = w - 2 * pad - ill_w
    f_kick = font(SANS_B, 20)
    draw.text((tx, ty), "THE GULF  \u2022  MIDDLE EAST", font=f_kick, fill=RED)
    ty += 32
    hs = 44
    while hs > 30:
        lines = wrap(draw, "IRAN CLAIMS NEW STRIKES ON U.S. RADARS IN BAHRAIN",
                     font(SERIF, hs), tw)
        if len(lines) <= 2:
            break
        hs -= 1
    f_head = font(SERIF, hs)
    lines = wrap(draw, "IRAN CLAIMS NEW STRIKES ON U.S. RADARS IN BAHRAIN",
                 f_head, tw)
    for ln in lines:
        draw.text((tx, ty), ln, font=f_head, fill=INK)
        ty += hs + 7
    ty += 5
    deck = ("Tehran says its missiles and drones hit two Patriot "
            "air-defence radars at American bases, and shows footage "
            "it says is two downed U.S. drones over the Gulf.")
    ds = 22
    while ds > 16:
        dlines = wrap(draw, deck, font(SERIF_REG, ds), tw)
        if len(dlines) <= 3:
            break
        ds -= 1
    f_deck = font(SERIF_REG, ds)
    dlines = wrap(draw, deck, f_deck, tw)
    while dlines and ty + len(dlines) * (ds + 7) > y + h - pad:
        dlines = dlines[:-1]
    for ln in dlines:
        draw.text((tx, ty), ln, font=f_deck, fill=BODY)
        ty += ds + 7
    # illustration panel
    ix0, iy0 = x + w - ill_w + 12, y + 12
    ix1, iy1 = x + w - 12, y + h - 12
    draw.rectangle([ix0, iy0, ix1, iy1], fill=NAVY)
    cx = (ix0 + ix1) // 2
    cy = (iy0 + iy1) // 2 + 28
    gold = (232, 184, 90)
    for r, wd in ((88, 7), (60, 5), (34, 4)):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=195, end=345,
                 fill=gold, width=wd)
    draw.line([cx, cy, cx + 62, cy - 62], fill=gold, width=5)
    draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=gold)
    draw.text((ix0 + 14, iy1 - 58), "AL-RIFFA  \u2022  AWALI",
              font=font(SANS_B, 17), fill=(255, 255, 255))
    draw.text((ix0 + 14, iy1 - 34), "IRGC claim, 22 Nov",
              font=font(SANS, 16), fill=(200, 210, 225))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # margin
    # --- masthead ---
    d.rectangle([m, 18, W - m, 22], fill=RED)
    f_title = font(SERIF, 58)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 26), title, font=f_title, fill=INK)
    f_date = font(SANS_B, 28)
    date = "SUNDAY, 22 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 98), date, font=f_date, fill=RED)
    f_sub = font(SERIF_REG, 18)
    sub = "The day's world news, in one picture"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 130), sub, font=f_sub, fill=SLATE)
    d.rectangle([m, 162, W - m, 166], fill=INK)

    # --- lead story ---
    draw_lead(d, m, 174, W - 2 * m, 258)

    # --- second row: two cards ---
    y2, h2 = 446, 184
    cw2 = (W - 2 * m - 16) // 2
    draw_card(d, m, y2, cw2, h2,
              "CLIMATE  \u2022  ANTALYA",
              "COP31 IN OVERTIME OVER FOSSIL FUELS",
              "Nearly 200 nations still deadlocked over a final pact "
              "in Antalya.",
              head_max=30, deck_max=18)
    draw_card(d, m + cw2 + 16, y2, cw2, h2,
              "WASHINGTON",
              "TRUMP VOWS 10% CAP ON CREDIT-CARD RATES",
              "The president says he will work with Democrats to "
              "limit card interest.",
              head_max=30, deck_max=18)

    # --- third row: three cards ---
    y3, h3 = 644, 156
    cw3 = (W - 2 * m - 32) // 3
    draw_card(d, m, y3, cw3, h3,
              "DEFENCE  \u2022  N. AMERICA",
              "PENTAGON TO CURB U.S.\u2013CANADA TIES",
              "New limits on military cooperation with Ottawa.",
              head_max=22, deck_max=15)
    draw_card(d, m + cw3 + 16, y3, cw3, h3,
              "PYONGYANG",
              "KIM\u2019S FACTORY TOUR AFTER \u2018TRUMP SNUB\u2019",
              "North Korea's leader visits industrial sites.",
              head_max=22, deck_max=15)
    draw_card(d, m + 2 * (cw3 + 16), y3, cw3, h3,
              "INDIA  \u2022  TECHNOLOGY",
              "PROTESTS HIT META OFFICES IN INDIA",
              "Opposition demonstrators rally at its offices.",
              head_max=22, deck_max=15)

    # --- fourth row: three small headline-only cards ---
    y4, h4 = 816, 104
    draw_card(d, m, y4, cw3, h4,
              "ARMS",
              "TALKS OPEN PATH TO \u2018KILLER ROBOT\u2019 PACT",
              "",
              head_max=22, deck_max=14, max_deck_lines=0)
    draw_card(d, m + cw3 + 16, y4, cw3, h4,
              "HUNGER",
              "WFP TO AID 91 MILLION IN 2027",
              "",
              head_max=22, deck_max=14, max_deck_lines=0)
    draw_card(d, m + 2 * (cw3 + 16), y4, cw3, h4,
              "EUROPE",
              "YOUTH TAKE TO THE STREETS",
              "",
              head_max=22, deck_max=14, max_deck_lines=0)

    # --- also-today strip ---
    y5 = 930
    d.rectangle([m, y5, W - m, y5 + 2], fill=INK)
    f_t = font(SERIF_REG, 15)
    strips = [
        "ALSO TODAY \u2014 Riyadh: Houthi missiles fired at the Saudi "
        "capital; all three intercepted, the coalition says",
        "Florida begins clean-up after historic floods \u2022 11 die in "
        "tainted liquor in Manipur \u2022 \u2018El Chapo Isidro\u2019 "
        "arrested in Mexico",
        "Estonia to shut its border with Russia \u2022 Rohingya hail the "
        "world court\u2019s genocide verdict \u2022 Cummins keeps the "
        "Test captaincy",
        "Modi opens the Nitish Setu bridge in Bihar \u2022 Seoul: speed "
        "is decisive in the AI race, says Lee",
    ]
    ty = y5 + 10
    for ln in strips:
        d.text((m, ty), ln, font=f_t, fill=INK)
        ty += 19

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
