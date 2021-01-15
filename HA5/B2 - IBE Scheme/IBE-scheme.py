from jacobi import jacobi
from hashlib import sha1
import string

def PKG(email, p, q):
    # Calculate modulus
    n = p*q

    # Hash the identity
    a = sha1(email.encode('utf-8')).digest()
    a_int = int.from_bytes(a, 'big')

    # Keep hashing id until the jacobi symbol is not equal 1
    while jacobi(a_int, n) != 1:
        a = sha1(a).digest()
        a_int = int.from_bytes(a, 'big')

    # Calculate r based on the identity hash, p, q and n
    r = pow(a_int, (n + 5 - (p+q)) // 8, n)
    r2 = (r*r) % n

    # Check that r satisfies the requirements
    if r2 != (a_int % n) and r2 != (-a_int % n):
        raise Exception("Error deriving r!")

    # Return the private key and the hashed identity, fill with 0 if r is not 64 long
    r = hex(r)[2:].zfill(64)

    return (r, r2, a, n)

def decrypt(m, r2, a, n, r):
    msg = m.split('\n')
    dec_msg = []

    # First encode r back to integer
    r = int(r.encode('utf-8'), 16)

    # Calculate r2
    r2 = 2*r

    # Decrypt each message bit using jacobi symbol. -1 = 0, +1 = 1
    dec_msg = [0 if jacobi((int(m.encode('utf-8'), 16) + r2), n) == -1 else 1 for m in msg]

    # Join togheter to make string and turn binary to decimal
    a_string = "".join([str(integer) for integer in dec_msg])
    dec_int = int(a_string, 2)
    
    print(f'\nDecrypted msg in bin:\t ({a_string})_2')
    print(f"Decrypted msg in dec:\t ({dec_int})_10")

if __name__ == '__main__':
    in_file = open("input_3.txt", 'r')
    msg_file = open("msg_input_3.txt", 'r')

    m = msg_file.read()

    p = int(in_file.readline().strip().split()[1], 16)
    q = int(in_file.readline().strip().split()[1], 16)
    email = in_file.readline().strip().split()[1]

    print("Input values:")
    print(f"p: {p}\nq: {q}\nEmail: {email}")
    r, r2, a, n = PKG(email, p, q)

    print(f"\nPrivatekey: {r}\nHashed ID: {a.hex()}")
    # test if input is correct with the provided input
    # print("814a8c2282ca8f4d0f2b2b72dfeeee6e5e3d8f438c039bdb5d059550739fdcec" == r)

    dec_msg = decrypt(m, r2, a, n, r)