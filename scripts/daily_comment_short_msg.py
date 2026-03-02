#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日定时：大号给推荐前 5 条沸点各发一条评论（刷活跃），每条评论间隔 1 分钟。
- 每天 9:30 由 GitHub Actions 触发（见 .github/workflows/daily-comment-short-msg.yml）
"""

import os
import sys
import time
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from scripts.juejin_short_msg import (
    get_recommend_short_msg_ids,
    comment_short_msg,
)

TOP_N = 5
COMMENT_INTERVAL_SEC = 60
DEFAULT_COMMENT_CONTENT = "刷个活跃,混个眼熟..."


def run_daily_comment_short_msg():
    """大号取推荐前 5 条沸点，每条发一条评论，间隔 1 分钟。"""
    cookies = os.getenv("JUEJIN_COOKIES")
    if not cookies:
        print("❌ 未找到 JUEJIN_COOKIES，请在 GitHub Secrets 中配置")
        return

    content = os.getenv("JUEJIN_COMMENT_CONTENT", DEFAULT_COMMENT_CONTENT)
    msg_ids = get_recommend_short_msg_ids(cookies, limit=TOP_N)
    if not msg_ids:
        print("❌ 未获取到推荐沸点列表")
        return

    print(f"📌 大号每日沸点评论：前 {TOP_N} 条，评论内容「{content}」")
    print(f"   每条评论间隔 {COMMENT_INTERVAL_SEC} 秒\n")

    ok = 0
    for i, msg_id in enumerate(msg_ids, 1):
        if comment_short_msg(cookies, msg_id, content):
            ok += 1
            print(f"  [{i}/{TOP_N}] ✅ 已评论 {msg_id}")
        else:
            print(f"  [{i}/{TOP_N}] ❌ 评论失败 {msg_id}")
        if i < len(msg_ids):
            time.sleep(COMMENT_INTERVAL_SEC)

    print(f"\n🎉 完成：成功 {ok}/{len(msg_ids)} 条\n")


if __name__ == "__main__":
    run_daily_comment_short_msg()
