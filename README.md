# AI热点 · AI / 时政 / 创业 / GitHub 日更 + Android App

给 Gui 用的多频道阅读器：每天抓取 X News（AI、全球时政、AI 应用创业）与 GitHub Trending/热度，写入 `data.json`；手机 App 大卡片阅读，支持本机收藏。

## App 功能

- 顶栏频道：**AI** | **时政** | **创业** | **GitHub** | **收藏**
- 收藏：点卡片右上角 ★，完整快照写入 WebView `localStorage`（键 `ainews.favorites.v1`），日更下架后仍可看
- 有网时下拉刷新拉 GitHub / jsDelivr

## 安装

1. 安装 `/workspace/x-ai-news/app/AI热点.apk`（或 `AI-news.apk`），包名 `com.gui.ainews`
2. 远端数据：
   - https://raw.githubusercontent.com/tianshanhangui89-glitch/niceo-ai-news/main/data.json
   - https://cdn.jsdelivr.net/gh/tianshanhangui89-glitch/niceo-ai-news@main/data.json

## 日更（同一条 Schedule，勿另建 cron）

1. Agent 用 `x.search_news` 抓 AI / 时政 / 创业 → `raw/YYYY-MM-DD-*.json`  
   - 时政文件名含 `-world-`；创业含 `-startup-`；AI 无特殊前缀或含 `-ai-`
2. Agent 抓 GitHub Trending（daily/weekly）与高星热度 → `raw/YYYY-MM-DD-github-*.json`
3. `python3 tools/fetch_news.py` → `data.json`（含 `ai_count` / `world_count` / `startup_count` / `github_count`）
4. `bash tools/publish.sh` → 推公开仓

重建 APK：

```bash
VERSION_NAME=1.1.20261106 VERSION_CODE=11061106 bash /workspace/x-ai-news/android/build_apk.sh
```

## 说明

- 摘要来自 X News / GitHub 公开榜，请点原文核实；不是投资或医疗建议。
- 收藏只存在本机，不会写入公开 `data.json`。
