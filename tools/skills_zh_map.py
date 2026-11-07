# Auto-maintained Chinese copy for skills channel (id -> {title, summary, hook, category})
# Prefer curated entries; fetch_news may append machine translations for new ids.
SKILLS_ZH: dict[str, dict[str, str]] = {
    "2118755137833300074": {
        "title": "社区热传：用 Claude Code 几分钟搭出 AI Agent 的免费指南",
        "summary": "Claude Code 可在终端或桌面端读项目、规划修改、跑命令，并用文件/搜索/联网工具迭代。项目里的 CLAUDE.md 会跨会话保留构建命令与偏好。社区热门包括六步速通、从提示词到多智能体的十阶手册、工程师 28 分钟视频，以及可定制技能的开源仓库，帮新手把重心从聊天转向监管自动化工作流。",
        "hook": "大家在传简易指南与速查表：不用高深编码，也能用 Anthropic 的 Claude Code 快速搭出强力 AI Agent。",
        "category": "指南 / Skills",
    },
    "2117603924928758218": {
        "title": "开发者转向「Harness 工程」：让 AI Agent 长时间稳定干活",
        "summary": "Harness 工程是在模型外搭脚手架：控制 Agent 看见什么、用哪些工具、如何校验输出与会话记忆，以缓解忘上下文、死循环等问题。社区分享 Claude Code 五层套件（记忆文件、Skills、护栏、子 Agent、插件），以及 Letta、CrewAI 等开源方案；配图与示例强调先做简单分层，再扩展到多智能体。",
        "hook": "开发者不再只靠一句提示词，而是搭完整运行环境，让 Claude 等模型能在复杂任务上稳定跑数小时。",
        "category": "Harness / 工程",
    },
    "2116222746040357036": {
        "title": "Anthropic 放出免费课：用 Claude Opus 5.5 做会思考、行动、复盘的 Agent",
        "summary": "课程介绍 Claude Managed Agents：把推理与执行拆开，由系统负责循环、状态与可恢复。开发者分享把岗位说明写成系统提示、关键动作加人工闸门、每周自评等实践，把 AI 当结构化同事。社区指南强调记忆层、Skills 与反馈环，许多人称能省下整天重复劳动，高风险环节仍保留人审。",
        "hook": "Anthropic 工程师发布详细免费课程，教你把 Claude Opus 5.5 做成会想、会做、会记、还会自检的智能体。",
        "category": "课程 / Agent",
    },
    "2117041383831896535": {
        "title": "给编程 Agent 套「Harness」：从一次巧妙回复变成可靠搭档",
        "summary": "2026 年 7 月一篇 arXiv 论文拆解 11 套生产级编程 harness（含 Claude Code 等），归纳循环、工具、编排等七大子系统。Anthropic 工程师称团队约九成在用这类配置，呼吁做可自提示系统而非单次提示。实用建议包括用 git 存配置、模块化 Skills、夜间复盘任务，让工作流能发现问题并承接上次进度。",
        "hook": "开发者给 Claude Opus 5.5 等模型套上自定义 harness，把聪明的一次性回答变成按步骤可靠写码的搭档。",
        "category": "Harness / 编程",
    },
    "2116795422505374197": {
        "title": "技术社区互传 CLAUDE.md：给 Claude 做持久记忆与生产力系统",
        "summary": "社区交换带规划模式、子 Agent、教训日志与测试规则的 CLAUDE.md，让项目上下文每会话自动加载。claude-mem 等工具把历史摘要进本地库，再注入新对话，降低 token 并在 Codex、Claude Code 间保持连贯。专家建议约半年清一次、用清晰目标提示对接邮件与 Notion，把 AI 当有共同记忆的协作同事。",
        "hook": "开发者厌倦中途换工具、反复向 AI 解释项目，开始用 CLAUDE.md 与记忆工具，让 Claude 成为记得住一切的队友。",
        "category": "记忆 / Skills",
    },
    "2118767668119691265": {
        "title": "Harness 工程成 AI Agent 新学科：提示、预算与系统三位一体",
        "summary": "Harness 用提示、记忆文件、校验环与沙箱托住长任务。Anthropic 的 Boris Cherny 概括为提示、预算与系统；也有人把 Agent 的「脑」与「手」拆开以便失败恢复与过夜交付。Google 与 Anthropic 为相关岗位开出高薪；公开指南展示可跨会话增量改动的双 Agent 体系。",
        "hook": "靠 Anthropic、Google 等工程师的巧妙配置，AI Agent 已能连做数天复杂编程，而不必全程人工救火。",
        "category": "Harness / 工程",
    },
    "2118806662517797207": {
        "title": "用自定义 Harness 释放 Claude Opus 5.5：长跑 Agent 更稳",
        "summary": "工程师以 Opus 5.5 做主编排，把任务派给 DeepSeek 等有严格范围、工作量证明与校验环的子 Agent，减少出错。Harness 含上下文管理、权限闸门、会话日志与 AGENTS.md 等持久文件，避免冷启动丢进度。Anthropic 强调模型能力要配上工程脚手架，才能把长任务跑满数小时乃至数天。",
        "hook": "开发者给 Claude Opus 5.5 配上规则、工具与校验的自定义 harness，让 Agent 能连续专注数小时甚至数天。",
        "category": "Harness / Agent",
    },
    "2117696468664586710": {
        "title": "Google Harmony Harness：让 Agent 按反馈改写自己的工具与护栏",
        "summary": "Google 的 Harmony Harness 允许 Agent 根据真实反馈改写工具、指令与检查项，在安全与性能间折中。基准如 SecRepoBench 上比旧法高出逾 10 分，并可并行演进多版 harness 而不顾此失彼。实践者分享免费课与 GitHub 仓库，把 harness 工程当成把聪明模型变成靠谱工人的关键一环。",
        "hook": "AI 圈热议 harness 工程：正是这套关键配置，把聪明模型变成能安全承接真实任务的靠谱工人。",
        "category": "Harness / 研究",
    },
}
