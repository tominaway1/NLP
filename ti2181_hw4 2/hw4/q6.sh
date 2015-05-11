# /bin/bash
python q6.py tag_train.dat $1 $2
bash q4.sh $1
python eval_tagger.py tag_dev.key tag_dev.out 



