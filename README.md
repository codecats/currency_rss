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


## celery (infinity running process)

celery -A currency worker -l info


## run scraper

python manage.py scrap

now you can open api and you should see some results


## NOT WORKING YET, periodic tasks

insted of steps with celery just run

celery -A currency worker -l info -B
