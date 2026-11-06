#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
python3 tools/fetch_news.py
mkdir -p github-publish
cp -f data.json index.html github-publish/
cp -f README.md github-publish/README.md 2>/dev/null || true
python3 tools/publish_to_github.py || {
  code=$?
  echo "推送未完成（exit $code）。本地产物已在 github-publish/"
  exit $code
}
LOCAL=$(python3 -c "import json;print(json.load(open('data.json'))['generated_at'])")
echo "本地数据版本: $LOCAL"
for i in 1 2 3 4 5 6; do
  R=$(curl -s -m 15 "https://raw.githubusercontent.com/tianshanhangui89-glitch/niceo-ai-news/main/data.json?t=$(date +%s%N)" \
    | python3 -c "import json,sys;print(json.load(sys.stdin).get('generated_at',''))" 2>/dev/null || echo "?")
  [ "$R" = "$LOCAL" ] && break
  sleep 8
done
echo "GitHub raw generated_at: $R"
[ "$R" = "$LOCAL" ] && echo "✅ 发布完成，App 下拉刷新即可" || echo "⚠️ raw 可能尚未同步，稍后刷新"
