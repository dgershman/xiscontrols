"""Extract the product catalog from the legacy xiscontrols.com index.html.

Usage: python3 -I parse.py <site_root> <out.json>
"""
import json, re, sys, os
from urllib.parse import unquote
from bs4 import BeautifulSoup, NavigableString

root, OUTFILE = sys.argv[1], sys.argv[2]
html = open(os.path.join(root, "index.html"), encoding="latin-1").read()
soup = BeautifulSoup(html, "lxml")

CAT_NAMES = {
    "boards": "Boards, Controllers & PLCs",
    "relays": "Relays",
    "solenoids": "Solenoids",
    "springs": "Springs",
    "microswitches": "Microswitches & Sensors",
    "counters": "Counters",
    "lamps": "Lamps, Switches & Enclosures",
    "power": "Power Supply Parts",
    "shocks": "Shock Absorbers & Speed Control",
    "bearings": "Bearings & Cams",
    "pawls": "Pawls, Linkages & Hardware",
    "assby": "Assemblies",
    "UsedTurnstiles": "Used Turnstiles",
    "gates": "Gates",
    "tools": "Tools",
    "bargain": "Bargain Bin",
}

# Decorative / status images that are not product photos
STATUS_IMG = {
    "sold out": "sold-out", "soldout": "sold-out", "out of stock": "out-of-stock",
    "backorder": "backorder", "back order": "backorder", "coming soon": "coming-soon",
    "special order": "special-order", "new": None, "reduced": "reduced",
}
ICON_HINTS = ["attention", "best choice", "top button", "sold out", "out of stock",
              "coming soon", "new.gif", "hot.gif", "finger", "arrow", "info ding",
              "lightbulb", "mag glass", "reduced", "special order", "back order",
              "backorder", "policy", "click", "pdf", "manual", "icon", "button"]


def norm_src(src):
    src = unquote(src or "").strip()
    src = re.sub(r"^https?://(www\.)?xiscontrols\.com/", "", src, flags=re.I)
    src = src.lstrip("/")
    return src


def text_of(el):
    t = el.get_text(" ", strip=True)
    t = t.replace("\xa0", " ")
    return re.sub(r"\s+", " ", t).strip()


def paragraphs(cell):
    """Return list of paragraph strings in reading order."""
    out = []
    blocks = cell.find_all(["p", "li"])
    if not blocks:
        t = text_of(cell)
        return [t] if t else []
    seen = set()
    for b in blocks:
        if b.find(["p"]):  # skip wrappers that contain other paragraphs
            continue
        t = text_of(b)
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    # catch loose text not in <p>
    if not out:
        t = text_of(cell)
        if t:
            out.append(t)
    return out


def classify_img(src):
    low = src.lower()
    base = os.path.basename(low)
    for k, v in STATUS_IMG.items():
        if k in base:
            return ("status", v)
    if "best choice" in base or "best%20choice" in base:
        return ("badge", "best-choice")
    if any(h in base for h in ICON_HINTS):
        return ("icon", None)
    return ("photo", None)


PRICE_RE = re.compile(r"\$\s*([\d,]+(?:\.\d{1,2})?)")

cat_anchor_names = set(CAT_NAMES)
products = []
current = None
row_index = 0

def top_rows(table):
    rows = []
    for child in table.children:
        if getattr(child, "name", None) == "tr":
            rows.append(child)
        elif getattr(child, "name", None) in ("tbody", "thead"):
            rows.extend(c for c in child.children if getattr(c, "name", None) == "tr")
    return rows

catalog_tables = []
for t in soup.find_all("table"):
    for r in top_rows(t):
        a = r.find("a", attrs={"name": True})
        if a and a["name"] in cat_anchor_names and a.find_parent("table") is t:
            catalog_tables.append(t)
            break

all_rows = []
for t in catalog_tables:
    carry = {}  # col index -> [cell, remaining]
    for tr in top_rows(t):
        cells = tr.find_all("td", recursive=False)
        grid = []
        ci = 0
        it = iter(cells)
        pending = list(cells)
        col = 0
        out = []
        while pending or any(k >= col for k in carry):
            if col in carry and carry[col][1] > 0:
                out.append(carry[col][0])
                carry[col][1] -= 1
                if carry[col][1] == 0:
                    del carry[col]
                col += 1
                continue
            if not pending:
                break
            c = pending.pop(0)
            rs = int(c.get("rowspan", 1) or 1)
            cs = int(c.get("colspan", 1) or 1)
            for k in range(cs):
                out.append(c)
                if rs > 1:
                    carry[col] = [c, rs - 1]
                col += 1
        all_rows.append((tr, out))

for tr, tds in all_rows:
    a = tr.find("a", attrs={"name": True})
    if a and a["name"] in cat_anchor_names:
        current = a["name"]
        CAT_NOTES = globals().setdefault("CAT_NOTES", {})
        CAT_NOTES[current] = text_of(tr)
        continue
    if current is None:
        continue
    # collapse duplicate colspan cells
    uniq = []
    for c in tds:
        if not uniq or uniq[-1] is not c:
            uniq.append(c)
    if len(uniq) != 4:
        # also record non-product rows (jokes / banners) for review
        BANNERS = globals().setdefault("BANNERS", [])
        BANNERS.append({"category": current, "text": text_of(tr)[:400],
                        "images": [norm_src(i.get("src")) for i in tr.find_all("img")]})
        continue
    tds = uniq
    c_img, c_desc, c_pn, c_price = tds
    pn_lines = [l for l in paragraphs(c_pn) if l]
    pn_text = " / ".join(pn_lines).strip()
    price_text = text_of(c_price)
    if not pn_text and not price_text:
        continue
    row_index += 1

    images, status, badges, docs = [], [], [], []
    for cell in (c_img, c_desc, c_pn, c_price):
        for img in cell.find_all("img"):
            src = norm_src(img.get("src"))
            if not src:
                continue
            kind, val = classify_img(src)
            if kind == "status" and val:
                status.append(val)
            elif kind == "badge":
                badges.append(val)
            elif kind == "photo":
                if src not in images:
                    images.append(src)
    for cell in (c_img, c_desc, c_pn, c_price):
        for link in cell.find_all("a", href=True):
            href = link["href"].strip()
            if href.startswith("#") or href.lower().startswith("mailto:"):
                continue
            label = text_of(link)
            if not label:
                im = link.find("img")
                label = os.path.basename(norm_src(im.get("src"))) if im else ""
            docs.append({"href": norm_src(href) if "xiscontrols.com" in href.lower() or not re.match(r"^https?:", href, re.I) else href,
                         "label": label})

    desc_paras = paragraphs(c_desc)
    bold = [text_of(b) for b in c_desc.find_all("b") if text_of(b)]
    title = bold[0] if bold and len(bold[0]) < 120 else ""

    m = PRICE_RE.search(price_text.replace(" ", ""))
    price = float(m.group(1).replace(",", "")) if m else None

    lowtxt = (" ".join(desc_paras) + " " + price_text + " " + pn_text).lower()
    for phrase, st in [("sold out", "sold-out"), ("out of stock", "out-of-stock"),
                       ("out of production", "discontinued"), ("coming soon", "coming-soon"),
                       ("special order", "special-order"), ("back order", "backorder"),
                       ("backorder", "backorder"), ("call for", "call"),
                       ("limited supply", "limited"), ("limited quantit", "limited")]:
        if phrase in lowtxt and st not in status:
            status.append(st)

    products.append({
        "row": row_index,
        "category": current,
        "category_name": CAT_NAMES[current],
        "part_raw": pn_text,
        "price_raw": price_text,
        "price": price,
        "title": title,
        "paragraphs": desc_paras,
        "images": images,
        "status": status,
        "badges": badges,
        "docs": docs,
    })

json.dump({"categories": CAT_NAMES, "category_notes": globals().get("CAT_NOTES", {}), "banners": globals().get("BANNERS", []),
           "products": products}, open(OUTFILE, "w"), indent=1)
from collections import Counter
print(len(products), "rows")
print(Counter(p["category"] for p in products))
print("no price:", sum(1 for p in products if p["price"] is None))
print("no image:", sum(1 for p in products if not p["images"]))
