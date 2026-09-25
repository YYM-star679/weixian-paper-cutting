#!/usr/bin/env python3
"""生成幻灯片 HTML（build/slides/），并用系统 Edge 无头模式截图成 PNG（assets/slides/）。"""
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
WIDTH, HEIGHT = 1920, 1080

# 配色：宣纸暖白 + 中国红
BG = "#FBF6EE"
RED = "#C8102E"
RED_DARK = "#9E0B1F"
INK = "#3A2E2A"


def _petals(n, cx, cy, cy0, rx, ry, fill):
    out = []
    for a in range(0, 360, 360 // n):
        out.append(
            f'<ellipse cx="{cx}" cy="{cy0}" rx="{rx}" ry="{ry}" fill="{fill}" '
            f'transform="rotate({a} {cx} {cy})"/>'
        )
    return "".join(out)


def motif(kind: str) -> str:
    R, B = RED, BG  # R=红  B=纸底

    if kind == "medallion":
        return (
            '<svg width="360" height="360" viewBox="0 0 220 220">'
            f'<circle cx="110" cy="110" r="96" fill="{R}"/>'
            f'<circle cx="110" cy="110" r="72" fill="none" stroke="{B}" stroke-width="3"/>'
            + _petals(8, 110, 110, 46, 15, 26, B)
            + f'<circle cx="110" cy="110" r="22" fill="{R}"/>'
            + f'<circle cx="110" cy="110" r="9" fill="{B}"/>'
            "</svg>"
        )

    if kind == "butterfly":
        return (
            f'<svg width="360" height="360" viewBox="0 0 220 220">'
            f'<g fill="{R}">'
            '<path d="M110 92 C 62 30, 18 42, 28 84 C 38 62, 70 72, 110 96 Z"/>'
            '<path d="M110 92 C 158 30, 202 42, 192 84 C 182 62, 150 72, 110 96 Z"/>'
            '<path d="M110 102 C 70 124, 40 154, 46 178 C 62 156, 86 132, 110 114 Z"/>'
            '<path d="M110 102 C 150 124, 180 154, 174 178 C 158 156, 134 132, 110 114 Z"/>'
            '<ellipse cx="110" cy="100" rx="10" ry="42"/>'
            '<circle cx="110" cy="58" r="11"/>'
            '</g>'
            f'<path d="M107 50 C 96 34, 86 24, 80 20" stroke="{R}" stroke-width="4" fill="none"/>'
            f'<path d="M113 50 C 124 34, 134 24, 140 20" stroke="{R}" stroke-width="4" fill="none"/>'
            f'<circle cx="70" cy="70" r="8" fill="{B}"/>'
            f'<circle cx="150" cy="70" r="8" fill="{B}"/>'
            f'<circle cx="70" cy="150" r="7" fill="{B}"/>'
            f'<circle cx="150" cy="150" r="7" fill="{B}"/>'
            "</svg>"
        )

    if kind == "snowflake":
        arms = []
        for a in range(0, 360, 60):
            arms.append(
                f'<g transform="rotate({a} 110 110)">'
                f'<line x1="110" y1="110" x2="110" y2="30" stroke="{R}" stroke-width="6"/>'
                f'<line x1="110" y1="70" x2="88" y2="52" stroke="{R}" stroke-width="5"/>'
                f'<line x1="110" y1="70" x2="132" y2="52" stroke="{R}" stroke-width="5"/>'
                f'<circle cx="110" cy="34" r="4" fill="{R}"/>'
                "</g>"
            )
        return (
            f'<svg width="360" height="360" viewBox="0 0 220 220">'
            + "".join(arms)
            + f'<circle cx="110" cy="110" r="9" fill="{R}"/>'
            "</svg>"
        )

    if kind == "blossom":
        return (
            f'<svg width="360" height="360" viewBox="0 0 220 220">'
            + _petals(5, 110, 110, 62, 26, 26, R)
            + f'<circle cx="110" cy="110" r="16" fill="{B}"/>'
            + f'<circle cx="110" cy="110" r="8" fill="{R}"/>'
            "</svg>"
        )

    if kind == "lantern":
        return (
            f'<svg width="360" height="360" viewBox="0 0 220 220">'
            f'<g fill="{R}">'
            '<rect x="85" y="34" width="50" height="12" rx="4"/>'
            '<rect x="74" y="50" width="72" height="102" rx="28"/>'
            '<rect x="85" y="156" width="50" height="12" rx="4"/>'
            '<line x1="110" y1="168" x2="110" y2="200" stroke="{R}" stroke-width="4"/>'
            '<path d="M98 200 L122 200 L110 214 Z"/>'
            '</g>'
            f'<g stroke="{B}" stroke-width="3" fill="none">'
            '<line x1="110" y1="52" x2="110" y2="150"/>'
            '<line x1="88" y1="62" x2="88" y2="140"/>'
            '<line x1="132" y1="62" x2="132" y2="140"/>'
            '<ellipse cx="110" cy="101" rx="26" ry="47"/>'
            "</g></svg>"
        )

    if kind == "opera":
        return (
            f'<svg width="360" height="360" viewBox="0 0 220 220">'
            f'<ellipse cx="110" cy="110" rx="80" ry="90" fill="{R}"/>'
            f'<path d="M110 42 L104 62 L116 62 Z" fill="{B}"/>'
            f'<path d="M68 100 Q 88 82 108 100 Q 88 102 68 100 Z" fill="{B}"/>'
            f'<path d="M152 100 Q 132 82 112 100 Q 132 102 152 100 Z" fill="{B}"/>'
            f'<path d="M104 108 L110 132 L116 108 Z" fill="{B}"/>'
            f'<path d="M86 152 Q 110 172 134 152 Q 110 164 86 152 Z" fill="{B}"/>'
            f'<circle cx="64" cy="132" r="7" fill="{B}"/>'
            f'<circle cx="156" cy="132" r="7" fill="{B}"/>'
            "</svg>"
        )

    if kind == "fish":
        return (
            f'<svg width="360" height="360" viewBox="0 0 220 220">'
            f'<g fill="{R}">'
            '<ellipse cx="92" cy="110" rx="72" ry="40"/>'
            '<path d="M160 110 L196 84 L186 110 L196 136 Z"/>'
            '<path d="M78 70 Q 100 52 122 72 Z"/>'
            '<path d="M80 126 Q 98 148 70 154 Z"/>'
            '</g>'
            f'<circle cx="48" cy="100" r="8" fill="{B}"/>'
            f'<circle cx="48" cy="100" r="4" fill="{R}"/>'
            f'<circle cx="92" cy="100" r="12" fill="{B}" opacity="0.65"/>'
            f'<circle cx="118" cy="100" r="12" fill="{B}" opacity="0.65"/>'
            f'<circle cx="92" cy="126" r="10" fill="{B}" opacity="0.65"/>'
            "</svg>"
        )

    return ""


def title_size(title: str) -> int:
    n = len(title)
    if n <= 5:
        return 120
    if n <= 7:
        return 100
    return 84


def render(seg, total):
    ts = title_size(seg["title"])
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  width:{WIDTH}px; height:{HEIGHT}px; background:{BG}; overflow:hidden;
  font-family:"Microsoft YaHei","DengXian","PingFang SC",sans-serif; color:{INK};
}}
.bg {{ position:absolute; inset:0; }}
.bg .wash {{ position:absolute; right:-120px; top:-120px; width:560px; height:560px; }}
.bg .wash svg {{ opacity:0.06; width:100%; height:100%; }}
.frame {{ position:absolute; inset:34px; border:3px solid {RED}; }}
.frame .in {{ position:absolute; inset:7px; border:1px solid {RED}; }}
.corner {{ position:absolute; width:44px; height:44px; }}
.corner svg {{ width:100%; height:100%; }}
.corner.tl {{ left:20px; top:20px; }} .corner.tr {{ right:20px; top:20px; transform:rotate(90deg); }}
.corner.br {{ right:20px; bottom:20px; transform:rotate(180deg); }}
.corner.bl {{ left:20px; bottom:20px; transform:rotate(270deg); }}
.content {{ position:absolute; left:140px; top:50%; transform:translateY(-50%); width:980px; }}
.eyebrow {{ font-size:32px; letter-spacing:14px; color:{RED_DARK}; font-weight:600; margin-bottom:34px; }}
.title {{ font-family:"STZhongsong","SimSun",serif; font-size:{ts}px; font-weight:700;
  color:{RED}; line-height:1.18; letter-spacing:3px; }}
.divider {{ width:128px; height:8px; background:{RED}; margin:44px 0; border-radius:4px; }}
.subtitle {{ font-size:44px; color:{INK}; font-weight:500; line-height:1.55; letter-spacing:1px; }}
.pageno {{ position:absolute; right:96px; bottom:74px; font-size:28px; letter-spacing:5px; color:{RED_DARK}; }}
.pageno b {{ font-size:40px; color:{RED}; font-weight:700; }}
</style></head>
<body>
<div class="bg"><div class="wash">{motif(seg['motif'])}</div></div>
<div class="frame"><div class="in"></div></div>
<div class="corner tl"><svg viewBox="0 0 44 44"><path d="M2 22 L22 2 L42 2 L42 22 Z" fill="{RED}"/><path d="M22 6 L22 22 L38 22" fill="none" stroke="{BG}" stroke-width="3"/></svg></div>
<div class="corner tr"><svg viewBox="0 0 44 44"><path d="M2 22 L22 2 L42 2 L42 22 Z" fill="{RED}"/><path d="M22 6 L22 22 L38 22" fill="none" stroke="{BG}" stroke-width="3"/></svg></div>
<div class="corner br"><svg viewBox="0 0 44 44"><path d="M2 22 L22 2 L42 2 L42 22 Z" fill="{RED}"/><path d="M22 6 L22 22 L38 22" fill="none" stroke="{BG}" stroke-width="3"/></svg></div>
<div class="corner bl"><svg viewBox="0 0 44 44"><path d="M2 22 L22 2 L42 2 L42 22 Z" fill="{RED}"/><path d="M22 6 L22 22 L38 22" fill="none" stroke="{BG}" stroke-width="3"/></svg></div>
<div class="content">
  <div class="eyebrow">蔚 县 剪 纸 · {seg['chapter']}</div>
  <div class="title">{seg['title']}</div>
  <div class="divider"></div>
  <div class="subtitle">{seg['subtitle']}</div>
</div>
<div class="motif" style="position:absolute; right:110px; top:50%; transform:translateY(-50%);">{motif(seg['motif'])}</div>
<div class="pageno"><b>{seg['id']:02d}</b> / {total:02d}</div>
</body></html>"""


def main():
    segs = json.load(open(os.path.join(ROOT, "src", "segments.json"), encoding="utf-8"))
    total = len(segs)

    html_dir = os.path.join(ROOT, "build", "slides")
    png_dir = os.path.join(ROOT, "assets", "slides")
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(png_dir, exist_ok=True)

    for seg in segs:
        i = seg["id"]
        html_path = os.path.join(html_dir, f"slide_{i:02d}.html")
        png_path = os.path.join(png_dir, f"slide_{i:02d}.png")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(render(seg, total))

        url = "file:///" + html_path.replace("\\", "/")
        png_abs = png_path.replace("\\", "/")
        subprocess.run(
            [
                EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                "--force-device-scale-factor=1", "--virtual-time-budget=1200",
                f"--window-size={WIDTH},{HEIGHT}",
                f"--screenshot={png_abs}", url,
            ],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        print(f"[{i}/{total}] slide -> {os.path.basename(png_path)}")

    print("all slides done.")


if __name__ == "__main__":
    main()
