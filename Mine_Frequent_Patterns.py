# -*- coding: utf-8 -*-
"""
Created on Wed Nov 1 19:14:54 2017

@author: Yuen Hoi, Lau
"""

import pandas as pd
from collections import defaultdict, namedtuple

#load data from a file
transactionDB = pd.read_csv("transactionDB.csv")

"""
The example 'transactionDB.csv' has two columns 'TID' and 'Items' respectively:
    
TID        Items 
100	 f,a,c,d,g,i,m,p
200      a,b,c,f,l,m,o
300	 b,f,h,j,o
400	 b,c,k,s,p
500	 a,f,c,e,l,p,m,n

"""

transactions = transactionDB["Items"]

def sorted_frequent_items(transactions, threshold=1):
    items_with_frequency= defaultdict(lambda: 0)      
    for eachTransaction in transactions:
        for item in eachTransaction:
            items_with_frequency[item] += 1
    if ',' in items_with_frequency:
        del items_with_frequency[',']

    
    items={}    
    for item, frequency in items_with_frequency.items() :
        if frequency >= threshold:
            items.update({item:frequency})
                    
    sorted_items = sorted(items.items(), key=lambda d: d[1], reverse=True)
     
    return sorted_items   
                      
def list_OrderedFI(transactions,threshold):
    '''return ordered frequent items in each transaction'''
    FI =sorted_frequent_items(transactions, threshold)
    Ordered_FI = [[]]*len(transactions)
    for i in range(len(transactions)):   
        for j in range(len(FI)):
            if FI[j][0] in transactions[i]:
                if Ordered_FI[i] == []:
                    Ordered_FI[i]=[FI[j][0]]
                else:
                    Ordered_FI[i].append(FI[j][0])
    return Ordered_FI

def mine_frequent_patterns(tree, threshold, suffix):
    for item, nodes in tree.items():
        support = sum(n.count for n in nodes)
            
        if support >= threshold and item not in suffix:
            found_set = [item] + suffix
            yield (found_set, support)
                
            cond_tree = conditional_FPtree(tree.prefix_paths(item))
            for s in mine_frequent_patterns(cond_tree, threshold, found_set):
                yield s
     
class Node(object):

    def __init__(self, tree, item, count=1):

        self._tree = tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._linkedNode = None

    def addChild(self, child):
        """Add a child node to the node you are specifying."""

        if not child.item in self._children:
            self._children[child.item] = child
            child.parent = self
            
    def search(self, item):
        """
        Search for a child of this node.
        """
        try:
            return self._children[item]

        except KeyError:
            return None
        
    @property
    def tree(self):
        return self._tree

    @property
    def item(self):
        return self._item

    @property
    def count(self):
         return self._count

    def increment(self):
        if self._count is None:
            raise ValueError("Root nodes have no associated count.")
        self._count += 1

    @property
    def root(self):
        return self._item is None and self._count is None

    @property
    def leaf(self):
        return len(self._children) == 0

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):

        if value and value.tree is not self.tree:
            raise ValueError("Cannot have a parent from another tree.")

        self._parent = value

    @property
    def linkedNode(self):
        return self._linkedNode

    @linkedNode.setter
    def linkedNode(self, node):
        if node and node.tree is not self.tree:
            raise ValueError("Cannot have a neighbor from another tree.")

        self._linkedNode = node

    @property
    def children(self):
        return tuple(self._children.values())

    def printSelfnChildren(self, depth=0):
        print (('  ' * depth) + repr(self))
        for child in self.children:
            child.printSelfnChildren(depth + 1)

    def __repr__(self):
        if self.root:
            return "<%s (root)>" % type(self).__name__
        return "<%s %r (%r)>" % (type(self).__name__, self.item, self.count)


class Tree(object):

    Route = namedtuple('Route','head tail') # the tuple containing the head and tail nodes of a node link

    def __init__(self):
        self._root = Node(self, None, None)  # The root node of the tree.
        self._nodeLinkRoutes = {} # The routes of linked nodes 

    @property
    def root(self):
        return self._root

    def addTransaction(self, transaction):
        point = self._root

        for item in transaction:
            next_point = point.search(item)
            if next_point:
                next_point.increment() # increase the count by 1 if there exists this node

            else:
                # Create a new point and add it as a child of the point we're currently looking at.
                next_point = Node(self, item)
                point.addChild(next_point)

                # Update the route of nodes that contain this item to include our new node.
                self.update_nodeLinkRoute(next_point)
            point = next_point

    def update_nodeLinkRoute(self, point):

        assert self is point.tree

        try:
            route = self._nodeLinkRoutes[point.item]
            route[1].linkedNode = point # route[1] is the tail
            self._nodeLinkRoutes[point.item] = self.Route(route[0], point)

        except KeyError:
            # First node for this item; start a new route.
            self._nodeLinkRoutes[point.item] = self.Route(point, point)

    def items(self):
        """
        Generate items and their linked nodes
        """
        for item in self._nodeLinkRoutes.keys():
            yield (item, self.linkedNodes(item))

    def linkedNodes(self, item):
        """
        Generate the sequence of nodes that contain the given item.
        """
        try:
            node = self._nodeLinkRoutes[item][0]

        except KeyError:
            return

        while node:
            yield node
            node = node.linkedNode

    def prefix_paths(self, item):
        """Generate the prefix paths that end with the given item."""
        def collect_path(node):
            path = []
            while node and not node.root:
                path.append(node)
                node = node.parent

            path.reverse()
            return path

        return (collect_path(node) for node in self.linkedNodes(item))

    def printTree(self):
        print ('Tree:')
        self.root.printSelfnChildren(1)

        print()
        print( 'Linked node Routes:')

        for item, nodes in self.items():
            print ('  %r' % item)
            for node in nodes:
                print ('    %r' % node)

def conditional_FPtree(paths):
    """Build a conditional FP-tree from the given prefix paths."""
    tree = Tree()
    condition_item = None
    items = set()

    # Import the nodes in the paths into the new tree. Only the counts of the leaf notes matter; the remaining counts will be reconstructed from the leaf counts.
    for path in paths:
        if condition_item is None:
            condition_item = path[-1].item
        point = tree.root

        for node in path:
            next_point = point.search(node.item)
            if not next_point:
                # Add a new node to the tree.
                items.add(node.item)
                count = node.count if node.item == condition_item else 0
                next_point = Node(tree, node.item, count)
                point.addChild(next_point)
                tree.update_nodeLinkRoute(next_point)
            point = next_point
   
    assert condition_item is not None

    # Calculate the counts of the non-leaf nodes.
    for path in tree.prefix_paths(condition_item):
        count = path[-1].count
        for node in reversed(path[:-1]):
            node._count += count
    
    return tree
  
    
#####  Implementation  #####
if __name__=='__main__':
    
    OrderedFI = list_OrderedFI(transactions,threshold=3) # Ordered frequent items in each transaction
    Atree=Tree()
    for i in range(len(OrderedFI)):
        Atree.addTransaction(OrderedFI[i])
    Atree.printTree()#print the tree with threshold=3
    
    print()
    print('Print all frequent pattern combinations of the tree:')
    for i in mine_frequent_patterns(Atree,threshold=3,suffix=[]):
        print(i) #print all frequent patterns of the tree

       
    BTree=conditional_FPtree(Atree.prefix_paths('b')) #construct a conditional FP tree with paths ending with 'm'
    print()
    print('Conditional tree: ')
    BTree.printTree() # print the conditional tree
    
    print()
    print('Print all frequent pattern combinations of the conditional tree:')
    for j in mine_frequent_patterns(BTree,threshold=3,suffix=[]):
        print(j) #print all frequent patterns of the conditional tree
