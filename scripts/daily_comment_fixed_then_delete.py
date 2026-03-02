#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日固定评论后删除（刷活跃）：只读 JUEJIN_COOKIES，其余写死。
- 每天 10:25 由 GitHub Actions 触发（见 .github/workflows/daily-comment-fixed-then-delete.yml）
- 执行 3 次：每次 发布固定评论 → 等待 1 分钟 → 删除该评论；每个 API 间隔 1 分钟。
- token 过期后需在脚本内更新 HARDCODED_MS_TOKEN / HARDCODED_A_BOGUS / HARDCODED_CSRF。
"""

import os
import sys
import time
from pathlib import Path

_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from scripts.juejin_collect import (
    comment_article_return_id,
    delete_comment,
)

# 写死：从浏览器评论/删除请求复制，过期后需更新
HARDCODED_MS_TOKEN = "x-hoXQKcRHIgCSRcSFAAzIRwNywSDWRuvJwqkYzXjA8sbJ_FUmMKOLbe6dGChoLhmf_YXUi7CbiVzmH_XxZrYqfDWqHSdhsdo-P_5Hgo7AVh7yoC_vUeW05KAatO1ebgDA%3D%3D"
HARDCODED_A_BOGUS = "Qj-YfOgyMsm1TGuIe7Dz9r6ARu60YW4lgZEN4u-fBzqF"
HARDCODED_CSRF = "000100000001e83be4c3102bb39fd7188db783157e4b15c643b25f254331c1bdc06bd45965121898e8d6ba668112"

FIXED_ITEM_ID = "7611068495070445577"
FIXED_COMMENT_CONTENT = "从贫血模型到 DDD：后端分层与领域建模实战"

REPEAT_TIMES = 3
INTERVAL_SEC = 60


def run():
    cookies = os.getenv("JUEJIN_COOKIES")
    if not cookies:
        print("❌ 未找到 JUEJIN_COOKIES")
        return

    print(f"📌 固定评论后删除 x{REPEAT_TIMES} 次，每次 API 间隔 {INTERVAL_SEC} 秒")
    print(f"   文章: {FIXED_ITEM_ID} | 评论: 「{FIXED_COMMENT_CONTENT}」\n")

    for i in range(REPEAT_TIMES):
        print(f"  [{i + 1}/{REPEAT_TIMES}] 发布评论…")
        comment_id = comment_article_return_id(
            cookies,
            FIXED_ITEM_ID,
            FIXED_COMMENT_CONTENT,
            ms_token=HARDCODED_MS_TOKEN,
            a_bogus=HARDCODED_A_BOGUS,
            csrf_token=HARDCODED_CSRF,
        )
        if not comment_id:
            print(f"  [{i + 1}/{REPEAT_TIMES}] ❌ 发布失败，跳过本次删除")
            if i < REPEAT_TIMES - 1:
                time.sleep(INTERVAL_SEC)
            continue
        print(f"  [{i + 1}/{REPEAT_TIMES}] ✅ 已发布 comment_id={comment_id}，{INTERVAL_SEC}s 后删除")
        time.sleep(INTERVAL_SEC)

        print(f"  [{i + 1}/{REPEAT_TIMES}] 删除评论 {comment_id}…")
        if delete_comment(cookies, comment_id, csrf_token=HARDCODED_CSRF):
            print(f"  [{i + 1}/{REPEAT_TIMES}] ✅ 已删除")
        else:
            print(f"  [{i + 1}/{REPEAT_TIMES}] ❌ 删除失败")
        if i < REPEAT_TIMES - 1:
            time.sleep(INTERVAL_SEC)

    print("\n🎉 完成\n")


if __name__ == "__main__":
    run()
