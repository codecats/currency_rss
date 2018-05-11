from scraper.const import CUR_PATTERNS
from scraper.parser import Parser


def scrap():
    for lang in CUR_PATTERNS:
        pars = Parser(lang)
        pars.parse_entry()
