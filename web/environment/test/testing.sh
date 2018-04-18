#!/bin/bash
python manage.py runserver --nostatic --settings=web.settings_test 0.0.0.0:8000
