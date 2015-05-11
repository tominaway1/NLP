This is a report for assignment 3.

HOW TO RUN BASH SCRIPT
To run script: bash run_script.sh 

Question 4 analysis: 
What I did:
For this problem, I implemented IBM model 1. I followed the pseudocode and made the necessary precautions. To optomize performance, I heavily utilized pythons dictionaries to increase efficiency. I also realized that I can reduce a lot of calculations by calculating the summation for delta outside of the loop since it's the same for all terms. I generated dev_output.txt for the results of dev_output. I also created an alignment_model1.txt file with the alignment for the first 20 sentences in the training data. 


Question 5 analysis:
What I did:
For this problem, I implemented IBM model 2. I followed the pseudocode and made the necessary precautions. To optomize performance, I heavily utilized pythons dictionaries to increase efficiency. I also realized that I can reduce a lot of calculations by calculating the summation for delta outside of the loop since it's the same for all terms. I generated dev_output1.txt for the results of dev_output for this model. I also created an alignment_model2.txt file with the alignment for the first 20 sentences in the training data. 


Question 6 analysis:
I extended what was done for number 5 to calculate the probability for every english german sentence pair given an alignment and found the pair with the highest probability. I then wrote that to output. The results are shown below. I was about 80% accurate which was not too bad at all. 

The results were:
Right Total Acc
81  100 0.810



