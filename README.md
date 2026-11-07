# AI热点 · AI / 时政 / 创业 / GitHub / 论文 / 模型 日更 + Android App

给 Gui 用的多频道阅读器：每天抓取 X News（AI、全球时政、AI 应用创业）、GitHub Trending/热度，以及一手源（smol.ai、The Batch、HF Daily Papers、arXiv、LMArena、Artificial Analysis），写入 `data.json`；手机 App 大卡片阅读，支持本机收藏。

## App 功能

- 顶栏频道（可横向滑动）：**AI** | **时政** | **创业** | **GitHub** | **论文** | **模型** | **技能** | **收藏**
- 收藏：点卡片右上角 ★，完整快照写入 WebView `localStorage`（键 `ainews.favorites.v1`），日更下架后仍可看
- **刷新**：只拉已发布的 `data.json`（便宜、不调 Cursor）
- **即时更新**：启动 **Cursor Cloud Agent**（消耗 Cursor 云端额度，不走 Grok Bot）。需在本机粘贴 Cursor API Key（Dashboard → API Keys）；密钥存 `localStorage ainews.cursor_api_key`，不上传。长按按钮可改/清密钥。Agent 按仓库根目录 `CURSOR_REFRESH.md` 抓取并 **push 到 main**。
- 有网时下拉刷新拉 GitHub / jsDelivr；即时更新完成后按 commit SHA 拉 raw，避开 CDN 缓存
- 论文条目可开 alphaXiv「讨论」；模型榜保留英文模型名 + 中文说明

## 一手源映射（@khyssabc）

| 源 | 频道 | 抓取方式 |
|---|---|---|
| news.smol.ai / latent.space | AI | beehiiv JSON |
| The Batch | AI | 官网 issue 列表 |
| Hugging Face Daily Papers | 论文 | `/api/daily_papers` |
| arXiv cs.AI / cs.LG / cs.CL | 论文 | Atom API |
| alphaXiv | 论文（讨论链） | `https://www.alphaxiv.org/abs/<id>` |
| LMArena | 模型 | HF 空间 Elo pickle 快照 |
| Artificial Analysis | 模型 | 公开榜单 HTML 表 |
| X 热门 AI 技能介绍 | 技能 | `raw/YYYY-MM-DD-skills-*.json`（Agent Skills / SKILL.md 等） |

## 安装

1. 安装 `/workspace/x-ai-news/app/AI热点.apk`（或 `AI-news.apk`），包名 `com.gui.ainews`
2. 远端数据：
   - https://raw.githubusercontent.com/tianshanhangui89-glitch/Niceo-ai-news/main/data.json
   - https://cdn.jsdelivr.net/gh/tianshanhangui89-glitch/Niceo-ai-news@main/data.json

## 日更（同一条 Schedule，勿另建 cron）

1. Agent 用 `x.search_news` 抓 AI / 时政 / 创业 → `raw/YYYY-MM-DD-*.json`
2. Agent 抓 GitHub Trending → `raw/YYYY-MM-DD-github-*.json`
2b. **技能预写（有 X 的 Bot，Cloud 之前）**：多路 `x.search_news`（写作/视频/办公/开发/Agent Skills/SKILL.md/Cursor·Claude skills/自动化/harness）→ `raw/YYYY-MM-DD-skills-*.json`，去重约 25–40+ 条；主题要散。Cloud Agent 无 X MCP，**不能指望它现场抓 skills**；无预写则保留旧 skills，勿清空。
3. `python3 tools/fetch_news.py`（会先跑 `ingest_primary.py` 刷新一手源）→ `data.json`（skills 走 `skills_zh_map` / 机翻，展示全中文）
4. `bash tools/publish.sh` → 推公开仓

重建 APK：

```bash
VERSION_NAME=1.4.20261107 VERSION_CODE=11061111 bash /workspace/x-ai-news/android/build_apk.sh
```

## 说明

- 摘要来自公开榜/简报，请点原文核实；不是投资或医疗建议。
- 收藏只存在本机，不会写入公开 `data.json`。
- GitHub / 论文 / 新 AI 一手条目的标题与摘要为中文；论文保留 `origin_title`，模型名保持英文。
- LMArena 使用 Hugging Face 空间公开 Elo 快照（非实时 SPA）；Artificial Analysis 数字来自公开页快照。
