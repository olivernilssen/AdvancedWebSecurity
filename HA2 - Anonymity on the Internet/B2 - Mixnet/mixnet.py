from pcapfile import savefile
import gzip
import shutil
import ipaddress
from ipaddress import IPv4Address


def collect_data(pcap_file):
    destinations = set()
    all_sets_R = list()
    user_messaged, new_round = False, False

    # Remember to change file name if you want to use a differnt file
    with open(pcap_file, 'rb') as f_out:
        capfile = savefile.load_savefile(f_out, layers=2, verbose=False)
        f_out.close()

    for pkt in capfile.packets:
        # all data is ASCII encoded (byte arrays). If we want to compare with strings
        # we need to decode the byte arrays into UTF8 coded strings
        ip_src = pkt.packet.payload.src.decode('UTF8')
        ip_dst = pkt.packet.payload.dst.decode('UTF8')

        # Look for the IP of the user
        # or add new IP destinations to set
        if(ip_dst == mixIP):
            # Check the last batch if the user sent any messages, otherwise there is no 
            # point in adding the destinations collected
            if(new_round):
                if(user_messaged):
                    all_sets_R.append(destinations.copy())
                destinations.clear()
                user_messaged, new_round = False, False

            if (ip_src == userIP): user_messaged = True
        elif(ip_src == mixIP):
            new_round = True
            destinations.add(ip_dst)

    # To include the last set
    if(user_messaged):
        all_sets_R.append(destinations.copy())

    print(f"\nNumber of sets found: {len(all_sets_R)}\n")

    return all_sets_R

# Learning phase. Finding set's equal to number of partners 
def learning_phase(ocap_file):
    # Pop the first set into our list of Recievers
    all_sets = collect_data(pcap_file)
    list_of_R = [all_sets.copy().pop(0)]

    # Ref: https://grocid.net/2015/03/19/understanding-the-disclosure-attack/
    # Collects enough disjoint set's to be equal the number of partners we are looking for 
    for i in range(partners-1):
        for R in all_sets:
            flag = 0
            for L in list_of_R:
                if len(L.intersection(R)) != 0:
                    flag = 1
                    break
            if flag == 0:
                list_of_R.append(R)
                break
    
    return all_sets, list_of_R

# Excluding phase to find one partner in each set
def exluding_phase(all_sets, list_of_R):
    disjoint_sets = list_of_R.copy()
    
    for R in all_sets:
        disjoint_set = []
        for i in range(len(list_of_R)):
            if not(list_of_R[i].isdisjoint(R)):
                disjoint_set.append(i)

        if len(disjoint_set) == 1: 
            list_of_R[disjoint_set[0]] &= R

    partner_IPs = set.union(*list_of_R)

    print("Partner no. \t|\t Partner IP")
    for i, partner in enumerate(partner_IPs): 
        print(f"\t{i+1} \t|\t {partner}")

    return partner_IPs

# Calculate the sum (integer) of all the IP addresses that has been found
def calculate_sum(list_partners):
    total = 0
    for partner in list_partners: 
        total += int(IPv4Address(partner))
    
    return total
    

if __name__ == '__main__':
    all_IPs = {}

    # Change info in input file and name of pcap file before running (if needed)
    # Just copy paste the input into a txt file
    file = open('input_info.txt', 'r')
    pcap_file = "cia.log.5.pcap"

    # Collect data from the input file
    userIP = file.readline().split(":")[1].strip()
    mixIP = file.readline().split(":")[1].strip()
    partners = int(file.readline().split(":")[1].strip())


    print("\nNazir's IP \t|\t Mix's IP \t\t|\t Partners")
    print(f"{userIP} \t|\t {mixIP} \t|\t {partners}")

    all_sets, learned_set = learning_phase(pcap_file)
    partner_IPs = exluding_phase(all_sets, learned_set)
    int_sum = calculate_sum(partner_IPs)
    
    print(f"Integer sum of all partner IP's: {int_sum}")

