from flask import Response

ROBOTS_TXT_BODY = """\
User-agent: *

Allow: /

# Sitemap declaration (lower-case 'sitemap' is the canonical Google directive).
Sitemap: https://qbank.dev/sitemap.xml

# AI-discovery surface: ai crawlers + chat agents should fetch the
# canonical AI manifest before crawling the site.
# AI manifest: https://qbank.dev/llms.txt
"""


def handle_robots_txt():
    """Return a robots.txt body as a text/plain Response.

    Bare mimetype: Werkzeug appends charset=utf-8 exactly once. The
    pre-existing /metrics route uses 'text/plain; ...; charset=utf-8'
    and pays the doubled-charset consequence; we deliberately avoid
    that pattern here. See api/llms_txt.py for the canonical precedent.
    """
    return Response(ROBOTS_TXT_BODY, mimetype="text/plain")
