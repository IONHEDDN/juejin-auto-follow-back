#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日定时：仅用大号给推荐沸点前 3 条点赞。
- 每天 8:00 由 GitHub Actions 触发（见 .github/workflows/daily-digg-short-msg.yml）
- 每次点赞间隔 2 秒
"""

import os
import sys
import time
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from scripts.juejin_short_msg import get_recommend_short_msg_ids, digg_short_msg

DIGG_INTERVAL_SEC = 2
TOP_N = 3


def run_daily_digg_short_msg():
    """大号获取推荐前 3 条沸点并逐个点赞。"""
    cookies = os.getenv("JUEJIN_COOKIES")
    if not cookies:
        print("❌ 未找到 JUEJIN_COOKIES，请在 GitHub Secrets 中配置")
        return

    msg_ids = get_recommend_short_msg_ids(cookies, limit=TOP_N)
    if not msg_ids:
        print("❌ 未获取到推荐沸点列表")
        return

    print(f"📌 大号每日沸点点赞：取前 {TOP_N} 条")
    print(f"   msg_ids: {msg_ids}")
    print(f"   每次点赞间隔 {DIGG_INTERVAL_SEC} 秒\n")

    ok = 0
    for i, msg_id in enumerate(msg_ids, 1):
        if digg_short_msg(cookies, msg_id):
            ok += 1
            print(f"  [{i}/{TOP_N}] ✅ 已点赞 {msg_id}")
        else:
            print(f"  [{i}/{TOP_N}] ❌ 点赞失败 {msg_id}")
        if i < len(msg_ids):
            time.sleep(DIGG_INTERVAL_SEC)

    print(f"\n🎉 完成：成功 {ok}/{len(msg_ids)} 条\n")


if __name__ == "__main__":
    run_daily_digg_short_msg()
