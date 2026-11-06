#!/usr/bin/env python3
"""把 github-publish/ 推到 tianshanhangui89-glitch/niceo-ai-news。
令牌优先: VM_SERVICES_GITHUB_TOKEN / NOTES_GITHUB_TOKEN / SKILLMAP_GITHUB_TOKEN / NICEO_GIT_TOKEN / GITHUB_TOKEN。
新仓若 NOTES 等无 Contents 写入权限，会自动换下一个能推送的令牌。
大文件走 git clone+push；仓库不存在则尝试创建公开仓。
"""
import json, os, shutil, subprocess, sys, tempfile, time, urllib.request, urllib.error

REPO = os.environ.get("AINEWS_REPO", "tianshanhangui89-glitch/niceo-ai-news")
BRANCH = "main"
TOKEN_ENVS = (
    "VM_SERVICES_GITHUB_TOKEN",
    "NOTES_GITHUB_TOKEN",
    "SKILLMAP_GITHUB_TOKEN",
    "NICEO_GIT_TOKEN",
    "GITHUB_TOKEN",
)

def listed_tokens():
    seen = set()
    out = []
    for name in TOKEN_ENVS:
        tok = os.environ.get(name)
        if tok and tok not in seen:
            seen.add(tok)
            out.append((name, tok))
    return out

TOKENS = listed_tokens()
TOK = TOKENS[0][1] if TOKENS else None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "github-publish")
FILES = sys.argv[1:] or ["data.json", "index.html", "README.md"]

def api(method, url, body=None):
    req = urllib.request.Request(
        url, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": "Bearer " + TOK,
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "niceo-ai-news-publish",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read()).get("message")
        except Exception:
            msg = str(e)
        return e.code, {"message": msg}

if not TOK:
    print("错误：未设置 NOTES_GITHUB_TOKEN / SKILLMAP_GITHUB_TOKEN 等，已把文件留在 github-publish/", file=sys.stderr)
    sys.exit(2)

owner, name = REPO.split("/", 1)
st, info = api("GET", "https://api.github.com/repos/%s" % REPO)
if st == 404:
    print("仓库不存在，尝试创建公开仓库…")
    st2, info2 = api("POST", "https://api.github.com/user/repos", {
        "name": name,
        "description": "Niceo AI热点 · App 在线数据源（X AI / 时政 / 创业 / GitHub）",
        "private": False, "auto_init": True,
        "has_issues": False, "has_projects": False, "has_wiki": False,
    })
    if st2 not in (200, 201):
        print("创建失败 HTTP %s: %s" % (st2, info2.get("message")))
        open(os.path.join(HERE, "CREATE_REPO.md"), "w", encoding="utf-8").write(
            "# 请先创建空仓库\n\n请用账号创建公开仓 **%s**，然后重跑 publish.sh\n\n失败: HTTP %s %s\n"
            % (REPO, st2, info2.get("message"))
        )
        sys.exit(3)
    print("已创建:", info2.get("html_url"))
    time.sleep(2)
elif st != 200:
    print("无法访问仓库 HTTP %s %s" % (st, info.get("message")), file=sys.stderr)
    sys.exit(4)
else:
    print("仓库已存在:", info.get("html_url"))

tmp = tempfile.mkdtemp(prefix="ainews-publish-")
try:
    url = "https://x-access-token:%s@github.com/%s.git" % (TOK, REPO)
    try:
        subprocess.check_call(["git", "clone", "--depth", "1", "-b", BRANCH, url, "repo"], cwd=tmp)
    except subprocess.CalledProcessError:
        subprocess.check_call(["git", "clone", "--depth", "1", url, "repo"], cwd=tmp)
        repo = os.path.join(tmp, "repo")
        subprocess.call(["git", "checkout", "-B", BRANCH], cwd=repo)
    repo = os.path.join(tmp, "repo")
    changed = []
    for f in FILES:
        src = os.path.join(HERE, f)
        if not os.path.exists(src):
            print("跳过（不存在）:", f); continue
        dst = os.path.join(repo, f)
        os.makedirs(os.path.dirname(dst) or repo, exist_ok=True)
        shutil.copy2(src, dst)
        changed.append(f)
    subprocess.check_call(["git", "config", "user.email", "niceo@mail.grokbot.com"], cwd=repo)
    subprocess.check_call(["git", "config", "user.name", "Niceo"], cwd=repo)
    subprocess.check_call(["git", "add", "--"] + changed, cwd=repo)
    status = subprocess.check_output(["git", "status", "--porcelain"], cwd=repo, text=True).strip()
    if not status:
        print("未变化: 与远端一致")
    else:
        msg = "update ai-news %s" % time.strftime("%Y-%m-%d %H:%M")
        subprocess.check_call(["git", "commit", "-m", msg], cwd=repo)
        pushed = False
        last_err = None
        for name, tok in TOKENS:
            remote = "https://x-access-token:%s@github.com/%s.git" % (tok, REPO)
            subprocess.call(["git", "remote", "set-url", "origin", remote], cwd=repo)
            try:
                subprocess.check_call(["git", "push", "origin", "HEAD:%s" % BRANCH], cwd=repo)
                print("已推送(%s):" % name, ", ".join(changed))
                pushed = True
                break
            except subprocess.CalledProcessError as e:
                last_err = e
                print("推送失败(%s)，尝试下一令牌" % name)
        if not pushed:
            raise last_err or RuntimeError("no token could push")
    for f in changed:
        try:
            urllib.request.urlopen(
                "https://purge.jsdelivr.net/gh/%s@%s/%s" % (REPO, BRANCH, f), timeout=20
            ).read()
            print("已刷新 jsDelivr:", f)
        except Exception as e:
            print("jsDelivr 刷新失败(不影响 GitHub 源):", f, e)
    print("仓库: https://github.com/%s" % REPO)
    print("raw: https://raw.githubusercontent.com/%s/%s/data.json" % (REPO, BRANCH))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
