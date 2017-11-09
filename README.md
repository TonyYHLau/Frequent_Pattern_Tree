# Frequent_Pattern_Tree
Mine frequent patterns from databases

# Reference
The program 'Mine Frequent Patterns.py' provides an implementation for the paper "Mining FrequentPatterns without Candidate Generation" by  Jiawei Han, Jian Pei, and Yiwen Yin.

# Data
The example 'transactionDB.csv' has two columns 'TID' and 'Items' respectively:<br>
    
TID        Items<br> 
100	 f,a,c,d,g,i,m,p <br>
200  a,b,c,f,l,m,o <br>
300	 b,f,h,j,o <br>
400	 b,c,k,s,p <br>
500	 a,f,c,e,l,p,m,n <br>

# Implementation
Run the 'Mine_Frequent_Patterns.py' file. You can adjust the threshold value in the implementation section of the file to suit your needs.

# Output
The output of the program can be described in the following: <br>
The numbers '1, 2 ,3 ...' is the frequency of an item 'a,b,c,...'<br>

Tree:<br>
<<Node (root)>
<<<Node 'f' (4)>
<<<<Node 'c' (3)>
<<<<<Node 'a' (3)>
<<<<<<Node 'm' (3)>
<<<<<<<Node 'p' (2)>
<<<<<<<Node 'b' (1)>
<<<<Node 'b' (1)>
<<Node 'c' (1)>
<<<<Node 'p' (1)>
<<<<<Node 'b' (1)>

Linked node Routes:
  'f'
    <Node 'f' (4)>
  'c'
    <Node 'c' (3)>
    <Node 'c' (1)>
  'a'
    <Node 'a' (3)>
  'm'
    <Node 'm' (3)>
  'p'
    <Node 'p' (2)>
    <Node 'p' (1)>
  'b'
    <Node 'b' (1)>
    <Node 'b' (1)>
    <Node 'b' (1)>

Print all frequent pattern combinations of the tree:
(['f'], 4)
(['c'], 4)
(['f', 'c'], 3)
(['a'], 3)
(['f', 'a'], 3)
(['c', 'a'], 3)
(['f', 'c', 'a'], 3)
(['m'], 3)
(['f', 'm'], 3)
(['c', 'm'], 3)
(['f', 'c', 'm'], 3)
(['a', 'm'], 3)
(['f', 'a', 'm'], 3)
(['c', 'a', 'm'], 3)
(['f', 'c', 'a', 'm'], 3)
(['p'], 3)
(['c', 'p'], 3)
(['b'], 3)
