''' 
Instead of doing all the DER encoding in python, we use the built-in openssl asn1parse functions
Since we know that the error lies in n=pq, we can just parse the key, and recalculate n=pq
This way we will get the INTEGER version of the new values and we can then recreate the key

To start with, we can check the key in cmd: 
    > openssl rsa -check -in privkey.key 
        >RSA key error: n does not equal p q

We then parse the key to a readable textformal, which uses DER format
    > openssl asn1parse -in privkey.key > output.txt

Which will give us the values we are looking for.
Now we just need to parse through this file, find the values we need and 
put them into a new file which we will use to create our functioning private key

Using this: https://tls.mbed.org/kb/cryptography/asn1-key-structures-in-der-and-pem
we can see what each line in the output file refers too; n, p, q, e, d and so on. 
'''

# Remeber to change the input file depending on what you are reading
key_params = open('key-3-output.txt', 'r')

# Read through the first 3 lines which is not used
key_params.readline()
key_params.readline()
key_params.readline()

# Now read the rest of the values and save the hexadecimal info
pubExp = key_params.readline().strip().split(':')[3]
privExp = key_params.readline().strip().split(':')[3]
p = key_params.readline().strip().split(':')[3]
q = key_params.readline().strip().split(':')[3]
e1 = key_params.readline().strip().split(':')[3]
e2 = key_params.readline().strip().split(':')[3]
coeff = key_params.readline().strip().split(':')[3]

# Print them to check if it worked
print(f'PubExp: {pubExp}\nPrivExp: {privExp}\np: {p}\nq: {q}\ne1: {e1}\ne2: {e2}\ncoeff: {coeff}')

# now we need to turn all values into integers
pubExpInt = int(pubExp, 16)
privExpInt = int(privExp, 16)
pInt = int(p, 16)
qInt = int(q, 16)
e1Int = int(e1, 16)
e2Int = int(e2, 16)
coeffInt = int(coeff, 16)

# Recalculate n = q*p
nInt = pInt * qInt
print(f'\nNew n = {nInt}')

# Now we need to create a new asn1 text file
# remember to change the name so it does not overwrite old files
output = open('asn1-3.txt', 'w+')

output.write("asn1=SEQUENCE:rsa_key\n\n")
output.write("[rsa_key]\n")
output.write("version=INTEGER:0\n")
output.write(f"modulus=INTEGER:{nInt}\n")
output.write(f"pubExp=INTEGER:{pubExpInt}\n")
output.write(f"privExp=INTEGER:{privExpInt}\n")
output.write(f"p=INTEGER:{pInt}\n")
output.write(f"q=INTEGER:{qInt}\n")
output.write(f"e1=INTEGER:{e1Int}\n")
output.write(f"e2=INTEGER:{e2Int}\n")
output.write(f"coeff=INTEGER:{coeffInt}")

output.close()

# Now we need to go to cmd and use openssl again
''' 
    ----- We now need to recreate the key, DER encoded. 

    > openssl asn1parse -genconf asn1-test.txt -out new.der

    ---- test the key with: 
    > openssl rsa -in asn1.der -text -check -inform DER > key.pem

    ----- Now we need to remove the part thats is above: ----BEGIN to create our new privatekye

    ----- We can now try to decrypt the message

    > openssl base64 -d -in msg-3.txt > msg-3.bin
    > openssl rsautl -decrypt -in msg-3.bin -inkey key-3.pem

'''
