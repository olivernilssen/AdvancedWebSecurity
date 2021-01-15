from pcapfile import savefile


file_path ='cia.log.5.pcap'


# nazirIP = "159.237.13.37"
# mixIP = "94.147.150.188"
# nbrPartners = 2

nazirIP = "160.66.13.37"
mixIP = "204.177.242.216"
nbrPartners = 15


long_set = list()
batch_set = set()
source_set = set()
new_batch = False
# --------------------------------------- LEARNING PHASE --------------------------------------------------------------
# --------------------------------------- LOAD BATCHES
with open(file_path, 'rb') as testcap:
    capfile = savefile.load_savefile(testcap, layers=2, verbose=False)
    testcap.close()
    for pkt in capfile.packets:

        ip_src = pkt.packet.payload.src.decode('UTF8')
        ip_dst = pkt.packet.payload.dst.decode('UTF8')

        if ip_dst == mixIP:
            if new_batch:
                # We will see if the batch is worth adding to the collection
                if nazirIP in source_set:
                    long_set.append(batch_set.copy())
                batch_set.clear()
                source_set.clear()
                new_batch = False
            source_set.add(ip_src)
        elif ip_src == mixIP:

            # Some sort of trigger for the new batch, though the new batch started earlier
            new_batch = True
            batch_set.add(ip_dst)
    # Last batch is skipped otherwise
    if nazirIP in source_set:
        long_set.append(batch_set.copy())

    print(len(long_set))

#------------create disjoint set----------------------


# Create Mutually Exclusive Sets
union_set = long_set.copy().pop(0)
disjoint_sets = [union_set]
for batch in long_set:
    if len(disjoint_sets) == nbrPartners:
        break
    elif union_set.isdisjoint(batch):
        disjoint_sets.append(batch)
        union_set = union_set.union(batch)

print(len(disjoint_sets))
partners = list()



for r in long_set:
    for i, ri in enumerate(disjoint_sets):
        disjoint = True

        if ri.intersection(r):

            #rest_union = union_set.difference(ri)

            for rj in disjoint_sets:

                if not r.isdisjoint(rj) and not rj == ri:
                    disjoint = False

            if disjoint:
                ri = ri.intersection(r)
                disjoint_sets[i] = ri
    
    done = True
    for batch in disjoint_sets:
        if len(batch) != 1:
            done = False
    if done:
        break

for disj in disjoint_sets:
    print("'Singleton' length:", len(disj), disj)



dec_sum = 0

# Should be a Singleton at this point, otherwise input data is too small
for singelton in disjoint_sets:
    partner = next(iter(singelton))

    ipSplit = partner.split(".")
    hexnum = "0x"
    for num in ipSplit:
        temp = hex(int(num))[2:]
        temp = (2 - len(temp)) * "0" + temp
        hexnum += temp

    dec_sum += int(hexnum, 16)

print(dec_sum)


