import pytest as pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="test",
        password="test",
    )


def test_urlconf_building():
    assert reverse("foo") == "/foo"


def test_login_required(client, settings, user):
    assert reverse("login_required") == "/login_required"
    response = client.get(reverse("login_required"))
    assert response.status_code == 302
    assert response.url == f"{settings.LOGIN_URL}?next=/login_required"

    client.force_login(user)
    response = client.get(reverse("login_required"))
    assert response.status_code == 200


def test_staff_required(client, user):
    assert reverse("staff_required") == "/staff_required"
    response = client.get(reverse("staff_required"))
    assert response.status_code == 403

    user.is_staff = True
    user.save()

    client.force_login(user)
    response = client.get(reverse("staff_required"))
    assert response.status_code == 200


def test_permissions_required(client, user):
    from django.contrib.auth.models import Permission

    assert reverse("permissions_required") == "/permissions_required"
    response = client.get(reverse("permissions_required"))
    assert response.status_code == 403

    user.user_permissions.add(
        Permission.objects.get(codename="view_user"),
    )
    client.force_login(user)
    response = client.get(reverse("permissions_required"))
    assert response.status_code == 200


def test_urlconf_building_with_url_params():
    assert reverse("foo_id", kwargs={"foo_id": 1}) == "/foo/1/"


def test_urlconf_building_with_url_params_and_optional_url_params():
    assert reverse("bar") == "/bar/"
    assert reverse("bar", kwargs={"bar_id": 1}) == "/bar/1/"
