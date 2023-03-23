import pytest
from django.apps import apps
from django.urls import reverse


@pytest.mark.django_db
def test_generic_list(client):
    Foo = apps.get_model("test_app", "Foo")

    from tests.test_app.models import Bar

    foo = Foo.objects.create(name="foo")
    bar = Bar.objects.create(name="bar", foo=foo)

    url = reverse("generic:list")
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["page_obj"].object_list[0] == bar
