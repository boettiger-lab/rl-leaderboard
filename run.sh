#!/bin/bash
set -e # Treat errors as errors

# read_sheets creates a txt with the repo urls from the google form.
pip install -r requirements.txt > /dev/null
python read_sheets.py

# consider parallel execution?
while read p; do
  # This slices the directory name from the repo url
  dir_name=$(echo $p | cut -d'/' -f 5 | cut -d'.' -f 1)

  if [ -d ${dir_name} ] 
  then
    echo "updating $dir_name"
    cd $dir_name
    git pull --quiet
  else
    echo "cloning $dir_name"
    git clone --quiet $p 
    cd $dir_name
    python3 -m venv .virtualenv
  fi

  echo "Creating virtual env..."
  source .virtualenv/bin/activate
  pip install -r ../shared_requirements.txt &> /dev/null
  if [ -f requirements.txt ]; then
    pip install -r requirements.txt &> /dev/null
  else
    pip install stable_baselines3 sb3_contrib
  fi
  echo "Scoring model..."
  python ../score_model.py -d "." || echo "Error with score_model.py for $p"
  
  # Cleaning up
  deactivate
  cd ..
  #rm -rf $dir_name
done <repo_urls.txt

