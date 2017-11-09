# Frequent_Pattern_Tree
Mine frequent patterns from databases

# Reference
The program 'Mine Frequent Patterns.py' provides an implementation for the paper "Mining FrequentPatterns without Candidate Generation" by  Jiawei Han, Jian Pei, and Yiwen Yin.

# Data
The example 'transactionDB.csv' has two columns 'TID' and 'Items' respectively:<br>

    TID        Items
    100  f,a,c,d,g,i,m,p
    200  a,b,c,f,l,m,o
    300  b,f,h,j,o
    400  b,c,k,s,p
    500  a,f,c,e,l,p,m,n

# Implementation
Run the 'Mine_Frequent_Patterns.py' file. You can adjust the threshold value in the implementation section of the file to suit your needs.

    if __name__=='__main__':
 
        print('Sorted frequent items: ', sorted_frequent_items(transactions,3))#print the sorted frequent items
        print()

        OrderedFI = list_OrderedFI(transactions,threshold=3) # Ordered frequent items in each transaction
        Atree=Tree()
        for i in range(len(OrderedFI)):
            Atree.addTransaction(OrderedFI[i])
        Atree.printTree()#print the tree with threshold=3

        print()
        print('Print all frequent pattern combinations of the tree:')
        for i in mine_frequent_patterns(Atree,threshold=3,suffix=[]):
            print(i) #print all frequent patterns of the tree

        BTree=conditional_FPtree(Atree.prefix_paths('b')) #construct a conditional FP tree with paths ending with 'b'
        print()
        print('Conditional tree: ')
        BTree.printTree() # print the conditional tree

        print()
        print('Print all frequent pattern combinations of the conditional tree:')
        for j in mine_frequent_patterns(BTree,threshold=3,suffix=[]):
            print(j) #print all frequent patterns of the conditional tree

# Output
An example of the output of the program can be described in the following: <br>
The numbers '1, 2 ,3 ...' is the frequency of an item 'a,b,c,...'<br>

    Sorted frequent items:  [('f', 4), ('c', 4), ('a', 3), ('m', 3), ('p', 3), ('b', 3)]

    Tree:
      <Node (root)>
        <Node 'f' (4)>
          <Node 'c' (3)>
            <Node 'a' (3)>
              <Node 'm' (3)>
                <Node 'p' (2)>
                <Node 'b' (1)>
          <Node 'b' (1)>
        <Node 'c' (1)>
          <Node 'p' (1)>
            <Node 'b' (1)>

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

    Conditional tree: 
    Tree:
      <Node (root)>
        <Node 'f' (2)>
          <Node 'c' (1)>
            <Node 'a' (1)>
              <Node 'm' (1)>
                <Node 'b' (1)>
          <Node 'b' (1)>
        <Node 'c' (1)>
          <Node 'p' (1)>
            <Node 'b' (1)>

    Linked node Routes:
      'f'
        <Node 'f' (2)>
      'c'
        <Node 'c' (1)>
        <Node 'c' (1)>
      'a'
        <Node 'a' (1)>
      'm'
        <Node 'm' (1)>
      'b'
        <Node 'b' (1)>
        <Node 'b' (1)>
        <Node 'b' (1)>
      'p'
        <Node 'p' (1)>

    Print all frequent pattern combinations of the conditional tree:
    (['b'], 3)
