#! /bin/bash
echo "Hi! I am running my script to test the counter without vertical markovization"
echo
python count_cfg_freq.py parse_train_vert.dat > results_with_vert
echo "A file 'modified_parse_train.dat' was made with an updated tree. "
echo "In addition, a file called 'results_with_vert' was made showing the resulting counts"
echo
echo "Now I am running the CYK on the modified_parse_train file. This will take about 3 minutes"
python ti2181.py modified_parse_train.dat parse_dev.dat
echo "The parsing is done. The results are shown below"
python eval_parser.py parse_dev.key prediction_file 
echo '#############################################################################'
echo
echo 