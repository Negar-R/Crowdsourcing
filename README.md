# Crowdsourcing

> Crowdsourcing software development or software crowdsourcing is an emerging area of software engineering. It is an open call for participation in any task of software development, including documentation, design, coding and testing. These tasks are normally conducted by either members of a software enterprise or people contracted by the enterprise. But in software crowdsourcing, all the tasks can be assigned to or are addressed by members of the general public. Individuals and teams may also participate in crowdsourcing contests.

## Setup project locally

[![Python Version](https://img.shields.io/badge/python-3.7-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-2.2-brightgreen.svg)](https://djangoproject.com)

First, clone the repository to your local machine:

```
git clone https://github.com/Negar-R/Crowdsourcing.git
cd Crowdsourcing
```

To activate virtual environments and install dependencies in, run the below commands:

```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirments.txt
```

To create project's tables in database do:

```
python manage.py makemigrations
python manage.py migrate
```

At last, to run the project:

```
python manage.py runserver
```
The project will be available at **127.0.0.1:8000**

## Run unit tests

To run unit test that blongs to accounts_app, use this command:

```
python manage.py test accounts
```

And to run tests in tasks_app, enter:

```
python manage.py test tasks
```

## URL's introduction

URL | Description
--- | ---
``127.0.0.1:8000/accounts/register`` | Some actions on this site require to be enrolled first. Then we send you a verification email and you should verify it. So please enter a valid email !
``127.0.0.1:8000/accounts/login`` | When you want to sign in to your account, give us your email. After that, we send you a code and by clicking on it, you can be logged in.
``127.0.0.1:8000/tasks/all_task`` | You can see all tasks here. They are sorted by last modified time. To see this page, it is not necessary to login.
``127.0.0.1:8000/tasks/reported_task`` | Any user that is an agent can see all tasks that are reported by the individual.
``127.0.0.1:8000/tasks/assigned_task`` | See the tasks that should be done by you, here.
``127.0.0.1:8000/tasks/add_task`` | Agents can create new tasks, from here.