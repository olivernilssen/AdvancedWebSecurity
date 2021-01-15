
import hashlib
import binascii

def hashPath(old_parent, path_parent):

    #Find position of new parent
    if(path_parent[0] == "R"):
        #concat it on the right side
        path_parent = path_parent[1:]
        concat_hash = old_parent + path_parent
    else:
        #concat it on the left side
        path_parent = path_parent[1:]
        concat_hash = path_parent + old_parent

    child = hashlib.sha1(bytearray.fromhex(concat_hash)).hexdigest()

    return child

if __name__ == '__main__':
    # Choose input file
    f = open('merkel_path_input.txt', 'r')

    # Go through file and concat input
    root_hash = b''
    i = 1
    for line in f:
        if(i == 1): 
            root_hash = line.strip()
            i = 2
        else:
            root_hash = hashPath(root_hash, line.strip())

    print(f"Root of the provided path is: {root_hash}")
