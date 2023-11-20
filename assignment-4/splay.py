from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

# DO NOT MODIFY!
class SplayTree():
    def  __init__(self,
                  root : Node = None):
        self.root = root

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    # DO NOT MODIFY!
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)
    
    # Helper functions
    # Rotate left
    def rotateLeft(self, root: Node):
        newRoot = root.rightchild
        if root:
            root.rightchild = newRoot.leftchild
            if newRoot.leftchild:
                newRoot.leftchild.parent = root
            newRoot.parent = root.parent
            if not root.parent:
                self.root = newRoot
            elif root == root.parent.leftchild:
                root.parent.leftchild = newRoot
            else:
                root.parent.rightchild = newRoot
            newRoot.leftchild = root
            root.parent = newRoot
    
    # Rotate right
    def rotateRight(self, root: Node):
        newRoot = root.leftchild
        if root:
            root.leftchild = newRoot.rightchild
            if newRoot.rightchild:
                newRoot.rightchild.parent = root
            newRoot.parent = root.parent
            if not root.parent:
                self.root = newRoot
            elif root == root.parent.rightchild:
                root.parent.rightchild = newRoot
            else:
                root.parent.leftchild = newRoot
            newRoot.rightchild = root
            root.parent = newRoot

    # Splay
    def splay(self, root: Node):
        while root.parent:
            if not root.parent.parent:
                # Zig
                if root == root.parent.leftchild:
                    self.rotateRight(root.parent)
                else:
                    self.rotateLeft(root.parent)
            # Zig-Zig
            # Left Left
            elif root == root.parent.leftchild and root.parent == root.parent.parent.leftchild:
                self.rotateRight(root.parent.parent)
                self.rotateRight(root.parent)
            # Right Right
            elif root == root.parent.rightchild and root.parent == root.parent.parent.rightchild:
                self.rotateLeft(root.parent.parent)
                self.rotateLeft(root.parent)
            # Zig-Zag
            # Left Right
            elif root == root.parent.rightchild and root.parent == root.parent.parent.leftchild:
                self.rotateLeft(root.parent)
                self.rotateRight(root.parent)
            # Right Left
            else:
                self.rotateRight(root.parent)
                self.rotateLeft(root.parent)

    # Search Helper
    def searchHelper(self, root: Node, key: int):
        if not root or root.key == key:
            return root
        # Key is greater than root: go right
        if key > root.key:
            if root.rightchild:
                return self.searchHelper(root.rightchild, key)
            else:
                return root
        # Key is less than root: go left
        else:
            if root.leftchild:
                return self.searchHelper(root.leftchild, key)
            else:
                return root                
    
    # Search for a node and return it, or the IOP/IOS if not found
    def searchNode(self,key:int):
        if not self.root:
            return None
        node = self.searchHelper(self.root, key)
        if node:
            self.splay(node)
        return node

    # Search
    def search(self,key:int):
        self.searchNode(key)

    # # BST Insert
    # def insertBST(self, root: Node, key: int):
    #     if not root:
    #         self.root = Node(key)
    #     elif key < root.key:
    #         if not root.leftchild:
    #             root.leftchild = Node(key)
    #             root.leftchild.parent = root
    #         else:
    #             self.insertBST(root.leftchild, key)
    #     else: # key > root.key
    #         if not root.rightchild:
    #             root.rightchild = Node(key)
    #             root.rightchild.parent = root
    #         else:
    #             self.insertBST(root.rightchild, key)

    # Insert Helper
    def insertHelper(self, key: int):
        self.search(key)
        if not self.root:
            self.root = Node(key)
        elif key > self.root.key:
            newRoot = Node(key)
            newRoot.rightchild = self.root.rightchild
            if self.root.rightchild:
                self.root.rightchild.parent = newRoot
            newRoot.leftchild = self.root
            self.root.parent = newRoot
            self.root.rightchild = None
            self.root = newRoot
        else: # key < self.root.key
            newRoot = Node(key)
            newRoot.leftchild = self.root.leftchild
            if self.root.leftchild:
                self.root.leftchild.parent = newRoot
            newRoot.rightchild = self.root
            self.root.parent = newRoot
            self.root.leftchild = None
            self.root = newRoot        

    # Insert Method 1
    def insert(self,key:int):
        self.insertHelper(key)
        # self.insertBST(self.root, key)

    # Delete Method 1
    def delete(self,key:int):
        root = self.searchNode(key)
        if root:
            if root.key == key:
                if not root.leftchild: # no left child
                    self.root = root.rightchild
                    if self.root:
                        self.root.parent = None
                elif not root.rightchild: # no right child
                    self.root = root.leftchild
                    if self.root:
                        self.root.parent = None
                else: # both children
                    left = root.leftchild
                    right = root.rightchild
                    self.root = right
                    self.root.parent = None
                    self.searchNode(key)
                    self.root.leftchild = left
                    self.root.leftchild.parent = self.root