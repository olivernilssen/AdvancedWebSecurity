import binascii
import math as m
from math import log2
import hashlib

# Build the tree using a list of nodes and a list of only the parents 
# recursively until we reach the root node
def build_tree(nodes, parents, count):
    if(len(parents) == 1):
        return nodes

    new_parent_nodes = []
    for i in range(0, len(parents), 2):
        # Get the first and second parent and concat them 
        hash1, hash2 = bytearray(parents[i]), bytearray(parents[i + 1])
        new_parent = hashlib.sha1(hash1 + hash2)
        new_parent = bytearray(new_parent.digest())
        
        # Add the new concat'ed sha to all nodes 
        # and to the "new parents list"
        nodes.append(new_parent)
        new_parent_nodes.append(new_parent)
    
    # If the there are more than 1 new parent and 
    # if the length is not an even number, add the last node to make it even
    if len(new_parent_nodes) != 1 and len(new_parent_nodes) % 2 != 0: 
        nodes.append(new_parent_nodes[-1])
        new_parent_nodes.append(new_parent_nodes[-1])
    
    return build_tree(nodes, new_parent_nodes, count)


# Find out how many nodes are in each "depth"
# it will be halved each increase in depth of the tree, until reaching root which has 1 node
def find_nodes_depth(number_leaves, depth):
    if number_leaves % 2 == 0: 
        nodes_in_depth = [number_leaves]
    else: 
        nodes_in_depth = [number_leaves + 1]
    
    for i in range (1, depth + 1): 
        number_of_nodes = nodes_in_depth[i-1] // 2
        if (number_of_nodes != 1 and number_of_nodes % 2 != 0):
            number_of_nodes += 1
        nodes_in_depth.append(number_of_nodes)
    return nodes_in_depth


def build_path(tree, index, depth, number_leaves):
    path_list = []
    starting_index = 0
    nodes_depth = find_nodes_depth(number_leaves, depth)
    
    # go through the nodes and find the correct one
    # when found, append R or L to the hexadecimal
    for node in range(depth):
        current = index + starting_index
        if(current % 2 == 0):
            this_node = "R" + binascii.hexlify(tree[current + 1]).decode('utf-8')
        else: 
            this_node = "L" + binascii.hexlify(tree[current - 1]).decode('utf-8')
        path_list.append(this_node)
        index = (current - starting_index) // 2
        starting_index += nodes_depth[node]
    
    # return list of path from provided index (sibling)
    return list(reversed(path_list))

def checkfile(leaves):
    # If the amount of leaves are uneven, add last node again
    i = int(leaves.pop(0))
    j = int(leaves.pop(0))

    # Add the last node if amount of nodes is an odd number
    if(len(leaves) % 2 == 1):
        leaves.append(leaves[-1])

    number_leaves = len(leaves)
    depth = m.ceil(log2(number_leaves))

    # first build tree, then use tree to find the sibling
    tree = build_tree(leaves, leaves, 0)
    path = build_path(tree, i, depth, number_leaves)

    return path[j-1] + binascii.hexlify(tree[-1]).decode('utf-8')

if __name__ == '__main__':
    file = open('leaves5.txt') #choose input file here

    leaves = [] #0 = i, 1 = j, 2++ = leaves

    for i, line in enumerate(file): 
        if (i == 0 or i == 1):
            leaves.append(line.strip())
        else: 
            leaves.append(bytearray(binascii.unhexlify(line.strip())))

    print(f"Given node + root node: \n{checkfile(leaves)}")