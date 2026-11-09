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
for k in ("item_count","ai_count","world_count","startup_count","github_count","papers_count","models_count","skills_count"):
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
| `skills` | 具名可装 Skill 安利（Morry 风格：技能名+场景+安装） |

- 用户可见标题 / 摘要 / hook：**全频道必须中文**（ai/world/startup/github 摘要/papers/models 说明/skills 全部适用）。模型名、GitHub `owner/repo`、论文英文原题可保留在 `title`（models/github）或 `origin_title`。
- **禁止**把英文原文或 `[EN]` 前缀当作最终展示；未知条目须机翻（`translate_en_to_zh`：Argos 离线 / MyMemory / gtx）并写入 `tools/news_zh_map.py`；精选文案优先 `ZH_MAP` / `skills_zh_map` / `github_zh_map`。
- skills 继续走具名可装过滤（`is_named_installable_skill`），不要退回 Harness 概念帖。
- 旧字段兼容；可有可选扩展字段。
- LMArena 若 live API 失败：继续用 HF 空间公开 Elo pickle 快照，并在摘要标明快照日期。

## 技能频道（skills）

- **产品标杆**：对标 @Morry4AI 类安利帖（例：开源 Skill `ljg-card`——场景价值 + 安装用法）。技能栏只收「对我实际有价值的**具名可装**热点技能」。
- **必须具备**：具体 Skill 名（可装可跑）+ 能解决什么问题/适用场景 + 怎么装或怎么用（有仓库 / `npx skills add` / Codex 安装路径更佳）。中文 `title`（偏「技能名 + 一句话价值」）/`summary`/`hook`；可选字段 `skill_name` / `install` / `repo` / `x_url` / `github_url`（详情页「看 X 原帖」「打开 GitHub」）。
- **不要**：Harness / Claude Code 闲聊、泛「Agent Skills 概念帖」、无具体技能名的讨论贴、纯工具对比。
- **采集（有 X 的 Bot）**：优先 `x.search_posts` / `search_posts_all`（以及作者时间线如 @Morry4AI），辅以少量 `search_news`。推荐 query 方向：
  - `开源 Skill` / `Skill：` / `npx skills add` / `SKILL.md` + 安装/Codex/Claude/Cursor
  - 内容创作可视化、短视频工作流、去 AI 味、设计 Skill、科研/营销/游戏合集中的**具名**项
  - 过滤：能抽出 skill 名或明确可安装对象；写 `raw/YYYY-MM-DD-skills-named.json`（或 `*-skills-*.json`），条目带 `skill_name`/`install`/`_pretranslated` 更佳。
- **入库过滤**：`fetch_news.py` 的 `is_named_installable_skill` 会剔除概念帖；精选中文走 `tools/skills_zh_map.py`。目标 **约 20+ 高质量**（质量优先，宁缺毋滥）。
- raw：`raw/YYYY-MM-DD-skills-*.json`（`channel: skills`；可多个文件）。
- **日更预写（关键）**：Cursor Cloud Agent **通常没有 X MCP**。Schedule `x-ai` 启动 Cloud **之前**，须由有 X 的 Bot 预写当日 named-skills raw；Cloud 只做 ingest/fetch/publish。无预写：保留已有 skills，**禁止整频道清空**；也不要用旧式概念向 `search_news` 结果灌水。

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
