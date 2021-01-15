from random import randint, randrange
import hashlib
from collections import defaultdict
import matplotlib.pyplot as plt

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
    collisions_list = list()

    print("Running: |", end="", flush=True)

    for l in range(1, LENGTH_X):
        for k in range(2**LENGTH_K):
            concat_0 = str(0) + str(k)
            concat_1 = str(1) + str(k)

            hash_cc_zeros = hashlib.sha1(concat_0.encode()).hexdigest()
            hash_cc_ones = hashlib.sha1(concat_1.encode()).hexdigest()

            binary_zeros = (bin(int(hash_cc_zeros, 16))[2:])[-l:]
            binary_ones = (bin(int(hash_cc_ones, 16))[2:])[-l:]

            zero_set.add(binary_zeros)
            ones_set.add(binary_ones)

        collisions = check_collision(zero_set, ones_set)
        collisions_list.append(collisions)

        if(collisions == 0):
            break

        collisions = 0
        print("-"*round(LENGTH_X * l/(LENGTH_X-1)), end='', flush=True)

    print("|")
    return collisions_list

def print_probability(col_list):
    coll_list_copy = col_list.copy()
    for i in range(1, len(coll_list_copy) + 1):
        collisions = coll_list_copy.pop(0)
        coll_percentage = 100*collisions/min(2**i, 2**LENGTH_K) #halp
        print(f"Length of X: {i} Nr. collisions: {collisions} \tProbability: {coll_percentage}%")

def int_to_bytes(value, size, byteorder='big'):
    if(size is None):
        size = value.bit_length() + 7
    return bytearray(value.to_bytes(size, byteorder))

def bytes_to_int(byte_array):
    return int.from_bytes(byte_array, byteorder='big')

def hash_function(byte_array, size = None):
    if(type(byte_array) is int):
        byte_array = int_to_bytes(byte_array, size)
    hash_object = hashlib.sha1(byte_array)
    return bytearray(hash_object.digest())

def commit(v, k, X):
    v_k = int_to_bytes(v, size=1) + int_to_bytes(k, size=2)
    return bytes_to_int(hash_function(v_k)) % 2**X


def binding_break(X):
    v = randint(0,2)
    k = randint(0, 2**LENGTH_K)
    org_commit = commit(v, k, X)
    new_v = 1^v

    for i in range(2**LENGTH_K):
        new_commit = commit(new_v, i, X)
        if new_commit == org_commit:
            return 1
    return 0

def conceal_prob(X):
    v0, v1 = 0, 1
    v = randrange(0, 2)
    k = randrange(0, 2**16)
    s_commit = commit(v, k, X)

    commits = {0: [], 1: []}
    for i in range(2**16):
        c0 = commit(v0, i, X)
        c1 = commit(v1, i, X)
        if c0 == s_commit: commits[v0].append(c0)
        if c1 == s_commit: commits[v1].append(c1)
    return len(commits[v]) / (len(commits[v0]) + len(commits[v1]))

if __name__ == "__main__":    
    # Globals
    LENGTH_X = 40
    LENGTH_K = 16
    prob_binding_tot, prob_conceal_tot = [], []
    print("__START COMMIT PHASE__")
    print("Running:.. |", end='', flush=True)
    for X in range(0, 30):
        prob_binding = [binding_break(X) for l in range(5)]
        prob_conceal = [conceal_prob(X) for l in range(5)]
        prob_binding_tot.append(100*(sum(prob_binding) / len(prob_binding)))
        prob_conceal_tot.append(100*(sum(prob_conceal) / len(prob_conceal)))
        print("-"*round(10*30/100), end='', flush=True)

    print("|", end="")
    x = [X for X in range(0, 30, 1)]
    plt.plot(x, prob_binding_tot, label="Binding probability")
    plt.plot(x, prob_conceal_tot, label="Concealing probability")
    plt.ylabel('Prob. breaking scheme %')
    plt.xlabel('X commited bits')
    plt.legend(loc='best')
    plt.show()

    # collision_list = commit_votes()
    # print_probability(collision_list)