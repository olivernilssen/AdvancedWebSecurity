from hashlib import sha1
from binascii import hexlify, unhexlify
from math import ceil

"""
    MGF1 
"""
def MGF1(mgfSeed, maskLen):  
    mgfSeed = unhexlify(mgfSeed)
    T = bytes()
    sh = sha1()
    hLen = sh.digest_size

    if maskLen > (hLen << 32): 
        raise Exception ("Mask too long")

    for i in range(ceil(maskLen/hLen)):
        C = I2OSP(i, 4)
        T += sha1(mgfSeed + C).digest() 

    output = hexlify(T[:maskLen]).decode('utf-8')
    return output


"""
    I2OSP converts a nonnegative integer to an octet string of a
    specified length.
"""
def I2OSP(x, xLen):
    if x >= 256**xLen:
        raise ValueError("integer too long")
    
    digits = []
    
    while x: 
        digits.append(int(x % 256))
        x //= 256
    
    for i in range(xLen - len(digits)):
        digits.append(0)
    
    return bytes(digits[::-1])

def OEAP_encode(M, seed, k=128, L=b""):
    lHash = sha1(L).digest() 
    hLen = sha1().digest_size #lenght of hash 
    Mbytes = unhexlify(M) #unhexify the message

    if (len(M) > 2**61-1):
        raise Exception("Message too long")
    
    PS = I2OSP(0,  k - len(M) // 2 - 2 * hLen - 2)

    DB = lHash  + PS + I2OSP(1, 1) +  Mbytes
    dbMask = MGF1(seed, k-hLen-1)
    maskedDB = bytes(a ^ b for a, b in zip(unhexlify(dbMask), DB))
    
    seedMask = MGF1(hexlify(maskedDB), hLen)
    maskedSeed = bytes(a ^ b for a, b in zip(unhexlify(seed), unhexlify(seedMask)))
    EM = I2OSP(0, 1) +  maskedSeed + maskedDB
    
    return hexlify(EM)


def OAEP_decode(EM, k=128, L=b''):
    hLen = sha1(L).digest_size
    EM = unhexlify(EM)

    #extract the seed and DB from the long string
    maskedSeed = EM[1:hLen+1]
    maskedDB = EM[hLen+1:]
    
    #MGF the maskedDB and xor it wit the seedMask to get seed
    seedMask = MGF1(hexlify(maskedDB), hLen)
    seed = bytes(a ^ b for a, b in zip(maskedSeed, unhexlify(seedMask)))
    
    #MGF the seed to get dbMask, xor it with the maskedDB to get DB 
    dbMask = MGF1(hexlify(seed), k - hLen - 1)
    DB = bytes(a ^ b for a, b in zip(unhexlify(dbMask), maskedDB))[hLen:]

    #find the index where msg starts without padding (0x01)
    index_padding = DB.index(1) + 1
    M = DB[index_padding:]
    
    #Turn message into hexadecimal before sending
    return hexlify(M)

if __name__ == "__main__":
    seed = "54bacfd9ce645dad640fbd5b83123c2e3fa90f3b8fcb" #hex
    length = 22 #int
    mgf = MGF1(seed, length)

    # print(len(mgf))
    print(f"MGF: {mgf}\n")
    # print(compare == mgf)
    
    M = '30c34580753883e1f421f3a012476e14b25afed894448d65aa'
    seed = '1e652ec152d0bfcd65190ffc604c0933d0423381'

    encoded_message = OEAP_encode(M, seed)
    print(f"Encoded message: {encoded_message}\n")

    decoded_message = OAEP_decode(encoded_message)
    print(f"Decoded message: {decoded_message}\n")

    EM = '0043759f100e1b0ffbaed6b5e234f085cfd20cb94962f786195f85f8d337481f2abb06da0f3f9b1a5e413d31e347a179461d13c47b4f6893c02220932443e5764a02e5e0233d76bbdbc5c2e65c3dc014dd42a6532a2b5dcf4327381adfb17506a65397e78b611b2080a5d90a4818eea05072f5cc639ae55f1c7462da3621dcd0'
    decode = OAEP_decode(EM)
    print(f"Test message to decode: {decode} ")