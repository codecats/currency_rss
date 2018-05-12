# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Model, DateTimeField, FloatField, CharField


class ScrapedCurrency(Model):
    created = DateTimeField(auto_now=True)
    updated = DateTimeField(null=True, blank=True)
    value = FloatField()
    country = CharField(max_length=3)