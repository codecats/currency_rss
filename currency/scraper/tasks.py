from celery.schedules import crontab

from currency.celery import app
from scraper.const import CUR_PATTERNS
from scraper.controller import Parser
from scraper.models import ScrapedCurrency


@app.task
def scrap(lang):
    pars = Parser(lang)
    pars.parse_entry()


app.conf.beat_schedule = {
    'scrap_{}'.format(cur): {
        'task': 'scraper.tasks.scrap',
        'schedule': crontab(minute=0, hour=i%24),
        'args': [cur],
    }
    for i, cur in enumerate(CUR_PATTERNS)
}
