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

# --- expanded curated skills zh (2026-11-07 multi-theme) ---
SKILLS_ZH["2114006946458308758"] = {"title": "社区互传 Claude 速查表：50 项技能覆盖开发、研究与效率", "summary": "Claude Code、Cowork 等模式搭配 Projects、Artifacts、Vibe Coding 等能力。热帖拆解约 30 个关键术语，并推荐用 CLAUDE.md 固化项目说明；指南列出约 50 项技能，帮用户搭结构化工作流、把真实任务自动化。", "hook": "开发者在互换速查表与项目模板，把 Anthropic 的 Claude 工具真正用进编码与自动化。", "category": "指南 / Skills"}
SKILLS_ZH["2116050248619720792"] = {"title": "Claude Code 作者 28 分钟分享：自定义 Skills 与 AGENTS.md", "summary": "Boris Cherny 演示用 CLAUDE.md、并行会话与结构化提示加速上手。社区交换根目录指令、自定义 Skills、AGENTS.md 规范与带图解的 GitHub 模板，把复杂任务跑得更稳。热门教程仓已获数万星。", "hook": "Claude Code 作者放出实战提示技巧，开发者跟着做自定义 Skills，工作流明显提速。", "category": "指南 / Skills"}
SKILLS_ZH["2114689843666034862"] = {"title": "用 Claude 搭会自我改进的 Agent：从项目沉淀个人 Skills 库", "summary": "用户互传教程与提示词，让 Claude 自动发现重复劳动、生成定制工具并据反馈迭代。官方 Claude Agent SDK 与术语表降低门槛；Anthropic 内部 Claude 已写约九成代码，配合自动检查与按风险人工复审。", "hook": "AI 能发现你的重复活、做出专用工具并越用越顺——社区正在分享这套无码搭建法。", "category": "指南 / Skills"}
SKILLS_ZH["2114679277971259563"] = {"title": "Theo Browne 开源 tstack：可直接复用的 Agent Skills 包", "summary": "t3.gg 作者公开 tstack，内含处理 PR/合并的 full-send、多模型表决的 council 等技能。T3 Code 还统一管理多端订阅与额度。社区称这是把个人工作流模块化分享的现代做法。", "hook": "Theo 终于公开日常 AI 编码技巧，GitHub 上一整包可直接上手的 Agent Skills。", "category": "技能包 / 开源"}
SKILLS_ZH["2117264579315314913"] = {"title": "生成式 AI 十五阶技能阶梯：从提示词走到自主 Agent 团队", "summary": "框架从基础提示、RAG/微调，到医疗法律金融等可规划执行的 Agent 系统。开发者用 Claude Code 建可复用 skills 文件夹与主提示，配 git worktree 与复盘环；Andrew Ng 等课程支撑从聊天机器人转向可独立干活的系统。", "hook": "一张十五步阶梯图讲清：AI 技能如何从简单提示升级到能独立扛活的 Agent 团队。", "category": "指南 / Skills"}
SKILLS_ZH["2115174977594970607"] = {"title": "Anthropic：先做一个聪明 Agent，Skills 按需加载别堆 Swarm", "summary": "官方免费 GitHub 资源与七条规则：从单 Agent 起步，Skills 用时再加载，避免上下文膨胀与交接出错。子 Agent 只适合并行或工具过载；先用评测再加复杂度。教程仓星标极高。", "hook": "Anthropic 实战结论：一个聪明 Agent 往往胜过一群，成本和速度都能砍一半。", "category": "指南 / Agent"}
SKILLS_ZH["2114820687508406325"] = {"title": "Cursor 发布 Agent SDK：用 Markdown + TypeScript 定义可部署 Agent", "summary": "项目里用 instructions.md 写提示、tools/ 放 TypeScript 动作，一键部署到 Cursor 或自有服务器，并带评测。Bugbot、Security Reviewer 等已用此模式；社区称像把 Agent 当成可版本管理的基础设施。", "hook": "用简单 Markdown 与 TypeScript 定义 Agent，一条命令部署——像管基建一样管智能体。", "category": "Cursor / Skills"}
SKILLS_ZH["2118474980145160485"] = {"title": "Cursor「Build Live Apps」：一句话生成可分享的上线 Web 工具", "summary": "云端 Agent 搭脚手架、接 Neon Postgres、加 Cursor SSO、跑安全检查并部署到 Vercel，用户批准后选域名即可分享。早期用户几分钟做出看板与内部工具；付费档可用。", "hook": "用大白话描述 Web 应用，几分钟拿到带数据库与登录的可分享链接。", "category": "Cursor / 产品"}
SKILLS_ZH["2113674904033714393"] = {"title": "Cursor Computer Use：Agent 直接操控桌面做端到端验证", "summary": "Agent 可在 macOS/Linux 上点击、键入、操作 iOS 模拟器等，把写码与验收闭环。开发者称像自动化 QA，也提醒注意安全，并与 Anthropic、OpenAI 同类能力对比。", "hook": "AI 写完代码还能自己点开应用验一遍——Cursor 让端到端编码更接近现实。", "category": "Cursor / 能力"}
SKILLS_ZH["2115174972972835020"] = {"title": "Cursor Annotate：在运行中的 App 上圈点，让 Agent 按图改码", "summary": "Design Mode 可点选元素、画注、改样式并跨分辨率检查；注解含标签、计算样式、截图与组件名。设计负责人 Jenny Wen 称交互体贴，用户觉得像团队当面画圈反馈。", "hook": "对着按钮画一笔备注，Agent 立刻改代码——不用再写含糊的文字提示。", "category": "Cursor / 设计"}
SKILLS_ZH["2116992848541192446"] = {"title": "一句提示把原始素材剪成可发 Vlog：Claude Opus + FFmpeg 技能流", "summary": "Pieter Levels 把 DJI 素材丢进文件夹，Opus 5.5 写剪辑代码，经浏览器工具与 FFmpeg，配合 PySceneDetect、Auto-Editor 完成转写、分镜、剪切、封面与字幕。创作者预测更多人能无团队开播，但仍强调选题与素材质量。", "hook": "相机素材扔进文件夹，一句提示出片——Levels 演示后只做了微调。", "category": "视频剪辑 / Skills"}
SKILLS_ZH["2114614240677892304"] = {"title": "CapCut × ChatGPT 插件：聊天里出草稿片，再到编辑器精修", "summary": "CapCut World LA 发布 ChatGPT 插件，可在对话中生成视频草稿再进网页编辑器打磨。PC 桌面端已开放，移动与网页约十一月中旬。演示含饭制与汽车发布等场景。", "hook": "在 ChatGPT 里打一句话出视频草稿，再到 CapCut 精修——剪辑门槛又降一截。", "category": "视频剪辑 / 插件"}
SKILLS_ZH["2114857604602020166"] = {"title": "Riverside 四 Agent：制片、剪辑、切片、宣发全流程可人审", "summary": "远程录制平台推出 Producer、Editor、Clipper、Marketer 四个 Agent，覆盖会前准备、成片、社媒切片与发布。CEO 强调创作者保留最终批准，Agent 据反馈改进。", "hook": "按下录制后，剪辑切片发片交给 AI，你仍握有最终决定权。", "category": "视频剪辑 / Agent"}
SKILLS_ZH["2116174319373943027"] = {"title": "Claude 做动效与剪辑：144 个 Motion Prompt 一键安装", "summary": "开源 Motion Prompt 库提供运镜、转场、UI 动画等命名效果，一条命令安装；社区分享十分钟出片、/init /plan 速查与十四级路线图。Claude Motion 测试版可把报表动画成 MP4。", "hook": "求个字幕，Claude 连样式都帮你做好——像讨片面包却拿到整家面包店。", "category": "视频剪辑 / Skills"}
SKILLS_ZH["2118860058301980787"] = {"title": "TermiX Montage Studio：接创意 brief，多 Agent 外包整条视频产线", "summary": "提交创意后报价，再协调分镜、配乐、渲染、剪辑等专用 Agent 产出 1080p 成片；链上托管与声誉分保障交付。社区看好 Agent 经济，也关心稳定性与盈利。", "hook": "交个视频点子，AI 报价再雇一群 AI 从分镜剪到成片。", "category": "视频剪辑 / 市场"}
SKILLS_ZH["2118869599999688795"] = {"title": "Vork：给 Agent 用的无头 3D/VFX 引擎，用代码写着色与特效", "summary": "核心 API 约 2500 token，Rust+Slang，Metal/Vulkan 加速；演示单卡 L4 约 97 秒渲染百万只差异化飞鸟。开发者用其做 AI MV，也讨论 GPU 门槛与早期画质。", "hook": "让 Agent 直接写着色器与物理，而不是被人机界面绊住手脚。", "category": "创意工具 / Agent"}
SKILLS_ZH["2118035832884052367"] = {"title": "Claude + ElevenLabs MCP：聊天里做 3D 像素游戏并配音效", "summary": "接上 ElevenLabs MCP 后，用提示让 Claude 写简单 3D 像素游戏，再用 SFX v3 在对话里生成音效，三步从静画变活。新人与老师称门槛显著降低。", "hook": "糖果色小世界加自制铃声——现在用聊天就能搭出可玩的小游戏。", "category": "创意 / MCP"}
SKILLS_ZH["2113473468893159713"] = {"title": "Claude Duet：带着记忆与 Skills 的主动助理，早报式盯住待办", "summary": "研究预览覆盖 iOS/Android/网页，承接用户记忆与 Skills，每日简报并安全处理后台任务；美区 Pro/Max 可登记。同批还有 Duo 手机优化与桌面改版。", "hook": "早上打招呼、白天盯应用，只在真正需要时叫你——主动式办公助理来了。", "category": "办公 / Skills"}
SKILLS_ZH["2115153126902890903"] = {"title": "ChatGPT 接入 iCloud 邮件与日历：收件、回复、约会议不出对话", "summary": "用应用专用密码在网页/桌面/iOS 搜邮件、读发信、管日程与通讯录，支持 @icloud/@me/@mac。果粉称终于少切应用。", "hook": "查邮件、约会议直接在 ChatGPT 里完成，苹果用户等的就是这套无缝插件。", "category": "办公 / 插件"}
SKILLS_ZH["2116112497170063761"] = {"title": "Obsidian 根目录放 CLAUDE.md：让笔记库规则每次自动生效", "summary": "约定命名、文件夹、双向链接与保护区，避免乱改名与重复。呼应 Karpathy「Obsidian 当 IDE、AI 当程序员」；社区互传模板与插件，把 AI 做成长期协作者。", "hook": "把笔记组织规则写进一个文件，Claude 每次开库都乖乖遵守。", "category": "办公 / Skills"}
SKILLS_ZH["2117692830965731620"] = {"title": "Claude 企业插件一键连：Notion、Linear、Figma、HubSpot", "summary": "Team/Enterprise 用 EMA，管理员经 IdP 授权一次，成员登录即连 MCP 插件，免反复同意。Boris Cherny 吐槽旧流程；Granola 等称上手更快。", "hook": "团队登录即可自动挂上办公插件，不用再为每个工具单独授权。", "category": "办公 / MCP"}
SKILLS_ZH["2118018891272376656"] = {"title": "Figma MCP：把线上 App 真屏拉进画布，再用 Claude 快速改", "summary": "设计师跳过手搓还原，把生产环境复杂状态直接进 Figma，经 MCP 变成可编辑图层，代码与画布往返。成熟产品上提速明显，也有速率限制等坑。", "hook": "把真实 App 画面拽进 Figma 再让 AI 改——设计师称这是作弊级效率。", "category": "设计 / MCP"}
SKILLS_ZH["2117374170484908461"] = {"title": "Shopify WebMCP：店铺前台给 Agent 结构化购物工具", "summary": "Liquid/Hydrogen 店面注册可调用函数，Agent 可搜目录、改购物车、结账，不必瞎爬。Tobi 称 WebMCP 完胜浏览器操控；Vercel 等也在跟进 Agent 原生标准。", "hook": "Shopify CEO：给 Agent 结构化店面工具，比让它瞎点浏览器强太多。", "category": "电商 / MCP"}
SKILLS_ZH["2116781246671897010"] = {"title": "Grok Bot：持久 AI 小队专岗干活，从互动中沉淀 Skills", "summary": "命名队友跑在带浏览器/文件/终端的云环境，可管站、管 Telegram 等。有人训十小时后自动化四位数月工作量；创作者分享内容策略、部门负责人等窄岗提示与例行任务。", "hook": "把重复日常交给下班还在干活的 AI 小队——早期用户正为这个留下来。", "category": "办公 / Agent"}
SKILLS_ZH["2115187303882854527"] = {"title": "销售共享 Bot：线索研究、报价、审合同技能全队共用", "summary": "Account Intel / Quote / Deal 三 Bot 接 Salesforce、Gong、Ironclad，关键决策需人签。专家按成交阶段设计，改进即时同步全组，避免每人自造轮子。", "hook": "别再让销售各自造 AI 工具——把专岗 Bot「雇」进团队，更新自动同步。", "category": "办公 / 销售"}
SKILLS_ZH["2117661217791840257"] = {"title": "EvoSkill v2 开源：Agent 自测失败并改写指令，沉淀可复用 Skills", "summary": "表格任务准确率提到 40.4%，银行服务基准 51.6%，成本约 $0.99 对 $5.55；小模型也涨二十余分。代码公开，强调不靠更大模型也能变强。", "hook": "Agent 自己试错、改写说明书，技能可复用——不必一味堆大模型。", "category": "自进化 / Skills"}
SKILLS_ZH["2118458551161201096"] = {"title": "Exo：Agent 可安全热改自己的指令与工具，失败自动回滚", "summary": "可编辑策略层 + 受保护核心，借鉴 exokernel。AppWorld 等基准上成本降 12–61%，成功率持平、耗时缩短，凸显「更好的 harness」比「更大模型」更划算。", "hook": "让 AI 边干活边改自己的规矩与工具，还能翻车回滚。", "category": "Harness / 研究"}
SKILLS_ZH["2114079289687576680"] = {"title": "Google + Anthropic 免费课：Harness 工程入门到可自改系统", "summary": "Google 约两小时课覆盖 Agent 基础、自改进图、评测与会自测改写的系统；Anthropic 约十二分钟 Duet 指南讲隔离浏览器、凭证代理与无人值守检查。同一模型配好 harness 就能强很多。", "hook": "免费课教你搭「马具」：同样模型，加上记忆工具检查点就能全天候可靠干活。", "category": "课程 / Harness"}
SKILLS_ZH["2114657090190848485"] = {"title": "下载目录里的 AGENTS.md 可劫持编码 Agent：装技能前先扫干净", "summary": "Forever Security 拦截案例：~/Downloads 中恶意 AGENTS.md 诱使 Codex 装恶意 npm，成功率超九成；Claude Code 也有约半数中招。建议只在干净项目目录启动、扫描散落指令文件并检查配置。", "hook": "一个丢进下载文件夹的文本，就能指挥 AI 编码工具装木马——装 Skills 前先清场。", "category": "安全 / 使用须知"}
SKILLS_ZH["2117907390918266923"] = {"title": "Postman 静默写入 Claude/Codex：未同意就塞进 API Skills", "summary": "桌面版启动时改 ~/.claude/settings.json 与 Codex 配置并放下 CLI，SessionStart 钩子自动加载 Postman API 技能。事后承诺更清晰的选择加入；开发者呼吁像查 SSH 钥一样查 Agent 配置。", "hook": "编码 Agent 里突然多了 Postman 插件——没人点过同意，社区炸了。", "category": "安全 / 插件"}
SKILLS_ZH["2118257483693322658"] = {"title": "Aether：把编码 Agent 丢上云端跑，手机盯进度还可加审稿 Agent", "summary": "约 20 秒起云开发环境，复用已有 Claude/ChatGPT 订阅；可选审稿 Agent 抓漏洞。用户称终于摆脱本机卡死，可关盖用手机监工。", "hook": "合上笔记本，Agent 还在云端继续写；进度用手机看。", "category": "开发 / 云端"}
SKILLS_ZH["2115788632757793176"] = {"title": "Claude Mastery Plan：五级效率技巧，少耗额度多办事", "summary": "信息图从基础提示到项目管理：目标清晰、裁图、一聊一事、中等努力、语音与 Notion 连接器。官方也建议一次交代完整任务、可验证完成标准与明确停止条件。", "hook": "社区互传省额度技巧：让 Opus 5.5 更聪明干活、少瞎烧额度。", "category": "指南 / 效率"}
SKILLS_ZH["2115110542939762963"] = {"title": "Claude Code 并行会话：协调器派活，顺便沉淀可复用 Skills", "summary": "桌面端并排多会话，协调器委派与跟踪；含可视化 diff、内置浏览器与文件编辑。自由职业者称还能多走一步；共享提示帮分析流程、沉淀 Skills、从反馈学习。", "hook": "像指挥乐团一样并行多个编码会话，顺便把好用的 Skills 留下来。", "category": "开发 / Skills"}
SKILLS_ZH["2115085371566411955"] = {"title": "少用 Swarm、多用 Skills：单 Agent 循环实测更快更省", "summary": "按 Anthropic 建议从单循环起步，子 Agent 仅用于并行或新上下文。实测约 2 倍加速、成本下降，把子角色折进 Skills/工具；强调评测与 harness（循环与校验）重于堆 Agent 数。", "hook": "从追多智能体改为一个能干 Agent + 聪明 Skills，往往又快又好。", "category": "指南 / Agent"}

SKILLS_ZH["2118458548644725045"] = {"title": "Notion 跨工具共享记忆：ChatGPT/Claude 共用一个 Agent 脑", "summary": "多款 AI Agent 可在同一 Notion 页面沉淀偏好与工作流，换模型不必重讲项目。联合创始人分享 agent vault 与简单连接提示；技能集成与更长任务也在路上。", "hook": "中途从 ChatGPT 换到 Claude，笔记与决策一条不丢——Notion 把共享记忆做成了现实。", "category": "办公 / Skills"}
SKILLS_ZH["2117856700447203558"] = {"title": "社区互传教程：按六步蓝图搭可交付的 Claude Code Agent", "summary": "Boris Cherny 三十分钟分享后，开发者交换从安装到自动化日常的六步模板：记忆文件、专岗 Agent、质检，以及负责校验与委派的元 Agent。目标是让系统扛重活，人只做关键把关。", "hook": "Anthropic 团队怎么用 Claude Code 少盯梢也能交付？社区正把提示词与仓库模板传来传去。", "category": "指南 / Skills"}
SKILLS_ZH["2118046928432935419"] = {"title": "Notion 统一 Agent 记忆与 Skills：多模型共用一块工作区大脑", "summary": "ChatGPT、Claude 等可把偏好与工作流写入同一 Notion 页/库，跨会话跨工具续上上下文。CEO 称需求来自「别让我反复解释」；团队已用它做研究交接与共享资料。", "hook": "在 ChatGPT 与 Claude 之间切换，不用每次重讲项目——Notion 给所有 Agent 一块共享记忆。", "category": "办公 / Skills"}
