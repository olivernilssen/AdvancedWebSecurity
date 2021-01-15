import hashlib
from collections import defaultdict

# bit limit
k_limit = 16

# after 35 it stops converging
x_limit = 36

# v is either 1 or 0
v = 0
# Our dictionaries for v= 1 || 0
zero_dict = defaultdict(bool)
one_dict = defaultdict(bool)

# Collision list and collision counter
coll_list = list()
collisions = 0

# Some useful strings
concat = ""
hash_res = ""

for x_length in range(1, x_limit):

    v = 0
    zero_dict = defaultdict(bool)
    one_dict = defaultdict(bool)

    # Basically, the 16 bits are simulated, its not important that k is explicitly binary
    for k in range(2**k_limit):

        # We add space, though it makes no difference, but if v could be larger, "v0k0" could be equal to "v1k1",
        # though "v0 k0" is never equal to "v1 k1". Basically we avoid "false" collisions
        concat = str(v) + " " + str(k)

        hash_res = hashlib.sha1(concat.encode()).hexdigest()
        bin_res = (bin(int(hash_res, 16))[2:])[-x_length:]
        zero_dict[bin_res] = True

    v = 1

    for k in range(2**k_limit):

        concat = str(v) + " " + str(k)

        hash_res = hashlib.sha1(concat.encode()).hexdigest()
        bin_res = (bin(int(hash_res, 16))[2:])[-x_length:]
        one_dict[bin_res] = True

    for key in zero_dict:
        if one_dict[key]:
            collisions += 1

    coll_list.append(collisions)

    # No point to continue
    if collisions == 0:
        print("-"*20 + "\nBreaking at run " + str(x_length) + ": Reached 0 collisions\n" + "-"*20)
        break

    collisions = 0
    print("Running... |" + "-"*x_length + "%" + " "*(x_limit - x_length) + "|")

copy_coll_list = coll_list.copy()

# Printing result
for i in range(1, len(coll_list) + 1):
    colls = coll_list.pop(0)
    print("X length = " + str(i) + " "*(3 - len(str(i))) + " - " + "Number collisions = " + str(colls) + " "*(10 - len(str(colls)))
          + "Probability: " + str(100*colls/min(2**i, 2**k_limit)) + "%")
    # "\t\t Out of " + str(16**i) + " "*(70 - len(str(16**i))) + "values \t" +

print("\nRemaining values give probability 0%")
print("Writing to file output.txt....")


# File writing
f = open("output.txt", 'w+')
f.write("Probabilities (%): \n")
for i in range(1, len(copy_coll_list) + 1):
    colls = copy_coll_list.pop(0)
    f.write(str(100*colls/min(2**i, 2**k_limit)) + "\n")
f.close()
print("Finished writing the file")

# To break the binding property, we need to find a value k, where h(0,k1) = h(1,k2)