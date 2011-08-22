#!/bin/bash

# verify user provided a name for the virtualenv
if [ -z "$1" ]; then
  echo "

    usage: $0 virtual_env_name

  "
  exit
fi
VIRTUALENV_NAME=$1

# make sure virtualenv stuff is available and create fresh environment
WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv $VIRTUALENV_NAME --no-site-packages
workon $VIRTUALENV_NAME

# run tests and capture return code to send back to jenkins
python setup.py install_dev
python example/manage.py jenkins --pep8-exclude=lettuce.django --output-dir=jenkins_reports
python example/manage.py harvest -a sample -S --verbosity=3 --with-xunit --xunit-file=jenkins_reports/lettuce.xml

test_result=$?

deactivate
rmvirtualenv $VIRTUALENV_NAME

exit $test_result