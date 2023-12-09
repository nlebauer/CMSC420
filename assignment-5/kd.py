from __future__ import annotations
import json
import math
from typing import List
import statistics

# Datum class.
# DO NOT MODIFY.
class Datum():
    def __init__(self,
                 coords : tuple[int],
                 code   : str):
        self.coords = coords
        self.code   = code
    def to_json(self) -> str:
        dict_repr = {'code':self.code,'coords':self.coords}
        return(dict_repr)

# Internal node class.
# DO NOT MODIFY.
class NodeInternal():
    def  __init__(self,
                  splitindex : int,
                  splitvalue : float,
                  leftchild,
                  rightchild):
        self.splitindex = splitindex
        self.splitvalue = splitvalue
        self.leftchild  = leftchild
        self.rightchild = rightchild

# Leaf node class.
# DO NOT MODIFY.
class NodeLeaf():
    def  __init__(self,
                  data : List[Datum]):
        self.data = data

# KD tree class.
class KDtree():
    def  __init__(self,
                  k    : int,
                  m    : int,
                  root = None):
        self.k    = k
        self.m    = m
        self.root = root

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    # DO NOT MODIFY.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            if isinstance(node,NodeLeaf):
                return {
                    "p": str([{'coords': datum.coords,'code': datum.code} for datum in node.data])
                }
            else:
                return {
                    "splitindex": node.splitindex,
                    "splitvalue": node.splitvalue,
                    "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                    "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
                }
        if self.root is None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)
    
    # Helper function for split
    # Returns the range of the given dimension
    def get_range(self,leaf:NodeLeaf,dim:int) -> float:
        return max(leaf.data,key=lambda datum: datum.coords[dim]).coords[dim] - min(leaf.data,key=lambda datum: datum.coords[dim]).coords[dim]

    # Helper function for insert
    # Returns a splitting node and its children resulting from an overfull leaf node
    def split(self,leaf:NodeLeaf) -> NodeInternal:
        # Find the dimension with largest range
        ranges = []
        for i in range(self.k):
            ranges.append(self.get_range(leaf, i))
        splitindex = ranges.index(max(ranges))

        # Cycle sorting 
        leaf.data.sort(key=lambda x: x.coords[splitindex])
        # for i in range(self.k):
        #     leaf.data.sort(key=lambda x: x.coords[(splitindex + i) % self.k])

        med = statistics.median([x.coords[splitindex] for x in leaf.data]) + 0.0

        splitting = NodeInternal(splitindex,med,None,None)
        leftdata = []
        rightdata = []
        for x in leaf.data:
            if x.coords[splitindex] < med:
                leftdata.append(x)
            else: # Equals goes right
                rightdata.append(x)
        
        splitting.leftchild = NodeLeaf(leftdata)
        splitting.rightchild = NodeLeaf(rightdata)

        return splitting

    # Insert the Datum with the given code and coords into the tree.
    # The Datum with the given coords is guaranteed to not be in the tree.
    def insert(self,point:tuple[int],code:str):
        # Helper for insert
        # Finds where to insert recursively
        def insert_helper(curr:NodeInternal):
            if curr is None:
                return NodeLeaf([Datum(point,code)])
            elif isinstance(curr,NodeInternal):
                if point[curr.splitindex] < curr.splitvalue:
                    curr.leftchild = insert_helper(curr.leftchild)
                else:
                    curr.rightchild = insert_helper(curr.rightchild)
                return curr
            else: # curr is a leaf node
                curr.data.append(Datum(point,code))
                if len(curr.data) > self.m:
                    return self.split(curr)
                else:
                    return curr
                
        self.root = insert_helper(self.root)

    # Delete the Datum with the given point from the tree.
    # The Datum with the given point is guaranteed to be in the tree.
    def delete(self,point:tuple[int]):
        def delete_helper(curr:NodeInternal):
            if curr is None:
                return None
            elif isinstance(curr,NodeInternal):
                if point[curr.splitindex] < curr.splitvalue:
                    curr.leftchild = delete_helper(curr.leftchild)
                    if curr.leftchild is None:
                        return curr.rightchild
                else:
                    curr.rightchild = delete_helper(curr.rightchild)
                    if curr.rightchild is None:
                        return curr.leftchild
                return curr
            else: # curr is a leaf node
                for x in curr.data:
                    if x.coords == point:
                        curr.data.remove(x)
                        break
                if len(curr.data) == 0:
                    return None
                else:
                    return curr
        self.root = delete_helper(self.root)

    # Find the k nearest neighbors to the point.
    def knn(self,k:int,point:tuple[int]) -> str:
        # Use the strategy discussed in class and in the notes.
        # The list should be a list of elements of type Datum.
        # While recursing, count the number of leaf nodes visited while you construct the list.
        # The following lines should be replaced by code that does the job.

        # Helper for knn to get range of node in a dimension
        def get_range(node,dim:int) -> tuple[float]:
            if isinstance(node,NodeLeaf):
                return (min(node.data,key=lambda datum: datum.coords[dim]).coords[dim],max(node.data,key=lambda datum: datum.coords[dim]).coords[dim])
            else:
                return (min(get_range(node.leftchild,dim)[0],get_range(node.rightchild,dim)[0]),max(get_range(node.leftchild,dim)[1],get_range(node.rightchild,dim)[1]))
            
        # Helper to get bounding box of a node
        def get_bounding_box(node) -> tuple[tuple[float]]:
            if isinstance(node, NodeLeaf):
                return tuple([get_range(node,i) for i in range(self.k)])
            else: # Splitting node
                return tuple([min(get_bounding_box(node.leftchild)[i][0],get_bounding_box(node.rightchild)[i][0]),max(get_bounding_box(node.leftchild)[i][1],get_bounding_box(node.rightchild)[i][1])]  for i in range(self.k))
            # return tuple([get_range(node,i) for i in range(self.k)])
        
        # Helper to get d^2 to bounding box of a node
        def dist_to_bounding_box(point:tuple[int],node) -> float:
            box = get_bounding_box(node)
            return sum(max(0,box[i][0] - point[i],point[i] - box[i][1])**2 for i in range(self.k))
                    
        # Helper for knn to get d^2 between two points
        def dist_to_point(point1:tuple[int],point2:tuple[int]) -> float:
            return sum([(point1[i] - point2[i])**2 for i in range(self.k)])

        # KNN Helper
        # Recursively finds the k nearest neighbors
        def knn_helper(curr,leaveschecked:int,knnlist:List[Datum]):
            if curr is None:
                return (leaveschecked,knnlist)            
            if isinstance(curr,NodeLeaf):
                leaveschecked += 1
                for x in curr.data:
                    if len(knnlist) < k:
                        knnlist.append(x)
                    else:
                        if dist_to_point(point,x.coords) < dist_to_point(point,knnlist[-1].coords):
                            knnlist[-1] = x
                        if dist_to_point(point,x.coords) == dist_to_point(point,knnlist[-1].coords):
                            if x.code < knnlist[-1].code:
                                knnlist[-1] = x
                    knnlist.sort(key=lambda x: dist_to_point(point,x.coords))
                return (leaveschecked,knnlist)
            else: # curr is a splitting node
                d_left = dist_to_bounding_box(point,curr.leftchild)
                d_right = dist_to_bounding_box(point,curr.rightchild)

                if d_left <= d_right:
                    if len(knnlist) < k or d_left <= dist_to_point(point,knnlist[-1].coords):
                        leaveschecked,knnlist = knn_helper(curr.leftchild,leaveschecked,knnlist)
                    if len(knnlist) < k or d_right <= dist_to_point(point,knnlist[-1].coords):
                        leaveschecked,knnlist = knn_helper(curr.rightchild,leaveschecked,knnlist)
                else:
                    if len(knnlist) < k or d_right <= dist_to_point(point,knnlist[-1].coords):
                        leaveschecked,knnlist = knn_helper(curr.rightchild,leaveschecked,knnlist)
                    if len(knnlist) < k or d_left <= dist_to_point(point,knnlist[-1].coords):
                        leaveschecked,knnlist = knn_helper(curr.leftchild,leaveschecked,knnlist)
                
                return (leaveschecked,knnlist)

        leaveschecked = 0
        knnlist = []
        leaveschecked,knnlist = knn_helper(self.root,leaveschecked,knnlist)

        # The following return line can probably be left alone unless you make changes in variable names.
        return(json.dumps({"leaveschecked":leaveschecked,"points":[datum.to_json() for datum in knnlist]},indent=2))

# Testing block
# kd_tree = KDtree(5,2)
# kd_tree.insert((16,14,10,19,0),'JGS')
# kd_tree.insert((13,6,4,5,5),'SBQ')
# kd_tree.insert((9,1,7,4,3),'GQC')
# kd_tree.insert((6,16,17,9,14),'JHV')
# kd_tree.insert((18,10,13,17,7),'WWM')
# kd_tree.insert((19,17,15,8,4),'MQS')
# kd_tree.insert((12,9,2,10,11),'WGE')
# kd_tree.insert((0,7,5,7,17),'ZGI')
# kd_tree.insert((17,13,8,14,1),'AUN')
# kd_tree.insert((8,8,19,16,9),'EXB')
# kd_tree.knn(1,(9,10,11,3,18))