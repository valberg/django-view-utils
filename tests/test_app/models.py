from django.db import models


class Foo(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Bar(models.Model):
    name = models.CharField(max_length=255)
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
