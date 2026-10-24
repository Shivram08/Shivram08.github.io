import re, sys, pathlib
from html.parser import HTMLParser

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(".")
PAGES = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]

STALE = [
    r"(–|-|&ndash;)\s*Present", r"150 reports", r"250\s?ms", r"Gemini 1\.5",
    r"3,200", r"190\s?s", r"resume_TK", r"Machine Learning Intern",
    r"custom unit tests", r"81\.6", r"LangChain", r"release readiness",
    r"Data Scientist Co-op", r"Institute of Experiential", r"Jan 2026",
    r"multimodal", r"OpenCV", r"Plotly",
]
BANNED = [r"→\s*</a>", r"·"]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.has_title, self.has_desc = [], set(), False, False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "title":
            self.has_title = True
        if tag == "meta" and a.get("name") == "description":
            self.has_desc = True
        for k in ("href", "src"):
            if k in a and a[k]:
                self.links.append(a[k])

parsed = {}
for p in PAGES:
    pg = Page()
    pg.feed(p.read_text(encoding="utf-8"))
    parsed[p.resolve()] = pg

errors = []
for p in PAGES:
    text = p.read_text(encoding="utf-8")
    pg = parsed[p.resolve()]
    if not pg.has_title or not pg.has_desc:
        errors.append(f"{p}: missing <title> or meta description")
    # Check stale claims in the raw HTML (catches hrefs) and with tags stripped
    # (catches "May 2026 – <time>Present</time>").
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text))
    for pat in STALE + BANNED:
        flags = re.IGNORECASE if pat == "multimodal" else 0
        hits = len(re.findall(pat, text, flags))
        if pat in STALE:
            hits = max(hits, len(re.findall(pat, plain, flags)))
        for _ in range(hits):
            errors.append(f"{p}: matches {pat!r}")
    for link in pg.links:
        if re.match(r"^(https?:|mailto:|tel:|data:)", link) or link == "#":
            continue
        path, _, frag = link.partition("#")
        if not path:
            target = p
        elif path.startswith("/"):
            target = ROOT / path.lstrip("/")
        else:
            target = p.parent / path
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            errors.append(f"{p}: broken link {link}")
            continue
        if frag and target.suffix == ".html":
            ids = parsed.get(target.resolve(), Page()).ids
            if frag not in ids:
                errors.append(f"{p}: missing anchor #{frag} in {target}")

print("\n".join(errors) if errors else "OK")
sys.exit(1 if errors else 0)
