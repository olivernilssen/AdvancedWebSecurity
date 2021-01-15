#!/usr/bin/python3
import socket
from random import randrange
from hashlib import sha1
from binascii import unhexlify
from functools import reduce

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
soc.connect(("eitn41.eit.lth.se", 1337))


def sock_send(message):
    soc.send(format(message, 'x').encode('utf8'))

def sock_recv():
    response = soc.recv(4096).decode('utf8').strip()
    return response


##########################
#### D-H Key Exchange ####
##########################
def DHKE(p, g):
    values = {'g_x1':0, 'g_x2':0}

    for key in values:
        values[key] = sock_recv
        print(f'{key} recieved')
    
    ## receive g**x1
    # receive the hex-string, decode, and remove trailing '\n'
    g_x1 = sock_recv()
    print(f"g_x1 recieved: {g_x1}")

    # interpret as a number
    g_x1 = int(g_x1, 16)
    
    # generate g**x2, x2 shall be a random number
    x2 = randrange(2, p)
    
    # calculate g**x2 mod p
    g_x2 = pow(g, x2, p)

    # send it
    sock_send(g_x2)
    
    # read the ack/nak. This should yield a nak due to x2 being 0
    print ('\nSent g_x2:', sock_recv())
    
    #create DH key
    shared_key = I2OSP(pow(g_x1, x2, p))

    print(f"DH KEY created...\n")
    return shared_key

def SMP(DH_key, g1, passphrase):
    #Shared secret, g^xy || passphrase and hashed
    y = int(sha1(DH_key + passphrase).hexdigest(), 16)

    print("___STARTING SMP PROTOCOL___\n")
    #Get g2_a2 from server and turn it into an int
    g1_a2 = sock_recv()
    print(f"Recv g1_a2")
    g1_a2 = int(g1_a2, 16)
    
    #create random from prime p
    b2 = randrange(2, p)

    #create g1_b2
    g1_b2 = pow(g1, b2, p) 

    #Send g1_b2
    sock_send(g1_b2)
    #Ack msg
    print(f"Send g1_b2: {sock_recv()}\n")

    #generate g2
    g2 = pow(g1_a2, b2, p)

    #Get g1_a3 from server and turn it into an int
    g1_a3 = sock_recv()
    print(f"Recv g1_a3")
    g1_a3 = int(g1_a3, 16)

    #Creat random from prime p
    b3 = randrange(2, p)
    
    #create g1_b3
    g1_b3 = pow(g1, b3, p)

    #send g1_b3 to server
    sock_send(g1_b3)
    #Ack msg
    print(f"Sent g1_b3: {sock_recv()}\n")

    #calculate g3 
    g3 = pow(g1_a3, b3, p)

    #Calculate random value a
    b = randrange(2, p)

    # Calculate Pa and Qa. Pb = g3^b and Qb = g1^b*g2^x -> x == dh key
    P_b = pow(g3, b, p)
    Q_b = pow(g1, b, p)*pow(g2, y, p)

    # Get Pa  from server and turn it into an int
    P_a = sock_recv()
    print(f"Recv P_a")
    P_a = int(P_a, 16)

    # Send values to server
    sock_send(P_b)
    # Ack msg for Pb
    print(f"Sent P_b: {sock_recv()}\n")

    #Resv Qa and turn it into an int
    Q_a = sock_recv()
    print(f"Recv Q_a")
    Q_a = int(Q_a, 16)

    #send Qb 
    sock_send(Q_b)
    #Ack msg for Qb
    print(f"Sent Q_b: {sock_recv()}\n")

    #Recv QaQb_a3 and turn it into an int
    R_a = sock_recv()
    print(f"Recv R_a")
    R_a = int(R_a, 16)

    Qb_inv = pow(Q_b, -1, p)
    R_b = pow(Q_a * Qb_inv, b3, p)

    #Send this value to server
    sock_send(R_b)
    #compare R_a and R_b
    print(f"Sent R_b: {sock_recv()}")
    print(f"Authenticated : {sock_recv()}")

    R_ab = pow(R_a, b3, p)
    P_b_inv = pow(P_b, -1, p)
    authenticated = R_ab == P_a * P_b_inv % p
    
    print('ACK', authenticated)
    return authenticated

def message(dh_key, msg):
    msg = I2OSP(0, len(dh_key) - len(msg)//2) + unhexlify(msg)
    encrypted_msg = bytes(m ^ dh for m, dh in zip(msg, dh_key))
    sock_send(int.from_bytes(encrypted_msg, byteorder='big'))
    print(f"Message from server: \n{sock_recv()}")
    

def I2OSP(x, xLen=None):
    if xLen is None: xLen = (x.bit_length() + 7) // 8
    
    digits = []
    
    while x: 
        digits.append(int(x % 256))
        x //= 256
    
    for i in range(xLen - len(digits)):
        digits.append(0)
    
    return bytes(digits[::-1])


if __name__ == "__main__":
    print("\n___DH KEY EXCHANGE___\n")

    # the p shall be the one given in the manual
    p = int('FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1' +
        '29024E088A67CC74020BBEA63B139B22514A08798E3404DD' +
        'EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245' +
        'E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED' +
        'EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D' +
        'C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F' +
        '83655D23DCA3AD961C62F356208552BB9ED529077096966D' +
        '670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF', 16)

    g = g1 = 2
    passphrase = "eitn41 <3".encode('utf8')
    msg = '7d5b5dc9cb3790cffeb5c58010e8573cdf8b3ec2'

    dh_key = DHKE(p, g)
    valid = SMP(dh_key, g1, passphrase)
    if(valid):
        message(dh_key, msg)


    