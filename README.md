# AI热点 · X 上的 AI 日更 + Android App

给 Gui 用的「X 上 AI 相关热点」阅读器：每天抓取 X News，写入 `data.json`，手机 App 打开即看大卡片；有网时下拉刷新拉 GitHub / jsDelivr。

## 安装 App

1. 把 `/workspace/x-ai-news/app/AI热点.apk`（或 `AI-news.apk`）拷到手机。
2. 允许「未知来源」安装。包名：`com.gui.ainews`，应用名：**AI热点**。
3. 打开后先读 APK 内嵌的今日数据；有网时点右上角 **刷新** 或下拉，会依次尝试：
   - https://raw.githubusercontent.com/tianshanhangui89-glitch/niceo-ai-news/main/data.json
   - https://cdn.jsdelivr.net/gh/tianshanhangui89-glitch/niceo-ai-news@main/data.json
4. 点卡片看摘要，再「打开 X 原文」（系统浏览器）。

桌面预览：浏览器打开 `file:///workspace/x-ai-news/index.html`（或同目录起个静态服务）。

## 日更会写哪些文件

由 Niceo-Schedule 统一建定时任务（本目录**不**自建 routine）。建议流程：

1. Agent 用 `x.search_news` 多路 query（AI / LLM / 大模型 / Sora…）抓过去 24h。
2. 原始结果写入 `raw/YYYY-MM-DD-*.json`（保留英文全文，不进简报）。
3. `python3 tools/fetch_news.py` → 去重、中文标题/摘要、写：
   - `/workspace/x-ai-news/data.json`
   - `app/data.json`、`github-publish/data.json`
4. `bash tools/publish.sh` → 推送到公开仓 `tianshanhangui89-glitch/niceo-ai-news`。
5. 手机 App **无需重装**，下拉即可看新数据。

重建 APK（换图标/壳子时才需要）：

```bash
bash /workspace/x-ai-news/android/build_apk.sh
```

## 目录

| 路径 | 说明 |
|------|------|
| `data.json` | 当前热点（Asia/Shanghai） |
| `index.html` | 手机竖屏阅读器 |
| `raw/` | X 接口原始条目 |
| `android/` | WebView 壳，`com.gui.ainews` |
| `app/AI热点.apk` | 可安装包 |
| `tools/fetch_news.py` | raw → data.json |
| `tools/publish.sh` | 发布到 GitHub |
| `github-publish/` | 待推 / 已推镜像 |

## 说明

- 摘要来自 X News 聚合，可能随讨论演变；请点原文核实。
- 传统文化/科技热点阅读参考，**不是**投资、医疗或人生决策依据。
- 与旧版 Horizon 日报（`/workspace/daily-report`，含 NFL）分开；本项目只做 X 向 AI 热点。
