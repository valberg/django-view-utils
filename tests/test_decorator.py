from django.test import SimpleTestCase
from django.urls import reverse


class URLConfBuildingTest(SimpleTestCase):
    def test_urlconf_building(self):
        assert reverse("foo") == "/foo"
