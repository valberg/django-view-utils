from django.conf import settings


class Settings:
    @property
    def DJANGO_VIEW_UTILS_AUTODISCOVER_VIEWS(self):
        return getattr(settings, "DJANGO_VIEW_UTILS_AUTODISCOVER_VIEWS", True)


conf = Settings()
