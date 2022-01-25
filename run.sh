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
  cd $dir_name
  # Creating virtual env to install requirements
  ## Consider mechanism to pre-populate virualenv with common packages?
  python3 -m venv .virtualenv/$dir_name
  source .virtualenv/$dir_name/bin/activate
  pip install -r requirements.txt > /dev/null
  pip install gitpython
  # Scoring model finally
  python ../score_model.py -d "." || echo "Error with score_model.py for $p"
  # Cleaning up
  deactivate
  cd ..
  ## Consider caching virtualenvs?
  rm -rf $dir_name
done <repo_urls.txt
