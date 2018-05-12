# Currency scrapper rss
scraps currencies from ecb.europa.eu/rss and presents results in REST service
 
last build status: [![Build Status](https://travis-ci.org/codecats/currency_rss.svg?branch=master)](https://travis-ci.org/codecats/currency_rss)

# Installation
I assume that you have installed python, python-dev, virtualenv and other libs for python 3.
Installation was tested for Ubuntu 16.10.
Project is compatible also with Python2.7.
## Step1: Clone
Clone the repository, this command will clone project into _currency_rss_ directory.:
```bash
git clone https://github.com/codecats/currency_rss 
```

Go to the project under _currency_rss_ directory:
```bash
cd currency_rss
```


Project structure should look similar like that:

    .
    └── currency # Content root
        ├── currency # All manage.py commands should be run from this 'app' dir
        └── scraper
            ├── management
            │   └── commands
            ├── migrations        
            └── rest
        


## Step 2 Create venv (optional)
It's good practice to keep requirements in independent enviroment. 
There is many ways to do it: conda, pipenv, virtualenv, docker or virtualenv...
In this step we use virtualenv:
```bash
virtualenv venv -p python3
```
_* -p parameter means we use python 3 interpreter_
## Step 3 Activate venv
Let's activate this environment, after this command python from virtualenv created in Step 3 is used
```bash
. venv/bin/activate
```

## Step 4 Install requirements
Install required libs stored in the `requirements.txt` file (Content root directory):
```bash
pip install -r requirements.txt
```
## Step 5 Set up database
Default Django's config uses sqllite, it's not recommended for production but for development purposes it's ok.
```bash
python manage.py migrate
```
Done.

# Run


## Server
As I mentioned before this command should be run from `currency` app directory.
```bash
python manage.py runserver
```
now open browser and hit `http://localhost:8000/scraper/api/`, you should see empty results


## Scraper
Scraper is a simple task that fetch currency. You can run it manually by simple `manage.py` command
```bash
python manage.py scrap
```

### When you want add this script to run in periodic tasks you can use CRON or Celery
Please don't use both solution in the same time!
#### CRON
Simpler and better (less heavy) solution, just add script to crontab.
You can simply add command `scrap` by simple entry in crontab:
```cron
# m h  dom mon dow   command
*0 3 * * * /path/to/app/currency_rss/venv/bin/python /path/to/app/currency_rss/currency/manage.py scrap
```
To keep this solution more pythonic and easier to manage and develop I used [django-crontab](https://github.com/kraiz/django-crontab) lib.
```bash
python manage.py crontab add
```
_* now if you have some changes in your code just re-run `crontab add` command_

#### Celery
I don't recomment install celery just for this scrapper porpouse but if you already use celery. For example you already have infrastructure on you system and your backend has free working power.

Run celery worker called `currency` with level info. Last argument is `beat` that runs  periodic task scheduler.
```bash
celery -A currency worker -l info -B
``` 
_You can run it directly from bash but I highly remommend supervisor for better manage_

## TODO:
 - add entries to scraper.const.py#CUR_PATTERNS
 - unittests
 - config for CI server
 - heroku demo app
