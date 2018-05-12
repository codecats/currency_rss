import re
from datetime import datetime
from time import mktime

import feedparser
from django.utils.functional import cached_property

from scraper.models import ScrapedCurrency


class Parser(object):
    _link = 'https://www.ecb.europa.eu/rss/fxref-{}.html'
    country = None
    _CURRENCY_PATTERN = re.compile('\d+\.\d+')

    def __init__(self, country: str = 'usd'):
        self._link = self._link.format(country)  # https://www.ecb.euroselfpa.eu/rss/fxref-usd.html
        self.country = country

    @cached_property
    def data(self):
        return feedparser.parse(self._link)

    @classmethod
    def parse_decimal(cls, text: str):
        return float(re.findall(cls._CURRENCY_PATTERN, text)[0])

    @classmethod
    def parse_date(cls, p_tuple):
        return datetime.fromtimestamp(mktime(p_tuple))

    @classmethod
    def parse_currency(cls, cur: str):
        return cur.strip().lower()

    def parse_entry(self):
        scraped = []
        d = self.data
        last_scraped = ScrapedCurrency.objects.filter(country=self.country).order_by('updated').first()
        for en in d.entries:
            valid = True
            try:
                value = self.parse_decimal(en.cb_exchangerate)
            except (TypeError, ValueError, IndexError):
                valid = False
            try:
                updated = self.parse_date(en.updated_parsed)
            except TypeError:
                valid = False
            try:
                cur = self.parse_currency(en.cb_targetcurrency)
            except AttributeError:
                valid = False
            else:
                valid = valid and cur == self.country

            # valid entry
            if valid == True:
                # already scraped data
                if last_scraped is not None and last_scraped.updated >= updated:
                    return
                scraped.append(ScrapedCurrency(updated=updated, value=value, country=self.country))
        ScrapedCurrency.objects.bulk_create(scraped)
