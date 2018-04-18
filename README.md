# installation

git clone 

virtualenv venv -p python2.7

. venv/bin/activate

cd currency

pip install -r requirements.txt

python manage.py migrate


# run


All commands should be run from `currency` directory


    .
    └── currency
        ├── currency <-`here`
        └── scraper
            ├── management
            │   └── commands
            ├── migrations        
            └── rest
        


##server

python manage.py runserver

now open browser and hit `http://localhost:8000/scraper/api/`, you should see empty results

## run scraper

celery -A currency worker -l info -B


## TODO:
 - add entries to scraper.const.py#CUR_PATTERNS
 - unittests
 - config for CI server
 - heroku demo app
