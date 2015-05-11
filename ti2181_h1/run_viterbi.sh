# /bin/bash

echo "Now I am running my script for my simple named entity tagger using viterbi"
echo
echo "Please be patient....."
echo
python ti2181.py ner_train.dat 
echo "A file 'output_v' was made. Below are the results compiled from the eval file"
echo
python eval_ne_tagger.py ner_dev.key output_v.dat 
echo
echo 
echo '#############################################################################'
echo
echo 