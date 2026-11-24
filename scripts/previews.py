#!/usr/bin/env python3
"""Draw a mock T3 Code window for every theme in themes/, in light and dark mode.

Writes previews/<theme>-light.svg and previews/<theme>-dark.svg. These are
illustrations built from each theme's color roles and T3 Code's own layout
(256px sidebar, 52px chat header, 36px thread rows, centered chat column),
not real screenshots.

Run from the repo root: python3 scripts/previews.py
"""
import json
import pathlib
import re
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1100, 640
SIDEBAR_W = 256
HEADER_H = 52
COL_W = 680
T3_FONT = "-apple-system,BlinkMacSystemFont,'Inter Variable','Segoe UI',system-ui,sans-serif"
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace"

# Shape details each theme's CSS sets, which color roles can't express.
# T3 Code's defaults: 8px rows and controls, 16px bubbles and message box.
DEFAULT_SHAPE = {"row": 8, "bubble": 16, "composer": 16, "button": 8, "code": 8}
SHAPE = {
    "cursor": {"row": 6, "bubble": 8, "composer": 10, "button": 6, "code": 6,
               "switch": {"light": "#F54E00", "dark": "#F54E00"}, "knob": "#FFFFFF"},
    "teams": {"row": 4, "bubble": 6, "composer": 4, "button": 4, "code": 4, "underline": True,
              "shadow": True},
    "slack": {"row": 6, "bubble": 8, "composer": 8, "button": 6, "code": 4,
              "switch": {"light": "#007A5A", "dark": "#007A5A"}, "knob": "#FFFFFF",
              "composer_border": 0.3},
    "discord": {"row": 4, "bubble": 8, "composer": 8, "button": 4, "code": 4, "borderless": True,
                "switch": {"light": "#23A55A", "dark": "#23A55A"}, "knob": "#FFFFFF"},
    "notion": {"row": 6, "bubble": 10, "composer": 12, "button": 6, "code": 4, "shadow": True,
               "inline_code": {"light": "#EB5757", "dark": "#FF7369"}},
    "github": {"row": 6, "bubble": 6, "composer": 12, "button": 6, "code": 6, "bubble_border": True},
    "spotify": {"row": 6, "bubble": 8, "composer": 24, "button": 999, "code": 8, "borderless": True,
                "bold_buttons": True},
}

# Lucide icon paths (ISC license), drawn on a 24px grid.
ICON = {
    "pen": '<path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.4 2.6a2.1 2.1 0 1 1 3 3L12 15l-4 1 1-4Z"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "chevron_r": '<path d="m9 18 6-6-6-6"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M2 12h3M19 12h3M4.9 19.1 7 17M17 7l2.1-2.1"/>',
    "diff": '<path d="M12 3v14M5 10h14M5 21h14"/>',
    "terminal": '<path d="m4 17 6-6-6-6"/><path d="M12 19h8"/>',
    "panel": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M15 3v18"/>',
    "up": '<path d="m5 12 7-7 7 7"/><path d="M12 19V5"/>',
    "paperclip": '<path d="m21.4 11-8.6 8.6a5.7 5.7 0 0 1-8-8l8.6-8.6a3.8 3.8 0 0 1 5.3 5.3l-8.6 8.6a1.9 1.9 0 0 1-2.7-2.7l8-8"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
}


def font_of(css):
    m = re.search(r"body\{font-family:([^;}]+)", css or "")
    return m.group(1).replace('"', "'") if m else T3_FONT


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    """color-mix(in srgb, a t, b)."""
    if a == "transparent":
        return b
    return "#" + "".join(f"{round(x * t + y * (1 - t)):02X}" for x, y in zip(hexrgb(a), hexrgb(b)))


class Svg:
    def __init__(self):
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill, r=0, stroke=None, extra=""):
        if fill == "transparent" and not stroke:
            return
        s = f' stroke="{stroke}" stroke-width="1"' if stroke else ""
        f = "none" if fill == "transparent" else fill
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(r, h / 2, w / 2)}" fill="{f}"{s}{extra}/>')

    def line(self, x1, y1, x2, y2, stroke):
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="1"/>')

    def text(self, x, y, s, fill, size=13, weight=400, anchor="start", mono=False):
        fam = f' font-family="{MONO}"' if mono else ""
        self.add(
            f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}"'
            f' text-anchor="{anchor}"{fam} xml:space="preserve">{escape(s)}</text>'
        )

    def icon(self, x, y, name, stroke, size=16):
        self.add(
            f'<g transform="translate({x} {y}) scale({size / 24})" fill="none" stroke="{stroke}" stroke-width="2"'
            f' stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</g>'
        )


def render(slug, theme, mode):
    c = theme["colors"] if theme["appearance"] == mode else {**theme["colors"], **theme["variants"][mode]}
    sh = {**DEFAULT_SHAPE, **SHAPE.get(slug, {})}
    dark = mode == "dark"
    svg = Svg()
    svg.add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"'
        f' font-family="{font_of(theme.get("css"))}">'
    )
    svg.add(f'<title>{escape(theme["name"])} theme, {mode} mode (mock)</title>')
    svg.add(
        '<defs><clipPath id="win"><rect width="100%" height="100%" rx="12"/></clipPath>'
        '<filter id="sh" x="-10%" y="-20%" width="120%" height="160%">'
        f'<feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000" flood-opacity="{0.35 if dark else 0.08}"/>'
        '</filter></defs>'
    )
    svg.add('<g clip-path="url(#win)">')
    svg.rect(0, 0, W, H, c["canvas"])

    # ---------- Sidebar ----------
    sb_fg, sb_mu = c["sidebarForeground"], c["sidebarMutedForeground"]
    svg.rect(0, 0, SIDEBAR_W, H, c["sidebar"])
    svg.line(SIDEBAR_W - 0.5, 0, SIDEBAR_W - 0.5, H, c["sidebarBorder"])
    for i, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        svg.add(f'<circle cx="{20 + i * 20}" cy="26" r="6" fill="{col}"/>')

    def row(y, label, icon=None, state=None, meta=None, indent=0):
        if state == "selected":
            svg.rect(8, y, SIDEBAR_W - 16, 36, c["sidebarRowSelected"], sh["row"])
        elif state == "hover":
            svg.rect(8, y, SIDEBAR_W - 16, 36, c["sidebarRowHover"], sh["row"])
        tx = 18 + indent
        if icon:
            svg.icon(tx, y + 10, icon, sb_fg if state else sb_mu, 16)
            tx += 26
        svg.text(tx, y + 23, label, sb_fg if state else sb_mu, 13, 600 if state == "selected" else 400)
        if meta:
            svg.text(SIDEBAR_W - 20, y + 23, meta, sb_mu, 11.5, 400, "end")

    def project(y, name, letters, open_):
        svg.icon(18, y + 11, "chevron" if open_ else "chevron_r", sb_mu, 14)
        tile, tile_fg = (c["accent"], c["accentForeground"]) if open_ else (c["sidebarControlSurface"], sb_fg)
        svg.rect(38, y + 8, 20, 20, tile, 5)
        svg.text(48, y + 22, letters, tile_fg, 9, 700, "middle")
        svg.text(66, y + 23, name, sb_fg, 13, 600)

    row(56, "New thread", "pen")
    row(92, "Search", "search")
    y = 144
    project(y, "t3-cosplay", "T3", True)
    y += 38
    for label, state, meta in [
        ("Add everyday themes", "selected", "now"),
        ("Fix contrast in light mode", "hover", "12m"),
        ("Rename theme files", None, "1h"),
        ("Merge README sections", None, "3h"),
        ("Draw theme previews", None, "1d"),
    ]:
        row(y, label, state=state, meta=meta, indent=18)
        y += 38
    project(y + 8, "dotfiles", "DF", False)
    row(H - 52, "Settings", "settings")

    # ---------- Chat header ----------
    mx, mw = SIDEBAR_W, W - SIDEBAR_W
    svg.rect(mx, 0, mw, HEADER_H, c["toolbar"])
    svg.line(mx, HEADER_H - 0.5, W, HEADER_H - 0.5, c["toolbarBorder"])
    svg.text(mx + 20, 31, "Add everyday themes", c["toolbarForeground"], 14, 600)
    bx = mx + 172
    svg.rect(bx, 17, 78, 20, mix(c["toolbarForeground"], c["toolbar"], 0.12), 999)
    svg.text(bx + 39, 31, "t3-cosplay", c["toolbarForeground"], 11, 500, "middle")
    bx = W - 16
    for ic in ("panel", "terminal", "diff"):
        bx -= 32
        svg.rect(bx, 12, 28, 28, c["toolbarControl"], sh["button"])
        svg.icon(bx + 6, 18, ic, c["toolbarControlForeground"], 16)

    # ---------- Conversation ----------
    cx = mx + (mw - COL_W) / 2
    fg, mu = c["text"], c["textMuted"]

    y = HEADER_H + 28
    bw = 350
    svg.rect(cx + COL_W - bw, y, bw, 40, c["messageSurface"], sh["bubble"],
             c["border"] if sh.get("bubble_border") else None)
    svg.text(cx + COL_W - bw + 16, y + 25, "Make T3 Code look like the apps I use every day.",
             c["messageForeground"], 13.5)

    y += 66
    svg.icon(cx, y - 12, "check", mu, 15)
    svg.text(cx + 22, y, "Worked for 1m 12s · Edited 5 files", mu, 12.5)
    svg.text(cx + 234, y, "+620", c["updateForeground"], 12.5, 600, mono=True)
    svg.text(cx + 276, y, "−3", c["errorForeground"], 12.5, 600, mono=True)

    y += 34
    svg.text(cx, y, "Done. Five new themes, each with a light and a dark variant:", fg, 14.5)
    inline_bg = mix(fg, c["canvas"], 0.08)
    inline_fg = sh.get("inline_code", {}).get(mode, fg)
    for name, rest in [("slack.json", " aubergine sidebar, green send button"),
                       ("discord.json", " blurple on charcoal"),
                       ("spotify.json", " black, white and that green")]:
        y += 28
        svg.add(f'<circle cx="{cx + 8}" cy="{y - 5}" r="2.5" fill="{fg}"/>')
        w = len(name) * 7.8 + 10
        svg.rect(cx + 20, y - 15, w, 21, inline_bg, 4)
        svg.text(cx + 25, y, name, inline_fg, 12.5, mono=True)
        svg.text(cx + 20 + w + 2, y, rest, fg, 14.5)

    y += 24
    svg.rect(cx, y, COL_W, 112, c["codeBackground"], sh["code"], c["border"])
    svg.text(cx + 14, y + 22, "json", mix(c["codeForeground"], c["codeBackground"], 0.72), 11.5, 500)
    for i, line in enumerate(['{ "name": "' + theme["name"] + '",',
                              '  "appearance": "' + mode + '",',
                              '  "accent": "' + c["accent"] + '" }']):
        svg.text(cx + 14, y + 50 + i * 21, line, c["codeForeground"], 13, mono=True)

    # ---------- Composer ----------
    comp_h = 108
    comp_y = H - comp_h - 22
    if sh.get("borderless"):
        stroke = None
    elif "composer_border" in sh:
        stroke = mix(fg, c["input"], sh["composer_border"])
    else:
        stroke = c["border"]
    svg.rect(cx, comp_y, COL_W, comp_h, c["input"], sh["composer"], stroke,
             ' filter="url(#sh)"' if sh.get("shadow") else "")
    if sh.get("underline"):
        svg.add(f'<rect x="{cx + 1}" y="{comp_y + comp_h - 2}" width="{COL_W - 2}" height="2" fill="{c["accent"]}"/>')
    svg.text(cx + 18, comp_y + 30, "Ask anything, @ to add files", c["placeholder"], 14)

    by = comp_y + comp_h - 42
    weight = 700 if sh.get("bold_buttons") else 500
    svg.icon(cx + 16, by + 7, "paperclip", c["iconMuted"], 16)
    chip_x = cx + 44
    for label, w in (("Opus 5.5", 92), ("High", 64)):
        svg.rect(chip_x, by, w, 30, c["secondary"], sh["button"])
        svg.text(chip_x + 12, by + 20, label, c["secondaryForeground"], 12.5, weight)
        svg.icon(chip_x + w - 22, by + 9, "chevron", c["secondaryForeground"], 12)
        chip_x += w + 8
    sx, sy = chip_x + 8, by + 6
    svg.rect(sx, sy, 34, 18, sh.get("switch", {}).get(mode, c["accent"]), 9)
    svg.add(f'<circle cx="{sx + 25}" cy="{sy + 9}" r="7" fill="{sh.get("knob", c["accentForeground"])}"/>')
    svg.text(sx + 42, sy + 13.5, "Plan", c["mutedForeground"], 12.5)
    sxc, syc = cx + COL_W - 30, by + 15
    svg.add(f'<circle cx="{sxc}" cy="{syc}" r="16" fill="{c["messageAction"]}"/>')
    svg.icon(sxc - 8, syc - 8, "up", c["messageActionForeground"], 16)

    svg.add("</g>")
    edge = mix("#FFFFFF" if dark else "#000000", c["canvas"], 0.14)
    svg.add(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{edge}"/>')
    svg.add("</svg>")
    return "\n".join(svg.parts) + "\n"


def main():
    dest = ROOT / "previews"
    dest.mkdir(exist_ok=True)
    for old in dest.glob("*.svg"):
        old.unlink()
    for path in sorted((ROOT / "themes").glob("*.json")):
        theme = json.loads(path.read_text())
        for mode in ("light", "dark"):
            out = dest / f"{path.stem}-{mode}.svg"
            out.write_text(render(path.stem, theme, mode))
            print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
