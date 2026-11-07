# AI热点 · Cursor Cloud 刷新说明（日更 + App「即时更新」）

本文档给 **Cursor Cloud Agent** 用（消耗 Cursor 云端额度，不是 Grok Bot）。  
日更（每天约 07:00 Asia/Shanghai）与手机 App「即时更新」都会启动 Cloud Agent，并要求 **严格按本文执行**。

## 仓库与分支（必读）

- 仓库：`https://github.com/tianshanhangui89-glitch/Niceo-ai-news`（小写 `niceo-ai-news` 亦可）
- **必须直接推送到 `main`**（启动参数应为 `workOnCurrentBranch: true` + `repos[].startingRef: "main"` + `autoCreatePR: false`）
- App 只读 `main` 上的 `data.json`。**不要**只推到 `cursor/*` 分支，**不要**只开 PR 不合并。
- 工作区应已是本仓库；时区按 **Asia/Shanghai（UTC+8）**；「今天」以系统日期为准。

## 成功标准

1. 跑完抓取流水线，写出新的 `data.json`（保留全部频道：`ai` / `world` / `startup` / `github` / `papers` / `models` / `skills`）。
2. `git add` + `commit` + **`git push origin main`**（或当前即为 main 时 `git push`）。
3. 在日志末尾打印：`generated_at` 与各频道条数（`ai_count` / `world_count` / `startup_count` / `github_count` / `papers_count` / `models_count` / `skills_count` / `item_count`）。

## 禁止事项

- 不要重建 / 改 Android APK、不要改 `index.html` UI（除非抓取脚本已坏到无法跑）。
- 不要登录、爬取或操作小红书 / 其它社交账号。
- 不要编造榜单数字、论文指标或「亲身经历」式文案。
- 不要把 API Key、GitHub Token、keystore 写入仓库或提交。
- 不要新建 cron / 其它仓库。

## 执行步骤（按顺序）

在仓库根目录：

```bash
# 0) 确认位置
pwd
ls tools/ingest_primary.py tools/fetch_news.py tools/github_zh_map.py data.json

# 1) 一手源（smol.ai / The Batch / HF Papers / arXiv / LMArena / Artificial Analysis）
python3 tools/ingest_primary.py

# 2) 合并 raw/ → data.json（含 X / 时政 / 创业 / GitHub 历史条目 + 一手源）
#    若本机刚跑过 ingest，也可：SKIP_PRIMARY_INGEST=1 python3 tools/fetch_news.py
python3 tools/fetch_news.py

# 3) 检查产物
python3 - <<'PY'
import json
d=json.load(open("data.json"))
print("generated_at=", d.get("generated_at"))
for k in ("item_count","ai_count","world_count","startup_count","github_count","papers_count","models_count"):
    print(f"{k}=", d.get(k))
assert d.get("items") and d.get("generated_at"), "data.json incomplete"
PY

# 4) 提交并推到 main（只改数据相关文件）
git status
git add data.json raw/*.json 2>/dev/null || git add data.json
git commit -m "chore(data): AI热点 refresh $(date +%Y-%m-%d)" || echo "no content change"
git push origin HEAD:main
```

若 `raw/` 未跟踪或不存在，至少保证 **`data.json` 已推到 main**。

## 频道与文案约定（已实现于脚本，勿破坏）

| 频道 | 来源 |
|------|------|
| `ai` | X News + news.smol.ai/latent.space + The Batch（去重） |
| `world` | 时政 X |
| `startup` | 创业 X |
| `github` | Trending / 热度（中文说明） |
| `papers` | HF Daily Papers + arXiv cs.AI/LG/CL；含 `alphaxiv_url` |
| `models` | LMArena Elo 快照 + Artificial Analysis 公开榜 |
| `skills` | X 上热门 AI 技能介绍（Agent Skills / SKILL.md / 技能包等） |

- 用户可见标题 / 摘要 / hook：**中文**（模型名、论文英文原题可放 `origin_title` / 英文 title）。
- 旧字段兼容；可有可选扩展字段。
- LMArena 若 live API 失败：继续用 HF 空间公开 Elo pickle 快照，并在摘要标明快照日期。

## 技能频道（skills）

- 来源：X `search_news` 抓「热门 AI 技能 / Agent Skills / SKILL.md / Claude·Cursor 技能包」介绍。
- raw：`raw/YYYY-MM-DD-skills-*.json`（`channel: skills`）。
- **展示文案一律中文**：`title` / `summary` / `hook` / `category`（英文模型名、产品名可保留原文）。入库走 `tools/skills_zh_map.py` 精选表，缺省时 `fetch_news.py` 可机翻并回写 map；禁止把未翻译的 `[EN]` 英文条当作最终展示。
- **若本次 Cloud 环境无 X 工具或抓取为空：保留 data.json 里已有 `channel=skills` 条目，禁止整频道清空。**

## 故障处理

- `ingest_primary` 某一源失败：记录原因，继续其它源；不要整次中止（除非完全无法写出 `data.json`）。
- 依赖：优先标准库；LMArena unpickle 可能需要 `pandas`/`numpy`（无则跳过 Arena，保留 AA）。
- 推送失败：检查 `git remote` / 权限后重试 push 到 **main**。

## 给启动方的提示词模板（App / 日更可用）

```
Follow CURSOR_REFRESH.md exactly. Today is <YYYY-MM-DD Asia/Shanghai>.
Refresh all AI热点 feeds now and publish data.json to main.
Steps: python3 tools/ingest_primary.py && python3 tools/fetch_news.py ;
commit data.json (+ raw if present) ; git push origin HEAD:main ;
print generated_at and per-channel counts.
Do not rebuild APK. Do not touch Xiaohongshu. Do not invent metrics.
```
