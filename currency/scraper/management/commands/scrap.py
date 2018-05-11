from django.core.management.base import BaseCommand

from scraper.const import CUR_PATTERNS
from scraper.parser import Parser


class Command(BaseCommand):
    help = 'Scrap currencies.'

    def handle(self, *args, **options):
        all_count = len(CUR_PATTERNS)
        for i, lang in enumerate(CUR_PATTERNS, 1):
            self.stdout.write(self.style.NOTICE('[{} %] Scrapping {}'.format(i*100 / all_count, lang)))
            pars = Parser(lang)
            pars.parse_entry()
        self.stdout.write(self.style.SUCCESS('Successfully scraped'))
