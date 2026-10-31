"""Extract The Library page into sections of documents and copy the files.
Usage: python3 -I library.py <site_root> <repo_root>
"""
import json, os, re, shutil, sys, unicodedata
from urllib.parse import unquote
from bs4 import BeautifulSoup

site, repo = sys.argv[1:3]
lib_dir = os.path.join(site, "Manuals")
soup = BeautifulSoup(open(os.path.join(lib_dir, "Library.htm"), encoding="latin-1").read(), "lxml")


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()


def copy(rel_from_manuals):
    rel = unquote(rel_from_manuals).replace("\\", "/")
    rel = re.sub(r"^https?://(www\.)?xiscontrols\.com/", "/", rel, flags=re.I)
    src = os.path.normpath(os.path.join(site, rel.lstrip("/")) if rel.startswith("/") else os.path.join(lib_dir, rel))
    if not os.path.isfile(src):
        return None
    relsite = os.path.relpath(src, site).split(os.sep)
    clean = [slugify(p) for p in relsite[:-1]]
    base, ext = os.path.splitext(relsite[-1])
    url = "/media/" + "/".join(clean + [slugify(base) + ext.lower()])
    dest = os.path.join(repo, "public", url.lstrip("/"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src, dest)
    return url


sections, current = [], None
for el in soup.body.descendants:
    if getattr(el, "name", None) == "a" and el.get("href"):
        href = el["href"]
        if href.startswith("#") or href.startswith("mailto"):
            continue
        label = re.sub(r"\s+", " ", el.get_text(" ", strip=True))
        if not label:
            continue
        url = copy(href)
        if url and current is not None:
            current["docs"].append({"label": label, "file": url})
    elif getattr(el, "name", None) in ("b", "strong"):
        t = re.sub(r"\s+", " ", el.get_text(" ", strip=True))
        if t and len(t) > 6 and not el.find_parent("a") and "Library" not in t and "XIS Controls" not in t:
            if current is None or current["docs"] or current["title"] != t:
                if current and not current["docs"]:
                    current["title"] = t
                    continue
                current = {"title": t, "note": "", "docs": []}
                sections.append(current)

sections = [s for s in sections if s["docs"]]
extra = []
for rel, label in [("Turnstile Bedfellows.pdf", "Strange Bedfellows: who bought whom in the turnstile business")]:
    u = copy("/" + rel)
    if u:
        extra.append({"label": label, "file": u})
if extra:
    sections.insert(0, {"title": "Industry history", "note": "", "docs": extra})
os.makedirs(os.path.join(repo, "src", "data"), exist_ok=True)
json.dump(sections, open(os.path.join(repo, "src", "data", "library.json"), "w"), indent=1)
for s in sections:
    print(s["title"], len(s["docs"]))
