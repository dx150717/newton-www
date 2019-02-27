This repo is for Newton's website https://www.newtonproject.org.

# Installation

## Install the Dependency
```
apt-get update && cat package.txt|xargs apt-get install -y --force-yes
```

## Install the python library
```
virtualenv ve && source ve/bin/activate
pip install -r web/requirements.txt
```
# Configure Database on local desktop
## create database
```
$mysql
mysql>create database newton_www default character set utf8;
```
## change the configuration file
open web/web/config/server.py for changing your database account.
The original is the following,
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newton_www',
        'USER': 'root', 
        'PASSWORD': '',
    },
}
```

# Run
```
cd web && ./environment/test/testing.sh
```

# Todo
## 1. Add the translation: Hebrew language;
## 2. Upgrade django from 1.6.5 to 2.0
## 3. Change python2 to python3;
## 4. Add the content management support by django-cms;



