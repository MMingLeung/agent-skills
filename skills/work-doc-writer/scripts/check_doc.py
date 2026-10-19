"""检查 Markdown 源稿：错别字、引号、图片与图号、禁用措辞、待确认项、手册三段式、界面名称是否出现在源码里。

用法：
  python check_doc.py <源稿.md> [--code-dir 程序源码目录]

有 ERROR 时退出码为 1；WARN 只提示。
"""
import argparse
import os
import re
import sys
from pathlib import Path

import yaml

TYPOS = {
    "EXCECL": "EXCEL", "EXECL": "EXCEL", "继继续": "继续", "从新排序": "重新排序", "从新生成": "重新生成",
    "从新运行": "重新运行", "帐号": "账号", "登陆": "登录", "既可": "即可", "按装": "安装",
}
BANNED = ["温馨提示", "友情提示", "您", "恭喜", "点击这里", "哦", "立即开始"]
ACTION_WORDS = ("点击", "双击", "选择", "勾选", "填写", "输入", "切换", "打开")
CODE_EXTS = {".py", ".json", ".ui", ".html", ".htm", ".js", ".ts", ".vue", ".bas", ".cls", ".frm", ".txt", ".yaml", ".yml", ".ini", ".bat"}
RE_IMAGE = re.compile(r"^!\[(.*?)\]\((.*?)\)\s*$")
RE_FIG = re.compile(r"^图(\d+)(?:-(\d+))?\s+\S")
RE_QUOTED = re.compile(r"“([^“”]+)”")


def load(path):
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        offset = fm.count("\n") + 1
        return yaml.safe_load(fm) or {}, body.splitlines(), offset
    return {}, text.splitlines(), 0


SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "site-packages", ".idea", ".pytest_cache"}
NAME_ONLY_DIRS = {"dist", "build", "_internal", "temp", "tmp", "logs", "log", "drivers", "downloads", "output", "outputs", "pages"}


def code_corpus(code_dir):
    """内容只读源码目录；dist、logs 等大目录只收集文件名（用来核对 exe、bat 名称）。"""
    chunks, names = [], set()
    for root, dirs, files in os.walk(code_dir):
        dirs[:] = [d for d in dirs if d.lower() not in SKIP_DIRS]
        rel_parts = {p.lower() for p in Path(root).relative_to(code_dir).parts}
        name_only = bool(rel_parts & NAME_ONLY_DIRS)
        if name_only:
            dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in files:
            names.add(fn)
            if name_only:
                continue
            f = Path(root) / fn
            if f.suffix.lower() in CODE_EXTS and f.stat().st_size < 1_000_000:
                try:
                    chunks.append(f.read_text(encoding="utf-8", errors="ignore"))
                except OSError:
                    pass
    return "\n".join(chunks), names


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("--code-dir")
    args = ap.parse_args()
    src = Path(args.source)
    meta, lines, offset = load(src)
    errors, warns = [], []

    def at(n):
        return f"第{n + offset}行"

    profile = meta.get("profile", "manual")
    for key in ("title",) + (("versions",) if profile != "report" else ()):
        if not meta.get(key):
            errors.append(f"文件头缺少 {key}")

    h1, h2_index, fig_prefix, fig_seq, last_fig = None, 0, None, 0, 0
    h2_blocks = []
    for n, raw in enumerate(lines):
        line = raw.strip()
        if not line or line.startswith("<!--"):
            continue
        for bad, good in TYPOS.items():
            if bad in line:
                errors.append(f"{at(n)} 错别字「{bad}」→「{good}」")
        if line.count("“") != line.count("”"):
            errors.append(f"{at(n)} 中文引号不成对：{line[:40]}")
        if re.search(r"(^|[^\w“])”[^“”]+”", line):
            errors.append(f"{at(n)} 引号方向错（左引号写成了右引号）：{line[:40]}")
        if '"' in line and re.search(r"[\u4e00-\u9fff]", line) and not line.startswith("|"):
            warns.append(f"{at(n)} 中文句子里用了英文引号，界面元素应使用“”")
        for w in BANNED:
            if w in line:
                warns.append(f"{at(n)} 措辞「{w}」不符合手册语气")
        if "待确认" in line:
            warns.append(f"{at(n)} 待确认：{line[:50]}")
        if line.startswith("# "):
            h1 = line[2:].strip()
        elif line.startswith("## "):
            h2_index += 1
            h2_blocks.append({"title": line[3:].strip(), "h1": h1, "h3": []})
        elif line.startswith("### ") and h2_blocks:
            h2_blocks[-1]["h3"].append(line[4:].strip())
        m = RE_IMAGE.match(line)
        if m:
            caption, img = m.group(1).strip(), Path(m.group(2))
            img = img if img.is_absolute() else src.parent / img
            if not img.exists():
                errors.append(f"{at(n)} 图片不存在：{img}")
            if not caption:
                warns.append(f"{at(n)} 图片没有图题")
                continue
            fm = RE_FIG.match(caption)
            if not fm:
                errors.append(f"{at(n)} 图题格式应为「图1-2 描述」或「图1 描述」：{caption}")
                continue
            major, minor = int(fm.group(1)), fm.group(2)
            if minor is None:
                if major != last_fig + 1:
                    errors.append(f"{at(n)} 图号不连续：{caption}（上一张是 图{last_fig}）")
                last_fig = major
            else:
                minor = int(minor)
                if major != fig_prefix:
                    if fig_prefix is not None and major != fig_prefix + 1:
                        errors.append(f"{at(n)} 图号章节号跳号：{caption}")
                    fig_prefix, fig_seq = major, 0
                if minor != fig_seq + 1:
                    errors.append(f"{at(n)} 图号不连续：{caption}（应为 图{major}-{fig_seq + 1}）")
                fig_seq = minor
        if len(line) > 120 and not line.startswith("|"):
            warns.append(f"{at(n)} 句子偏长（{len(line)} 字），考虑拆成两步或放进（注：……）")

    if profile == "manual":
        for b in h2_blocks:
            if b["h1"] == "操作说明":
                missing = [s for s in ("准备数据", "操作步骤", "结果说明") if s not in b["h3"]]
                web_variant = any(h.startswith(("资料准备", "开始录入")) for h in b["h3"])
                if missing and not web_variant:
                    warns.append(f"功能「{b['title']}」缺少小节：{'、'.join(missing)}")

    if args.code_dir:
        corpus, names = code_corpus(args.code_dir)
        seen = set()
        for n, raw in enumerate(lines):
            if not any(w in raw for w in ACTION_WORDS):
                continue
            for name in RE_QUOTED.findall(raw):
                if name in seen:
                    continue
                seen.add(name)
                if name in corpus or name in names:
                    continue
                warns.append(f"{at(n)} 界面名称「{name}」在源码里没找到，核对是否与界面一致")

    for e in errors:
        print("ERROR", e)
    for w in warns:
        print("WARN ", w)
    print(f"RESULT errors={len(errors)} warns={len(warns)}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
