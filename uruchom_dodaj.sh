#!/bin/bash
rm db.sqlite3
rm -r wyniki/migrations
rm -r myvenv
python3 -m venv myvenv
source myvenv/bin/activate
pip3 install django==1.8
pip3 install django_jinja
pip3 install numpy
python3 manage.py makemigrations wyniki
python3 manage.py sqlmigrate wyniki 0001
python3 manage.py migrate
python3 dodaj.py
python3 manage.py createsuperuser
echo "Wykonaj teraz polecenie : python3 manage.py runserver"