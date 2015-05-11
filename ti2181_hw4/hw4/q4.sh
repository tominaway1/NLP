# /bin/bash
python q4.py $1 tag_dev.dat tag_dev.out
echo $1
python eval_tagger.py tag_dev.key tag_dev.out 



