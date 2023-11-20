import json
from typing import List

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  word      : str,
                  leftchild,
                  rightchild):
        self.key        = key
        self.word      = word
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "word": node.word,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)


# height
# Return the height of the tree rooted at root.
def height(root: Node) -> int:
    if (root == None):
        return 0
    return 1 + max(height(root.leftchild), height(root.rightchild))

# balanceFactor
# Return the balance factor of the tree rooted at root.
def balanceFactor(root: Node) -> int:
    return height(root.leftchild) - height(root.rightchild)

# rotateLeft
# Perform a single left rotation on the tree rooted at root.
# Return the new root.
def rotateLeft(root: Node) -> Node:
    newRoot = root.rightchild
    root.rightchild = newRoot.leftchild
    newRoot.leftchild = root

    return newRoot

# rotateRight
# Perform a single right rotation on the tree rooted at root.
# Return the new root.
def rotateRight(root: Node) -> Node:
    newRoot = root.leftchild
    root.leftchild = newRoot.rightchild
    newRoot.rightchild = root

    return newRoot

# rebalance
# Rebalance the tree rooted at root.
# Return the new root.
def rebalance(root: Node) -> Node:
    if (balanceFactor(root) > 1):
        if (balanceFactor(root.leftchild) < 0):
            root.leftchild = rotateLeft(root.leftchild)
        root = rotateRight(root)
    elif (balanceFactor(root) < -1):
        if (balanceFactor(root.rightchild) > 0):
            root.rightchild = rotateRight(root.rightchild)
        root = rotateLeft(root)

    return root

# insert
# For the tree rooted at root, insert the given key,word pair and then balance as per AVL trees.
# The key is guaranteed to not be in the tree.
# Return the root.
def insert(root: Node, key: int, word: str) -> Node:
    # if (root != None):
    #     print("Key: " + key)
    #     print("Root.key: " + root.key)
    if (root == None):
        return Node(key,word,None,None)
    if (int(key) < int(root.key)):
        root.leftchild = insert(root.leftchild, key,word)
    else:
        root.rightchild = insert(root.rightchild, key,word)

    return rebalance(root)

# stdInsert
# For the tree rooted at root, insert the given key,word pair as if the tree were a standard BST, with no balancing.
# Return the root.
def stdInsert(root: Node, key: int, word: str) -> Node:
    if (root == None):
        return Node(key,word,None,None)
    if (int(key) < int(root.key)):
        root.leftchild = stdInsert(root.leftchild, key,word)
    else:
        root.rightchild = stdInsert(root.rightchild, key,word)

    return root

# preordList
# For the tree rooted at root, find the preorder traversal.
# Return the list of [key,word] pairs.
def preordList(root: Node) -> List:
    if (root == None):
        return []
    else:
        return [[root.key, root.word]] + preordList(root.leftchild) + preordList(root.rightchild)

# bulkInsert
# The parameter items should be a list of pairs of the form [key,word] where key is an integer and word is a string.
# For the tree rooted at root, first insert all of the [key,word] pairs as if the tree were a standard BST, with no balancing.
# Then do a preorder traversal of the [key,word] pairs and use this traversal to build a new tree using AVL insertion.
# Return the root
def bulkInsert(root: Node, items: List) -> Node:
    for item in items:
        root = stdInsert(root, item[0], item[1])

    list = preordList(root)
    newRoot = None

    for item in list:
        newRoot = insert(newRoot, int(item[0]), item[1])

    return newRoot

# bulkDelete
# The parameter keys should be a list of keys.
# For the tree rooted at root, first tag all the corresponding nodes (however you like),
# Then do a preorder traversal of the [key,word] pairs, ignoring the tagged nodes,
# and use this traversal to build a new tree using AVL insertion.
# Return the root.
def bulkDelete(root: Node, keys: List[int]) -> Node:
    list = preordList(root)
    taggedList = []
    for item in list:
        if (item[0] not in keys):
            taggedList.append(item)

    newRoot = None
    for item in taggedList:
        newRoot = insert(newRoot, item[0], item[1])
        
    return newRoot

# searchList
# For the tree rooted at root, calculate the list of keys on the path from the root to the search_key,
# then appends the word associated with the search_key.
def searchList(root: Node, search_key: int) -> List:
    if (root == None):
        return []
    elif (search_key == root.key):
        return [root.key, root.word]
    elif (int(search_key) < int(root.key)):
        return [root.key] + searchList(root.leftchild, search_key)
    else:
        return [root.key] + searchList(root.rightchild, search_key)

# search
# For the tree rooted at root, calculate the list of keys on the path from the root to the search_key,
# including the search key, and the word associated with the search_key.
# Return the json stringified list [key1,key2,...,keylast,word] with indent=2.
# If the search_key is not in the tree return a word of None.
def search(root: Node, search_key: int) -> str:
    list = searchList(root, search_key)

    return json.dumps(list, indent=2)

# replace
# For the tree rooted at root, replace the word corresponding to the key search_key by replacement_word.
# The search_key is guaranteed to be in the tree.
# Return the root
def replace(root: Node, search_key: int, replacement_word:str) -> Node:
    if (root == None):
        return None
    elif (int(search_key) < int(root.key)):
        root.leftchild = replace(root.leftchild, search_key, replacement_word)
    elif (int(search_key) > int(root.key)):
        root.rightchild = replace(root.rightchild, search_key, replacement_word)
    else: # search_key == root.key
        root.word = replacement_word

    return root