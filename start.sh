#!/bin/bash
project_name="eyesmedia-data-governance-service"
cd /usr/services/eyesmedia/apps/"${project_name}"

if ! [ -f /usr/services/eyesmedia/apps/"${project_name}"/venv/bin/activate ];
# CentOS(biz-develop)
then
  echo 'clean __pycache__'
  rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./*/__pycache__ __pycache__
  echo 'installing virtual envirement'
  python3 -m venv venv
  echo 'installing requirements package'
  echo 'start project...'
  source venv/bin/activate
#  pip3 install --upgrade pip
  pip3 install -r requirements.txt
  python3 start.py
else
  echo 'clean __pycache__'
  rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info ./*/__pycache__ __pycache__
  # need to check package version
  source venv/bin/activate
  echo 'checking requirements package'
  pip3 install -r requirements.txt
  python3 start.py
fi