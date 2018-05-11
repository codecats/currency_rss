from celery.schedules import crontab

from currency.celery import app
from scraper.const import CUR_PATTERNS
from scraper.parser import Parser


@app.task
def scrap(lang):
    pars = Parser(lang)
    pars.parse_entry()


app.conf.beat_schedule = {
    'scrap_{}'.format(cur): {
        'task': 'scraper.tasks.scrap',
        'schedule': crontab(minute=0, hour=i % 24),  # every hour different language
        'args': [cur],
    }
    for i, cur in enumerate(CUR_PATTERNS)
}
