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

# Run
```
cd web && ./environment/test/testing.sh
```

# Todo
## 1. Add the translation: Hebrew language;
## 2. Upgrade django from 1.6.5 to 2.0
## 3. Change python2 to python3;
## 4. Add the content management support by django-cms;



