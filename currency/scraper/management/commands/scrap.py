from django.core.management.base import BaseCommand, CommandError

from scraper.const import CUR_PATTERNS
from scraper.parser import Parser


class Command(BaseCommand):
    help = ''


    def handle(self, *args, **options):
        from scraper.tasks import scrap
        for lang in CUR_PATTERNS:
            pars = Parser(lang)
            pars.parse_entry()
        self.stdout.write(self.style.SUCCESS('Successfully scraped'))