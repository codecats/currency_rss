import re
from datetime import datetime
from time import mktime

import feedparser
from django.utils.functional import cached_property

from scraper.models import ScrapedCurrency


class Parser(object):
    link = 'https://www.ecb.europa.eu/rss/fxref-{}.html'
    country = None
    _CURRENCY_PATTERN = re.compile('\d+\.\d+')

    def __init__(self, country: str = 'usd'):
        self.link = self.link.format(country)  # https://www.ecb.europa.eu/rss/fxref-usd.html
        self.country = country

    @cached_property
    def data(self):
        return feedparser.parse(self.link)

    def parse_entry(self):
        scraped = []
        d = self.data
        last_scraped = ScrapedCurrency.objects.filter(country=self.country).order_by('updated').first()
        for en in d.entries:
            valid = True
            try:
                value = float(re.findall(self._CURRENCY_PATTERN, en.cb_exchangerate)[0])
            except (TypeError, ValueError):
                valid = False
            valid = valid and en.cb_targetcurrency.lower() != self.country

            # invalid entry, skip this one
            if valid == False:
                updated = datetime.fromtimestamp(mktime(en.updated_parsed))

                # already scraped data
                if last_scraped is not None and last_scraped.updated >= updated:
                    return
                scraped.append(ScrapedCurrency(updated=updated, value=value, country=self.country))
        ScrapedCurrency.objects.bulk_create(scraped)
