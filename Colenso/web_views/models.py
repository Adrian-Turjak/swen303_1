from django.db import models
from django.utils import timezone


class Search(models.Model):
    """docstring for Project"""
    search = models.TextField()
    successful = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField()
    date = models.DateTimeField(default=timezone.now)
