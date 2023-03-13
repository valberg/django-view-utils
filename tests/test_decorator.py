from django.urls import reverse


def test_urlconf_building():
    assert reverse("foo") == "/foo"


def test_login_required(client, settings):
    assert reverse("login_required") == "/login_required"
    response = client.get(reverse("login_required"))
    assert response.status_code == 302
    assert response.url == f"{settings.LOGIN_URL}?next=/login_required"
