from django.core.management.base import BaseCommand, CommandError

from scraper.const import CUR_PATTERNS
from scraper.controller import Parser


class Command(BaseCommand):
    help = ''


    def handle(self, *args, **options):
        from scraper.tasks import scrap
        for lan in CUR_PATTERNS:
            scrap.apply_async([lan])
        self.stdout.write(self.style.SUCCESS('Successfully scraped'))