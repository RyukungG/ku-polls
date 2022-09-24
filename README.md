# KU-polls
## Online Polls And Surveys

An application for conducting online polls and surveys based
on the [django-tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/), with
additional features.

App created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th/en/community-home).

## Install and Run
make sure that you have [python](https://www.python.org/downloads/) in your computer.
1. clone the repo into directory
2. then create a virtual environment in your repo directory
```sh
python -m venv env
```

to activate a virtual environment om Windows
```sh
. env/Scripts/activate
```
to exit the environment
```sh
deactivate
```

3. then to install the requirements
```sh
pip install -r requirements.txt
```

4. you have to create file name ```.env``` to configuration. Follow the example on sample.env.
you may generate your secretkeys on [this site](https://djecrety.ir/)

5. then to create the database run
```sh
python manage.py migrate
```

6. load the data
```sh
python manage.py loaddata data/polls.json data/users.json
```

7. run server
```sh
python manage.py runserver
```

 you can go to ```http://127.0.0.1:8000/``` to use the web application.

## User that exists in the KU-polls
| Username  | Password    |
|-----------|-------------|
| b6410545550| RyuN2@@2   |
| kuruga    | kuruga2545   |
| ryunosuke | ryunosuke2545|

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)

- [Requirements](../../wiki/Requirements)

- [Development Plan](../../wiki/Development&20Plan)

- [Iteration 1 Plan](https://github.com/RyukungG/ku-polls/wiki/Iteration-1-Plan)

- [Iteration 2 Plan](https://github.com/RyukungG/ku-polls/wiki/Iteration-2-Plan)

- [Iteration 3 Plan](https://github.com/RyukungG/ku-polls/wiki/Iteration-3-Plan)

- [Iteration 4 Plan](https://github.com/RyukungG/ku-polls/wiki/Iteration-4-Plan)

- [Task Board](https://github.com/users/RyukungG/projects/2/views/1)

