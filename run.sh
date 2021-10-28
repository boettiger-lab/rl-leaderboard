#!/bin/bash

## Download all the models:
wget --content-disposition --trust-server-names -i models.txt


## FIXME:
# really we ought to clone full repos, install requirements.txt, then run score

## Score the models:
python score_model.py -m fishing-v1-A2C-team_vanilla.zip

cat models.txt | xargs basename
#| xargs score_model.py