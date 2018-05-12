from django.test import TestCase

from scraper.models import ScrapedCurrency


class ScrapedCurrencyTest(TestCase):
    def create_scraped_currency(self, value=100., country='usd'):
        return ScrapedCurrency.objects.create(value=value, country=country)

    def test_scraped_currency_creation(self):
        sc = self.create_scraped_currency()
        self.assertTrue(isinstance(sc, ScrapedCurrency))
