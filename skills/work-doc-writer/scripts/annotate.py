"""截图标注：坐标网格辅助定位、对照表输出、按清单画红框和序号。

用法：
  python annotate.py grid <图片或文件夹> [-o 输出目录] [--step 100]
  python annotate.py table <shots.json>
  python annotate.py apply <shots.json>

shots.json 格式见 reference/screenshots.md。
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageStat

RED = (230, 27, 27)
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}
FONT_DIRS = [Path(r"C:\Windows\Fonts"), Path.home() / r"AppData\Local\Microsoft\Windows\Fonts"]
TEXT_FONTS = ["simfang.ttf", "仿宋_GB2312.ttf", "STFANGSO.TTF", "msyh.ttc"]
DIGIT_FONTS = ["msyh.ttc", "arial.ttf", "simhei.ttf"]


def find_font(candidates, size):
    for name in candidates:
        for d in FONT_DIRS:
            p = d / name
            if p.exists():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default(size)


def list_images(target):
    p = Path(target)
    if p.is_dir():
        return sorted(f for f in p.iterdir() if f.suffix.lower() in IMAGE_EXTS)
    return [p]


def cmd_grid(args):
    out_dir = Path(args.output) if args.output else None
    for img_path in list_images(args.target):
        im = Image.open(img_path).convert("RGB")
        w, h = im.size
        overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)
        font = find_font(DIGIT_FONTS, max(12, w // 90))
        step = args.step
        for x in range(0, w, step // 2):
            major = x % step == 0
            d.line([(x, 0), (x, h)], fill=(0, 120, 255, 150 if major else 60), width=1)
            if major:
                d.text((x + 2, 2), str(x), fill=(0, 90, 220, 255), font=font, stroke_width=2, stroke_fill="white")
        for y in range(0, h, step // 2):
            major = y % step == 0
            d.line([(0, y), (w, y)], fill=(0, 120, 255, 150 if major else 60), width=1)
            if major and y:
                d.text((2, y + 2), str(y), fill=(0, 90, 220, 255), font=font, stroke_width=2, stroke_fill="white")
        res = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
        target_dir = out_dir or img_path.parent / "_grid"
        target_dir.mkdir(parents=True, exist_ok=True)
        out = target_dir / f"{img_path.stem}.grid.png"
        res.save(out)
        print(f"{img_path.name}\t{w}x{h}\t{out}")


def load_spec(path):
    spec_path = Path(path)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    base = spec_path.parent
    src = Path(spec.get("source_dir", "."))
    out = Path(spec.get("output_dir", "annotated"))
    spec["_source_dir"] = src if src.is_absolute() else base / src
    spec["_output_dir"] = out if out.is_absolute() else base / out
    return spec


def cmd_table(args):
    spec = load_spec(args.spec)
    print("| 序号 | 截图文件 | 放在哪里 | 标注内容 | 图题 |")
    print("|---|---|---|---|---|")
    for i, shot in enumerate(spec["shots"], 1):
        marks = [m.get("label") or m.get("text", "") for m in shot.get("marks", [])]
        marks_text = "；".join(m for m in marks if m) or "不标注"
        print(f"| {i} | {shot['file']} | {shot.get('section', '待确认')} | {marks_text} | {shot.get('caption', '待确认')} |")


def overlaps(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def busyness(gray, rect):
    crop = gray.crop(tuple(int(v) for v in rect))
    return ImageStat.Stat(crop).stddev[0]


def place_label(box, size, gray, occupied, pos, gap):
    """在框四周找最空白、不压其他标注的位置；pos 指定方向时只在该方向内微调。"""
    x1, y1, x2, y2 = box
    tw, th = size
    w, h = gray.size
    cy = (y1 + y2 - th) / 2
    cands = [
        ("top", x1, y1 - th - gap), ("top", x2 - tw, y1 - th - gap),
        ("right", x2 + gap, cy), ("right", x2 + gap, y1), ("right", x2 + gap, y2 - th),
        ("bottom", x1, y2 + gap), ("bottom", x2 - tw, y2 + gap),
        ("left", x1 - tw - gap, cy),
    ]
    if pos in {"top", "right", "bottom", "left"}:
        cands = [c for c in cands if c[0] == pos]
    best, best_score = None, None
    for rank, (_, x, y) in enumerate(cands):
        if pos in {"top", "right", "bottom", "left"}:
            x, y = min(max(0, x), w - tw), min(max(0, y), h - th)
        rect = (x, y, x + tw, y + th)
        if x < 0 or y < 0 or rect[2] > w or rect[3] > h:
            continue
        score = busyness(gray, rect) + rank * 0.5
        if any(overlaps(rect, o) for o in occupied):
            score += 1000
        if best_score is None or score < best_score:
            best, best_score = (x, y), score
    return best or (x1 + gap, y1 + gap)


def annotate_one(shot, spec):
    src = spec["_source_dir"] / shot["file"]
    if not src.exists():
        raise FileNotFoundError(f"截图不存在：{src}")
    im = Image.open(src).convert("RGB")
    gray = im.convert("L")
    w, h = im.size
    d = ImageDraw.Draw(im)
    line_w = shot.get("line_width") or spec.get("line_width") or max(3, round(w / 340))
    text_size = shot.get("font_size") or spec.get("font_size") or max(16, round(w * 0.024))
    digit_size = round(text_size * 1.4)
    gap = max(4, line_w * 2)
    warnings = []
    boxes = []
    for m in shot.get("marks", []):
        if "box" in m:
            x1, y1, x2, y2 = m["box"]
            if not (0 <= x1 < x2 <= w and 0 <= y1 < y2 <= h):
                warnings.append(f"{shot['file']}: 框 {m['box']} 超出图片范围 {w}x{h}")
            box = (max(0, x1), max(0, y1), min(w, x2), min(h, y2))
            d.rectangle(box, outline=RED, width=line_w)
            boxes.append((box, m))
    occupied = [b for b, _ in boxes]
    for box, m in boxes:
        label = m.get("label")
        if not label:
            continue
        digit_only = label.strip().isdigit()
        font = find_font(DIGIT_FONTS if digit_only else TEXT_FONTS, digit_size if digit_only else text_size)
        l, t, r, b = d.textbbox((0, 0), label, font=font, stroke_width=2)
        if "label_at" in m:
            x, y = m["label_at"]
        else:
            x, y = place_label(box, (r - l, b - t), gray, occupied, m.get("pos", "auto"), gap)
        d.text((x - l, y - t), label, fill=RED, font=font, stroke_width=2, stroke_fill="white")
        occupied.append((x, y, x + r - l, y + b - t))
    for m in shot.get("marks", []):
        if "text" in m and "at" in m:
            font = find_font(TEXT_FONTS, m.get("font_size", text_size))
            d.text(tuple(m["at"]), m["text"], fill=RED, font=font, stroke_width=2, stroke_fill="white")
    if shot.get("crop"):
        im = im.crop(tuple(shot["crop"]))
    out_dir = spec["_output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{shot['id']}.png"
    im.save(out)
    return out, warnings


def cmd_apply(args):
    spec = load_spec(args.spec)
    all_warn = []
    for shot in spec["shots"]:
        if "id" not in shot:
            print(f"ERROR {shot['file']}: 缺少 id（如 \"1-2\"）", file=sys.stderr)
            sys.exit(1)
        if not shot.get("marks") and not shot.get("crop"):
            src = spec["_source_dir"] / shot["file"]
            spec["_output_dir"].mkdir(parents=True, exist_ok=True)
            out = spec["_output_dir"] / f"{shot['id']}.png"
            if src.suffix.lower() == ".png":
                shutil.copyfile(src, out)
            else:
                Image.open(src).convert("RGB").save(out)
            print(f"{shot['id']}\t{out}\t(未标注)")
            continue
        out, warns = annotate_one(shot, spec)
        all_warn.extend(warns)
        print(f"{shot['id']}\t{out}")
    for wmsg in all_warn:
        print("WARN", wmsg, file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("grid", help="生成带坐标网格的副本，用来读框坐标")
    g.add_argument("target")
    g.add_argument("-o", "--output")
    g.add_argument("--step", type=int, default=100)
    t = sub.add_parser("table", help="输出截图对照表（给用户确认）")
    t.add_argument("spec")
    a = sub.add_parser("apply", help="按 shots.json 画红框和序号")
    a.add_argument("spec")
    args = ap.parse_args()
    {"grid": cmd_grid, "table": cmd_table, "apply": cmd_apply}[args.cmd](args)


if __name__ == "__main__":
    main()
