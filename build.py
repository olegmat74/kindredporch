#!/usr/bin/env python3
"""Kindred Porch static builder -> public/ (Render static site). Go links: /go/his-secret/<code>/ (Render redirect rules)."""
import pathlib, shutil, html, datetime, json
from content import L, GO, REV, HOP
R = pathlib.Path(__file__).parent; OUT = R/"public"; URL = "https://kindredporch.onrender.com"
shutil.rmtree(OUT, ignore_errors=True); OUT.mkdir()
VERBS = ["Read the guide he'd never tell you about", "See what James Bauer teaches", "Take a look at the program", "Watch the free presentation",
         "Find out what drives him", "See the full guide", "Learn the idea behind it", "Open the official page", "Hear it from the coach",
         "Discover the instinct", "Get the guide", "See if it fits you"]
def go(code=""): return GO + (code + "/" if code else "")
def btn(i, code, cls="pill"): return f'<a class="{cls}" href="{go(code)}" rel="nofollow sponsored noopener" target="_blank">{VERBS[i % len(VERBS)]}</a>'
SHELVES = []
for a in L:
    if a["shelf"] not in SHELVES: SHELVES.append(a["shelf"])
def anchor(s): return s.lower().replace(" & ", "-").replace(" ", "-")
def page(title, desc, inner, path, cls=""):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{URL}{path}">
<meta property="og:type" content="article"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Young+Serif&family=Figtree:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/porch.css"><link rel="icon" href="/lantern.svg"></head><body class="{cls}">
<header class="mast"><p class="kicker">letters on love, from a Tucson porch</p><a class="name" href="/">Kindred <span>Porch</span></a>
<nav>{''.join(f'<a href="/#{anchor(s)}">{s}</a>' for s in SHELVES)}<a href="{REV}">The Review</a></nav></header>
<main>{inner}</main>
<footer><div class="sig">— Marisol</div><p>Kindred Porch is one woman's notes on long-term love. It isn't therapy or counseling. If you feel unsafe, call the National Domestic Violence Hotline: 1-800-799-7233.</p>
<p>Some links are affiliate links. If you buy through them, I may earn a commission at no extra cost to you. <a href="/disclosure/">Disclosure</a> · <a href="/privacy/">Privacy</a> · <a href="/about/">About</a> · © {datetime.date.today().year}</p></footer></body></html>"""
def write(p, s):
    d = OUT/p.strip("/"); d.mkdir(parents=True, exist_ok=True); (d/"index.html").write_text(s)
for i, a in enumerate(L):
    style = ["postcard", "ribbon", "note"][i % 3]
    box = f'<aside class="cta {style}">{a["cta"]}{btn(i, a["code"])}<small>affiliate link · <a href="/disclosure/">how this site earns</a></small></aside>'
    body = a["body"]
    if a["cta_pos"] == "mid":
        parts = body.split("<h2>"); k = max(2, len(parts)//2)
        body = "<h2>".join(parts[:k]) + box + "<h2>" + "<h2>".join(parts[k:])
    else: body += box
    sib = [b for b in L if b["shelf"] == a["shelf"] and b is not a][:2] + [b for b in L if b["shelf"] != a["shelf"]][i % 9:i % 9 + 1]
    more = "".join(f'<li><a href="/{b["slug"]}/">{b["title"]}</a></li>' for b in sib)
    inner = f'<article class="letter"><p class="shelf">{a["shelf"]} · {a["mins"]}-minute read</p><h1>{a["title"]}</h1><p class="dek">{a["desc"]}</p><div class="prose">{body}</div><section class="next"><h3>Keep reading</h3><ol>{more}</ol></section></article>'
    write(f"/{a['slug']}/", page(a["title"], a["desc"], inner, f"/{a['slug']}/"))
# home
idx = ""
for s in SHELVES:
    items = "".join(f'<li><a href="/{a["slug"]}/"><b>{a["title"]}</b><span>{a["desc"]}</span></a></li>' for a in L if a["shelf"] == s)
    idx += f'<section class="shelfblock" id="{anchor(s)}"><h2>{s}</h2><ol>{items}</ol></section>'
home = f"""<section class="hello"><p>Hi, I'm Marisol. Twelve years married, two kids, one slightly crooked porch swing where most of our best talks happen. I write these letters for women who want a closer, warmer relationship without playing games.</p></section>
<section class="feature"><div><p class="shelf">the one resource I point friends to</p><h2>Why does he pull close one month and drift the next?</h2><p>Relationship coach James Bauer's guide explains an instinct most men never put into words. I read it, tried it, and wrote <a href="{REV}">an honest review</a>.</p></div>{btn(4, "home", "pill big")}<small>affiliate link</small></section>
<div class="index">{idx}</div>"""
write("/", page("Kindred Porch — honest letters on love and long-term relationships", "Warm, practical relationship notes for women: date nights, conversation questions, appreciation and keeping the spark alive.", home, "/", "home"))
# review / compare
today = datetime.date.today()
rv = f"""<article class="letter review"><p class="shelf">Review · updated {today:%B %Y}</p><h1>His Secret Obsession Review: What It Is, What Works, Who Should Skip It</h1>
<p class="dek">I read James Bauer's His Secret Obsession cover to cover and used it for two months. Here's the honest version.</p>
<div class="prose"><div class="verdict"><p><b>My verdict:</b> worth it if your relationship is basically healthy and you want to understand what makes a man feel drawn to commit. Not a fix for a relationship with disrespect, cheating or abuse.</p>{btn(0, "rv1")}<small>affiliate link</small></div>
<h2>What it is</h2><p>His Secret Obsession is a digital guide (ebook plus audio) by relationship coach James Bauer. Its central idea is what he calls the "hero instinct": a drive many men have to feel needed, respected and useful to the person they love. The guide gives specific phrases, texts and situations that speak to that instinct.</p>
<h2>What I liked</h2><ul><li>The core idea is simple and, for us, true. My husband responded noticeably when I asked for his help and thanked him specifically.</li><li>Lots of concrete examples, not just theory.</li><li>Works for dating, new relationships and long marriages.</li><li>One-time price and a 60-day refund through ClickBank, the retailer.</li></ul>
<h2>What I didn't love</h2><ul><li>The sales video is long and dramatic. Skip ahead if you like.</li><li>Some phrasing feels scripted. I rewrote lines in my own voice.</li><li>Upsells after purchase. You don't need them.</li><li>It's written from a traditional view of gender roles, which won't suit everyone.</li></ul>
<aside class="cta ribbon"><h3>Curious about the "hero instinct"?</h3><p>The free presentation explains it before you spend anything.</p>{btn(3, "rv2")}<small>affiliate link · <a href="/disclosure/">disclosure</a></small></aside>
<h2>How it compares</h2>
<table><thead><tr><th></th><th>His Secret Obsession</th><th>Couples counseling</th><th>Popular relationship books</th></tr></thead><tbody>
<tr><td>Cost</td><td>Low, one-time</td><td>$100–$200 per session</td><td>$15–$30</td></tr>
<tr><td>Focus</td><td>What draws a man closer</td><td>Both partners, any issue</td><td>Broad</td></tr>
<tr><td>Needs his participation</td><td>No</td><td>Yes</td><td>Ideally</td></tr>
<tr><td>Speed</td><td>Read in a weekend</td><td>Weeks to months</td><td>Varies</td></tr>
<tr><td>Serious problems (abuse, affairs)</td><td>Not suitable</td><td>Best choice</td><td>Limited</td></tr>
<tr><td>Refund</td><td>60 days via ClickBank</td><td>No</td><td>Store policy</td></tr></tbody></table>
<h2>Who it's for</h2><p>Women who feel their partner is a little distant, women in new relationships who want to understand men better, and long-married women who want the warmth back.</p>
<h2>Who should skip it</h2><p>If there's abuse, control or repeated cheating, a guide is not the answer. Talk to a licensed counselor, and if you're in danger, call 1-800-799-7233.</p>
<h2>Bottom line</h2><p>It's not magic, but it's a useful lens. The biggest change for me was learning to say what I admire and ask for help without nagging. That alone was worth the price.</p>
<div class="verdict alt">{btn(5, "rv3")}<small>affiliate link · results vary, use your judgment</small></div>
<p>Related letters: <a href="/signs-he-is-pulling-away/">signs he's pulling away</a>, <a href="/make-him-feel-appreciated/">making him feel appreciated</a>, <a href="/sweet-texts-to-send-him/">sweet texts to send</a>.</p></div></article>"""
write(REV, page("His Secret Obsession Review (2026): Honest Pros, Cons and Comparison", "An honest His Secret Obsession review by a married woman: the hero instinct, pros and cons, price, refund and who should skip it.", rv, REV))
write("/about/", page("About Kindred Porch", "About Marisol and Kindred Porch.", '<article class="letter"><h1>About</h1><div class="prose"><p>I\'m Marisol, a former middle-school counselor\'s aide living in Tucson with my husband, two kids and a very loud cat. I started Kindred Porch to write down the small things that kept our marriage warm through new babies, job changes and one very long kitchen remodel.</p><p>I\'m not a therapist. These are notes from real life, plus what I\'ve learned from books and courses along the way.</p></div></article>', "/about/"))
write("/disclosure/", page("Affiliate Disclosure", "How Kindred Porch earns money.", '<article class="letter"><h1>Affiliate disclosure</h1><div class="prose"><p>Some links on this site are affiliate links, including links to His Secret Obsession sold through ClickBank. If you buy through them, I may earn a commission at no extra cost to you. I only recommend things I have read or used myself. ClickBank is the retailer of products on this site; CLICKBANK® is a registered trademark of Click Sales, Inc.</p></div></article>', "/disclosure/"))
write("/privacy/", page("Privacy", "Privacy policy.", '<article class="letter"><h1>Privacy</h1><div class="prose"><p>This site doesn\'t use analytics or tracking cookies of its own. Affiliate partners may set cookies when you click their links, under their own policies. Google Fonts is used for typography.</p></div></article>', "/privacy/"))
(OUT/"404.html").write_text(page("Not found", "Page not found", '<article class="letter"><h1>This letter got lost in the mail</h1><div class="prose"><p><a href="/">Back to the porch</a></p></div></article>', "/404.html"))
for f in ["porch.css", "lantern.svg"]: shutil.copy(R/"static"/f, OUT/f)
(OUT/"robots.txt").write_text(f"User-agent: *\nDisallow: /go/\nSitemap: {URL}/sitemap.xml\n")
urls = ["/", REV] + [f"/{a['slug']}/" for a in L] + ["/about/"]
(OUT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{URL}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls) + "</urlset>")
codes = ["home", "rv1", "rv2", "rv3"] + [a["code"] for a in L]
json.dump([{"source": "/go/his-secret", "dest": HOP + "pin04"}, {"source": "/go/his-secret/", "dest": HOP + "pin04"}] +
          [{"source": f"/go/his-secret/{c}/", "dest": HOP + "pin04" + c} for c in codes] + [{"source": f"/go/his-secret/{c}", "dest": HOP + "pin04" + c} for c in codes],
          open(R/"redirects.json", "w"), indent=0)
print("built", len(urls), "pages;", len(codes), "go codes")
