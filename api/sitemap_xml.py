from flask import Response

# Canonical public GET pages, in the priority order they should appear
# in the sitemap. Sourced from app.py route definitions at this branch
# (origin/main = a1050a87), every path listed resolves to 200 on a fresh
# boot of the demo. Excluded by design (see commit message):
#   - session-gated routes: /dashboard, /account, /transactions, /logout
#   - form-only POST routes: /login (GET only render the form; not
#     meaningful as a crawlable entry), /transfer (GET renders the form)
#   - /metrics (Prometheus exposition, not a crawl surface)
#   - /robots.txt (well-known crawlers fetch /robots.xml directly)
#   - /sitemap.xml itself (no self-reference)
#   - /api/* (JSON, session-gated, not crawlable)
#   - /*-static variants (snapshot routes for split-Variation demos; we
#     list the current canonical versions in /pricing and /home instead)
SITEMAP_URLSET = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    "  <url><loc>https://qbank.dev/</loc></url>\n"
    "  <url><loc>https://qbank.dev/about</loc></url>\n"
    "  <url><loc>https://qbank.dev/pricing</loc></url>\n"
    "  <url><loc>https://qbank.dev/demo</loc></url>\n"
    "  <url><loc>https://qbank.dev/hello</loc></url>\n"
    "  <url><loc>https://qbank.dev/time</loc></url>\n"
    "  <url><loc>https://qbank.dev/llms.txt</loc></url>\n"
    "  <url><loc>https://qbank.dev/llms-full.txt</loc></url>\n"
    "</urlset>\n"
)


def handle_sitemap_xml():
    """Return the /sitemap.xml urlset as an application/xml Response.

    Bare mimetype: Werkzeug appends exactly one charset=utf-8 token
    (consistent with /llms.txt + /robots.txt + /llms-full.txt). The
    Content-Type comes out as 'application/xml; charset=utf-8' — one
    'charset=' in the string. Writing 'application/xml; charset=utf-8'
    here would still dedupe in Werkzeug 3.x but the bare-string
    discipline guards against a future Werkzeug version that splits
    the difference.

    The urlset is hand-curated and intentionally small (8 paths). The
    canonical-content-model refactor (out of scope, gated separately)
    is the right move once entities and relations are modeled; today
    this is the direct answer to Grok's dangling-reference finding.
    """
    return Response(SITEMAP_URLSET, mimetype="application/xml")
