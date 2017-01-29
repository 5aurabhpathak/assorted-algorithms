#!/bin/bash
#Author: Saurabh Pathak
#Second step
#performs truecasing on monolingual as well as parallel corpus (english part)
#uses perl scripts provided with moses
#Run after - 'download_corpora.sh'
#Requires - Monolingual Corpus and Parallel Corpus in respective directories
echo Generating truecase model...
cd /home/phoenix/src/python/nlp/mtech-thesis/data/corpus/monolingual
time /opt/moses/moses-scripts/recaser/train-truecaser.perl --model ../truecase-model.en --corpus monolingual.tok.en
echo truecasing monolingual corpus...
time /opt/moses/moses-scripts/recaser/truecase.perl --model ../truecase-model.en < monolingual.tok.en > monolingual.true.en
cd ../bilingual/parallel
echo truecasing english side of bilingual corpus...
time /opt/moses/moses-scripts/recaser/truecase.perl --model ../../truecase-model.en < IITB.en-hi.tok.en > IITB.en-hi.true.en
exit 0
