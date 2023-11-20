import json
from typing import List

# DO NOT MODIFY THIS CLASS!
class Node():
    def  __init__(self,
                  key        = None,
                  keycount   = None,
                  leftchild  = None,
                  rightchild = None):
        self.key        = key
        self.keycount   = keycount
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY THIS FUNCTION!
# For the tree rooted at root, dump the tree to stringified JSON object and return.
# NOTE: in future projects you'll need to write the dump code yourself,
# but here it's given to you.
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "keycount": node.keycount,
            "leftchild": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "rightchild": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

#---------------------------------------------------------------------------------------------------

# For the tree rooted at root and the key given:
# If the key is not in the tree, insert it with a keycount of 1.
# If the key is in the tree, increment its keycount.
def insert(root: Node, key: int) -> Node:
    if root is None: # empty tree
        return Node(key, 1)
    elif key == root.key: # key already in tree
        root.keycount += 1
    elif key < root.key: 
        root.leftchild = insert(root.leftchild, key)
    else: # key > root.key
        root.rightchild = insert(root.rightchild, key)
    return root

# For the tree rooted at root and the key given:
# If the key is not in the tree, do nothing.
# If the key is in the tree, decrement its key count. If they keycount goes to 0, remove the key.
# When replacement is necessary use the inorder successor.
def delete(root: Node, key: int) -> Node:
    if root is None: # empty tree
        return root
    elif key < root.key: 
        root.leftchild = delete(root.leftchild, key)
    elif key > root.key:
        root.rightchild = delete(root.rightchild, key)
    else: # key == root.key
        if root.keycount > 1: # key is root and keycount > 1
            root.keycount -= 1
        else: # key is root and keycount == 1
            if root.leftchild is None:
                temp = root.rightchild
                root = None
                return temp
            elif root.rightchild is None:
                temp = root.leftchild
                root = None
                return temp
            else: # root has two children, replace with inorder successor
                temp = inorder_successor(root.rightchild) # temporarily stores inorder successor
                root.key = temp.key # replace root key with inorder successor key
                root.keycount = temp.keycount # replace root keycount with inorder successor keycount
                count = temp.keycount 
                while count > 0: # deletes all instances of inorder successor
                    root.rightchild = delete(root.rightchild, temp.key)
                    count -= 1
    return root

# Find inorder successor of node.
# Helper method for delete.
def inorder_successor(node: Node) -> Node:
    if node.leftchild is None:
        return node
    else:
        return inorder_successor(node.leftchild)

# For the tree rooted at root and the key given:
# Calculate the list of keys on the path from the root towards the search key.
# The key is not guaranteed to be in the tree.
# Return the json.dumps of the list with indent=2.
def search(root: Node, search_key: int) -> str:
    return(json.dumps(search_list(root, search_key), indent=2))

# Helper method for search.
# Generates list of keys on path from root to search_key.
def search_list(root: Node, search_key: int) -> List[int]:
    if root is None:
        return []
    elif search_key == root.key:
        return [root.key]
    elif search_key < root.key:
        return [root.key] + search_list(root.leftchild, search_key)
    else: # search_key > root.key
        return [root.key] + search_list(root.rightchild, search_key)

# For the tree rooted at root, find the preorder traversal.
# Return the json.dumps of the list with indent=2.
def preorder(root: Node) -> str:
    return(json.dumps(preord_list(root), indent=2))

# Helper for preorder.
# Generates list of keys in preorder traversal.
def preord_list(root: Node) -> List[int]:
    if root is None:
        return []
    else:
        return [root.key] + preord_list(root.leftchild) + preord_list(root.rightchild)

# For the tree rooted at root, find the inorder traversal.
# Return the json.dumps of the list with indent=2.
def inorder(root: Node) -> str:
    return(json.dumps(inord_list(root), indent=2))

# Helper for inorder.
# Generates list of keys in inorder traversal.
def inord_list(root: Node) -> List[int]:
    if root is None:
        return []
    else:
        return inord_list(root.leftchild) + [root.key] + inord_list(root.rightchild)

# For the tree rooted at root, find the postorder traversal.
# Return the json.dumps of the list with indent=2.
def postorder(root: Node) -> str:
    return(json.dumps(postord_list(root), indent=2))

# Helper for postorder.
# Generates list of keys in postorder traversal.
def postord_list(root: Node) -> List[int]:
    if root is None:
        return []
    else:
        return postord_list(root.leftchild) + postord_list(root.rightchild) + [root.key]

# For the tree rooted at root, find the BFT traversal (go left-to-right).
# Return the json.dumps of the list with indent=2.
def bft(root: Node) -> str:
    if root is None:
        return json.dumps([])
    else:
        queue = [root]
        pathlist = []

        while (len(queue) > 0):
            node = queue.pop(0)
            pathlist.append(node.key)

            if node.leftchild is not None:
                queue.append(node.leftchild)
            if node.rightchild is not None:
                queue.append(node.rightchild)
    # Then tweak the next line so it uses your list rather than None.
    return json.dumps(pathlist, indent=2)