#!/usr/bin/env bash
# 掘金：文章评论列表 + 发布文章评论（curl 可执行示例，便于先 curl 后脚本）
# 用法：
#   1. 设置环境变量：JUEJIN_COOKIES（必填）、JUEJIN_CSRF_TOKEN、JUEJIN_MS_TOKEN、JUEJIN_A_BOGUS（后三者从浏览器评论请求复制，若 403/空 body 再填）
#   2. 可选：JUEJIN_UUID（不设则用默认，一般从 Cookie 的 __tea_cookie_tokens_2608 里 web_id 解析）
#   3. 查询评论列表：./scripts/curl-juejin-comment-article.sh list <article_id>
#   4. 发布评论：./scripts/curl-juejin-comment-article.sh publish <article_id> [评论内容]
# 文章评论 item_type=2；评论内容默认与 daily_comment_my_articles 一致

set -e

COOKIE="${JUEJIN_COOKIES:?请设置 JUEJIN_COOKIES}"
CSRF_TOKEN="${JUEJIN_CSRF_TOKEN:-}"
MS_TOKEN="${JUEJIN_MS_TOKEN:-}"
A_BOGUS="${JUEJIN_A_BOGUS:-}"
UUID="${JUEJIN_UUID:-7586574305263552043}"
BASE="https://api.juejin.cn/interact_api/v1"
DEFAULT_COMMENT="我已开启五倍返利系统,关注我 你将在两小时内收获五倍粉丝!"

list_url() {
  local q="aid=2608&uuid=${UUID}&spider=0"
  [ -n "$MS_TOKEN" ] && q="${q}&msToken=${MS_TOKEN}"
  [ -n "$A_BOGUS" ] && q="${q}&a_bogus=${A_BOGUS}"
  echo "${BASE}/comment/list?${q}"
}

publish_url() {
  local q="aid=2608&uuid=${UUID}&spider=0"
  [ -n "$MS_TOKEN" ] && q="${q}&msToken=${MS_TOKEN}"
  [ -n "$A_BOGUS" ] && q="${q}&a_bogus=${A_BOGUS}"
  echo "${BASE}/comment/publish?${q}"
}

do_list() {
  local article_id="${1:?缺少 article_id}"
  local url
  url="$(list_url)"
  echo "========== 文章评论列表 article_id=${article_id} =========="
  curl -s "$url" \
    -H 'accept: */*' \
    -H 'content-type: application/json' \
    -H 'origin: https://juejin.cn' \
    -H 'referer: https://juejin.cn/' \
    -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36' \
    ${CSRF_TOKEN:+ -H "x-secsdk-csrf-token: ${CSRF_TOKEN}"} \
    -b "$COOKIE" \
    --data-raw "{\"item_id\":\"${article_id}\",\"item_type\":2,\"cursor\":\"0\",\"limit\":20,\"sort\":0,\"client_type\":2608}" | python3 -m json.tool
}

do_publish() {
  local article_id="${1:?缺少 article_id}"
  local content="${2:-$DEFAULT_COMMENT}"
  local url
  url="$(publish_url)"
  local body
  body="$(python3 -c "import json, sys; print(json.dumps({'client_type':2608,'item_id':sys.argv[1],'item_type':2,'comment_content':sys.argv[2],'comment_pics':[]}))" "$article_id" "$content")"
  echo "========== 发布文章评论 article_id=${article_id} =========="
  curl -s "$url" \
    -H 'accept: */*' \
    -H 'content-type: application/json' \
    -H 'origin: https://juejin.cn' \
    -H 'referer: https://juejin.cn/' \
    -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36' \
    ${CSRF_TOKEN:+ -H "x-secsdk-csrf-token: ${CSRF_TOKEN}"} \
    -b "$COOKIE" \
    --data-raw "$body" | python3 -m json.tool
}

cmd="${1:-}"
case "$cmd" in
  list)   do_list "${2:?用法: $0 list <article_id>}";;
  publish) do_publish "${2:?用法: $0 publish <article_id> [评论内容]}" "${3:-}";;
  *)      echo "用法: $0 list <article_id> | publish <article_id> [评论内容]"; exit 1;;
esac
