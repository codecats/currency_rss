from datetime import datetime
from unittest.mock import MagicMock, patch

import feedparser
from django.test import TestCase
from django.utils.timezone import now

from scraper.models import ScrapedCurrency
from scraper.parser import Parser


class HardcodedDataParser(Parser):
    def __init__(self, country: str = 'usd'):
        super().__init__(country)
        self.data = MagicMock(entries=[])


class ParserTest(TestCase):
    def test_invalid_data(self):
        self.assertEqual(ScrapedCurrency.objects.all().count(), 0)
        parser = HardcodedDataParser('usd')
        parser.data.entries.append(MagicMock(cb_exchangerate='invalid money'))
        parser.parse_entry()
        self.assertEqual(ScrapedCurrency.objects.all().count(), 0)

        parser.data.entries.append(MagicMock())
        parser.parse_entry()
        self.assertEqual(ScrapedCurrency.objects.all().count(), 0)

        parser.data.entries.append(MagicMock(cb_targetcurrency=None))
        parser.parse_entry()
        self.assertEqual(ScrapedCurrency.objects.all().count(), 0)

        parser.data.entries.append(MagicMock(cb_exchangerate='123.8 EUR', updated_parsed='invalid'))
        parser.parse_entry()
        self.assertEqual(ScrapedCurrency.objects.all().count(), 0)

        parser.data.entries.append(
            MagicMock(cb_exchangerate='123.8 EUR', updated_parsed=now(), cb_targetcurrency='EUR'))
        parser.parse_entry()
        self.assertEqual(ScrapedCurrency.objects.all().count(), 0)

    def test_old_data(self):
        ScrapedCurrency.objects.create(country='usd', value=1.8, updated=now())
        self.assertEqual(ScrapedCurrency.objects.all().count(), 1)
        parser = HardcodedDataParser('usd')
        parser.data.entries.append(MagicMock(
            cb_exchangerate='12.00 EUR', updated_parsed=(1980, 2, 17, 17, 3, 38, 1, 48, 0), cb_targetcurrency='usd'))
        parser.parse_entry()
        self.assertEqual(ScrapedCurrency.objects.all().count(), 1)
        ScrapedCurrency.objects.all().delete()

    def test_valid_data(self):
        self.assertEqual(ScrapedCurrency.objects.all().count(), 0)
        parser = HardcodedDataParser('usd')
        parser.data.entries.append(
            MagicMock(cb_exchangerate='123.8 EUR', updated_parsed=(2009, 2, 17, 17, 3, 38, 1, 48, 0),
                      cb_targetcurrency='USD'))
        parser.parse_entry()
        self.assertEqual(ScrapedCurrency.objects.all().count(), 1)

    def test_parse_currency(self):
        pusd = HardcodedDataParser('usd')
        self.assertEqual(pusd.parse_currency('usd'), 'usd')
        self.assertEqual(pusd.parse_currency('usD'), 'usd')
        self.assertEqual(pusd.parse_currency('  usd '), 'usd')
        with self.assertRaises(AttributeError):
            pusd.parse_currency(None)

        with self.assertRaises(AttributeError):
            pusd.parse_currency(1)

    def test_parse_decimal(self):
        p = HardcodedDataParser('usd')
        self.assertEqual(p.parse_decimal('1.0'), 1.0)

        self.assertEqual(p.parse_decimal('Text before 1.0'), 1.0)
        self.assertEqual(p.parse_decimal('1.0 Text after'), 1.0)
        self.assertEqual(p.parse_decimal('In the 1.0 middle .'), 1.0)

    def test_parse_date(self):
        p = HardcodedDataParser('eur')
        with self.assertRaises((TypeError, ValueError, IndexError)):
            p.parse_date(1)

        with self.assertRaises((TypeError, ValueError, IndexError)):
            p.parse_date(None)

        with self.assertRaises((TypeError, ValueError, IndexError)):
            p.parse_date('2017')

        with self.assertRaises((TypeError, ValueError, IndexError)):
            p.parse_date((1, 2))
        self.assertIsInstance(p.parse_date((2009, 2, 17, 17, 3, 38, 1, 48, 0)), datetime)

    @patch.object(feedparser, 'parse')
    def test_parser_usage(self, mock):
        p = Parser('usd')
        p.data
        self.assertTrue(mock.called)
