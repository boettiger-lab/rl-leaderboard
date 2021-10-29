#!/bin/bash

## FIXME:
# really we ought to clone full repos, install requirements.txt, then run score
repo_name=$(sed '1q;d' repos.txt)
git clone $repo_name

## Score the models:
dir_name=$(echo $repo_name | cut -d'/' -f 5 | cut -d'.' -f 1)
pip install -r $dir_name/requirements.txt
python score_model.py -m $dir_name/*.zip
rm -rf $dir_name