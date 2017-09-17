import sys
import socket
import re
import random
import copy

#flag{ch3ck-exp3rian-dat3-b3for3-us3}
def generateCard(brand, last): # Last is only used for test requiring specified last digits
    card = ""
    luhn = 0
    cardLength = 15
    final = last % 10
    if brand == 'd': #Discover IIN (Issuer Identification Number)
        nums = [6,0,1,1]
    elif brand == 'm': #MasterCard IIN
        nums = [5,3,0,1,1,1]
    elif brand == 'v': #Visa IIN
        nums = [4,0,4,6,4,5]
    elif brand == 'a': #American Express IIN
        nums = [3,7,4,3,1,4]
        cardLength = 14 #American Express cards are 15 digits
    else:
        nums = [int(x) for x in str(brand)] #When first numbers are specified
    while len(nums) < cardLength: #Adds random numbers after IIN
        nums.append(random.randint(0,9))
    print(last) 
    if last != 0: #Sets last 3 non-check digits to specified numbers
        nums[14] = (last // 10) % 10
        nums[13] = (last // 100) % 10
        nums[12] = (last // 1000)
    cardLength -= 1
    cv = copy.deepcopy(nums) 
    while cardLength > -1: #Luhn's Algorithm
        nums[cardLength] = 2 * nums[cardLength]
        if nums[cardLength] >= 10:
            nums[cardLength] -= 9
        cardLength -= 2
    for digit in cv:
        card += str(digit)
    for digit in nums: 
        luhn += digit
    luhn = luhn % 10 #setting check digit
    luhn = 10 - luhn
    if luhn == 10:
        luhn = 0
    card += str(luhn)
    return card

def checkLuhn(cardIn): #Only used for checking generated numbers. Somewhat buggy - I think it fails on 15-digit numbers, but it worked consistently enough to get the flag after a few tries
    
    luhn = 0
    nums = [int(x) for x in str(cardIn)] # Due to the way numbers are retrieved from the string, the last two are the options 1 and 0, and must be removed
    del nums[-1]
    del nums[-1]
    cardLength = len(nums);
    i = cardLength - 2 #otherwise, run Luhn's as above
    while i > -1:
        nums[i] = 2 * nums[i]
        if nums[i] >= 10:
            nums[i] -= 9
        i -= 2
    print(nums)
    for digit in nums: 
        luhn += digit
    print(luhn)
    if luhn  % 10 == 0: #Adding the check digit should result in a multiple of ten
        return 1
    else:
        return 0

    

def con_to_server(): #server connection stuff
    target = "misc.chal.csaw.io"
    port = 8308

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.connect((target, port))
    return sock

if __name__ == "__main__":

    sock = con_to_server()

    while(True):
        out = "not set" #Required so that it doesn't try to run the main code when it needs to verify a given number
        problem = sock.recv(4096)
        print(problem)
        problem = str(problem)
        if "valid" in problem: #Is this credit card number valid?
            out = checkLuhn(int(filter(str.isdigit, problem)))
            out = str(out)
        elif "Discover" in problem: #Calls for when issuer is specified
            brand = 'd'
        elif "Visa" in problem:
            brand = 'v'
        elif "Master" in problem:
            brand = 'm'
        elif "American" in problem:
            brand = 'a'
        else: #When first or last digits are specified
            brand = int(filter(str.isdigit, problem)) 
        if "end" in problem and  brand > 10 and not "valid" in problem: #Ends in 4 digits
            while not out.endswith(str(brand % 10)): #Generate repeatedly until last digit matches
                   out = generateCard('v',brand)
                   print(out + "bad!\n")

        if brand < 10 and not "valid" in problem: #ends in 1 digit
            while not out.endswith(str(brand)): #Same as above
                   out = generateCard(brand,0)
                   print(out + "bad!\n") 
        if "not set" in out: #Prevents overwriting a validity check
            out = generateCard(brand,0)
        out = out + '\n'
        print(out)
        sock.sendall(out.encode('utf-8'))
        
        junk2 = sock.recv(20)
        print(junk2)
