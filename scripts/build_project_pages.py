#!/usr/bin/env python3
"""Build the Serenia project pages and apply site-wide SEO fixes (run on the drafts branch).

    python3 scripts/build_project_pages.py          # from the repo root

Creates blog/serenia/<slug>/index.html (price list, floor plans, RERA details,
amenities, overview) by reusing the header, footer, form and scripts of an
existing guide page. Also idempotently:
  * puts "Serenia Kiwale" in the H1 of every guide / hub page
  * adds the project name to image alt text (logo marks, House of Jets photos)
  * adds ?v= cache-busting to local CSS and JS links
  * adds the Serenia pages to the hub, site map page, home page and sitemap.xml
"""
import re, os, glob, html, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://sereniakiwale.com"
DATE = "2026-11-26"
VER = "20261126a"
RERA = "PM1260002602794"
CAT = "serenia"
TPL = os.path.join(ROOT, "blog/buying-guides/2-bhk-vs-3-bhk/index.html")


def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, t):
    full = os.path.join(ROOT, p); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(t)
def esc(s): return html.escape(s, quote=True)
def slugify(t): return re.sub(r"[^a-z0-9]+", "-", html.unescape(re.sub(r"<[^>]+>", "", t)).lower()).strip("-")
def mins(b): return max(2, round(len(re.sub(r"<[^>]+>", " ", b).split()) / 200))

BRAND = "Serenia Kiwale"
IMG = {  # slug -> (image base, alt)
    "aerial": ("aerial-view", "Aerial view of the Serenia township, Kiwale"),
    "tower": ("tower-garden-view", "Towers rising above the landscaped garden, Serenia by House of Jets, Kiwale"),
    "podium": ("podium-garden", "Podium garden at Serenia by House of Jets, Kiwale"),
}

P = {}
P["serenia-price-list"] = dict(
    img="podium", tag="Price list",
    t="Serenia Kiwale Price List: 2 & 3 BHK Packages",
    h="Serenia Kiwale price list: 2 BHK and 3 BHK all-inclusive packages",
    d="Serenia Kiwale price list: 2 BHK about ₹95 L–₹1 Cr and 3 BHK about ₹1.35–1.40 Cr all-inclusive, with carpet area and covered parking. Simplex on request.",
    dek="Indicative all-inclusive packages for 2 BHK and 3 BHK at Serenia, Kiwale, with carpet area and parking.",
    tk=["2 BHK: carpet 674 to 678 sq ft, all-inclusive package about ₹95 lakh to ₹1 crore, 1 covered parking.",
        "3 BHK: carpet 956 to 962 sq ft, all-inclusive package about ₹1.35 to ₹1.40 crore, 2 covered parkings.",
        "2+2 (4 BHK) and 3+3 (6 BHK) Simplex homes are in C Tower; their pricing is shared by the relationship manager.",
        "Prices are indicative and subject to change; confirm the latest price sheet in writing."],
    body='''<p>Serenia by House of Jets is a 10-acre township in Kiwale, near Mukai Chowk, Pune, with 9 towers and 1,800 residences. This page lists the indicative price of each home type so you can compare options before you visit.</p>
<h2>Serenia Kiwale price list at a glance</h2>
<div class="tw"><table class="compare"><thead><tr><th>Residence</th><th>Carpet area</th><th>All-inclusive package</th><th>Covered parking</th></tr></thead><tbody>
<tr><td>2 BHK</td><td>674 – 678 sq ft</td><td>about ₹95 L – ₹1 Cr</td><td>1</td></tr>
<tr><td>3 BHK</td><td>956 – 962 sq ft</td><td>about ₹1.35 – 1.40 Cr</td><td>2</td></tr>
<tr><td>2+2 Simplex (4 BHK)</td><td>On request</td><td>Shared by relationship manager</td><td>On request</td></tr>
<tr><td>3+3 Simplex (6 BHK)</td><td>On request</td><td>Shared by relationship manager</td><td>On request</td></tr></tbody></table></div>
<p>Total area (including the balcony) is 746, 749 and 750 sq ft for the 2 BHK and 1,036, 1,038 and 1,042 sq ft for the 3 BHK. Carpet area is the usable area inside the home, so it is the best figure for comparing projects.</p>
<h2>Simplex homes in C Tower</h2>
<p>C Tower, the tallest tower in Kiwale, offers 2+2 (4 BHK) and 3+3 (6 BHK) Simplex homes on all floors. Pricing, carpet area, parking and floor plans for these are shared privately by the relationship manager. Read <a href="../../buying-guides/what-is-a-simplex-home/">what a Simplex home is</a> to see if it suits you.</p>
<h2>What to ask before you book</h2>
<ul><li>Is the package all-inclusive of stamp duty, registration and GST?</li><li>Are maintenance, club and parking charges included or extra?</li><li>What is the payment schedule, and what does the EOI amount adjust against? See <a href="../../buying-guides/what-is-eoi-in-real-estate/">what EOI means</a>.</li></ul>
<p>Not sure which size to choose? Compare them in <a href="../../buying-guides/2-bhk-vs-3-bhk/">2 BHK vs 3 BHK</a>. Packages are indicative and subject to change. For a written price sheet use the enquiry form on the <a href="../../../#enquire">home page</a>.</p>''')

P["serenia-floor-plans"] = dict(
    img="tower", tag="Floor plans",
    t="Serenia Kiwale Floor Plans & Carpet Areas",
    h="Serenia Kiwale floor plans and carpet areas: 2 BHK and 3 BHK",
    d="Serenia Kiwale floor plans: 2 BHK 746, 749, 750 sq ft and 3 BHK 1,036, 1,038, 1,042 sq ft total area, plus the C Tower typical plan. View the plans.",
    dek="Unit plans by Abhikalpan Architects & Planners, with total and carpet areas for each home type.",
    tk=["2 BHK: 746, 749 and 750 sq ft total area (674 to 678 sq ft carpet).",
        "3 BHK: 1,036, 1,038 and 1,042 sq ft total area (956 to 962 sq ft carpet).",
        "Total area includes the balcony; carpet area is the usable area inside the home.",
        "Simplex floor plans for C Tower are shared by the relationship manager."],
    body='''<p>Serenia's unit plans are by Abhikalpan Architects &amp; Planners, Pune. Here are the plans, the areas and what to look for before you choose.</p>
<h2>Area by home type</h2>
<div class="tw"><table class="compare"><thead><tr><th>Residence</th><th>Total area (with balcony)</th><th>Carpet area</th></tr></thead><tbody>
<tr><td>2 BHK</td><td>746 / 749 / 750 sq ft</td><td>674 – 678 sq ft</td></tr>
<tr><td>3 BHK</td><td>1,036 / 1,038 / 1,042 sq ft</td><td>956 – 962 sq ft</td></tr></tbody></table></div>
<h2>2 BHK floor plans</h2>
<figure class="plan"><img src="../../../images/plans/2bhk-746-compact.webp" width="1280" height="716" loading="lazy" decoding="async" alt="2 BHK 746 sq ft floor plan, Serenia by House of Jets, Kiwale"><figcaption>2 BHK, 746 sq ft</figcaption></figure>
<figure class="plan"><img src="../../../images/plans/2bhk-749-compact.webp" width="1280" height="716" loading="lazy" decoding="async" alt="2 BHK 749 sq ft floor plan, Serenia by House of Jets, Kiwale"><figcaption>2 BHK, 749 sq ft</figcaption></figure>
<figure class="plan"><img src="../../../images/plans/2bhk-750-compact.webp" width="1280" height="716" loading="lazy" decoding="async" alt="2 BHK 750 sq ft floor plan, Serenia by House of Jets, Kiwale"><figcaption>2 BHK, 750 sq ft</figcaption></figure>
<h2>3 BHK floor plans</h2>
<figure class="plan"><img src="../../../images/plans/3bhk-1036-compact.webp" width="1280" height="716" loading="lazy" decoding="async" alt="3 BHK 1,036 sq ft floor plan, Serenia by House of Jets, Kiwale"><figcaption>3 BHK, 1,036 sq ft</figcaption></figure>
<figure class="plan"><img src="../../../images/plans/3bhk-1038-compact.webp" width="1280" height="716" loading="lazy" decoding="async" alt="3 BHK 1,038 sq ft floor plan, Serenia by House of Jets, Kiwale"><figcaption>3 BHK, 1,038 sq ft</figcaption></figure>
<figure class="plan"><img src="../../../images/plans/3bhk-1042-compact.webp" width="1280" height="716" loading="lazy" decoding="async" alt="3 BHK 1,042 sq ft floor plan, Serenia by House of Jets, Kiwale"><figcaption>3 BHK, 1,042 sq ft</figcaption></figure>
<h2>What to look for in a plan</h2>
<ol><li>Is the living room wide enough for your furniture, and where does the light come from?</li><li>Are bedrooms and bathrooms placed so doors do not clash?</li><li>How large is the balcony, and does it open off the living room or a bedroom?</li><li>Where is the kitchen, and is there room for a utility area?</li></ol>
<p>See what each size costs in the <a href="../serenia-price-list/">Serenia Kiwale price list</a>, or compare them in <a href="../../buying-guides/2-bhk-vs-3-bhk/">2 BHK vs 3 BHK</a>. Plans are indicative and subject to change as per approvals. Ask about C Tower Simplex plans through the <a href="../../../#enquire">enquiry form</a>.</p>''')

P["serenia-rera-details"] = dict(
    img="aerial", tag="RERA details",
    t="Serenia Kiwale RERA Number & Developer Details",
    h="Serenia Kiwale RERA number and developer details",
    d="Serenia by House of Jets, Kiwale is registered with MahaRERA under PM1260002602794. Developer details and how to verify the registration yourself.",
    dek="The MahaRERA registration number, the developer and the location, and how to check them yourself.",
    tk=["MahaRERA registration number: PM1260002602794.",
        "Developed under the House of Jets brand; location: Kiwale, near Mukai Chowk, Pune.",
        "You can verify any project on the official MahaRERA website before you book.",
        "Always match the number on your agreement with the one on the website."],
    body='''<p>RERA registration is one of the first things to check before buying an under-construction home. This page lists the details for Serenia, Kiwale and shows how to verify them yourself.</p>
<h2>Serenia project details</h2>
<div class="tw"><table class="compare"><thead><tr><th>Detail</th><th>Information</th></tr></thead><tbody>
<tr><td>Project</td><td>Serenia by House of Jets (C Tower), Kiwale, Pune</td></tr>
<tr><td>Brand</td><td>House of Jets</td></tr>
<tr><td>MahaRERA registration</td><td>PM1260002602794</td></tr>
<tr><td>Location</td><td>Kiwale, near Mukai Chowk, Pune</td></tr>
<tr><td>Township</td><td>10 acres, 9 towers, 1,800 residences</td></tr>
<tr><td>Homes</td><td>2 BHK, 3 BHK, and 2+2 / 3+3 Simplex in C Tower</td></tr></tbody></table></div>
<h2>How to verify the registration</h2>
<ol><li>Open the official <a href="https://maharera.maharashtra.gov.in/" target="_blank" rel="noopener">MahaRERA website</a>.</li><li>Go to the registered projects search and enter the registration number PM1260002602794.</li><li>Check the project name, the promoter, the address and the dates shown for the project.</li><li>Match the registration number with the one on the agreement and the brochure.</li></ol>
<h2>Why it matters</h2>
<p>A RERA-registered project has its approvals, timelines and details on public record. The registration page also shows the possession timeline declared for the project, so read it there and confirm it with the relationship manager in writing.</p>
<p>Before you pay anything, read <a href="../serenia-price-list/">the price list</a> and <a href="../../buying-guides/what-is-eoi-in-real-estate/">what EOI means</a>.</p>''')

P["serenia-amenities"] = dict(
    img="tower", tag="Amenities",
    t="Serenia Kiwale Amenities: Pool, Clubhouse & More",
    h="Serenia Kiwale amenities: pool, clubhouse, podium garden and more",
    d="Serenia Kiwale amenities: podium garden, swimming pool, clubhouse, gymnasium, yoga zone, amphitheatre, jogging track, co-working lounge and more.",
    dek="The amenities planned at Serenia, Kiwale, grouped by how you will use them.",
    tk=["Serenia lists 18 amenities, from a landscaped podium garden to EV charging points.",
        "Fitness: gymnasium, yoga and meditation zone, jogging track, indoor games room, swimming pool.",
        "Family and community: clubhouse, play area, amphitheatre, party hall, co-working lounge.",
        "The amenity list is indicative; confirm what will be ready at possession."],
    body='''<p>Amenities shape daily life in a gated township. Here are the amenities planned at Serenia by House of Jets, Kiwale, grouped by use. The list is indicative, and images shown on the project are artistic impressions.</p>
<h2>Fitness and wellness</h2>
<ul><li>Swimming pool and sundeck</li><li>Fully equipped gymnasium</li><li>Yoga and meditation zone</li><li>Jogging and walking track</li><li>Indoor games room</li></ul>
<h2>Family and community</h2>
<ul><li>Clubhouse</li><li>Children's play area</li><li>Landscaped podium garden</li><li>Amphitheatre seating</li><li>Gazebo and senior sit-out</li><li>Multipurpose party hall</li><li>Co-working lounge</li></ul>
<h2>Convenience and safety</h2>
<ul><li>Grand entrance lobby</li><li>High-speed lifts</li><li>24x7 security and CCTV</li><li>EV charging points</li><li>Power backup (common areas)</li><li>Rainwater harvesting</li></ul>
<h2>Questions to ask before you book</h2>
<ol><li>Which amenities will be ready at possession, and which later?</li><li>Are club and maintenance charges included in the package? See the <a href="../serenia-price-list/">price list</a>.</li><li>Where are the amenities placed relative to your tower? Check the <a href="../serenia-floor-plans/">floor plans</a>.</li></ol>
<p>For the full project facts, read the <a href="../serenia-kiwale-overview/">Serenia Kiwale overview</a>.</p>''')

P["serenia-kiwale-overview"] = dict(
    img="aerial", tag="Project overview",
    t="Serenia Kiwale: Project Overview | House of Jets",
    h="Serenia Kiwale project overview: House of Jets township in Pune",
    d="Serenia by House of Jets, Kiwale, Pune: 10 acres, 9 towers, 1,800 residences, 2 and 3 BHK plus Simplex in C Tower. Overview, amenities and facts.",
    dek="Everything about Serenia in Kiwale in one place: size, towers, homes, amenities and location.",
    tk=["Serenia is a 10-acre township with 9 towers and 1,800 residences in Kiwale, near Mukai Chowk, Pune.",
        "C Tower is the tallest tower in Kiwale and offers 2+2 and 3+3 Simplex homes on all floors.",
        "2 BHK from about ₹95 lakh and 3 BHK from about ₹1.35 crore, all-inclusive and indicative.",
        "MahaRERA registration number: PM1260002602794."],
    body='''<p>Serenia by House of Jets is a residential township in Kiwale, Pune. It is also searched as Serenia Kiwale or Serenia Pune, and this page brings the main facts together.</p>
<h2>Project snapshot</h2>
<div class="tw"><table class="compare"><thead><tr><th>Detail</th><th>Information</th></tr></thead><tbody>
<tr><td>Brand</td><td>House of Jets</td></tr><tr><td>Location</td><td>Kiwale, near Mukai Chowk, Pune</td></tr>
<tr><td>Township</td><td>10 acres, 9 towers, 1,800 residences</td></tr><tr><td>C Tower</td><td>Tallest tower in Kiwale, Simplex homes on all floors</td></tr>
<tr><td>Homes</td><td>2 BHK (674–678 sq ft carpet), 3 BHK (956–962 sq ft carpet), 2+2 and 3+3 Simplex</td></tr>
<tr><td>Starting price</td><td>about ₹95 lakh (all-inclusive, indicative)</td></tr><tr><td>MahaRERA</td><td>PM1260002602794</td></tr></tbody></table></div>
<h2>Location</h2>
<p>Serenia is at the Pune end of the Mumbai–Pune Expressway, close to Ravet, Akurdi and Dehu Road. Read the <a href="../../locality/kiwale-locality-overview/">Kiwale locality overview</a> for more on the area, and check live routes on <a href="https://www.google.com/maps/search/?api=1&amp;query=Serenia+House+of+Jets+Kiwale+Pune" target="_blank" rel="noopener">Google Maps</a>.</p>
<h2>Amenities</h2>
<p>The project lists 18 amenities, including a podium garden, swimming pool, clubhouse, gymnasium, yoga zone, amphitheatre, jogging track and a co-working lounge. See the <a href="../serenia-amenities/">Serenia amenities guide</a> for the full list.</p>
<h2>Next steps</h2>
<ul><li>Compare homes in <a href="../serenia-floor-plans/">floor plans and carpet areas</a>.</li><li>Check the <a href="../serenia-price-list/">price list</a>.</li><li>Verify the <a href="../serenia-rera-details/">RERA details</a>.</li></ul>
<p>Information is indicative and subject to change as per approvals.</p>''')

ORDER = ["serenia-kiwale-overview", "serenia-price-list", "serenia-floor-plans", "serenia-rera-details", "serenia-amenities"]
CATNAME = "Serenia project"


def card(s, depth):
    p = "../" * depth; g = P[s]; im, alt = IMG[g["img"]]
    return (f'<a class="gcard rv" href="{p}blog/{CAT}/{s}/" data-title="{esc(g["h"])}" data-tags="project"><div class="im">\n'
            f'<img src="{p}images/{im}-800.webp" width="800" height="500" loading="lazy" decoding="async" alt="{esc(alt)}"></div>\n'
            f'<div class="tx">\n<small>{g["tag"]}</small>\n<h3>{g["h"][:1].upper()+g["h"][1:]}</h3>\n<p>{g["dek"]}</p>\n'
            f'<div class="ft">\n<span>{mins(g["body"])} min read</span><em>Read guide →</em></div>\n</div>\n</a>')


def build_page(s):
    g = P[s]; t = rd(os.path.relpath(TPL, ROOT))
    path = f"/blog/{CAT}/{s}/"; im, alt = IMG[g["img"]]
    body = g["body"]
    heads = re.findall(r"<h2>(.*?)</h2>", body)
    for h in heads: body = body.replace(f"<h2>{h}</h2>", f'<h2 id="{slugify(h)}">{h}</h2>', 1)
    m = mins(body)
    # head metadata
    t = re.sub(r"<title>.*?</title>", f"<title>{esc(g['t'])}</title>", t, flags=re.S)
    t = re.sub(r'(<meta name="description" content=")[^"]*', lambda x: x.group(1) + esc(g["d"]), t)
    t = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda x: x.group(1) + URL + path, t)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda x: x.group(1) + esc(g["t"]), t)
    t = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda x: x.group(1) + esc(g["d"]), t)
    t = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda x: x.group(1) + URL + path, t)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": g["h"], "description": g["d"], "datePublished": DATE, "dateModified": DATE,
         "timeRequired": f"PT{m}M", "image": URL + "/images/og-image.jpg", "mainEntityOfPage": URL + path,
         "author": {"@type": "Organization", "name": "Serenia by House of Jets"},
         "publisher": {"@type": "Organization", "name": "Serenia by House of Jets", "logo": {"@type": "ImageObject", "url": URL + "/images/logo/mark.png"}},
         "inLanguage": "en-IN", "articleSection": CATNAME},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": URL + q}
            for i, (n, q) in enumerate([("Home", "/"), ("Guides", "/blog/"), (CATNAME, f"/blog/{CAT}/"), (g["h"], path)])]}]}
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda x: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, indent=1) + "</script>", t, count=1, flags=re.S)
    # hero
    hero = f'''<section class="bhero">
<img src="../../../images/{im}.webp" srcset="../../../images/{im}-800.webp 800w, ../../../images/{im}.webp 1600w" sizes="100vw" width="1600" height="900" fetchpriority="high" decoding="async" alt="{esc(alt)}">
<div class="wrap">
<p class="crumbs">
<a href="../../../">Home</a> › <a href="../../../blog/">Guides</a> › <a href="../../../blog/{CAT}/">{CATNAME}</a></p>
<div class="tags" style="margin-top:12px">
<span class="tag-pill">{g["tag"]}</span></div>
<h1>{g["h"][:1].upper()+g["h"][1:]}</h1>
<p class="dek">{g["dek"]}</p>
<div class="metarow">
<span><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg> {m} min read</span><span><svg viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/></svg> {DATE}</span><span>Serenia by House of Jets, Kiwale</span></div>
</div>
</section>
'''
    t = re.sub(r'<section class="bhero">.*?</section>\n', lambda x: hero, t, count=1, flags=re.S)
    # article body
    others = [o for o in ORDER if o != s][:2]
    i = ORDER.index(s); prev = ORDER[i - 1] if i > 0 else None; nxt = ORDER[i + 1] if i < len(ORDER) - 1 else None
    def pn(o, cls, lab): return f'<a class="{cls}" href="../../../blog/{CAT}/{o}/"><small>{lab}</small>\n<b>{P[o]["h"][:1].upper()+P[o]["h"][1:]}</b></a>'
    pnh = (pn(prev, "prev", "← Previous guide") if prev else "<span></span>") + (pn(nxt, "next", "Next guide →") if nxt else "<span></span>")
    art = f'''<article class="post-body">
<div class="takeaways">
<h2>Key takeaways</h2>
<ul>
{"".join(f"<li>{x}</li>" for x in g["tk"])}
</ul>
</div>
{body}
<div class="helpful">
<b>Was this guide helpful?</b><button type="button" data-v="yes">Yes</button>
<button type="button" data-v="no">Not really</button>
<span class="thanks">Thanks for your feedback.</span></div>
<h2 class="relh">Related guides</h2>
<div class="gcards two">
{"".join(card(o, 3) for o in others)}</div>
<div class="pn">
{pnh}</div>
</article>'''
    t = re.sub(r'<article class="post-body">.*?</article>', lambda x: art, t, count=1, flags=re.S)
    toc = "".join(f'<li>\n<a href="#{slugify(h)}">{h}</a></li>\n' for h in heads)
    t = re.sub(r'(<details class="toc">\n<summary>On this page</summary>\n<ol>\n).*?(</ol>)', lambda x: x.group(1) + toc + x.group(2), t, count=1, flags=re.S)
    wr(f"blog/{CAT}/{s}/index.html", t)


def list_page():
    """Category page /blog/serenia/, cloned from the buying-guides category page."""
    t = rd("blog/buying-guides/index.html")
    path = f"/blog/{CAT}/"
    title = "Serenia Kiwale Price, Plans & RERA | House of Jets"
    desc = "Serenia by House of Jets, Kiwale, Pune: price list, floor plans and carpet areas, MahaRERA details, amenities and a full project overview."
    t = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", t, flags=re.S)
    t = re.sub(r'(<meta name="description" content=")[^"]*', lambda x: x.group(1) + esc(desc), t)
    t = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda x: x.group(1) + URL + path, t)
    t = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda x: x.group(1) + esc(title), t)
    t = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda x: x.group(1) + esc(desc), t)
    t = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda x: x.group(1) + URL + path, t)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Serenia Kiwale project guides", "url": URL + path,
         "hasPart": [{"@type": "BlogPosting", "headline": P[s]["h"], "url": f"{URL}/blog/{CAT}/{s}/"} for s in ORDER]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": URL + q}
            for i, (n, q) in enumerate([("Home", "/"), ("Guides", "/blog/"), (CATNAME, path)])]}]}
    t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda x: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, indent=1) + "</script>", t, count=1, flags=re.S)
    t = t.replace('› Buying guides</p>', f'› {CATNAME}</p>')
    t = re.sub(r"<h1>.*?</h1>", f'<h1><span class="h1-brand">{BRAND}</span> Price, floor plans, RERA and amenities</h1>', t, count=1, flags=re.S)
    t = t.replace('Clear answers to common questions before you buy a new home in Kiwale.', 'Price list, floor plans and carpet areas, MahaRERA details, amenities and an overview of Serenia, Kiwale.')
    t = t.replace('Search guides, e.g. Simplex, EOI, 3 BHK', 'Search, e.g. price, floor plan, RERA')
    o = ORDER[1]; g = P[o]; im, alt = IMG[g["img"]]
    feat = (f'<a class="feature rv" href="../../blog/{CAT}/{o}/"><div class="im">\n<img src="../../images/{im}.webp" width="1200" height="700" loading="lazy" decoding="async" alt="{esc(alt)}"></div>\n'
            f'<div class="tx">\n<span class="pill-new">Most searched</span><h2>{g["h"][:1].upper()+g["h"][1:]}</h2>\n<p>{g["dek"]}</p>\n<span class="btn btn-cu">Read the guide</span></div>\n</a>')
    t = re.sub(r'<a class="feature rv".*?</a>\n', lambda x: feat + "\n", t, count=1, flags=re.S)
    t = re.sub(r'<p class="catintro">.*?</p>', '<p class="catintro">Everything about Serenia by House of Jets in one place: the price list, floor plans and carpet areas, MahaRERA details, amenities and a project overview. All figures come from the current price sheet and plans and are indicative.</p>', t, count=1, flags=re.S)
    t = re.sub(r'<div class="chips2".*?</div>\n', "", t, count=1, flags=re.S)
    cards = "".join(card(s, 2) for s in ORDER)
    t = re.sub(r'(<div class="gcards">).*?(</div>\s*(?=<div class="empty"|<div class="band"|</main>))', lambda x: x.group(1) + "\n" + cards + "\n" + x.group(2), t, count=1, flags=re.S)
    return t, path


def sitewide():
    """Idempotent site-wide SEO fixes applied to every page under ROOT."""
    pages = [f for f in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True)
             if "/node_modules/" not in f and "/scripts/" not in f]
    for f in pages:
        rel = os.path.relpath(f, ROOT); t = open(f, encoding="utf-8").read(); o = t
        # brand in every blog / hub / site map H1 (home page already has it)
        if rel != "index.html" and (rel.startswith("blog/") or rel == "sitemap/index.html"):
            m = re.search(r"<h1>(.*?)</h1>", t, re.S)
            if m and "serenia" not in m.group(1).lower() and "h1-brand" not in m.group(1):
                t = t.replace(m.group(0), f'<h1><span class="h1-brand">{BRAND}</span> {m.group(1)}</h1>', 1)
        # alt text: logo marks and House of Jets photos carry the project name
        t = re.sub(r'(<img src="[^"]*logo/mark(?:-light)?-sm\.png"[^>]*?)alt=""', r'\1alt="Serenia by House of Jets logo"', t)
        def alt(m):
            v = m.group(1)
            return m.group(0) if "serenia" in v.lower() or "House of Jets" not in v else f'alt="{v}, Serenia Kiwale"'
        t = re.sub(r'alt="([^"]*)"', alt, t)
        # cache-busting on local css / js
        t = re.sub(r'((?:href|src)="(?:\.\./)*(?:css|js)/[A-Za-z0-9._-]+\.(?:css|js))(?:\?v=[^"]*)?"', lambda m: m.group(1) + f'?v={VER}"', t)
        if t != o: open(f, "w", encoding="utf-8").write(t)

    # shared styles (idempotent)
    css = rd("css/blog.css")
    if "h1-brand" not in css:
        css += """
.bhero h1 .h1-brand{display:block;font-family:inherit;font-size:.4em;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--cu-l);margin-bottom:8px}
figure.plan{margin:18px 0}figure.plan img{width:100%;height:auto;border-radius:14px;border:1px solid var(--line,#e6e0d8)}figure.plan figcaption{font-size:14px;color:var(--mut,#6b6b6b);margin-top:6px;text-align:center}
"""
        wr("css/blog.css", css)
    st = rd("css/site.css")
    if "gl-quick" not in st:
        st += """
.gl-quick{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:22px 0 0}
.gl-quick a{font-size:13px;font-weight:600;color:var(--deep,#0B3B3F);background:#fff;border:1px solid rgba(11,59,63,.18);border-radius:99px;padding:7px 14px;text-decoration:none;transition:background .2s,border-color .2s}
.gl-quick a:hover{background:#fff4ea;border-color:var(--cu,#C9714A)}
"""
        wr("css/site.css", st)

    # hub: project cards + filter chip
    t = rd("blog/index.html")
    if "/blog/serenia/" not in t and 'blog/serenia/' not in t:
        t = t.replace('<div class="gcards">\n', '<div class="gcards">\n' + "".join(card(x, 1) for x in ORDER) + "\n", 1)
        t = t.replace('<button type="button" data-tag="eoi">EOI &amp; booking</button>', '<button type="button" data-tag="eoi">EOI &amp; booking</button>\n<button type="button" data-tag="project">Price, plans &amp; RERA</button>', 1)
        wr("blog/index.html", t)

    # site map page: project section
    t = rd("sitemap/index.html")
    if "blog/serenia/" not in t:
        sec = '<section class="rv">\n<h2>Serenia project pages</h2>\n<ul>\n<li>\n<a href="../blog/serenia/">All project pages</a></li>\n' + "".join(
            f'<li>\n<a href="../blog/{CAT}/{x}/">{P[x]["h"][:1].upper()+P[x]["h"][1:]}</a></li>\n' for x in ORDER) + '</ul>\n</section>\n'
        t = t.replace('<section class="rv">\n<h2>Guides</h2>', sec + '<section class="rv">\n<h2>Guides</h2>', 1)
        wr("sitemap/index.html", t)

    # home page: quick links under the guides + footer link
    t = rd("index.html")
    if "gl-quick" not in t:
        q = '<p class="gl-quick">' + "".join(f'<a href="blog/{CAT}/{x}/">{lab}</a>' for x, lab in [
            ("serenia-price-list", "Price list"), ("serenia-floor-plans", "Floor plans"), ("serenia-rera-details", "RERA details"),
            ("serenia-amenities", "Amenities"), ("serenia-kiwale-overview", "Project overview")]) + "</p>\n"
        t = t.replace('<p style="margin-top:22px">\n<a class="btn btn-dark" href="blog/">All guides</a></p>', q + '<p style="margin-top:22px">\n<a class="btn btn-dark" href="blog/">All guides</a></p>', 1)
        t = t.replace('<a href="#plans">Floor plans</a><br>', '<a href="#plans">Floor plans</a><br><a href="blog/serenia/serenia-price-list/">Price list</a><br>', 1)
        wr("index.html", t)

    # sitemap.xml
    sm = rd("sitemap.xml")
    add = [f"/blog/{CAT}/"] + [f"/blog/{CAT}/{x}/" for x in ORDER]
    for u in add:
        if URL + u not in sm:
            sm = sm.replace("</urlset>", f"  <url><loc>{URL}{u}</loc><lastmod>{DATE}</lastmod></url>\n</urlset>")
    wr("sitemap.xml", sm)


def enrich_schema():
    """Richer structured data on the home page and on every guide (facts already on the page only)."""
    from PIL import Image
    t = rd("index.html"); pat = r'(<script type="application/ld\+json">)(.*?)(</script>)'
    m = re.search(pat, t, re.S); d = json.loads(m.group(2)); g = d["@graph"]
    ids = {x.get("@id"): x for x in g if isinstance(x, dict)}
    org = ids[URL + "/#org"]; cx = ids[URL + "/#complex"]
    org["@type"] = ["Organization", "RealEstateAgent"]
    org["description"] = "Serenia by House of Jets: 2 BHK, 3 BHK and Simplex residences in Kiwale, near Mukai Chowk, Pune."
    org["brand"] = {"@type": "Brand", "name": "House of Jets"}
    org["contactPoint"] = {"@type": "ContactPoint", "contactType": "sales", "areaServed": "IN", "availableLanguage": ["en", "hi", "mr"], "url": URL + "/#enquire"}
    def img(name, f, caption):
        w, h = Image.open(os.path.join(ROOT, "images", f)).size
        return {"@type": "ImageObject", "@id": f"{URL}/#img-{name}", "url": f"{URL}/images/{f}", "contentUrl": f"{URL}/images/{f}", "width": w, "height": h, "caption": caption, "inLanguage": "en-IN"}
    imgs = [img("aerial", "aerial-view.webp", "Aerial view of 9-tower township, Serenia by House of Jets, Kiwale"),
            img("podium", "podium-garden.webp", "Podium garden with seating and pathways, Serenia by House of Jets, Kiwale"),
            img("towers", "tower-garden-view.webp", "Towers rising above the landscaped garden, Serenia by House of Jets, Kiwale")]
    primary = {"@type": "ImageObject", "@id": URL + "/#primaryimage", "url": URL + "/images/og-image.jpg", "contentUrl": URL + "/images/og-image.jpg", "width": 1200, "height": 630, "caption": "Serenia by House of Jets, Kiwale, Pune", "inLanguage": "en-IN"}
    cx["image"] = [{"@id": primary["@id"]}] + [{"@id": i["@id"]} for i in imgs]
    cx["containedInPlace"] = {"@type": "Place", "name": "Kiwale, near Mukai Chowk, Pune", "hasMap": "https://www.google.com/maps/search/?api=1&query=Serenia+House+of+Jets+Kiwale+Pune",
                              "address": {"@type": "PostalAddress", "addressLocality": "Kiwale, Pune", "addressRegion": "Maharashtra", "addressCountry": "IN"}}
    title = re.search(r"<title>(.*?)</title>", t, re.S).group(1); desc = re.search(r'name="description" content="([^"]*)"', t).group(1)
    page = {"@type": "WebPage", "@id": URL + "/#webpage", "url": URL + "/", "name": html.unescape(title), "description": html.unescape(desc), "inLanguage": "en-IN",
            "isPartOf": {"@id": URL + "/#website"}, "about": {"@id": URL + "/#complex"}, "primaryImageOfPage": {"@id": primary["@id"]}, "breadcrumb": {"@id": URL + "/#breadcrumb"}}
    crumb = {"@type": "BreadcrumbList", "@id": URL + "/#breadcrumb", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Serenia by House of Jets, Kiwale", "item": URL + "/"}]}
    nav = {"@type": "ItemList", "@id": URL + "/#projectpages", "name": "Serenia Kiwale project pages", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": P[x]["h"][:1].upper() + P[x]["h"][1:], "url": f"{URL}/blog/{CAT}/{x}/"} for i, x in enumerate(ORDER)]}
    have = {x.get("@id") for x in g}
    for node in [page, primary] + imgs + [crumb, nav]:
        if node["@id"] not in have: g.append(node)
    t = t[:m.start()] + m.group(1) + json.dumps(d, ensure_ascii=False, indent=1) + m.group(3) + t[m.end():]
    wr("index.html", t)
    # every guide / project page: tie the BlogPosting to the project
    for f in glob.glob(os.path.join(ROOT, "blog/**/index.html"), recursive=True):
        rel = os.path.relpath(f, ROOT); tt = rd(rel); mm = re.search(pat, tt, re.S)
        if not mm: continue
        dd = json.loads(mm.group(2)); ch = False
        for x in dd.get("@graph", []):
            if x.get("@type") == "BlogPosting" and "about" not in x:
                x["about"] = {"@id": URL + "/#complex"}; x["isPartOf"] = {"@id": URL + "/#website"}; ch = True
        if ch: wr(rel, tt[:mm.start()] + mm.group(1) + json.dumps(dd, ensure_ascii=False, indent=1) + mm.group(3) + tt[mm.end():])


def main():
    # 1) project pages
    for s in ORDER: build_page(s)
    # 2) category page
    t, path = list_page()
    wr(f"blog/{CAT}/index.html", t)
    sitewide()
    enrich_schema()
    print("project pages built:", ORDER)


if __name__ == "__main__":
    main()
