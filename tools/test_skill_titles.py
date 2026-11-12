#!/usr/bin/env python3
"""技能标题必须保持「技能名：一句话用途」，刷新不得写回推文。"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from fetch_news import (  # noqa: E402
    SKILLS_ZH,
    ensure_item_chinese,
    is_clean_skill_title,
    load_raw_stories,
    normalize,
    persist_skills_zh,
    resolve_skill_display_title,
)

# 改写前真实标题。这些字符串不得再作为展示标题。
BEFORE_TITLES = [
    "seo-party-skills ：连接OpenSEO获取数据：",
    "推出Shoutout ！ -您可以在网站上添加一个小按钮，为设计师提供信用< 3",
    "穴居人： https://t.co/ni1Olb3wvq",
    "humanizer：每天分享一个实用 Skill。",
    "Vercel Labs的代理浏览器允许AI代理一次驱动浏览器一个shell命令。快照将页面作为紧凑的可访问性树返回，每个元素",
    "ljg-card：把文字变成知识长图 / 白板 / 漫画",
    "gsap-skills：让 Claude Opus 5.5 一个人干完一整个动效工作室的活，差的就是这 20 个 GitHub 仓库👇",
    "这是f * cking wild。谷歌、Cloudflare、Obsidian的首席执行官和现在构建Claude Code的人都将他们的人工智能配置免费放在GitHub上",
]

CHANNEL_COUNTS = {
    "ai": 369,
    "world": 483,
    "startup": 172,
    "github": 60,
    "papers": 368,
    "models": 74,
    "skills": 157,
}


def _has_cjk(text: str) -> bool:
    return any("一" <= c <= "鿿" for c in text or "")


class SkillTitleTests(unittest.TestCase):
    def test_before_titles_are_rejected(self):
        for title in BEFORE_TITLES:
            self.assertFalse(is_clean_skill_title(title), title)

    def test_purpose_composition_and_rejection(self):
        composed = resolve_skill_display_title(
            {},
            {"skill_name": "ljg-card", "purpose": "把文字排成知识长图、白板或漫画"},
        )
        self.assertEqual(composed, "ljg-card：把文字排成知识长图、白板或漫画")
        self.assertEqual(
            resolve_skill_display_title(
                {"title": "demo：打开 https://t.co/abc 再安装"},
                {},
            ),
            "",
        )

    def test_map_and_data_titles_match(self):
        data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        skills = [it for it in data["items"] if it.get("channel") == "skills"]
        self.assertEqual(len(skills), 157)
        self.assertEqual(len(SKILLS_ZH), 157)
        self.assertEqual(data.get("skills_count"), 157)
        for it in skills:
            mapped = SKILLS_ZH[it["id"]]
            self.assertEqual(it["title"], mapped["title"])
            self.assertTrue(is_clean_skill_title(it["title"]), it["title"])
            self.assertTrue(it["title"].startswith(it.get("skill_name", "") + "："))
            self.assertNotIn("origin_title", it)
            self.assertNotIn("http", it["title"])
            self.assertNotIn("npx", it["title"].lower())
            self.assertNotIn("…", it["title"])
            self.assertTrue(it.get("url"))
            if it.get("repo"):
                self.assertTrue(it.get("github_url", "").startswith("https://github.com/"))
            if str(it.get("url", "")).find("x.com/") >= 0 and "/status/" in str(it.get("url")):
                self.assertEqual(it.get("x_url"), it["url"])

    def test_known_links_and_install_survive(self):
        data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        by_id = {it["id"]: it for it in data["items"] if it.get("channel") == "skills"}
        ljg = by_id["2119012866351411403"]
        self.assertEqual(ljg["title"], "ljg-card：把文字排成知识长图、白板或漫画")
        self.assertEqual(ljg["skill_name"], "ljg-card")
        self.assertEqual(ljg["install"], "npx skills add lijigang/ljg-skills --skill ljg-card")
        self.assertEqual(ljg["x_url"], "https://x.com/Morry4AI/status/2119012866351411403")
        self.assertEqual(ljg["github_url"], "https://github.com/lijigang/ljg-skills")
        self.assertIn("知识长图", ljg["source_title"])
        seo = by_id["2119929107077292486"]
        self.assertEqual(seo["title"], "seo-party-skills：连接OpenSEO获取数据")
        self.assertEqual(seo["github_url"], "https://github.com/every-app/seo-party-skills")
        self.assertIn("Connect OpenSEO", seo["source_title"])
        card = by_id["2119913201626443805"]
        self.assertEqual(card["title"], "floor-by-floor：把公司画成逐层大楼图")
        self.assertEqual(card["install"], "npx skills add glazec/floor-by-floor")
        caveman = by_id["2119912921732190366"]
        self.assertEqual(caveman["title"], "caveman：让Agent少说少读且代码仍准")
        self.assertEqual(caveman["repo"], "JuliusBrussee/caveman")
        human = by_id["2119823886976156152"]
        self.assertEqual(human["title"], "humanizer：删掉文本里的AI套话")

    def test_other_channels_stay_chinese(self):
        data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
        counts = {}
        for it in data["items"]:
            counts[it.get("channel") or "ai"] = counts.get(it.get("channel") or "ai", 0) + 1
        self.assertEqual(counts, CHANNEL_COUNTS)
        self.assertEqual(data.get("item_count"), 1683)
        for ch in ("ai", "world", "startup"):
            for it in data["items"]:
                if it.get("channel") == ch:
                    self.assertTrue(_has_cjk(it.get("title") or ""), it.get("id"))
                    self.assertFalse(str(it.get("title") or "").startswith("[EN]"))

    def test_refresh_uses_curated_title_not_tweet(self):
        seen = set()
        for story in load_raw_stories():
            if story.get("_channel") != "skills":
                continue
            sid = str(story.get("id"))
            if sid in seen or sid not in SKILLS_ZH:
                continue
            seen.add(sid)
            item = normalize(story, "2026-11-10")
            self.assertIsNotNone(item, sid)
            self.assertEqual(item["title"], SKILLS_ZH[sid]["title"])
            self.assertNotIn("origin_title", item)
            raw_head = (story.get("name") or story.get("title") or "").strip()
            if raw_head and raw_head != item["title"]:
                self.assertEqual(item.get("source_title"), raw_head)
        self.assertEqual(seen, set(SKILLS_ZH))

    def test_uncurated_tweet_is_dropped(self):
        story = {
            "id": "skill-title-test-uncurated",
            "name": "推出一个按钮给设计师信用",
            "title": "推出一个按钮给设计师信用",
            "summary": "这是一条推文，不是用途。npx skills add someone/demo",
            "hook": "具名可装",
            "url": "https://x.com/someone/status/1",
            "_channel": "skills",
            "skill_name": "demo",
            "install": "npx skills add someone/demo",
        }
        self.assertIsNone(normalize(story, "2026-11-10"))

    def test_clean_raw_title_is_kept_but_dirty_title_is_not_persisted(self):
        import fetch_news

        saved = fetch_news.persist_skills_zh
        calls = []
        fetch_news.persist_skills_zh = lambda *args, **kwargs: calls.append(args)
        try:
            story = {
                "id": "skill-title-test-clean-raw",
                "name": "demo-skill：把备注收成待办清单",
                "title": "demo-skill：把备注收成待办清单",
                "summary": "把零散备注收成一份待办清单。",
                "url": "https://x.com/someone/status/2",
                "_channel": "skills",
                "skill_name": "demo-skill",
                "install": "npx skills add someone/demo-skill",
            }
            item = normalize(story, "2026-11-10")
            self.assertEqual(item["title"], "demo-skill：把备注收成待办清单")
            self.assertEqual(calls[0][0], "skill-title-test-clean-raw")
            self.assertTrue(is_clean_skill_title(calls[0][1]["title"]))
        finally:
            fetch_news.persist_skills_zh = saved

        sid = "skill-title-test-should-not-persist"
        persist_skills_zh(sid, {"title": BEFORE_TITLES[0], "summary": "测试"})
        self.assertNotIn(sid, SKILLS_ZH)
        self.assertNotIn(sid, (ROOT / "tools" / "skills_zh_map.py").read_text(encoding="utf-8"))

    def test_history_item_is_rewritten_on_refresh(self):
        item = {
            "id": "2119929107077292486",
            "channel": "skills",
            "title": BEFORE_TITLES[0],
            "summary": "连接 OpenSEO 读取站点数据。",
            "hook": "具名可装",
            "category": "AI技能",
        }
        out = ensure_item_chinese(item)
        self.assertEqual(out["title"], "seo-party-skills：连接OpenSEO获取数据")
        self.assertEqual(out["source_title"], BEFORE_TITLES[0])
        ai = {
            "id": "ai-sample",
            "channel": "ai",
            "title": "中文标题保持不变",
            "summary": "中文摘要保持不变",
            "hook": "中文导语",
            "category": "动态",
        }
        kept = ensure_item_chinese(dict(ai))
        self.assertEqual(kept["title"], ai["title"])
        self.assertEqual(kept["summary"], ai["summary"])


if __name__ == "__main__":
    unittest.main()
