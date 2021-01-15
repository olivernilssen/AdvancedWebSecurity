from scipy import interpolate 
from _pydecimal import Decimal

def read_input(filename):
    fd = open(filename, "r")
    k = int(fd.readline().split(":")[1].strip())
    n = int(fd.readline().split(":")[1].strip())

    print(f"Threshold scheme: ({k},{n})")

    # Get Poly from input file
    tp = fd.readline().split("=")[1].strip().split("+")
    p = split_poly(tp)

    print(f"Polynominal: {p}")

    # Get shared (s)ecret from input file
    s = []
    for si in range (n-1):
        si = fd.readline().split("=")[1].strip()
        s.append(int(si))
    
    print(f"Shared points {s}")

    # Get revealed (m)aster points from collaboration
    # And collaborators id
    m = []
    for mi in range(k-1):
        mi = fd.readline().split("=")
        m.append([int(mi[0].strip("f()")),  int(mi[1].strip())])

    print(f"Collaborates {m}")

    return k, n, p, s, m


def split_poly(poly):
    p = []
    for s in poly: 
        if("^" in s):
            s = s.split('^')
            p.append([int(s[0].strip('x')), int(s[1].strip())])
        else:
            p.append(int(s.strip('x')))
    
    return p


def find_our_secret(poly):
    # return lambda x: sum([poly[i]*x**i for i in range(len(poly))])
    return lambda x: sum([val[0]*x**val[1] if isinstance(val, list) else val*x**i for i, val in enumerate(poly)])
    

def find_secret_code(k, poly, shares, master_shares): 
    # Combines shares using  
    # Lagranges interpolation.  
    # Shares is an array of shares 
    # being combined 
    master_poly = find_our_secret(poly)
    our_master = master_poly(1)

    # Append our master share into the list of shares
    master_shares.insert(0, [1, (sum(shares) + our_master)])
    
    if (len(master_shares) < k): 
        print("\n____Too few secrets for scheme____")
        return 0 
    
    sums, prod_arr = 0, [] 

    # Refrence: https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/

    for j in range(len(master_shares)): 
        xj, yj = master_shares[j][0],master_shares[j][1] 
        prod = Decimal(1)
          
        for i in range(len(master_shares)): 
            xi = master_shares[i][0] 
            if i != j: prod *= Decimal(Decimal(xi)/(xi-xj)) 
                  
        prod *= yj 
        sums += Decimal(prod) 
          
    return int(round(Decimal(sums),0)) 

if __name__ == "__main__":
    print("__Take input__")

    # Read and assign values from input file
    k, n, p, s, m = read_input("input3.txt")
    
    # find deactivation code
    code = find_secret_code(k, p, s, m)

    print(f"Deactivation code: {code}")



    