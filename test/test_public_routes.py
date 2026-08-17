"""Unauthenticated routes: status codes and small stable substrings (Split-safe)."""

import pytest


@pytest.mark.public
def test_home_after_demo_entry_shows_wrapper_shell(client):
    client.get("/demo")

    response = client.get("/")

    assert response.status_code == 200
    lower = response.data.lower()
    assert b"home-variant" in lower or b"demo mode" in lower


@pytest.mark.public
def test_pricing_after_demo_entry_shows_wrapper_or_iframes(client):
    client.get("/demo")

    response = client.get("/pricing")

    assert response.status_code == 200
    lower = response.data.lower()
    assert b"iframe" in lower or b"demo mode" in lower


@pytest.mark.public
def test_home_root_serves_recognizable_shell(client):
    """Split off uses default home.html ('Harness Demo'); other flags use Quantum or variant markers."""
    response = client.get("/")

    assert response.status_code == 200
    lower = response.data.lower()
    assert any(
        needle in lower
        for needle in (
            b"quantum",
            b"harness demo",
            b"home-variant-",
            b"/new-home-static",
            b"cutting-edge",
        )
    )


@pytest.mark.public
def test_demo_entry_shows_quantum_branding(client):
    response = client.get("/demo")

    assert response.status_code == 200
    assert b"quantum" in response.data.lower()


@pytest.mark.public
def test_pricing_page_renders_pricing_title(client):
    response = client.get("/pricing")

    assert response.status_code == 200
    assert b"pricing - quantum bank" in response.data.lower()


@pytest.mark.public
def test_hello_returns_greeting(client):
    response = client.get("/hello")

    assert response.status_code == 200
    assert b"Hello, World!" in response.data


@pytest.mark.public
def test_time_endpoint_shows_time_label(client):
    response = client.get("/time")

    assert response.status_code == 200
    assert b"Current server time is:" in response.data


@pytest.mark.public
def test_about_returns_plain_text_message(client):
    response = client.get("/about")

    assert response.status_code == 200
    assert b"This is a simple HTTP server." in response.data


@pytest.mark.public
def test_home_content_json_shape(client):
    response = client.get("/api/home-content")

    assert response.status_code == 200
    body = response.get_json()
    assert body is not None
    assert "treatment" in body
    assert "template" in body
    assert "url" in body
    assert isinstance(body["treatment"], str)
    assert isinstance(body["template"], str)
    assert isinstance(body["url"], str)
    assert len(body["url"]) > 0
    assert body["template"].endswith(".html")


@pytest.mark.public
@pytest.mark.parametrize(
    "path",
    (
        "/old-home-static",
        "/new-home-static",
        "/v3-home-static",
        "/old-pricing-static",
        "/new-pricing-static",
        "/v3-pricing-static",
    ),
)
def test_static_variant_routes_return_ok(client, path):
    response = client.get(path)

    assert response.status_code == 200


@pytest.mark.public
def test_unknown_path_returns_404_page(client):
    response = client.get("/yodawg20044")

    assert response.status_code == 404
    assert b"404" in response.data


@pytest.mark.public
def test_metrics_exposes_prometheus_text(client):
    response = client.get("/metrics")

    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert "# HELP" in data or "# TYPE" in data


@pytest.mark.public
def test_llms_txt_returns_plain_text(client):
    response = client.get("/llms.txt")
    assert response.status_code == 200
    ct = response.headers.get("Content-Type", "")
    assert ct.startswith("text/plain")
    # Lock the doubled-charset fix: Werkzeug adds one charset for text/plain.
    # A regression to mimetype="text/plain; charset=utf-8" would produce two
    # (RFC-7231-malformed) and must fail here. See /metrics for the un-fixed defect.
    assert ct.lower().count("charset=") == 1
    body = response.get_data(as_text=True)
    # Required substrings per pilot spec acceptance criteria.
    assert "Quantum Bank" in body
    assert "Split.io" in body
    # Demo-disclaimer: spec calls for "a fictional bank for Rod Clemente & friends' demos".
    low = body.lower()
    assert "demo" in low
    assert "fictional" in low


@pytest.mark.public
def test_robots_txt_serves_plain_text(client):
    response = client.get("/robots.txt")
    assert response.status_code == 200
    ct = response.headers.get("Content-Type", "")
    assert ct.startswith("text/plain")
    # Same Werkzeug-charset lock as /llms.txt: exactly one charset= token.
    assert ct.lower().count("charset=") == 1
    body = response.get_data(as_text=True)
    # Required substrings per spec acceptance criteria.
    assert "User-agent: *" in body
    assert "Allow: /" in body
    assert "llms.txt" in body


@pytest.mark.public
def test_llms_full_txt_serves_expanded_manifest(client):
    response = client.get("/llms-full.txt")
    assert response.status_code == 200
    ct = response.headers.get("Content-Type", "")
    assert ct.startswith("text/plain")
    # Lock the doubled-charset fix: exactly one charset= token.
    assert ct.lower().count("charset=") == 1
    body = response.get_data(as_text=True)
    # Required substrings per spec: full name, platform, demo disclaimer.
    assert "Quantum Bank" in body
    assert "Split.io" in body
    assert "demo" in body.lower()
    # Disclaimer coverage lock — match the sibling /llms.txt test. The
    # body already contains "fictional"; this assertion guards the lock
    # against a future body rewrite that accidentally drops it.
    assert "fictional" in body.lower()

    # /llms-full.txt must be the FULL manifest, not a copy of /llms.txt.
    # Cross-fetch both surfaces inside the same test session and assert
    # len(full) strictly greater than len(short).
    short = client.get("/llms.txt").get_data(as_text=True)
    assert len(body) > len(short), (
        f"/llms-full.txt must be longer than /llms.txt — "
        f"got full={len(body)} short={len(short)}"
    )


@pytest.mark.public
def test_sitemap_xml_serves_valid_urlset(client):
    import xml.etree.ElementTree as ET

    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    ct = response.headers.get("Content-Type", "")
    assert ct.startswith("application/xml"), ct
    # Bare mimetype pattern (same discipline as /llms.txt + /robots.txt):
    # Werkzeug must emit exactly one charset= token. A regression that
    # types 'application/xml; charset=utf-8' (the doubled-charset trap)
    # would surface as count == 2 here.
    assert ct.lower().count("charset=") == 1, ct
    body = response.get_data(as_text=True)
    # Body must parse as XML. Raises on malformed structures.
    ET.fromstring(body)
    # Required canonical surfaces must be present.
    assert "https://qbank.dev/" in body, "sitemap must list the homepage"
    assert "https://qbank.dev/llms.txt" in body, "sitemap must reference /llms.txt"
    # Exclusion locks: gated routes, /api/*, /metrics, /robots, /sitemap
    # itself, /*-static variants must NOT appear.
    assert "/api/" not in body, "sitemap must not include /api/* routes"
    assert (
        "/dashboard" not in body
    ), "sitemap must not include /dashboard (session-gated)"
    assert "/metrics" not in body, (
        "sitemap must not include /metrics " "(Prometheus; out of crawl surface)"
    )
    assert "/robots.txt" not in body, "sitemap must not self-reference /robots.txt"


@pytest.mark.public
def test_robots_sitemap_promise_resolves(client):
    """Tighten the robots.txt promise: the Sitemap: URL it advertises
    must actually resolve on the same host. Closes Grok's dangling-
    reference finding (robots.txt + /llms-full.txt pointed at /sitemap.xml
    but that route 404'd).

    Reads the Sitemap URL straight from robots.txt (no hard-coding the
    path in the test) and probes that path on the Flask test client.
    Rewriting robots.txt's Sitemap: line to any other URL is fine —
    this test must keep working for any URL.
    """
    import re
    from urllib.parse import urlparse

    r = client.get("/robots.txt")
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    m = re.search(r"^\s*Sitemap:\s*(\S+)\s*$", body, re.MULTILINE | re.IGNORECASE)
    assert m, "robots.txt is missing a Sitemap: directive"
    sitemap_url = m.group(1)
    path = urlparse(sitemap_url).path
    assert path.startswith("/"), f"unexpected Sitemap URL: {sitemap_url!r}"
    r2 = client.get(path)
    assert r2.status_code == 200, (
        f"robots.txt advertises Sitemap: {sitemap_url} but GET {path} "
        f"returned {r2.status_code} — Grok's dangling-reference finding is "
        f"back on the live surface."
    )
