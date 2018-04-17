from currency.celery import app
from scraper.controller import Parser


@app.task
def scrap(lang):
    print 'TASK', lang
    pars = Parser(lang)
    pars.parse_entry()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, scrap.s(2,2), name='add every 10')

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )