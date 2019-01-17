This repo is for Newton's website https://www.newtonproject.org.

# Installation

## Dependency
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



