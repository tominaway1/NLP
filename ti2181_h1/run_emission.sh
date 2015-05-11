#! /bin/bash
echo "Hi! I am running my script for my simple named entity tagger using emission counts"
echo
python count_freqs.py ner_train.dat 
echo "A file 'output_e' was made. Below are the results compiled from the eval file"
echo
python eval_ne_tagger.py ner_dev.key output_e.dat 
echo
echo 
echo '#############################################################################'
echo
echo 