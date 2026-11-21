#!/usr/bin/env python3
"""Build the live site from the full set of guides on the `drafts` branch.

Usage (from a checkout of main):
    git archive drafts | tar -x -C /tmp/src
    python3 /tmp/src/scripts/apply-schedule.py /tmp/src . [--published slug,slug]

SRC holds every page. DEST (the main checkout) receives only the locality
guides listed in --published (default: scripts/schedule.json "published").
Links, cards and sitemap entries for unpublished guides are removed so the
live site never links to a page that does not exist yet.
"""
import re, sys, os, json, shutil, glob

src, dest = sys.argv[1], sys.argv[2]
sched = json.load(open(os.path.join(src, "scripts/schedule.json")))
order = sched["order"]
pub_arg = None
for i, a in enumerate(sys.argv):
    if a == "--published":
        pub_arg = [x for x in sys.argv[i + 1].split(",") if x]
published = pub_arg if pub_arg is not None else sched["published"]
published = [s for s in order if s in published]
unpub = [s for s in order if s not in published]

def rd(p): return open(os.path.join(src, p), encoding="utf-8").read()
def wr(p, t):
    full = os.path.join(dest, p); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(t)

def prune(html):
    for u in unpub:
        # cards linking to an unpublished guide
        html = re.sub(r'<a class="gcard[^>]*href="[^"]*/locality/%s/"[^>]*>.*?</a>\s*' % re.escape(u), "", html, flags=re.S)
        # list items in the HTML site map
        html = re.sub(r'<li>\s*<a href="[^"]*/locality/%s/">.*?</a>\s*</li>\s*' % re.escape(u), "", html, flags=re.S)
        # home-page guide cards
        html = re.sub(r'<a class="g" href="[^"]*/locality/%s/">.*?</a>\s*' % re.escape(u), "", html, flags=re.S)
        # previous / next links
        html = re.sub(r'<a class="(?:prev|next)" href="[^"]*/locality/%s/">.*?</a>' % re.escape(u), "<span></span>", html, flags=re.S)
        # inline links to sibling guides
        html = re.sub(r'<a href="(?:\.\./)+%s/">(.*?)</a>' % re.escape(u), r"\1", html, flags=re.S)
        html = re.sub(r'<a href="(?:\.\./)*blog/locality/%s/">(.*?)</a>' % re.escape(u), r"\1", html, flags=re.S)
    # empty related block
    html = re.sub(r'<h2 class="relh">Related guides</h2>\s*<div class="gcards two">\s*</div>\s*', "", html, flags=re.S)
    return html

# 1) locality guide pages
live_dirs = set(published)
for d in glob.glob(os.path.join(dest, "blog/locality/*/")):
    if os.path.basename(d.rstrip("/")) not in live_dirs: shutil.rmtree(d)
for s in published:
    wr(f"blog/locality/{s}/index.html", prune(rd(f"blog/locality/{s}/index.html")))

for d in glob.glob(os.path.join(dest, "blog/locality")):
    if os.path.isdir(d) and not os.listdir(d): os.rmdir(d)

# 2) locality category page
cat = os.path.join(dest, "blog/locality/index.html")
if published:
    t = prune(rd("blog/locality/index.html"))
    def ld(m):
        d = json.loads(m.group(2))
        for it in d["@graph"]:
            if it["@type"] == "CollectionPage":
                it["hasPart"] = [p for p in it["hasPart"] if any(f"/{s}/" in p["url"] for s in published)]
        return m.group(1) + json.dumps(d, ensure_ascii=False, indent=1) + m.group(3)
    t = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld, t, count=1, flags=re.S)
    wr("blog/locality/index.html", t)
elif os.path.exists(cat):
    os.remove(cat)

# 3) guides hub
t = prune(rd("blog/index.html"))
if not published:
    t = re.sub(r'\s*<button type="button" data-tag="locality">Locality</button>', "", t)
    t = t.replace("locality guides, 2 BHK vs 3 BHK", "2 BHK vs 3 BHK")
wr("blog/index.html", t)

# 4) home page
t = prune(rd("index.html"))
if "kiwale-locality-overview" not in published:
    t = re.sub(r'<li>\s*Read our Kiwale locality guide\s*</li>\s*', "", t)
    t = re.sub(r'<li>\s*<a href="blog/locality/kiwale-locality-overview/">.*?</a>\s*</li>\s*', "", t, flags=re.S)
wr("index.html", t)

# 4b) other pages that carry the footer or the full guide list, and shared styles
for pth in sorted(glob.glob(os.path.join(src, "blog/buying-guides/**/index.html"), recursive=True)) + [os.path.join(src, "sitemap/index.html")]:
    rel = os.path.relpath(pth, src)
    t = prune(rd(rel))
    if not published:
        t = re.sub(r'<li>\s*<a href="[^"]*/blog/locality/">.*?</a>\s*</li>\s*', "", t, flags=re.S)
        t = re.sub(r'<section class="rv">\s*<h2>Locality guides</h2>\s*<ul>\s*</ul>\s*</section>\s*', "", t, flags=re.S)
    wr(rel, t)
for css in ("css/site.css", "css/blog.css"):
    shutil.copyfile(os.path.join(src, css), os.path.join(dest, css))

# 5) sitemap
sm = rd("sitemap.xml")
def keep(m):
    u = m.group(1)
    if "/blog/locality/" not in u: return m.group(0)
    if u.rstrip("/").endswith("/blog/locality"): return m.group(0) if published else ""
    return m.group(0) if any(f"/{s}/" in u for s in published) else ""
sm = re.sub(r'<url><loc>([^<]*)</loc>.*?</url>\n?', keep, sm, flags=re.S)
wr("sitemap.xml", sm)
d = os.path.join(dest, "blog/locality")
if os.path.isdir(d) and not os.listdir(d): os.rmdir(d)
print("published:", published, "| held back:", unpub)
