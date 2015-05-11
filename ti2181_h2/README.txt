This is a report for assignment 2.

HOW TO RUN BASH SCRIPT
To run both scripts: bash run_script.sh 
To test without vertical markovization: bash bash run_counter.sh
To test with vertical markovization: bash run_counter_vert.sh

Question 4 analysis: Generating the emission counts and mapping infrequent words
What I did:
For this problem, I decided to write everything in count_freq.py because I believed that generating emission counts should be done in the Counter object. I first decided to find all the rare words. So I created a function count() that counted the total number of times all terminal variables were found in the file. I then wrote a new tree to a file called 'modified_parse_train.dat' that replaced all terminal variables in the tree with __RARE__. I also kept a dictionary called wordbank to keep track of all the terminals. For the second part of the problem, I created a function called calculate_probabilities that parsed through the unary and binary dictionaries and calculated the probabilities as described in the instructions.


Question 5 analysis:
What I did:
For these problems, I created a seperate file ti2181.py and imported everything from count_freq.py. I generated all the necessary information for that tree and started to read the "parse_dev.dat" file. For every sentence I read, I ran it through CYK that I implemented directly from the psuedocode. When I first ran it, it took about 10 minutes to run. But I changes alot of my arrays to hashmaps and cut the time down to around 3 minutes.

The results were:
      Type       Total   Precision      Recall     F1 Score
===============================================================
         .         370     1.000        1.000        1.000
       ADJ         164     0.827        0.555        0.664
      ADJP          29     0.333        0.241        0.280
  ADJP+ADJ          22     0.542        0.591        0.565
       ADP         204     0.955        0.946        0.951
       ADV          64     0.694        0.531        0.602
      ADVP          30     0.333        0.133        0.190
  ADVP+ADV          53     0.756        0.642        0.694
      CONJ          53     1.000        1.000        1.000
       DET         167     0.988        0.976        0.982
      NOUN         671     0.752        0.842        0.795
        NP         884     0.625        0.524        0.570
    NP+ADJ           2     0.286        1.000        0.444
    NP+DET          21     0.783        0.857        0.818
   NP+NOUN         131     0.641        0.573        0.605
    NP+NUM          13     0.214        0.231        0.222
   NP+PRON          50     0.980        0.980        0.980
     NP+QP          11     0.667        0.182        0.286
       NUM          93     0.984        0.645        0.779
        PP         208     0.588        0.625        0.606
      PRON          14     1.000        0.929        0.963
       PRT          45     0.957        0.978        0.967
   PRT+PRT           2     0.400        1.000        0.571
        QP          26     0.647        0.423        0.512
         S         587     0.629        0.785        0.698
      SBAR          25     0.091        0.040        0.056
      VERB         283     0.683        0.799        0.736
        VP         399     0.559        0.594        0.576
   VP+VERB          15     0.250        0.267        0.258

     total        4664     0.714        0.714        0.714
#############################################################################


Question 6 analysis:
I did not really have to change anything for number 5. I just changed the training file to "parse_train_vert.py" instead of "parse_train.py". It ran almost around the same time as question 5 and worked the exact same way.

The results were:
      Type       Total   Precision      Recall     F1 Score
===============================================================
         .         370     1.000        1.000        1.000
       ADJ         164     0.689        0.622        0.654
      ADJP          29     0.324        0.414        0.364
  ADJP+ADJ          22     0.591        0.591        0.591
       ADP         204     0.960        0.951        0.956
       ADV          64     0.759        0.641        0.695
      ADVP          30     0.417        0.167        0.238
  ADVP+ADV          53     0.700        0.660        0.680
      CONJ          53     1.000        1.000        1.000
       DET         167     0.988        0.994        0.991
      NOUN         671     0.795        0.845        0.819
        NP         884     0.617        0.548        0.580
    NP+ADJ           2     0.333        0.500        0.400
    NP+DET          21     0.944        0.810        0.872
   NP+NOUN         131     0.610        0.656        0.632
    NP+NUM          13     0.375        0.231        0.286
   NP+PRON          50     0.980        0.980        0.980
     NP+QP          11     0.750        0.273        0.400
       NUM          93     0.914        0.688        0.785
        PP         208     0.623        0.635        0.629
      PRON          14     1.000        0.929        0.963
       PRT          45     1.000        0.933        0.966
   PRT+PRT           2     0.286        1.000        0.444
        QP          26     0.650        0.500        0.565
         S         587     0.704        0.814        0.755
      SBAR          25     0.667        0.400        0.500
      VERB         283     0.790        0.813        0.801
        VP         399     0.663        0.677        0.670
   VP+VERB          15     0.294        0.333        0.312

     total        4664     0.742        0.742        0.742
#############################################################################


