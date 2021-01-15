# takes a dictionary of input then XOR it depending on the given b
def broadcast_message(info):
    #XOR the two data messages from A and B
    broadcast = info['DA'] ^ info['DB']
    data = info['SA'] ^ info['SB']

    broadcast = (hex(broadcast ^ info['M'])[2:].zfill(4) if info['b'] == 1 
                    else hex(data)[2:].zfill(4) + hex(broadcast ^ data)[2:].zfill(4))

    return broadcast.upper() #output as capital letter hexadecimal

if __name__ == "__main__":
    file = open("quiz_input.txt", "r")

    info = {}

    for line in file: 
        line = line.strip().split()

        #turn input into int unless it's b
        info[line[0].strip(":")] = (int(line[1], 16) if line[0] != 'b' else int(line[1]))

    message = broadcast_message(info)
    print(f"Broadcast: {message}")
    