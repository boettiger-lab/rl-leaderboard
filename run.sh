#!/bin/bash

python read_sheets.py

while read p; do
  ## FIXME:
  # really we ought to clone full repos, install requirements.txt, then run score
  git clone $p
  #
  ### Score the models:
  dir_name=$(echo $p | cut -d'/' -f 5 | cut -d'.' -f 1)
  pip install -r $dir_name/requirements.txt
  python score_model.py -m $dir_name/*.zip
  rm -rf $dir_name
done <repo_urls.txt
