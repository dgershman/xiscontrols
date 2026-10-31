"""Turn raw.json rows into clean product records + copy referenced media.

Usage: python3 -I normalize.py <raw.json> <site_root> <repo_root>
Writes:
  <repo>/src/content/parts/<slug>.md   (one per product, YAML frontmatter + body)
  <repo>/public/media/...              (photos, drawings, PDFs actually referenced)
  <repo>/src/data/import-report.json
"""
import json, os, re, shutil, sys, unicodedata
from collections import Counter, defaultdict

raw_path, site, repo = sys.argv[1:4]
raw = json.load(open(raw_path))

BRANDS = [
    ("Robot", [r"\brobot\b"]),
    ("Burle", [r"\bburle\b", r"\bburl\b"]),
    ("Philips", [r"\bphilips\b", r"\bphillips\b"]),
    ("Dearborn", [r"\bdearborn\b"]),
    ("Tomsed", [r"\btomsed\b"]),
    ("Boon Edam", [r"\bboon\s*edam\b", r"\bturnlock\b", r"\btrilock\b"]),
    ("Alvarado", [r"\balvarado\b"]),
    ("Hayward", [r"\bhayward\b"]),
    ("Perey", [r"\bperey\b", r"\broto-?gate\b"]),
    ("Controlled Access", [r"\bcontrolled access\b", r"\bCA-\d"]),
    ("Aegis Mectronics", [r"\baegis\b"]),
    ("Automatic Systems", [r"\bautomatic systems\b"]),
    ("Cubic", [r"\bcubic\b"]),
    ("Ingress Control", [r"\bingress\b"]),
    ("Designed Security", [r"\bdesigned security\b", r"\bDSI\b"]),
    ("Hard Logic", [r"\bhard logic\b"]),
    ("Horton", [r"\bhorton\b"]),
    ("Kidde", [r"\bkidde\b"]),
    ("Tanza", [r"\btanza\b"]),
    ("Ozak", [r"\bozak\b"]),
]
MODEL_RE = re.compile(
    r"\b(TUT-?\d{2}[A-Z]{0,4}|TST-?\d{2}[A-Z]{0,3}|THT-?\d{3}[A-Z]{0,3}|TOT-?\d{2}[A-Z]{0,3}|THG-?\d{2}[A-Z]{0,3}"
    r"|MST(?:-[A-Z0-9]+)?|FMST|CLSTX?|CPSTX?|MSTX|MXT|EDCX?|SLT|STG|CSTG|ASTG|RLT2?|HSWG|HSG|AHSG|SHSG|CHSG"
    r"|PUPKIT(?:\s?I{1,3}\+?)?|Model\s\d{2,3}|Series\s\d{3}|HT\s?431|HGO-\d+)\b", re.I)
PN_TOKEN = re.compile(r"^[A-Z0-9][A-Z0-9\-/\.\+ ]{1,24}$", re.I)
PRICE_RE = re.compile(r"\$?\s*(\d{1,3}(?:,\d{3})*|\d+)\.(\d{2})")
OEM_PATTERNS = [
    r"(?:marked|AKA|a\.k\.a\.|replaces|replacement for|also known as|identical to|equivalent to|same as|cross[- ]reference)\s+(?:the\s+|part\s+|p/n\s+|number\s+)?([A-Z]{0,6}[\- ]?\d[\w\-\.]{2,18})",
    r"\b((?:MSA|LT|J|EB|SDO|CR|FP0|HG-SWA|BZ|D)-?\d[\w\-\.]{2,16})\b",
]
SYNONYM_HINTS = {
    "pawl": ["dog", "locking bar", "latch", "paul"],
    "solenoid": ["coil", "actuator", "plunger magnet"],
    "microswitch": ["limit switch", "micro switch", "roller switch", "sensor switch"],
    "spring": ["coil spring", "return spring"],
    "bearing": ["bushing", "flange bearing"],
    "shock": ["damper", "dashpot", "speed control", "hydraulic"],
    "board": ["controller", "circuit board", "pcb", "logic board", "brain"],
    "relay": ["ice cube relay", "contactor"],
    "counter": ["totalizer", "register"],
    "power supply": ["transformer", "rectifier"],
    "lamp": ["light", "led", "indicator", "bulb"],
}


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s or "part"


def media_name(rel):
    """Sanitize a legacy relative path into /media/<dir>/<file>."""
    parts = rel.replace("\\", "/").split("/")
    clean = []
    for i, p in enumerate(parts):
        base, ext = (os.path.splitext(p) if i == len(parts) - 1 else (p, ""))
        clean.append(slugify(base) + ext.lower())
    return "/media/" + "/".join(clean)


copied = {}
missing = set()


def copy_media(rel):
    if not rel or re.match(r"^https?:", rel):
        return rel
    if rel in copied:
        return copied[rel]
    src = os.path.join(site, rel)
    if not os.path.isfile(src):
        # case-insensitive fallback
        d, f = os.path.split(src)
        if os.path.isdir(d):
            for cand in os.listdir(d):
                if cand.lower() == f.lower():
                    src = os.path.join(d, cand)
                    break
    if not os.path.isfile(src):
        missing.add(rel)
        copied[rel] = None
        return None
    dest_url = media_name(rel)
    dest = os.path.join(repo, "public", dest_url.lstrip("/"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src, dest)
    copied[rel] = dest_url
    return dest_url


def first_sentence(t):
    m = re.split(r"(?<=[a-z0-9\)])\.\s", t, maxsplit=1)
    return m[0].strip().rstrip(".")


def make_title(p):
    t = p["title"].strip(" .:-")
    paras = [x for x in p["paragraphs"] if x and not x.startswith("$")]
    if not t or len(t) < 6 or t.lower() in ("fail-safe", "complete", "green", "best performance", "stainless steel"):
        t = first_sentence(paras[0]) if paras else p["part_raw"]
    t = re.sub(r"\s+", " ", t)
    # trim long titles at a natural break
    if len(t) > 78:
        for sep in [" for ", " used ", " - ", ", ", " with "]:
            i = t.lower().find(sep)
            if 18 < i < 78:
                t = t[:i]
                break
        else:
            t = t[:75].rsplit(" ", 1)[0] + "..."
    return t.strip(" ,;:-")


def split_pn(part_raw):
    toks = [x.strip() for x in part_raw.split(" / ") if x.strip()]
    pns, notes = [], []
    for t in toks:
        if PN_TOKEN.match(t) and re.search(r"\d", t) and not PRICE_RE.search(t) and len(t.split()) <= 3 \
                and not re.search(r"(overall|voltage|vdc|vac|diagram|manual|info|instructions|case of|set|complete|drawing|schematic)", t, re.I):
            pns.append(t)
        else:
            notes.append(t)
    return pns, notes


def find_prices(text):
    return [float(a.replace(",", "") + "." + b) for a, b in PRICE_RE.findall(text)]


DOC_LABELS = [
    ("install", "Installation manual"), ("instruction", "Instructions"), ("booklet", "Installation manual"),
    ("schematic", "Schematic"), ("wiring", "Wiring diagram"), ("hookup", "Hookup diagram"),
    ("sheet", "Spec sheet"), ("drawing", "Drawing"), ("mechanism", "Mechanism drawing"),
    ("disassembly", "Disassembly guide"), ("calibration", "Positioning instructions"),
    ("compare", "Comparison sheet"), ("whats new", "What's different"), ("components", "Component layout"),
    ("parts", "Parts diagram"), ("lock plates", "Parts breakdown"), ("shaft", "Exploded drawing"),
    ("hub", "Exploded drawing"), ("thrust", "Spec sheet"), ("governor", "Instructions"),
]


def doc_label(href, label, notes):
    low = (href + " " + label).lower()
    if label and not re.search(r"\.(gif|jpg|jpeg|png)$", label, re.I) and len(label) > 3:
        return label[0].upper() + label[1:]
    for k, v in DOC_LABELS:
        if k in low:
            return v
    for n in notes:
        if re.search(r"(manual|diagram|instructions|schematic|drawing|info|different)", n, re.I):
            return n
    return "Drawing" if re.search(r"\.(jpg|jpeg|png|gif)$", href, re.I) else "Document"



FIXUPS = {
    1: {"sku": "PUPKIT III+", "title": "PUPKIT III+ upgrade controller"},
    5: {"sku": "PPLCO", "also": ["51-215", "PLC 8.03"]},
    31: {"sku": "85-225-C20", "title": "Case of 20: 85-225 solenoids"},
    50: {"sku": "10244-BRKT"},
    81: {"sku": "BCS-SHORT", "title": "Key bypass connecting spring, short (2.5\" overall)"},
    82: {"sku": "BCS-LONG", "title": "Key bypass connecting spring, long (4.5\" overall)"},
    138: {"sku": "46-008", "title": "Indicator lamp, green (11/16\" hole)"},
    139: {"sku": "46-009", "title": "Indicator lamp, red (11/16\" hole)"},
    147: {"sku": "LED-SET-RG", "title": "Replacement LED lamp set, red and green"},
    165: {"sku": "8508", "title": "Waist high transformer 110/220VAC to 20VAC"},
    232: {"sku": "THT-100-LINK", "title": "THT-100 locking pawl linkages"},
    275: {"sku": "TUT-65RTB", "title": "Used Tomsed TUT-65RTB stadium turnstile"},
    276: {"sku": "TUT-65ES", "title": "Used Tomsed TUT-65ES, fail-lock entry"},
    277: {"sku": "PEREY-47-USED", "title": "Used Perey Model 47 waist high turnstile"},
    295: {"sku": "BH-46-001-B", "title": "Bargain: waist high solenoid coil, new old stock"},
    19: {"sku": "53-139", "title": "2-pole plug-in relay (8-pin DPDT)"},
    20: {"sku": "53-129", "title": "3-pole plug-in relay (11-pin 3PDT)"},
    227: "drop",
}

records = []
seen_sku = {}
slugs = Counter()
order_in_cat = Counter()
report = {"no_price": [], "multi_price": [], "needs_review": []}

for p in raw["products"]:
    fx = FIXUPS.get(p["row"], {})
    if fx == "drop":
        continue
    pns, notes = split_pn(p["part_raw"])
    if fx.get("sku"):
        pns = [fx["sku"]] + [x for x in pns if x != fx["sku"]] + fx.get("also", [])
    price_text = p["price_raw"]
    prices = find_prices(price_text) or find_prices(p["part_raw"])
    body_text = " ".join(p["paragraphs"])
    alltext = " ".join([p["part_raw"], price_text, body_text])

    if not pns and not fx:
        # fall back to a part number mentioned in the description
        m = re.search(r"\b(\d{2,3}-\d{3,4}[A-Z\-]*|[A-Z]{1,4}-\d{3,5}[A-Z\-]*)\b", body_text)
        if m:
            pns = [m.group(1)]
        else:
            report["needs_review"].append({"row": p["row"], "part_raw": p["part_raw"], "why": "no part number"})
            pns = [p["part_raw"].split(" / ")[0][:24] or f"row-{p['row']}"]
    sku = pns[0]

    options = []
    if len(pns) > 1 and len(prices) == len(pns):
        options = [{"part": pn, "price": pr} for pn, pr in zip(pns, prices)]
    price = prices[0] if prices else None
    price_note = ""
    clean_price_text = re.sub(r"\s+", " ", price_text).strip()
    if price is None:
        price_note = clean_price_text or "Call for price"
        report["no_price"].append({"row": p["row"], "sku": sku, "price_raw": price_text})
    elif not re.fullmatch(r"\$?\s*[\d,]+\.\d{2}", clean_price_text):
        price_note = clean_price_text
        if len(prices) > 1 and not options:
            report["multi_price"].append({"row": p["row"], "sku": sku, "price_raw": price_text})

    brands = [name for name, pats in BRANDS if any(re.search(pt, alltext, re.I) for pt in pats)]
    models = []
    for m in MODEL_RE.findall(alltext):
        m = re.sub(r"\s+", " ", m.upper())
        if m not in models:
            models.append(m)
    low = alltext.lower()
    style = []
    if "full height" in low or re.search(r"\bfh\b", low):
        style.append("Full height")
    if "waist high" in low or re.search(r"\bwh\b", low):
        style.append("Waist high")
    if re.search(r"slide gate|sliding gate|swing gate|vehicle", low):
        style.append("Gates")
    if "optical" in low:
        style.append("Optical")

    xrefs = []
    for pat in OEM_PATTERNS:
        for m in re.findall(pat, body_text, re.I):
            m = m.strip(" .,;")
            if m and m.upper() not in [x.upper() for x in xrefs + pns] and re.search(r"\d", m) and len(m) >= 4:
                xrefs.append(m)
    xrefs = xrefs[:10]
    also = [x for x in pns[1:]]

    status = "in-stock"
    st = p["status"]
    for key in ["sold-out", "discontinued", "out-of-stock", "coming-soon", "backorder", "special-order", "call", "limited"]:
        if key in st:
            status = {"discontinued": "sold-out", "call": "call"}.get(key, key)
            break
    if price is None and status == "in-stock":
        status = "call"

    images = [u for u in (copy_media(i) for i in p["images"]) if u]
    docs = []
    seen = set()
    for d in p["docs"]:
        href = d["href"]
        if href.lower().endswith(".htm") or href.lower().endswith(".html"):
            url = "/library/spi/" if "spi" in href.lower() else None
        else:
            url = copy_media(href)
        if not url or url in seen:
            continue
        seen.add(url)
        docs.append({"label": doc_label(href, d["label"], notes), "file": url})

    title = fx.get("title") or make_title(p)
    # merge exploded-drawing duplicates (same part, same price) into the first listing
    key = sku.upper()
    if key in seen_sku and seen_sku[key]["fm"]["price"] == price:
        first = seen_sku[key]
        have = {d["file"] for d in first["fm"]["documents"]}
        first["fm"]["documents"] += [d for d in docs if d["file"] not in have]
        for im in images:
            if im not in first["fm"]["images"]:
                first["fm"]["images"].append(im)
        continue
    base = slugify(sku)
    slugs[base] += 1
    slug = base if slugs[base] == 1 else f"{base}-{slugs[base]}"
    order_in_cat[p["category"]] += 1

    cat_word = {
        "boards": "board", "relays": "relay", "solenoids": "solenoid", "springs": "spring",
        "microswitches": "microswitch", "counters": "counter", "lamps": "lamp", "power": "power supply",
        "shocks": "shock", "bearings": "bearing", "pawls": "pawl",
    }.get(p["category"], "")
    keywords = list(SYNONYM_HINTS.get(cat_word, []))

    body_paras = [x for x in p["paragraphs"] if x.strip() and x.strip() != title]
    records.append({
        "slug": slug,
        "fm": {
            "sku": sku,
            "title": title,
            "category": p["category"],
            "order": order_in_cat[p["category"]] * 10,
            "price": price,
            "price_note": price_note,
            "options": options,
            "status": status,
            "best_choice": "best-choice" in p["badges"],
            "brands": brands,
            "models": models,
            "style": style,
            "also_known_as": also + xrefs,
            "keywords": keywords,
            "images": images,
            "documents": docs,
            "notes": notes,
            "legacy_row": p["row"],
        },
        "body": "\n\n".join(body_paras),
    })
    seen_sku.setdefault(key, records[-1])


def yaml_str(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    return json.dumps(v, ensure_ascii=False)


def to_yaml(fm):
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            elif isinstance(v[0], dict):
                lines.append(f"{k}:")
                for item in v:
                    first = True
                    for ik, iv in item.items():
                        lines.append(("  - " if first else "    ") + f"{ik}: {yaml_str(iv)}")
                        first = False
            else:
                lines.append(f"{k}:")
                lines.extend(f"  - {yaml_str(x)}" for x in v)
        else:
            lines.append(f"{k}: {yaml_str(v)}")
    lines.append("---")
    return "\n".join(lines)


out_dir = os.path.join(repo, "src", "content", "parts")
os.makedirs(out_dir, exist_ok=True)
for r in records:
    with open(os.path.join(out_dir, r["slug"] + ".md"), "w") as f:
        f.write(to_yaml(r["fm"]) + "\n\n" + r["body"].strip() + "\n")

# humor / banner rows for the editorial pages
banners = []
for b in raw.get("banners", []):
    imgs = []
    for i in b["images"]:
        u = copy_media(i)
        if u and u not in imgs and "top-button" not in u and "greenclick" not in u:
            imgs.append(u)
    banners.append({"category": b["category"], "text": b["text"], "images": imgs})

os.makedirs(os.path.join(repo, "src", "data"), exist_ok=True)
report["missing_media"] = sorted(missing)
report["counts"] = Counter(r["fm"]["category"] for r in records)
report["status"] = Counter(r["fm"]["status"] for r in records)
report["brands"] = Counter(b for r in records for b in r["fm"]["brands"])
json.dump(report, open(os.path.join(repo, "src", "data", "import-report.json"), "w"), indent=1)
json.dump(banners, open(os.path.join(raw_path + ".banners.json"), "w"), indent=1)
print(len(records), "products;", len(copied) - len(missing), "media copied;", len(missing), "missing")
print("no price", len(report["no_price"]), "multi", len(report["multi_price"]), "review", len(report["needs_review"]))
print(report["status"]); print(report["brands"])
