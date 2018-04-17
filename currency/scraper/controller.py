from datetime import datetime
from time import mktime

import feedparser

from scraper.models import ScrapedCurrency


class Parser(object):
    link = 'https://www.ecb.europa.eu/rss/fxref-{}.html'
    country = None

    def __init__(self, country='usd'):
        self.link = self.link.format(country)
        self.country = country

    def parse_entry(self):
        print 'parsed'
        scraped = []
        d = feedparser.parse(self.link)  # https://www.ecb.europa.eu/rss/fxref-usd.html
        last_scraped = ScrapedCurrency.objects.filter(country=self.country).order_by('updated').first()
        for en in d.entries:
            try:
                value = float(en.cb_exchangerate.replace('EUR', ''))
            except (TypeError, ValueError):
                # todo: log here
                continue
            updated = datetime.fromtimestamp(mktime(en.updated_parsed))

            # already scraped data
            if last_scraped is not None and last_scraped.updated >= updated:
                return
            scraped.append(ScrapedCurrency(updated=updated, value=value, country=self.country))
        ScrapedCurrency.objects.bulk_create(scraped)
