#!/bin/bash
set -e # Treat errors as errors

# read_sheets creates a txt with the repo urls from the google form.
pip install -r requirements.txt > /dev/null
python read_sheets.py

# consider parallel execution?
while read p; do
  # This slices the directory name from the repo url
  dir_name=$(echo $p | cut -d'/' -f 5 | cut -d'.' -f 1)
  echo $dir_name

  # Allow directory to persist
  if [ -d ${dir_name} ] 
  then
    cd $dir_name
    git pull --quiet
  else
    git clone --quiet $p 
    cd $dir_name
    python3 -m venv .virtualenv/$dir_name
  fi

  # Creating virtual env to install requirements
  source .virtualenv/$dir_name/bin/activate
  pip install gitpython wheel sb3_contrib stable-baselines3 &> /dev/null # needed for score_model.py
  pip install -r requirements.txt &> /dev/null
  
  # Scoring model finally
  python ../score_model.py -d "." || echo "Error with score_model.py for $p"
  
  # Cleaning up
  deactivate
  cd ..
  #rm -rf $dir_name
done <repo_urls.txt

