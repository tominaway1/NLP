This is a report for assignment 4.

HOW TO RUN BASH SCRIPT
To run all features and then execute them: bash run_script.sh 

Question 4:

To Run hw4, you can run bash q4.sh [model file]. 
so execute: bash q4.sh tag_dev.dat 
The output was like this:
	2226 2459 0.905246034974
Analysis: The results were consistently around low 90 and seemed to be working properly


Question 5: 
To Run hw5, you can run bash q5.sh 
so execute: bash q4.sh tag_dev.dat 
2265 2459 0.921106140708
Analysis:The results were consistently around 92 and seemed to be working properly. There was definetely and improvement from part 4


Question 6 analysis: 
Three new features:
1) Length
To run need to run:
bash q6.sh len_tagger.model 1

Results: 2293 2459 0.932492883286
Analysis: did very well

2) Prefix
To run need to run:
bash q6.sh prefix_tagger.model 2
Results: 2262 2459 0.919886132574
Analysis: surprisingly did poorly

3) Form of string using regex
To run need to run:
bash q6.sh form_tagger.model 3
Results: 2289 2459 0.930866205775
Analysis: did very well

4) all of them run together
To run need to run:
bash q6.sh all_tagger.model 4
Results: 2294 2459 0.932899552664
Analysis: did very well


