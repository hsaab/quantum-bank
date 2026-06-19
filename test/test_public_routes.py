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
def test_home_content_dev_home_uses_v3_template(client, monkeypatch):
    class FakeSplitClient:
        def get_treatment(self, user_key, flag_name):
            return "dev_home"

    monkeypatch.setattr("api.home_content.get_split_client", lambda: FakeSplitClient())

    response = client.get("/api/home-content")

    assert response.status_code == 200
    body = response.get_json()
    assert body["treatment"] == "dev_home"
    assert body["template"] == "home_v3.html"


@pytest.mark.public
def test_banking_metrics_use_actual_request_method(client):
    client.get("/login")
    client.get("/transfer")

    data = client.get("/metrics").get_data(as_text=True)

    assert 'app_request_count{method="GET",endpoint="/login"' in data
    assert 'app_request_count{method="GET",endpoint="/transfer"' in data


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
