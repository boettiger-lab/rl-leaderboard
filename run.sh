#!/bin/bash
set -e # Treat errors as errors

pip install -r requirements.txt > /dev/null
python read_sheets.py

while read p; do
  # read_sheets creates a txt with the repo urls from the google form.
  # We then clone each repo and score the models in the repos
  git clone $p
  # This slices the directory name from the repo url
  dir_name=$(echo $p | cut -d'/' -f 5 | cut -d'.' -f 1)
  rm -r models/$dir_name
  mv $dir_name models/
  # Creating virtual env to install requirements
  python3 -m venv .virtualenv/$dir_name
  source .virtualenv/$dir_name/bin/activate
  pip install -r models/$dir_name/requirements.txt > /dev/null
  pip install gitpython
  # Scoring model finally
  python score_model.py -d $dir_name
  # Cleaning up
  rm -rf models/$dir_name
  deactivate
  rm -rf .virtualenv/$dir_name
done <repo_urls.txt
