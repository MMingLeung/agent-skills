# -*- coding: utf-8 -*-
"""交付包资源完整性检查（通用版）。

扫交付包内 .py 源码引用的 resources/ imgs/ models/ templates/ assets/ 路径；
源码仓库里存在、交付包里缺失 → 判失败（退出码 1）。

用法：
    python check_delivery_resources.py --source <源码仓库根> --delivery <交付根>
        [--delivery <另一个交付根> ...]
        [--ignore-referrer 相对交付根的引用文件=原因 ...]
        [--dirs resources,imgs,models]
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

DEFAULT_RESOURCE_DIRS = ("resources", "imgs", "models", "templates", "assets")
SKIP_DIR_NAMES = frozenset(
    {"__pycache__", "py11", "chrome", "output", "browser_profile", ".git", "site-packages", "tests", ".venv", "venv"}
)


@dataclass
class ResourceCheckResult:
    delivery_root: Path
    checked: list[str] = field(default_factory=list)
    missing: list[tuple[str, str]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.missing


def _patterns(resource_dirs: Iterable[str]) -> tuple[re.Pattern[str], re.Pattern[str]]:
    alt = "|".join(re.escape(d) for d in resource_dirs)
    literal = re.compile(rf"""["']((?:{alt})[/\\][^"'\n{{}}*]+)["']""")
    chain = re.compile(rf"""["']({alt})["']((?:\s*/\s*["'][^"'\n{{}}*]+["'])+)""")
    return literal, chain


_SEGMENT_RE = re.compile(r"""["']([^"']+)["']""")


def extract_resource_refs(text: str, resource_dirs: Iterable[str] = DEFAULT_RESOURCE_DIRS) -> set[str]:
    literal_re, chain_re = _patterns(resource_dirs)
    refs: set[str] = set()
    for match in literal_re.finditer(text):
        refs.add(match.group(1).replace("\\", "/").strip())
    for match in chain_re.finditer(text):
        segments = [match.group(1), *_SEGMENT_RE.findall(match.group(2))]
        refs.add("/".join(seg.strip().strip("/") for seg in segments))
    return {ref for ref in refs if ref and ".." not in ref}


def _iter_py_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if any(part in SKIP_DIR_NAMES for part in path.relative_to(root).parts):
            continue
        if path.name.startswith("_tmp_"):
            continue
        yield path


def _exists_in_delivery(rel: str, py_file: Path, delivery_root: Path) -> bool:
    for candidate in (delivery_root / rel, py_file.parent / rel, py_file.parent.parent / rel):
        if candidate.is_file():
            return True
        if candidate.is_dir() and any(candidate.iterdir()):
            return True
    return False


def check_delivery_resources(
    source_root: Path,
    delivery_root: Path,
    *,
    ignored_referrers: dict[str, str] | None = None,
    resource_dirs: Iterable[str] = DEFAULT_RESOURCE_DIRS,
) -> ResourceCheckResult:
    result = ResourceCheckResult(delivery_root=delivery_root)
    if not delivery_root.is_dir():
        result.missing.append(("<交付根>", f"交付目录不存在: {delivery_root}"))
        return result
    ignored = ignored_referrers or {}
    dirs = tuple(resource_dirs)
    seen: set[str] = set()
    for py_file in _iter_py_files(delivery_root):
        referrer = py_file.relative_to(delivery_root).as_posix()
        if referrer in ignored:
            continue
        try:
            text = py_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for rel in sorted(extract_resource_refs(text, dirs)):
            source_path = source_root / rel
            if not (source_path.is_file() or source_path.is_dir()):
                continue
            if rel not in seen:
                result.checked.append(rel)
                seen.add(rel)
            if not _exists_in_delivery(rel, py_file, delivery_root):
                result.missing.append((rel, referrer))
    result.missing = sorted(set(result.missing))
    return result


def _parse_ignores(values: list[str]) -> dict[str, str]:
    ignores: dict[str, str] = {}
    for value in values:
        path, sep, reason = value.partition("=")
        if not sep or not reason.strip():
            raise SystemExit(f"--ignore-referrer 必须写原因：{value!r}（格式：相对路径=原因）")
        ignores[path.strip().replace("\\", "/")] = reason.strip()
    return ignores


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="交付包资源完整性检查")
    parser.add_argument("--source", required=True, type=Path, help="源码仓库根")
    parser.add_argument("--delivery", required=True, type=Path, action="append", help="交付根，可多次")
    parser.add_argument("--ignore-referrer", default=[], action="append", help="相对交付根的引用文件=原因")
    parser.add_argument("--dirs", default=",".join(DEFAULT_RESOURCE_DIRS), help="资源目录名，逗号分隔")
    args = parser.parse_args(argv)

    ignores = _parse_ignores(args.ignore_referrer)
    dirs = [d.strip() for d in args.dirs.split(",") if d.strip()]
    failed = 0
    for delivery_root in args.delivery:
        result = check_delivery_resources(args.source, delivery_root, ignored_referrers=ignores, resource_dirs=dirs)
        if result.ok:
            print(f"RESOURCE_CHECK_OK {delivery_root} checked={len(result.checked)}")
            continue
        failed += 1
        print(f"RESOURCE_CHECK_FAIL {delivery_root}")
        for rel, where in result.missing:
            print(f"  - {rel}（引用于 {where}）")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
