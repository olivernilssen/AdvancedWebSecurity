from random import randint, randrange
import hashlib
from collections import defaultdict

def check_collision(zeros, ones):
    collisions = 0
    for value in zeros:
        if value in ones: 
            collisions += 1

    return collisions
def commit_votes():
    v = 0
    zero_set = set()
    ones_set = set()
    collisions_list = defaultdict()
    zero_coll = 0

    print("Running: |", end="", flush=True)

    for l in range(1, LENGTH_X):
        for k in range(1, 2**LENGTH_K):
            concat_0 = str(0) + str(k)
            concat_1 = str(1) + str(k)

            hash_cc_zeros = hashlib.sha1(concat_0.encode()).hexdigest()
            hash_cc_ones = hashlib.sha1(concat_1.encode()).hexdigest()

            binary_zeros = (bin(int(hash_cc_zeros, 16))[2:])[-l:]
            binary_ones = (bin(int(hash_cc_ones, 16))[2:])[-l:]

            zero_set.add(binary_zeros)
            ones_set.add(binary_ones)

        collisions = check_collision(zero_set, ones_set)
        collisions_list[collisions] = len(zero_set)

        if(collisions == 0):
            zero_coll += 1
            if zero_coll == 5:
                break

        collisions = 0
        print("-"*round((l/LENGTH_X)), end='', flush=True)

    print("|")
    return collisions_list

def print_probability(col_list):
    coll_list_copy = col_list.copy()
    i = 0
    for key, value in coll_list_copy.items():
        coll_percentage = 100*(key/value)
        print(f"Length of X: {i} Nr. collisions: {key} \tProbability: {coll_percentage}%")
        i += 1

if __name__ == "__main__":    
    # Globals
    LENGTH_X = 40
    LENGTH_K = 16

    print("__START COMMIT PHASE__")
    
    collision_list = commit_votes()
    print_probability(collision_list)

