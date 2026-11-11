#!/usr/bin/env python3
"""汇总构建任务上传的 SUSFS 元数据 artifact。

各矩阵构建项在克隆 SUSFS 源码（含 config/config 的 commit 锁定）后写出
`susfs-meta/<CONFIG>.json`，内容形如：

    {"branch": "...", "source": "...", "commit": "...", "commit_date": "...", "version": "..."}

Release 作业把它们下载到同一目录后调用本脚本，按分支去重（同一分支的多个
矩阵项取值一致），每行输出：

    <branch>|<version>|<commit>|<commit_date>|<source>

用法:
    python3 scripts/susfs_meta.py <metadata-dir>

目录不存在或没有 json 文件时不输出任何内容（不报错），由调用方决定如何提示。
"""

from __future__ import annotations

import glob
import json
import os
import sys


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: susfs_meta.py <metadata-dir>", file=sys.stderr)
        return 2

    seen: dict[str, tuple[str, str, str, str]] = {}
    for path in sorted(glob.glob(os.path.join(argv[1], "*.json"))):
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError) as exc:
            print(f"::warning::忽略无法解析的 SUSFS 元数据 {path}: {exc}", file=sys.stderr)
            continue
        if not isinstance(data, dict):
            print(f"::warning::忽略非对象的 SUSFS 元数据 {path}", file=sys.stderr)
            continue
        branch = str(data.get("branch") or "").strip()
        if not branch or branch in seen:
            continue
        seen[branch] = (
            str(data.get("version") or ""),
            str(data.get("commit") or ""),
            str(data.get("commit_date") or ""),
            str(data.get("source") or ""),
        )

    for branch, (version, commit, date, source) in sorted(seen.items()):
        print(f"{branch}|{version}|{commit}|{date}|{source}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
