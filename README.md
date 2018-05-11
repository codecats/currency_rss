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
        ├── currency # All commands should be run from this dir
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
Install required libs stored in the `requirements.txt` file:
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
As I mentioned before this command should be run from `currency` directory.
```bash
python manage.py runserver
```
now open browser and hit `http://localhost:8000/scraper/api/`, you should see empty results




## celery (infinity running process)

celery -A currency worker -l info


## run scraper (CRON once a day)

python manage.py scrap

now you can open api and you should see some results


## NOT WORKING YET, periodic tasks

insted of steps with celery just run

celery -A currency worker -l info -B


## TODO:

 - complete celery beat configuration
 - add entries to scraper.const.py#CUR_PATTERNS
 - unittests
 - config for CI server
 - heroku demo app
