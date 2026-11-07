#!/usr/bin/env python3
"""Fetch primary AI sources into raw/YYYY-MM-DD-{ai-smol,ai-batch,papers-*,models-*}.json.

Sources (from @khyssabc 一手清单):
  - news.smol.ai / latent.space AI News → channel ai
  - The Batch (deeplearning.ai) → channel ai
  - Hugging Face Daily Papers + arXiv cs.AI/LG/CL → channel papers (+ alphaXiv URL)
  - LMArena (HF elo snapshot) + Artificial Analysis → channel models

Called by fetch_news.py at start of main so the daily path refreshes them.
"""
from __future__ import annotations

import csv
import html as H
import io
import json
import pickle
import re
import ssl
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
SH = timezone(timedelta(hours=8))
UA = {"User-Agent": "Mozilla/5.0 (compatible; NiceoAINews/1.2; +https://github.com/tianshanhangui89-glitch/Niceo-ai-news)"}
CTX = ssl.create_default_context()

ARENA_PKL = (
    "https://huggingface.co/spaces/lmarena-ai/lmarena-leaderboard/"
    "resolve/main/elo_results_20250829.pkl"
)
ARENA_SNAP = "2025-08-29"


def now_sh() -> datetime:
    return datetime.now(SH)


def today() -> str:
    return now_sh().strftime("%Y-%m-%d")


def iso_now() -> str:
    return now_sh().strftime("%Y-%m-%dT%H:%M:%S.000+08:00")


def fetch(url: str, timeout: int = 45) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        return r.read()


def slug(s: str, n: int = 72) -> str:
    s = re.sub(r"[^a-zA-Z0-9._+-]+", "-", (s or "").strip()).strip("-")
    return s[:n] or "x"


def write_raw(prefix: str, channel: str, items: list[dict], meta: dict | None = None) -> Path:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"{today()}-{prefix}.json"
    payload = {
        "fetched_at": iso_now(),
        "channel": channel,
        "data": items,
    }
    if meta:
        payload["meta"] = meta
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  wrote {path.name} n={len(items)}")
    return path


def ingest_smol() -> tuple[int, str]:
    html = fetch("https://news.smol.ai").decode("utf-8", "replace")
    items_raw: list[dict] = []
    for s in re.findall(r"<script[^>]*>(.*?)</script>", html, re.S):
        if '"items"' not in s or "ainews" not in s:
            continue
        try:
            d = json.loads(s)
            items_raw = (d.get("initial") or {}).get("items") or d.get("items") or []
            if items_raw:
                break
        except json.JSONDecodeError:
            continue
    if not items_raw:
        hrefs = sorted(set(re.findall(r'href="(/p/ainews-[^"#?]+)"', html)))
        items_raw = [{"slug": h.rstrip("/").split("/")[-1], "title": h.rstrip("/").split("/")[-1], "web_url": f"https://news.latent.space{h}"} for h in hrefs]

    out = []
    for it in items_raw[:40]:
        slug_s = it.get("slug") or ""
        title = (it.get("title") or slug_s).strip()
        title = re.sub(r"^\[AINews\]\s*", "", title)
        url = f"https://news.latent.space/p/{slug_s}/" if slug_s else (it.get("web_url") or it.get("url") or it.get("sourceUrl") or "")
        if not url.startswith("http"):
            url = "https://news.latent.space" + (url if url.startswith("/") else f"/p/{url}")
        published = it.get("date") or it.get("published_at") or it.get("modifiedAt") or iso_now()
        if isinstance(published, (int, float)):
            published = datetime.fromtimestamp(published, tz=timezone.utc).isoformat()
        oid = "smol-" + slug(slug_s or title)
        out.append({
            "id": oid,
            "name": title,
            "title": f"【一手】{title}",
            "origin_title": title,
            "summary": f"来源：news.smol.ai / Latent Space AI News 日更。原题：{title}",
            "url": url,
            "updated_at": published,
            "category": "一手简报",
            "contexts": {"topics": ["smol.ai", "Latent Space"]},
            "hook": "一手简报 · smol.ai",
            "disclaimer": "一手简报摘要，请点原文核实。",
            "source": "smol.ai",
            "_channel": "ai",
            "_pretranslated": True,
        })
    write_raw("ai-smol", "ai", out, {"source": "https://news.smol.ai"})
    return len(out), "https://news.smol.ai"


def ingest_batch() -> tuple[int, str]:
    html = fetch("https://www.deeplearning.ai/the-batch/").decode("utf-8", "replace")
    issues = sorted({int(x) for x in re.findall(r"/the-batch/issue-(\d+)/?", html)}, reverse=True)
    out = []
    for num in issues[:9]:
        url = f"https://www.deeplearning.ai/the-batch/issue-{num}/"
        title_en = f"The Batch Issue {num}"
        # try to pull title from listing card
        m = re.search(rf'issue-{num}/[^>]*>\s*([^<]{{12,180}})\s*<', html)
        if m:
            title_en = H.unescape(m.group(1)).strip()
        # rough date: weekly; leave none → fetch_news uses today; set relative guess from issue order
        # Issue 377 ≈ 2026-10-30 from prior ingest
        out.append({
            "id": f"batch-issue-{num}",
            "name": title_en,
            "title": f"《The Batch》第 {num} 期",
            "origin_title": title_en,
            "summary": f"Andrew Ng 团队周报（Issue {num}）。原题：{title_en}。请打开原文阅读 Data Points / ML Research。",
            "url": url,
            "updated_at": None,
            "author": "Andrew Ng / DeepLearning.AI",
            "category": "一周精选",
            "contexts": {"topics": ["The Batch", "Andrew Ng"]},
            "hook": "Andrew Ng / DeepLearning.AI 周报",
            "disclaimer": "周报摘要，请点原文核实。",
            "source": "The Batch",
            "_channel": "ai",
            "_pretranslated": True,
        })
    # stamp dates for the newest few based on weekly cadence ending ~2026-10-30 for 377
    if out:
        # find max issue
        base_issue = max(int(x["id"].split("-")[-1]) for x in out)
        base_date = datetime(2026, 10, 30, 12, 0, tzinfo=SH)
        for it in out:
            n = int(it["id"].split("-")[-1])
            d = base_date - timedelta(weeks=base_issue - n)
            it["updated_at"] = d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    write_raw("ai-batch", "ai", out, {"source": "https://www.deeplearning.ai/the-batch/"})
    return len(out), "https://www.deeplearning.ai/the-batch/"


def ingest_hf_papers() -> list[dict]:
    data = json.loads(fetch("https://huggingface.co/api/daily_papers"))
    out = []
    for it in data[:40]:
        paper = it.get("paper") or {}
        pid = paper.get("id") or it.get("title") or ""
        title = (paper.get("title") or it.get("title") or pid).strip()
        summary = (paper.get("ai_summary") or paper.get("summary") or it.get("summary") or "").strip()
        summary = re.sub(r"\s+", " ", summary)[:400]
        authors = ", ".join(
            (a.get("name") if isinstance(a, dict) else str(a))
            for a in (paper.get("authors") or [])[:6]
        )
        published = paper.get("publishedAt") or it.get("publishedAt") or iso_now()
        arxiv_id = pid
        url = f"https://huggingface.co/papers/{pid}"
        abs_url = f"https://arxiv.org/abs/{arxiv_id}" if re.match(r"^\d{4}\.\d+", str(arxiv_id)) else url
        alpha = f"https://www.alphaxiv.org/abs/{arxiv_id}" if re.match(r"^\d{4}\.\d+", str(arxiv_id)) else None
        out.append({
            "id": f"hf-{slug(str(pid))}",
            "name": title,
            "title": f"论文｜{title}",
            "origin_title": title,
            "summary": f"来源：Hugging Face Daily Papers（社区投票）。原题「{title}」。{('AI 摘要：'+summary) if summary else ''}",
            "url": abs_url if abs_url.startswith("https://arxiv.org") else url,
            "arxiv_url": abs_url if "arxiv.org" in abs_url else None,
            "updated_at": published,
            "author": authors or None,
            "category": "HF Daily Papers",
            "contexts": {"topics": ["huggingface", "daily-papers"]},
            "hook": "HF 日更论文 · 可开 alphaXiv 讨论" if alpha else "HF 日更论文",
            "disclaimer": "预印本/社区摘要，请点原文核实。",
            "source": "Hugging Face",
            "paper_id": str(pid),
            "arxiv_id": str(arxiv_id) if re.match(r"^\d{4}\.\d+", str(arxiv_id)) else None,
            "alphaxiv_url": alpha,
            "_channel": "papers",
            "_pretranslated": True,
        })
    return out


def ingest_arxiv(cats: list[str] | None = None) -> list[dict]:
    cats = cats or ["cs.AI", "cs.LG", "cs.CL"]
    out = []
    seen = set()
    for cat in cats:
        q = (
            "https://export.arxiv.org/api/query?"
            f"search_query=cat:{cat}&start=0&max_results=20"
            "&sortBy=submittedDate&sortOrder=descending"
        )
        xml = fetch(q).decode("utf-8", "replace")
        root = ET.fromstring(xml)
        ns = {"a": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("a:entry", ns):
            eid = (entry.findtext("a:id", default="", namespaces=ns) or "")
            m = re.search(r"arxiv\.org/abs/([0-9.]+)", eid)
            arxiv_id = m.group(1) if m else ""
            if not arxiv_id or arxiv_id in seen:
                continue
            seen.add(arxiv_id)
            title = re.sub(r"\s+", " ", (entry.findtext("a:title", default="", namespaces=ns) or "").strip())
            summary = re.sub(r"\s+", " ", (entry.findtext("a:summary", default="", namespaces=ns) or "").strip())[:400]
            published = entry.findtext("a:published", default="", namespaces=ns)
            authors = ", ".join(
                (a.findtext("a:name", default="", namespaces=ns) or "")
                for a in entry.findall("a:author", ns)[:6]
            )
            alpha = f"https://www.alphaxiv.org/abs/{arxiv_id}"
            out.append({
                "id": f"arxiv-{arxiv_id}",
                "name": title,
                "title": f"论文｜{title}",
                "origin_title": title,
                "summary": f"来源：arXiv {cat}。原题「{title}」。英文摘要：{summary}…",
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "arxiv_url": f"https://arxiv.org/abs/{arxiv_id}",
                "updated_at": published,
                "author": authors or None,
                "category": cat,
                "contexts": {"topics": ["arxiv", cat]},
                "hook": f"arXiv {cat} · 可开 alphaXiv 讨论",
                "disclaimer": "预印本，未经同行评审；请点原文核实。",
                "source": "arXiv",
                "paper_id": arxiv_id,
                "arxiv_id": arxiv_id,
                "alphaxiv_url": alpha,
                "_channel": "papers",
                "_pretranslated": True,
            })
    return out


def ingest_papers() -> tuple[int, str]:
    hf = ingest_hf_papers()
    ax = ingest_arxiv()
    # prefer HF first, then arxiv not already present
    seen = {x.get("arxiv_id") or x.get("paper_id") for x in hf}
    merged = list(hf)
    for it in ax:
        if it.get("arxiv_id") in seen:
            continue
        merged.append(it)
        seen.add(it.get("arxiv_id"))
    write_raw("papers-hf-arxiv", "papers", merged, {
        "hf": "https://huggingface.co/api/daily_papers",
        "arxiv": "https://export.arxiv.org/api/query",
        "alphaxiv_pattern": "https://www.alphaxiv.org/abs/<id>",
    })
    return len(merged), "hf+arxiv"


def ingest_aa() -> list[dict]:
    html = fetch("https://artificialanalysis.ai/leaderboards/models", timeout=90).decode("utf-8", "replace")
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S)
    out = []
    rank = 0
    for r in rows:
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)
        texts = [H.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c))).strip() for c in cells]
        if len(texts) < 6:
            continue
        name = texts[0]
        # skip header
        if not name or name.lower() in ("model", "models") or "Intelligence" in name:
            continue
        # expect: name, context, org, quality, price, speed, latency, ...
        context = texts[1] if len(texts) > 1 else ""
        org = texts[2] if len(texts) > 2 else ""
        quality_s = texts[3] if len(texts) > 3 else ""
        price = texts[4] if len(texts) > 4 else ""
        speed = texts[5] if len(texts) > 5 else ""
        latency = texts[6] if len(texts) > 6 else ""
        try:
            quality = float(quality_s)
        except ValueError:
            continue
        rank += 1
        if rank > 40:
            break
        frag = slug(name)
        out.append({
            "id": f"aa-{frag}",
            "name": name,
            "title": name,
            "origin_title": name,
            "summary": (
                f"Artificial Analysis 公开榜：智能指数 {quality}，任务成本 {price}，"
                f"任务耗时 {speed} 分钟，首 token 延迟 {latency} 秒。厂商：{org or '—'}。"
            ),
            "url": f"https://artificialanalysis.ai/leaderboards/models#{frag}",
            "updated_at": iso_now(),
            "author": org or None,
            "category": "Artificial Analysis",
            "contexts": {"topics": ["leaderboard", "benchmark"]},
            "hook": f"智能指数 {quality} · {org}" if org else f"智能指数 {quality}",
            "disclaimer": "榜单数字取自公开页快照，可能随站点更新变化。",
            "source": "Artificial Analysis",
            "aa_quality": quality,
            "aa_price": price,
            "aa_speed": speed,
            "aa_latency": latency,
            "rank": rank,
            "metrics": {"aa_quality": quality, "aa_price": price, "aa_speed": speed, "context": context},
            "_channel": "models",
            "_pretranslated": True,
        })
    return out


def ingest_arena() -> list[dict]:
    class FigStub:
        def __init__(self, *a, **k):
            pass

        def __setstate__(self, state):
            if isinstance(state, dict):
                self.__dict__.update(state)
            else:
                self._state = state

    def make_stub(name):
        return type(name, (), {
            "__init__": lambda self, *a, **k: None,
            "__setstate__": lambda self, s: setattr(self, "_s", s),
            "__call__": lambda self, *a, **k: self,
        })

    class U(pickle.Unpickler):
        def find_class(self, module, name):
            if module.startswith("plotly"):
                if name == "Figure":
                    return FigStub
                return make_stub(name)
            return super().find_class(module, name)

    blob = fetch(ARENA_PKL, timeout=120)
    obj = U(io.BytesIO(blob)).load()
    df = obj["text"]["full"]["leaderboard_table_df"]
    # df index = model name
    out = []
    df2 = df.sort_values("rating", ascending=False).head(25)
    for i, (name, row) in enumerate(df2.iterrows(), 1):
        score = float(row["rating"])
        battles = int(row["num_battles"]) if "num_battles" in row else None
        ranking = int(row["final_ranking"]) if "final_ranking" in row else i
        frag = slug(str(name))
        out.append({
            "id": f"arena-{frag}",
            "name": str(name),
            "title": str(name),
            "origin_title": str(name),
            "summary": (
                f"LMArena 文本对战公开快照（HF 空间 {ARENA_SNAP}）："
                f"Arena Score {score:.1f}，排名 #{ranking}"
                + (f"，约 {battles} 场对战。" if battles else "。")
                + "实时榜请打开 lmarena.ai / arena.ai。"
            ),
            "url": f"https://lmarena.ai/#{frag}",
            "updated_at": f"{ARENA_SNAP}T00:00:00.000Z",
            "category": "LMArena",
            "contexts": {"topics": ["LMArena", "elo"]},
            "hook": f"Arena Score {score:.0f} · #{ranking}",
            "disclaimer": f"公开 Elo 快照 {ARENA_SNAP}，非实时；请点榜单核实。",
            "source": "LMArena",
            "arena_score": score,
            "rank": ranking,
            "metrics": {"arena_score": score, "rank": ranking, "votes": battles, "snapshot": ARENA_SNAP},
            "_channel": "models",
            "_pretranslated": True,
        })
    return out


def ingest_models() -> tuple[int, str]:
    aa = []
    last_err = None
    for attempt in range(3):
        try:
            aa = ingest_aa()
            break
        except Exception as e:
            last_err = e
            print(f"  AA attempt {attempt+1} failed: {e}")
    if not aa and last_err:
        print(f"  AA failed; trying reuse")
        for pth in sorted(RAW.glob("*-models-*.json"), reverse=True):
            try:
                d = json.loads(pth.read_text(encoding="utf-8"))
                aa = [x for x in (d.get("data") or []) if x.get("source") == "Artificial Analysis"]
                if aa:
                    print(f"  reused {len(aa)} AA from {pth.name}")
                    break
            except Exception:
                continue
    try:
        arena = ingest_arena()
    except Exception as e:
        print(f"  LMArena pickle failed: {e}; keeping prior arena items if any")
        arena = []
        # reuse from existing raw
        for p in sorted(RAW.glob("*-models-*.json"), reverse=True):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                arena = [x for x in (d.get("data") or []) if x.get("source") == "LMArena"]
                if arena:
                    print(f"  reused {len(arena)} arena from {p.name}")
                    break
            except Exception:
                continue
    merged = aa + arena
    write_raw("models-aa-arena", "models", merged, {
        "aa": "https://artificialanalysis.ai/leaderboards/models",
        "arena": ARENA_PKL,
        "arena_snapshot": ARENA_SNAP,
    })
    return len(merged), "aa+arena"


def main() -> int:
    print(f"[ingest_primary] {today()}")
    status: dict[str, Any] = {}
    for name, fn in [
        ("smol.ai", ingest_smol),
        ("The Batch", ingest_batch),
        ("papers", ingest_papers),
        ("models", ingest_models),
    ]:
        try:
            n, url = fn()
            status[name] = {"ok": n, "url": url}
        except Exception as e:
            status[name] = {"ok": 0, "error": f"{type(e).__name__}: {e}"}
            print(f"  FAIL {name}: {e}")
    status["alphaXiv"] = {"ok": "url_pattern", "note": "https://www.alphaxiv.org/abs/<id>"}
    meta_path = RAW / "PRIMARY_SOURCES_META.json"
    meta_path.write_text(json.dumps({"sources": status, "fetched_at": iso_now()}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("meta", status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
