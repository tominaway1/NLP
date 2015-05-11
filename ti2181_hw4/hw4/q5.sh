# /bin/bash
python q5.py tag_train.dat suffix_tagger.model
bash q4.sh suffix_tagger.model
python eval_tagger.py tag_dev.key tag_dev.out 



