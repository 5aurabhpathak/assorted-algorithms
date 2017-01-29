#!/bin/bash
#Author: Saurabh Pathak
#Third Step
#cleaning of parallel corpus - uses (my own) python scripts.
#monolingual corpus was not cleaned. However, certain literatures suggest that such a cleaning might benefit the translation system. (Ref. topic 'Controlled Language rules in MT'). I am not much inclined towards it as of now because of the nature and proportion of my work. Furthermore, we also have the post edition option to correct any errors introduced by noise in the corpus.
cd /home/phoenix/src/python/nlp/mtech-thesis/prepare
echo Cleaning parallel corpus...
./clean_bilingual_corpus.py
cd ../data/corpus/bilingual
mv cleaned_parallel/stage3/IITB.en-hi.en parallel/IITB.en-hi.clean.en
mv cleaned_parallel/stage3/IITB.en-hi.hi parallel/IITB.en-hi.clean.hi
rm -rf cleaned_parallel filtered_out
echo done.
exit 0
