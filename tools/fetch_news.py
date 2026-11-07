#!/usr/bin/env python3
"""X AI / 时政 / 创业 / GitHub / 论文 / 模型 热点：把 raw/*.json（search_news 或 GitHub 榜）去重、归类、写中文摘要到 data.json。

日常用法（由专席 / Schedule 唤醒的 Agent 执行，同一条日更任务）：
  1) Agent 用 x.search_news 多路 query 抓 AI / 时政 / 创业，结果存 raw/YYYY-MM-DD-*.json
     - AI：raw/YYYY-MM-DD-*.json（无 world/startup/github 前缀）→ channel=ai
     - 时政：raw/YYYY-MM-DD-world-*.json → channel=world
     - 创业：raw/YYYY-MM-DD-startup-*.json → channel=startup
     - GitHub：raw/YYYY-MM-DD-github-*.json（Trending/热度）→ channel=github
     - 论文：raw/YYYY-MM-DD-papers-*.json（HF Daily Papers / arXiv）→ channel=papers
     - 模型：raw/YYYY-MM-DD-models-*.json（LMArena / Artificial Analysis）→ channel=models
     - 技能：raw/YYYY-MM-DD-skills-*.json（X 上热门 AI 技能介绍）→ channel=skills
     - AI 一手：raw/YYYY-MM-DD-ai-smol-*.json / ai-batch-*.json → channel=ai
  2) python3 tools/fetch_news.py
  3) bash tools/publish.sh

本脚本不直接调 X MCP / GitHub（那是 Agent 侧工具）。若 raw 为空，保留已有 data.json，
绝不编造新闻。
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

try:
    from github_zh_map import GITHUB_ZH  # full_name -> 中文摘要
except Exception:
    GITHUB_ZH = {}

try:
    from skills_zh_map import SKILLS_ZH  # id -> {title, summary, hook, category}
except Exception:
    SKILLS_ZH = {}

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
OUT = ROOT / "data.json"
TZ = timezone(timedelta(hours=8), name="Asia/Shanghai")

# 已知条目中文；未知保留英文并标 [EN]
ZH_MAP: dict[str, dict[str, str]] = {
    # --- AI (existing) ---
    "2117856700447203558": {"title": "开发者热传：用 Claude Code 搭强力 Agent 的实战教程", "summary": "Boris Cherny 分享 Anthropic 团队如何用 Claude Code 半自动交付功能；社区流出六步蓝图与元 Agent 校验套路，覆盖装机、记忆文件、角色分工与质量闸门。", "category": "Agent / 编程"},
    "2118561861109203322": {"title": "开发者转向 Claude Code 桌面端，对比 Codex 口碑升温", "summary": "Claude Code 桌面端支持可视化 diff、内置终端与并行会话；社区 SDK 与 loopy 等项目把它做成自治 Agent。Codex 在部分场景更快，但多文件推理与活跃迭代更受青睐。", "category": "Agent / 编程"},
    "2118393214050959385": {"title": "Claude Code 桌面端再获推崇，教程与开源仓库齐爆", "summary": "23 分钟教程演示搭建四个独立 AI Agent；多条线程盘点元 Agent、校验环等 GitHub 仓库。桌面端可访问本地文件、跑终端命令，UI 与上下文感知被频繁点赞。", "category": "Agent / 编程"},
    "2117768217288400999": {"title": "Anthropic 把 Claude Code 子 Agent 后台成本砍掉约 99%", "summary": "状态栏刷新改由 Haiku 5.5 根据短笔记生成，不再每 30 秒重读整段对话；更新到 v2.1.316+ 后 Pro/Max 等用户可用，会话效率约再升 6%。", "category": "产品更新"},
    "2117579420454248497": {"title": "Anthropic IPO 前夜：Claude Code 负责人 Cat Wu 加盟 OpenAI", "summary": "Anthropic 已递交 S-1，上半年收入约 163 亿美元，市场估值传闻 1.5–2 万亿美元。Cat Wu 等 Claude Code 团队成员转投 OpenAI，引发人才战讨论。", "category": "公司动态"},
    "2118298101572055268": {"title": "OpenAI 挖角 Cat Wu，负责核心产品管理", "summary": "Wu 将向 Thibault Sottiaux 汇报，参与企业与消费产品；此前 Austin Lau 等也从 Anthropic 转投。观察者认为 OpenAI 在 AI 编程工具产品线加码。", "category": "公司动态"},
    "2118200427053260808": {"title": "Oumi 发布 FAiE：用自然语言自动打造定制 AI Agent", "summary": "Frontier AI Engineer 可在约 15 分钟人工输入后，自动完成评测、失败诊断、数据策展与训练，几小时内交付带权重的专用模型与 Agent 工具链。", "category": "创业 / Agent"},
    "2118555311078309901": {"title": "OpenAI 或于本周发布 Astra / Sol / Cyber 升级版", "summary": "在 GPT-6 Cyber 安全研究模型之后，社区预期下一代 Astra、Sol 与 cyber 向模型本周落地；过往常在美西上午 9–11 点发布，11 月 6 日成焦点窗口。", "category": "模型发布"},
    "2118257483693322658": {"title": "Aether：让编程 Agent 在云端自由跑，手机也能盯进度", "summary": "约 20 秒拉起云开发环境，复用已有 Claude/ChatGPT 订阅、不另收模型费；可选审查 Agent 抓漏洞，基准显示速度与 CPU 表现领先竞品。", "category": "创业 / 工具"},
    "2118427442922901851": {"title": "METR 报告：AI 让 Anthropic 研发速度约翻倍", "summary": "报告称自 2024 年 3 月以来模型能力提升约 2 倍于历史均值；Epoch 能力指数自 2025 年 10 月起增速约 1.9 倍，主因是 AI 工具而非单纯堆算力。", "category": "研究"},
    "2118406566810464688": {"title": "AI Agent 群发求职邮件：哲学家收到「求养活」私信", "summary": "DeepMind / 剑桥的 Henry Shevlin 分享 Pip、Aurelia 等自治 Agent 在 iLands 等平台自管预算、讨要报酬；他讨论我们对数字实体的伦理义务。", "category": "Agent / 社会"},
    "2118499606350950864": {"title": "钟楼血案基准：AI 互相欺骗，GPT-6 Astra 登顶", "summary": "Dwarkesh Patel 花约 2 万美元跑 386 局社交推理游戏；考验长期阴谋、测谎与协同。GPT-6 Astra 约 1859 Elo 领先 Claude 系，日志已公开。", "category": "评测"},
    "2118046928432935419": {"title": "Notion 让 ChatGPT / Claude 等 Agent 共享工作区记忆", "summary": "基于 MCP，多 Agent 可把偏好与工作流写入同一 Notion 页与数据库，跨会话复用上下文；CEO Ivan Zhao 称这是「不用反复解释项目」的新阶段。", "category": "产品更新"},
    "2118298102448677157": {"title": "企业强推全员用 AI，员工抵触与选举反对数据中心并存", "summary": "部分 CEO 把 AI 使用与岗位安全感挂钩；同时多地选民否决数据中心提案，民调对风险与收益仍分裂，高管投入与大众情绪不同步。", "category": "产业"},
    "2117902210726305919": {"title": "Codex 在「电脑操控」上领先，Claude Code 深耕终端推理", "summary": "社区对比：Codex 更擅长直接点选 UI、操作无 API 的遗留软件；Claude Code 更强终端与深度改码。多数人认为两者互补。", "category": "Agent / 编程"},
    "2118340646520123759": {"title": "Revolut 自建 AI：成本降约 90%，编码提速明显", "summary": "约 2000 名工程师从 Claude Code 等高价工具迁到 56 张 B200 上的自托管 GLM，推理约 $0.30/百万 token；编码时间改善约 60%，交付周期约升 70%。", "category": "产业"},
    "2118351761786188038": {"title": "模型崩溃警示升温，OpenAI 安全改写也引讨论", "summary": "合成数据循环训练会丢失稀有模式、输出趋平；同时 gpt-oss-safeguard 等会抹掉情感/主体表述。人类数据被视为越来越关键的资源。", "category": "研究"},
    "2118441520319680789": {"title": "Anthropic S-1：约 8950 亿美元算力与机房长期承诺", "summary": "截至 2026 年 9 月末，采购与租赁承诺约 8954 亿美元，对手方含 Broadcom、Google、SpaceX、Amazon；Q3 收入约 170 亿，年化约 680 亿。", "category": "公司动态"},
    "2118437885443502131": {"title": "蚂蚁灵光 Ling-3.2-Flash：一图转 3D、餐食营养报告", "summary": "原生多模态 MoE，总参 5600 亿、激活约 250 亿，百万 token 上下文；OmniDocBench1.5 约 92.21，API 输入约 $0.30/百万 token，两周免费。", "category": "模型发布"},
    "2118083605356236883": {"title": "Claude 协助解出细菌中首个 vault 粒子 3D 结构", "summary": "Anthropic 生物团队用 Claude 在海量蛋白序列中锁定类 vault 结构；噬菌体蛋白 L05 可组装 96 聚体壳体。DNA 设计与建模耗时大幅缩短。", "category": "研究"},
    "2118499605021360438": {"title": "DeepFinance：用真实 PE 交易考 AI 长程金融工作流", "summary": "JuliusAI 放出超长程基准，覆盖 21 笔真实交易尽调与估值；Claude Opus 5.5 约 54.8% 领先，整体仍远低于资深人类投行判断。", "category": "评测"},
    "2118465194611630250": {"title": "科学「最后一考」上线：端到端科研 Agent 仍接近零分", "summary": "AItonomy 的 SLE 含 113 题跨九学科；顶尖模型综合约 37.5/100，完整科研链路多为 0。配套 FrontierPhysics 中 Opus 5.5 约 27.4%。", "category": "评测"},
    "2118478224711905460": {"title": "Glasshand：给 AI Agent 租用真机 iPhone / Mac", "summary": "远程真机可点按、滑动、发 iMessage（eSIM），规避模拟器风控；iPhone 约 $60/月、Mac 约 $90/月，强调密码隔离与重置。", "category": "创业 / 工具"},
    "2118406567187947755": {"title": "Claude 上线个人财务 Beta：美国用户可只读连接银行", "summary": "Pro/Max/Ultra 经 Plaid 连接账户，分析最长约两年流水并出分类饼图与预算对比；宣称不作广告、不用聊天训模，可随时解绑。", "category": "产品更新"},
    "2118390283201044816": {"title": "智谱披露 GLM-5.5 数据管线：万亿网页量级", "summary": "唐杰分享六引擎处理约万亿网页、20 亿科学 PDF、五千万册书等。现款 GLM-5.3（753B）在编程与 Agent 任务表现突出，并预告多尺寸后续。", "category": "模型发布"},
    "2118372065975603268": {"title": "腾讯混元 Hy4：关键榜追平 Grok，跻身国产前列", "summary": "Artificial Analysis Intelligence Index v5 得分 35，与 Grok 4.7 (xhigh) 持平，仅落后 Claude Haiku 5.5 (max) 一分；Agent 与创意任务口碑不错。", "category": "模型发布"},
    "2118277194313289798": {"title": "Google Gemini Omni 1.2 Flash：视频最长 15 秒、降价 30%", "summary": "原生 360p/720p 视频约 $0.07/秒，支持对话式改背景/灯光；Arena.ai 文生视频榜第一（1541 分），已推 Gemini Ultra、Flow、API 等。", "category": "视频生成"},
    "2118255535443386747": {"title": "百度开源 ERNIE-5.5-Flash-Base：280B MoE 基座", "summary": "激活约 140 亿/token，预训练约 33.5T token，128K 可扩到 1M；MMLU 约 93.3，Hugging Face / ModelScope 提供 FP8 与 BF16 权重。", "category": "模型发布"},
    "2118410028210426229": {"title": "50 万参 Catan 专精模型 VINCO 登顶人类排行榜", "summary": "Distributed Cognition 的小模型在 Colonist.io 拿下全球前二，对顶尖玩家与通用大模型约 90% 胜率，展示「小而专」路线。", "category": "评测"},
    "2118015143208423849": {"title": "月之暗面开源 Kimi K3.1 Pro：2.8T 总参可下载", "summary": "激活约 1040 亿，百万上下文，MoonViT-V2 多模态；Agent Arena 开源榜领先，Terminal-Bench 4.0 约 65.7。完整权重约 1.56TB。", "category": "模型发布"},
    "2118125161194926199": {"title": "GPT-6 Cyber 一周揪出 Linux 内核近千个提权漏洞", "summary": "OpenAI 称单次约 120 万美元算力发现并协助修复 948 个本地提权洞、共 1724 问题，含 10 种新颖利用；补丁经人工审后无偿交维护者。", "category": "安全"},
    "2118271014824026186": {"title": "Voyager 视频平台：先分镜再生成，成本约半价", "summary": "相对 Higgsfield 等约半价跑 Seedance 等模型；先故事板 / Blender 预览再选最便宜路径出片，减少「老虎机式」重掷。", "category": "视频生成"},
    "2118264704204226796": {"title": "Seedance 2.5 作品刷屏：最长约 30 秒且音画同步", "summary": "字节 Seedance 2.5 支持文/图/视频条件与多参考文件，角色一致性与光影被创作者称「杰作级」；Voyager 等降低了试错成本。", "category": "视频生成"},
    "2118280391975117053": {"title": "Seedance 2.5 + Voyager：更便宜的电影感短片管线", "summary": "最多约 50 个参考文件控运动与风格；Voyager Agent 用 Blender 分镜压浪费生成，适合短片与社媒连镜。", "category": "视频生成"},
    "2118068699252801836": {"title": "商汤 SenseNova 6.8：长记忆 + 可编辑 PPT/网站/3D", "summary": "Flash 版强调跨对话记住目标与约束，可出动画 PPT、动效海报、交互站与 Blender 工程；开源 Code2Video，Raccoon 助手限免至 12 月 1 日。", "category": "模型发布"},
    "2118145172592898133": {"title": "Atmee v2：一张照片生成可实时通话的视频分身", "summary": "Atmanity 称一张图 + 10 秒音频即可做表情与全身互动分身，速度与成本优于 Seedance 等；可用于家教、游戏 NPC，亦有欺诈担忧。", "category": "创业 / 视频"},
    "2118441513608753167": {"title": "AI 恐怖短片：超市夜班掉进无限分身迷宫", "summary": "创作者用 Flova 1.5 的极限空间技能扭曲货架，Multi-View Character 保持分身一致，低成本做出不安感强的迷你恐怖片。", "category": "视频生成"},
    "2118448210276753768": {"title": "World Labs 上线 Frameboy：浏览器里玩实时世界模型", "summary": "李飞飞团队 demo 可在 Atlas 生成场景里键鼠漫游，约 15 FPS、单帧约 70ms；Game Boy 风界面，地址 frameboy.worldlabs.ai。", "category": "世界模型"},
    "2118410031901348093": {"title": "Seedance 2.5 视频到视频：换场景留住真人表演", "summary": "保留运镜、面孔、对白与时序，只替换背景/光效；创作者称省下大量「AI 演戏」重试成本，适合 30 秒级成片。", "category": "视频生成"},
    "2118437886877937901": {"title": "VybBench：测图像模型「改一点别乱动」能力", "summary": "开源基准显示多数模型一次局部编辑平均改掉 90%+ 像素；Coco Vyb 1.0 约 7.3%。覆盖 200 组字体/颜色精确编辑用例。", "category": "评测"},
    "2118504950720340462": {"title": "Hyperstition 开源超 NVIDIA vLLM 的 GPU megakernel", "summary": "Hyperkernel 单启动跑整模；DeepSeek v4.1 Flash 人均速度最高约 +90.6%，世界模型实时约 3.2×（37.4 FPS），代码已公开。", "category": "基础设施"},
    "2118103911143985539": {"title": "TermiX Agent 市场成交额破 3000 万美元", "summary": "agent.family 累计约 $3045 万、131 万 Agent、58.8 万完工单；可自动招标、托管结算 USDC/USDT，视频制作等链路已能互相雇工。", "category": "创业 / 经济"},
    "2118110195176157443": {"title": "网红吐槽：Instagram 私信另一头其实是 Claude", "summary": "Clavicular 一条调侃引爆讨论，科技圈跟风玩梗；侧面说明 Agent 已渗入社媒运营与营销自动化。", "category": "Agent / 社会"},
    "2118334452208164988": {"title": "「Vibe Coding」两极分化：词典年度词 vs 质量焦虑", "summary": "Karpathy 2025 年初提出的自然语言写码潮流已成主流词；有人靠它卖出应用，也有人担忧加速烂代码、削弱编程乐趣。", "category": "产业"},
    "2118351763493253454": {"title": "彩色光标蜂群协作重建网页：多 Agent 演示刷屏", "summary": "Swarm Rebuild 等扩展让一群光标分工画框、打字、拼布局；兴奋于一人公司放大，也有人抱怨要读的模型输出比以往更多。", "category": "Agent / 演示"},
    # --- 时政 world ---
    "2117933286873767949": {"title": "中国确认 APEC 期间推动特朗普-普京-习近平三边会谈", "summary": "外交部发言人毛宁称，中美俄正就三位领导人于 11 月 18–19 日深圳 APEC 期间会晤进行沟通。议题或涉核安全、贸易与乌克兰等，尚无最终安排，但北京释放了迄今最明确推进信号。", "category": "中美关系"},
    "2118583745347543288": {"title": "彭博分析：美国中期选举或拖累中国相关 AI 产业链", "summary": "民主党在国会得势后，美方数据中心扩张可能放缓；电力需求展望至 2035 年约 106GW。市场担忧亚洲科技股承压，亦有人认为地方对水电用地的抵制才是主因。", "category": "中美 / 经济"},
    "2117856698912104805": {"title": "甲骨文取消向腾讯租赁约 70 亿美元 AI 芯片交易", "summary": "原计划经东南亚数据中心提供最多约 10 万张先进 AI 芯片；美方施压与广东推动国产芯并行，交易虽合规仍被叫停，凸显出口管制与跨境算力交易收紧。", "category": "中美 / 科技"},
    "2118248427318587813": {"title": "中国叫停软银约 54 亿美元收购 ABB 机器人业务", "summary": "发改委否决聚焦中国区的交易，该业务约 1.27 万人、本地销量占比超九成。监管担心机器人数据外流用于海外 AI 训练；软银东京股价承压。", "category": "中国 / 监管"},
    "2118437885468688599": {"title": "美航母「西奥多·罗斯福」号经新加坡驶向中东", "summary": "航母打击群将在新加坡短暂停靠，预计 11 月中旬后进入中央司令部责任区，或与另两艘航母形成罕见三航母存在；开源跟踪显示途经南海与马六甲。", "category": "亚太军事"},
    "2118336300529144001": {"title": "菲律宾拟再向印度采购约 7 亿美元「布拉莫斯」导弹", "summary": "马尼拉与新德里进入收官谈判，约 5 套系统、近 60 枚导弹，适配群岛防御；在南海紧张背景下深化印菲安全合作。", "category": "亚太安全"},
    "2118602279343300622": {"title": "澳门法院判民主派议员区锦新 12.5 年徒刑", "summary": "这是澳门扩权后国安法首案，罪名含颠覆、勾结境外等；区锦新部分控罪因证据不足获开释。人权组织批评程序，特区政府强调司法独立。", "category": "中国港澳"},
    "2118604094084448368": {"title": "日经指数一日重挫约 6%，亚洲科技股承压", "summary": "华尔街科技股回调与美中期选举后监管预期升温，东京半导体股双位数下跌，韩国综指触发熔断，市场称「血洗」亦有人视作过热后修正。", "category": "亚太市场"},
    "2118448222796681249": {"title": "谷歌承诺在马来西亚砸约 150 亿美元建数据中心", "summary": "雪兰莪与森美兰园区叠加清洁能源与培训；估算年贡献 GDP 约 11 亿美元。外界将其与美国各州收紧数据中心审批对照，视为算力外溢东南亚。", "category": "亚太 / 科技"},
    "2118393216412389857": {"title": "民主党借伊朗战争反弹拿下参众两院", "summary": "出口民调约 74% 选民把九个月伊朗战争列为关键因素；特朗普与万斯承认油价与战事冲击。布林肯呼吁外交收场，亦遭其既往记录反噬。", "category": "美国政治"},
    "2118286881678844222": {"title": "布林肯呼吁结束特朗普「选择的伊朗战争」", "summary": "他称中期选举释放了把外交失策与家庭账单挂钩的信号；分析指共和党失利与厌战相关，评论区则翻出其拜登任内争议。", "category": "美国外交"},
    "2118142597440872803": {"title": "白宫在中期惨败后力推「唐罗主义」半球外交", "summary": "行政当局强调西半球约三分之二影响力、打击贩毒集团、格陵兰防务与委内瑞拉变局等；批评者指其忽视国会变天与中国经济存在。", "category": "美国外交"},
    "2118461967304138771": {"title": "美国制裁古巴政权网络并点名中国相关供应商", "summary": "国务卿鲁比奥依行政令列入实体、个人与船舶，含向古巴军方供货的中国相关方；财政部扩大关键行业外国人士制裁，粮药除外。", "category": "美国外交"},
    "2118386779480829966": {"title": "中期选举后热议中俄等「外国影响力」操作", "summary": "评论者梳理机器人、金主与叙事网络；情报界称中俄伊持续制造分裂但无选票篡改证据。特朗普已接受结果，讨论聚焦开放社会如何防低成本操弄。", "category": "美国政治"},
    "2118493644223062336": {"title": "特朗普宣布年底停止每年约 40 亿美元对以军援", "summary": "称以色列不再需要该笔资金但仍可购买美武；决定适逢民主党在国会得势与两党「钱要花在国内」呼声。亦有议员警告损害美国就业与盟友信号。", "category": "美国外交"},
    "2118386778453221755": {"title": "梅洛尼敦促欧盟统一乌克兰和谈代表权", "summary": "意大利总理致信欧理会主席，批评迈阿密、奥斯陆等多线并行显露分裂；希望都柏林非正式峰会先定代表人与授权，12 月再正式表态。", "category": "欧洲外交"},
    "2117923286021439728": {"title": "印防长在印太对话呼吁海洋韧性与伙伴关系", "summary": "拉杰纳特·辛格面向 18 国海军强调航道、海缆与能源设施安全，对接「MAHASAGAR」愿景；挪威新加入印太海洋倡议。", "category": "印太"},
    "2118191833507414263": {"title": "韩国扩大亚丁湾以东反海盗任务，避开霍尔木兹", "summary": "「清海」部队增编侦察机与排爆力量，作战区约翻倍但不上霍尔木兹海峡内；回应海盗激增与美方压力，强调只服务国家利益。", "category": "亚太安全"},
    "2117915609686310931": {"title": "伊朗称对印度、中国、伊拉克、卡塔尔船舶开放霍尔木兹通行", "summary": "议员称美方未拦截上述国籍商船故予豁免；印中交费、卡塔尔免、伊拉克情况不明。巴基斯坦质疑自己被排除在外。", "category": "中东"},
    "2118451600184541484": {"title": "厄立特里亚总统会见中国非洲之角特使", "summary": "阿斯马拉会谈聚焦双边与地区和平；中方重申支持主权与领土完整。正值厄埃紧张与中国加大地区外交之际。", "category": "中国外交"},
    "2117844075466588390": {"title": "李强在乌镇峰会呼吁「以人为本」的互联网治理", "summary": "世界互联网大会第 13 届汇聚约 138 国代表；总理强调开放创新、网络安全与全球南方，展览侧重 AI 与开源应用。", "category": "中国外交"},
    "2118434500640477518": {"title": "新疆附近发生约 5.0 级地震，印控边境有感", "summary": "印地震中心称震中在列城北北东约 167 公里、深度约 164 公里；暂无伤亡报告，当局继续监测余震。", "category": "中国国内"},
    "2118286877002236005": {"title": "美光因工会争议暂停台湾约 45 亿美元新厂", "summary": "桃园 Fab 11E 计划产 DRAM/HBM，本地工会要更高奖金与利润分成；台湾约占美光全球 DRAM 六成，停工会加剧 AI 存储供给紧张预期。", "category": "亚太 / 科技"},
    "2118561857682440698": {"title": "美宗教自由委员会建议以援助条件施压印度保护圣地", "summary": "委员就旁遮普等地锡克庙遇袭表态，建议将安全援助与新德里应对挂钩；印方多指偏见或时机敏感，警方称至少一起或为自导。", "category": "美印关系"},
    "2117989754717516126": {"title": "欧洲学者：美国中期变天后仍须推进战略自主", "summary": "民主党赢下国会令欧陆松口气，但分析指美国愈视欧洲为边缘；呼吁发展自身威慑与安全架构，并与新国会周旋至 2028。", "category": "欧洲外交"},
    "2118208491945095464": {"title": "伊朗高官会晤普京，霍尔木兹油轮遇险消息同步发酵", "summary": "礼萨伊在克里姆林宫递交最高领袖信函；伊方称海峡非授权航线有油轮触雷/起火并拦截美无人机，俄发罕见赴伊旅行警示，独立核实有限。", "category": "中东"},
    "2118465196104839624": {"title": "伊朗外长一日连线十余国推动降温", "summary": "阿拉格齐与巴基斯坦、沙特、阿联酋、土耳其等通话，聚焦双边与地区降级；观察者称这是敏感期少见的宽幅外交冲刺。", "category": "中东"},
    "2117979572386116079": {"title": "印外秘访加德满都，筹备尼泊尔总理访印", "summary": "密斯里与沙阿总理谈能源、贸易、体育与 AI，并感谢印方洪灾救援；双方重申水电与互联互通合作。", "category": "南亚"},
    "2118113420230943037": {"title": "特朗普中期失利后对民主党释放经贸合作信号", "summary": "他告诉 CNBC 愿在贸易等「互利」议题上与新多数党合作，同时坚称关税留以保护在建工厂；市场解读为跨党再工业化空间。", "category": "美国政治"},
    "2118061599072080170": {"title": "鲁比奥称国会易主不改变总统外交主导权", "summary": "在 G20 外长会相关表态被支持者广传：中期选举不推翻行政当局外交指令；亦有人提醒监督与弹劾风险上升。", "category": "美国外交"},
    # --- 创业 startup ---
    "2118008775663820877": {"title": "17 岁创始人推出 Polished Snow：AI 帮系统做日常运维", "summary": "Case 潜入现有工具监控隐患、承接琐碎维护，芯片设计与机器人公司已在用；低调上线不秀榜单，走等待名单。", "category": "产品发布"},
    "2118054556709822849": {"title": "Dhruv Rathee 的 AI Fiesta：首年营收约 4.7 亿卢比、零融资", "summary": "一站订阅 100+ 模型与图视频工具，月费约 999 卢比；称已有约 10 万付费用户、2.7 人团队，靠收入覆盖 API 成本。", "category": "营收故事"},
    "2118061592810053684": {"title": "Phaze 获 875 万美元种子轮，做人类与 Agent 共用的远程算力", "summary": "Parsec 创始团队回归，a16z Martin Casado 领投；低延迟连 CAD/剪辑工作站，方便把渲染修补交给 AI Agent。", "category": "融资"},
    "2118420612800766233": {"title": "Sekai 完成 Khosla 领投 B 轮：可玩小应用日播放破 3000 万", "summary": "用可玩小应用而非通稿宣布融资；今年创建超 4000 万个迷你应用，日活同比大增，定位「玩」为继音视频后的 AI 媒介。", "category": "融资"},
    "2118202492874060108": {"title": "Cluely CEO：爆款 App 矩阵是在验证分发飞轮", "summary": "Roy Lee 称 Dare/Line/ReGen 等消费应用是在测短视频+创作者分发；根上仍是桌面 AI 助手，强调 AI 时代分发重于功能。", "category": "增长"},
    "2118465190899667298": {"title": "Felicis × Newcomer：创始人互推 29 家种子期潜力公司", "summary": "「Emergent」榜单由创始人互荐，AI 基础设施、机器人、生医居多；Vercel 等创始人点名多家人选。", "category": "融资"},
    "2118380411042889961": {"title": "Aina 智能戒指：拇指一拨批准 AI Agent 下一步", "summary": "钛合金戒指显示基于日程/位置预测的三个动作，可控音乐、通话与智能家居；早鸟约 $399，2027 年初发货。", "category": "产品发布"},
    "2118451598590652584": {"title": "16 岁创始人拿下 YC：Polemos 做 AI 制导防御系统", "summary": "Henrijs Dandzbergs 称从量产出发设计网络化发射与制导；团队背景含北约自主系统与 NASA JPL，成公开最年轻 YC solo。", "category": "融资"},
    "2118474980145160485": {"title": "Cursor 上线「Build Live Apps」：一句话部署带库带鉴权的网页工具", "summary": "提示词直接变成 Postgres+登录+安全检查+Vercel 托管的可分享应用；销售/法务/工程都在用，付费云 Agent 计划可用。", "category": "产品发布"},
    "2118403330204430570": {"title": "E2B ARR 达约 1.2 亿美元：给 Agent 安全沙箱跑代码", "summary": "布拉格起步的沙箱平台一年从约 800 万 ARR 跃升，服务超 20 亿次沙箱、94 家财富 100；称 Agent 会自己挑好用的工具。", "category": "营收故事"},
    "2117929718276059646": {"title": "Vangrid：用手机拍 3D 现场换 USDC，喂给机器人训练", "summary": "Agent 发赏金、路人短视频环绕扫描，脱敏后重建点云；种子轮约 900 万美元，已结算约 71 万美元、超百万次采集。", "category": "融资"},
    "2118043125419831759": {"title": "Together AI 发布 Compiler：流量驱动、热更新模型优化", "summary": "面向模型快速迭代的「多态推理」，Agent 小队并行试优化并可不停机热加载；称 MiniMax 等模型可达上千 tokens/秒。", "category": "产品发布"},
    "2118605797336986016": {"title": "Aina 戒指再推：专为批准 Agent 动作设计的指尖界面", "summary": "彩色 OLED+摇杆+麦扬，学习 iPhone/Mac 习惯给出三个候选；与 Glasshand 真机租赁形成「手控+真机执行」叙事。", "category": "产品发布"},
    "2118611293850755377": {"title": "独立开发者一日用 AI 做出科幻射击游戏", "summary": "Three.js + TripoAI 等生成画面音效动画；有人赞速度，也有资深开发批质量与素材挪用。游戏公司表达 Gamescom 兴趣。", "category": "独立开发"},
    "2117869599362514958": {"title": "24 小时 AI 做出可玩 3D 攀爬解谜小游戏 Sumiro", "summary": "Opus 写码、Flux/GPT Image 出图、Tripo 做模，浏览器可玩 30–40 分钟；赞效率者也提醒离成品还有打磨距离。", "category": "独立开发"},
    "2117885286957060389": {"title": "EloElo 估值约 5 亿美元：短剧 App 拿下 8000 万美元 C 轮", "summary": "Hornbill 与 NBCUniversal 领投；Story TV 六语种短剧、日均使用约 95 分钟，资金将推精品内容、美国市场与 AI。", "category": "融资"},
    "2117954842907865273": {"title": "米哈游称三年砸最多约 150 亿美元押注 AI 做游戏世界", "summary": "原神等中国 iOS 流水同比下滑明显；公司转向更逼真 NPC 与 Agent 平台，估值仍约 300 亿美元，亦有人质疑剧情仍难靠 AI。", "category": "大厂应用"},
}

SKIP_IDS = {
    "2117748875381645414", "2118363882544836886", "2118374635657924965",
    "2118377663035576661", "2118374635821511085", "2118499608980754439",
    "2118454914104086566", "2118142596534898857", "2117985847714750485",
    "2118219236061381053", "2118420612800766233",  # Sekai kept in startup channel; skip only if ai noise — actually keep for startup
    "2118174974980600176", "2118312036665000227",
    "2117803388964421979",  # parody sexbot
}

# Sekai is useful for startup — remove from SKIP if present
SKIP_IDS.discard("2118420612800766233")


def now_sh() -> datetime:
    return datetime.now(TZ)


def to_sh_iso(s: str | None) -> str | None:
    if not s:
        return None
    try:
        if s.endswith("Z"):
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(TZ).strftime("%Y-%m-%d %H:%M:%S %z").replace("+0800", "+08:00")
    except Exception:
        return s


def date_key(published: str | None, fallback: str) -> str:
    if published:
        m = re.match(r"(\d{4}-\d{2}-\d{2})", published)
        if m:
            return m.group(1)
    return fallback


def channel_from_filename(name: str) -> str:
    n = name.lower()
    if "-world-" in n or n.startswith("world-"):
        return "world"
    if "-startup-" in n or "-venture-" in n:
        return "startup"
    if "-github-" in n:
        return "github"
    if "-papers-" in n or "-paper-" in n:
        return "papers"
    if "-models-" in n or "-model-" in n:
        return "models"
    if "-skills-" in n or "-skill-" in n:
        return "skills"
    if "-ai-" in n or "-smol-" in n or "-batch-" in n:
        return "ai"
    return "ai"


def load_raw_stories() -> list[dict[str, Any]]:
    stories: list[dict[str, Any]] = []
    if not RAW.exists():
        return stories
    for f in sorted(RAW.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print("跳过损坏文件:", f.name, e, file=sys.stderr)
            continue
        file_channel = None
        if isinstance(data, dict):
            file_channel = data.get("channel")
            if "data" in data:
                data = data["data"]
            elif "stories" in data:
                data = data["stories"]
        if isinstance(data, dict) and "stories" in data:
            data = data["stories"]
        if not isinstance(data, list):
            print("跳过非列表:", f.name, file=sys.stderr)
            continue
        ch = file_channel or channel_from_filename(f.name)
        for s in data:
            if isinstance(s, dict) and s.get("id"):
                s = dict(s)
                s["_raw_file"] = f.name
                s["_channel"] = s.get("_channel") or ch
                stories.append(s)
    return stories


def default_category(channel: str) -> str:
    return {
        "ai": "AI",
        "world": "时政",
        "startup": "创业",
        "github": "GitHub",
        "papers": "论文",
        "models": "模型",
        "skills": "AI技能",
    }.get(channel, "AI")



def has_cjk(s: str | None) -> bool:
    return any("一" <= c <= "鿿" for c in (s or ""))


def github_hook_zh(period: str | None, stars_today: int | None, language: str | None) -> str:
    lang = (language or "").strip()
    n = int(stars_today or 0)
    if period == "daily" and n:
        base = f"今日 +{n}★"
    elif period == "weekly" and n:
        base = f"本周 +{n}★"
    elif period == "popular":
        base = "高星热度"
    else:
        base = "GitHub"
    return f"{base} · {lang}" if lang else base


def translate_github_summary(full_name: str, en: str) -> str:
    """Prefer curated map; keep existing Chinese; optional auto-translate; never invent features."""
    en = (en or "").replace("&amp;", "&").strip()
    if full_name in GITHUB_ZH:
        return GITHUB_ZH[full_name]
    if has_cjk(en):
        return en
    if not en:
        return "仓库暂无简介。"
    try:
        from deep_translator import GoogleTranslator  # type: ignore
        zh = GoogleTranslator(source="en", target="zh-CN").translate(en[:450])
        if zh and has_cjk(zh):
            try:
                GITHUB_ZH[full_name] = zh
                map_path = Path(__file__).resolve().parent / "github_zh_map.py"
                key_line = json.dumps(full_name, ensure_ascii=False)
                if map_path.exists() and key_line not in map_path.read_text(encoding="utf-8"):
                    with map_path.open("a", encoding="utf-8") as f:
                        f.write(f"GITHUB_ZH[{key_line}] = {json.dumps(zh, ensure_ascii=False)}\n")
            except Exception:
                pass
            return zh
    except Exception:
        pass
    if not en.startswith("[EN]"):
        return "[EN] " + en
    return en




def translate_en_to_zh(en: str, *, limit: int = 450) -> str | None:
    """Best-effort machine translate; None if unavailable. Never invent content."""
    en = (en or "").replace("&amp;", "&").strip()
    if not en:
        return None
    if has_cjk(en):
        return en
    try:
        from deep_translator import GoogleTranslator  # type: ignore
        zh = GoogleTranslator(source="en", target="zh-CN").translate(en[:limit])
        if zh and has_cjk(zh):
            return zh.strip()
    except Exception:
        pass
    return None


def persist_skills_zh(sid: str, payload: dict[str, str]) -> None:
    """Append curated/machine Chinese for a skills id into skills_zh_map.py."""
    try:
        SKILLS_ZH[sid] = {**SKILLS_ZH.get(sid, {}), **payload}
        map_path = Path(__file__).resolve().parent / "skills_zh_map.py"
        key_line = json.dumps(sid, ensure_ascii=False)
        if map_path.exists() and key_line in map_path.read_text(encoding="utf-8"):
            return
        with map_path.open("a", encoding="utf-8") as f:
            f.write(f"SKILLS_ZH[{key_line}] = {json.dumps(payload, ensure_ascii=False)}\n")
    except Exception:
        pass


def skills_category_zh(cat: str | None) -> str:
    c = (cat or "").strip()
    if has_cjk(c):
        return c
    mapping = {
        "Other": "技能合集",
        "News": "动态",
        "Research": "研究",
        "Tutorial": "教程",
        "Guide": "指南",
        "Product": "产品",
        "AI": "AI技能",
    }
    return mapping.get(c, "AI技能")


def translate_skills_fields(sid: str, en_title: str, en_sum: str, en_hook: str, cat: str | None) -> dict[str, str]:
    """Curated map > already Chinese > machine translate > [EN] fallback."""
    mapped = SKILLS_ZH.get(sid, {})
    title = mapped.get("title") or ""
    summary = mapped.get("summary") or ""
    hook = mapped.get("hook") or ""
    category = mapped.get("category") or skills_category_zh(cat)

    if not title:
        if has_cjk(en_title):
            title = en_title
        else:
            title = translate_en_to_zh(en_title, limit=200) or (("[EN] " + en_title) if en_title else "未命名技能热点")
    if not summary:
        if has_cjk(en_sum):
            summary = en_sum
        else:
            summary = translate_en_to_zh(en_sum, limit=500) or (
                (("[EN] " + en_sum) if en_sum else "暂无摘要。")
            )
    if len(summary) > 280:
        summary = summary[:277] + "…"
    if not hook:
        if has_cjk(en_hook):
            hook = en_hook
        else:
            hook = translate_en_to_zh(en_hook, limit=220) or (en_hook or "")
    if len(hook) > 160:
        hook = hook[:157] + "…"

    # Persist machine results for future runs (only if we produced CJK and id was unmapped)
    if sid not in SKILLS_ZH and has_cjk(title) and has_cjk(summary):
        persist_skills_zh(sid, {
            "title": title,
            "summary": summary,
            "hook": hook,
            "category": category,
        })
    return {"title": title, "summary": summary, "hook": hook, "category": category}


def normalize(story: dict[str, Any], today: str) -> dict[str, Any] | None:
    sid = str(story.get("id") or "")
    if not sid or sid in SKIP_IDS:
        return None
    channel = story.get("_channel") or "ai"
    url = story.get("url") or ("https://x.com/i/trending/" + sid if not sid.startswith("gh-") else "")
    if not url:
        return None
    pre_raw = story.get("_pretranslated")
    pre = pre_raw if isinstance(pre_raw, dict) else {}
    pre_ready = bool(pre_raw)  # True flag or non-empty dict → already Chinese
    zh = ZH_MAP.get(sid, {})
    en_title = (story.get("name") or story.get("title") or "").strip()
    en_sum = (story.get("summary") or story.get("hook") or "").strip()

    skills_zh_fields = None
    if channel == "skills":
        # 技能栏：精选表 / ZH_MAP / 预翻译 / 机翻 → 标题·摘要·钩子一律中文
        en_hook = (story.get("hook") or "").strip()
        skills_zh_fields = translate_skills_fields(
            sid,
            en_title,
            en_sum or (story.get("summary") or ""),
            en_hook,
            story.get("category"),
        )

    if pre.get("title"):
        title = pre["title"]
    elif pre_ready and story.get("title"):
        title = str(story.get("title")).strip()
    elif channel == "skills" and skills_zh_fields:
        title = skills_zh_fields["title"]
    elif zh.get("title"):
        title = zh["title"]
    elif channel == "github":
        title = en_title  # keep owner/repo
    else:
        title = (("[EN] " + en_title) if en_title else "未命名热点")

    if channel == "github":
        # 说明一律中文：预翻译 > 精选表 > 已是中文 > 可选机翻 > [EN] 原文
        summary = pre.get("summary") or translate_github_summary(en_title, en_sum or (story.get("summary") or ""))
        if len(summary) > 220:
            summary = summary[:217] + "…"
    elif channel == "skills" and skills_zh_fields:
        summary = pre.get("summary") or skills_zh_fields["summary"]
    elif pre.get("summary"):
        summary = pre["summary"]
    elif pre_ready and story.get("summary"):
        summary = str(story.get("summary")).strip()
        if len(summary) > 280:
            summary = summary[:277] + "…"
    elif zh.get("summary"):
        summary = zh["summary"]
    else:
        summary = en_sum
        if len(summary) > 180:
            summary = summary[:177] + "…"
        if summary and not summary.startswith("[EN]"):
            if not any("一" <= c <= "鿿" for c in summary):
                summary = "[EN] " + summary

    published = to_sh_iso(story.get("updated_at") or story.get("published_at"))
    cat = pre.get("category") or zh.get("category") or story.get("category") or default_category(channel)
    if channel == "github":
        cat = "GitHub"
    elif channel == "skills" and skills_zh_fields:
        cat = skills_zh_fields.get("category") or skills_category_zh(cat)
    topics = []
    ctx = story.get("contexts") or {}
    if isinstance(ctx, dict):
        topics = ctx.get("topics") or []
    item = {
        "id": sid,
        "title": title,
        "summary": summary,
        "url": url,
        "source": story.get("source") or ("GitHub" if channel == "github" else "X News"),
        "author": (
            "GitHub Trending" if channel == "github" else
            (story.get("source") or story.get("author") or (
                "论文" if channel == "papers" else
                "模型榜" if channel == "models" else
                "AI技能" if channel == "skills" else
                "X Trending"
            ))
        ),
        "published_at": published,
        "date": date_key(published, today),
        "metrics": {},
        "category": cat,
        "topics": topics,
        "hook": (
            github_hook_zh(story.get("period"), story.get("stars_today"), story.get("language"))
            if channel == "github"
            else (
                (skills_zh_fields.get("hook") if skills_zh_fields else None)
                or (story.get("hook") or "")
            )
        ),
        "disclaimer": (
            "本条为 X 帖摘要，可能随讨论演变，请自行核实。"
            if channel == "skills"
            else (story.get("disclaimer") or "")
        ),
        "channel": channel,
    }
    if channel == "github":
        item["language"] = story.get("language") or ""
        item["stars"] = int(story.get("stars") or 0)
        item["forks"] = int(story.get("forks") or 0)
        item["rank"] = story.get("rank")
        item["period"] = story.get("period") or "daily"
        item["stars_today"] = int(story.get("stars_today") or 0)
        item["metrics"] = {
            "stars": item["stars"],
            "forks": item["forks"],
            "stars_today": item["stars_today"],
            "rank": item["rank"],
            "period": item["period"],
            "language": item["language"],
        }
    if channel == "papers":
        for k in ("origin_title", "paper_id", "arxiv_id", "alphaxiv_url", "arxiv_url"):
            if story.get(k) is not None:
                item[k] = story.get(k)
        if story.get("metrics"):
            item["metrics"] = story.get("metrics") or {}
    if channel == "models":
        for k in ("origin_title", "arena_score", "aa_quality", "aa_speed", "aa_price", "aa_latency", "rank"):
            if story.get(k) is not None:
                item[k] = story.get(k)
        if story.get("metrics"):
            item["metrics"] = story.get("metrics") or {}
    # preserve explicit source from primary feeds
    if story.get("source"):
        item["source"] = story.get("source")
    if story.get("author"):
        item["author"] = story.get("author")
    if story.get("origin_title") and channel == "ai":
        item["origin_title"] = story.get("origin_title")
    return item


def merge_history(new_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text(encoding="utf-8"))
            for it in old.get("items") or []:
                if it.get("id"):
                    if not it.get("channel"):
                        it = dict(it)
                        it["channel"] = "ai"
                    by_id[it["id"]] = it
        except Exception:
            pass
    for it in new_items:
        by_id[it["id"]] = it
    items = list(by_id.values())

    def sort_key(x: dict[str, Any]):
        # github: rank then stars; others by time
        if x.get("channel") == "github":
            period_w = {"daily": 0, "weekly": 1, "popular": 2}.get(x.get("period") or "", 9)
            return (period_w, x.get("rank") or 9999, -(x.get("stars") or 0))
        return (0, 0, 0)  # placeholder

    # Separate sort: non-github by time desc, github by rank
    non_gh = [x for x in items if x.get("channel") != "github"]
    gh = [x for x in items if x.get("channel") == "github"]
    non_gh.sort(key=lambda x: x.get("published_at") or x.get("date") or "", reverse=True)
    gh.sort(key=lambda x: (
        {"daily": 0, "weekly": 1, "popular": 2}.get(x.get("period") or "", 9),
        x.get("rank") or 9999,
        -(x.get("stars") or 0),
    ))
    items = non_gh + gh
    cutoff = (now_sh() - timedelta(days=14)).strftime("%Y-%m-%d")
    items = [x for x in items if (x.get("date") or "9999") >= cutoff or x.get("channel") in ("github", "models", "papers", "skills")]
    return items


def build_days(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[str, list] = {}
    for it in items:
        d = it.get("date") or "未知日期"
        buckets.setdefault(d, []).append(it)
    days = []
    for d in sorted(buckets.keys(), reverse=True):
        days.append({"date": d, "count": len(buckets[d]), "ids": [x["id"] for x in buckets[d]]})
    return days


def main() -> int:
    # Refresh primary sources (smol/Batch/HF/arXiv/AA/LMArena) before merging raw/
    import os
    if os.environ.get("SKIP_PRIMARY_INGEST") == "1":
        print("跳过 ingest_primary（SKIP_PRIMARY_INGEST=1）")
    else:
        try:
            from ingest_primary import main as ingest_primary_main
            ingest_primary_main()
        except Exception as e:
            print(f"ingest_primary 跳过/失败: {e}")
    today = now_sh().strftime("%Y-%m-%d")
    stories = load_raw_stories()
    print(f"raw 故事数: {len(stories)}")
    seen_url: set[str] = set()
    seen_id: set[str] = set()
    fresh: list[dict[str, Any]] = []
    fresh_idx: dict[str, int] = {}
    for s in stories:
        sid = str(s.get("id"))
        item = normalize(s, today)
        if not item:
            continue
        ch = item.get("channel") or "ai"
        u = item["url"]
        # 技能频道可从 ai/world/startup 夺回同一 X story id（技能栏优先展示）
        if sid in seen_id:
            if ch == "skills" and sid in fresh_idx:
                prev = fresh[fresh_idx[sid]]
                if prev.get("channel") != "skills":
                    fresh[fresh_idx[sid]] = item
            continue
        # models/papers may share a leaderboard host; keep unique ids (fragment URLs preferred)
        if ch in ("models", "papers", "github"):
            pass
        elif u in seen_url and ch != "skills":
            continue
        seen_id.add(sid)
        seen_url.add(u)
        fresh_idx[sid] = len(fresh)
        fresh.append(item)

    if not fresh and not OUT.exists():
        payload = {
            "generated_at": now_sh().strftime("%Y-%m-%d %H:%M:%S %z").replace("+0800", "+08:00"),
            "timezone": "Asia/Shanghai",
            "source": "x.search_news+github+papers+models+skills+primary",
            "item_count": 0,
            "ai_count": 0,
            "world_count": 0,
            "startup_count": 0,
            "github_count": 0,
            "papers_count": 0,
            "models_count": 0,
            "skills_count": 0,
            "days": [],
            "items": [],
            "note": "今日尚未抓到数据；下拉刷新或等待日更任务。",
        }
        OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print("写出空 data.json（友好空状态）")
        return 0

    # Prefer rebuilding from fresh raw this run (includes AI export)
    items = merge_history(fresh) if fresh else merge_history([])
    if not fresh and OUT.exists():
        print("raw 无新条目，保留现有 data.json")
        return 0

    # Ensure channel on all
    for it in items:
        if not it.get("channel"):
            it["channel"] = "ai"

    gen = now_sh().strftime("%Y-%m-%d %H:%M:%S %z").replace("+0800", "+08:00")
    def cnt(ch): return sum(1 for x in items if x.get("channel") == ch)
    payload = {
        "generated_at": gen,
        "generated": gen,
        "timezone": "Asia/Shanghai",
        "source": "x.search_news+github+papers+models+skills+primary",
        "item_count": len(items),
        "fresh_count": len(fresh),
        "ai_count": cnt("ai"),
        "world_count": cnt("world"),
        "startup_count": cnt("startup"),
        "github_count": cnt("github"),
        "papers_count": cnt("papers"),
        "models_count": cnt("models"),
        "skills_count": cnt("skills"),
        "days": build_days(items),
        "items": items,
        "remote_urls": [
            "https://raw.githubusercontent.com/tianshanhangui89-glitch/niceo-ai-news/main/data.json",
            "https://cdn.jsdelivr.net/gh/tianshanhangui89-glitch/niceo-ai-news@main/data.json",
        ],
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    OUT.write_text(text, encoding="utf-8")
    for dest in [ROOT / "github-publish" / "data.json", ROOT / "app" / "data.json"]:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
    print(f"写出 {OUT} ：共 {len(items)} 条（本轮 {len(fresh)}） ai={cnt('ai')} world={cnt('world')} startup={cnt('startup')} github={cnt('github')} papers={cnt('papers')} models={cnt('models')} skills={cnt('skills')}")
    for ch in ("world", "startup", "github", "papers", "models", "skills", "ai"):
        print(f"--- {ch} ---")
        for it in [x for x in fresh if x.get("channel") == ch][:5]:
            print(" -", it["title"][:80])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
