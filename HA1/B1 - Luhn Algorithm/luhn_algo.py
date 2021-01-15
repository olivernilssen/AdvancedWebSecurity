#turn input from text file or user into a reversed list
#and find the missing number at the same time 
import sys

def create_list(cc):
    cc_list = list(cc.strip())
    cc_list = reversed(cc_list)
    
    cc_num = []
    x_index = 0

    for i, x in enumerate(cc_list):
        if(x == 'X'):
            cc_num.append(x)
            x_index = i
        elif(x == '\n'):
            continue
        else:
            cc_num.append(int(x))

    # Depending on which number is missing
    # Either bruteforce or run once to get the checksum
    if(x_index == 0):
        return find_checksum(cc_num, x_index)
    else:
        return bruteforce_missing(cc_num, x_index)

    
# Find the missing number by bruteforcing the 
# the luhn algorithm
def bruteforce_missing(cc, index):
    for i in range(0, 10):
        cc[index] = i
        result = calculate_sum(cc, index)
        if(result != 'x'):
            return i
                
    return "x" #if this returns, there is a bug in the code! :(


def find_checksum(cc, index):
    c = calculate_sum(cc, index)
    if c == 'x':
        return 'NaN' # This shouldn't be returned, it equals a bug somewhere 
    else:
        return c

    

def calculate_sum(cc, x_index):
    new_cc = list(cc)
    i = 1
    
    # Go through all the numbers and add them together
    for i in range(len(new_cc)):
        if(i == 0): continue
        
        if (i+1) % 2 == 0:
            new_digit = int(new_cc[i]) * 2
            if new_digit > 9:
                new_digit -= 9
            new_cc[i] = int(new_digit)
        else:
            new_cc[i] = int(new_cc[i])

    full_sum = 0
    checksum = 0

    # Find checksum depending on if it is the missing number or not
    if(x_index == 0):  
        digit_sum = sum(new_cc[1:])   
        checksum = (digit_sum % 10) 
        if (checksum != 0): #if the checksum is not 0, then we need to get the amount needed to make it zero
            checksum = 10-checksum
        full_sum = digit_sum + checksum
    else: 
        full_sum = sum(new_cc)
        checksum = new_cc[0]
        
    if full_sum % 10 == 0:
        return checksum
    else: 
        return 'x'



if __name__ == '__main__':
    f = open("quiz-test.txt", "r") # Input from file
    list_numbs = []

    # comment out if using stdin
    for i, lines in enumerate(f):
        list_numbs.append(create_list(lines))

    string_numb = str(''.join(str(n) for n in list_numbs))
    print("List of concat numbers \n" + string_numb)

