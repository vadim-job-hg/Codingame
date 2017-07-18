# https://www.codingame.com/ide/puzzle/chuck-norris
import sys
import math

def string2bits(st=''):
    return ' '.join(format(ord(x), 'b') for x in st)
     
    

def form_words(letter, strike):
    if letter == "1":
        result = "0 "
    else:
        result = "00 "
    return result + ("0"*strike)
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
omessage = []
message = input()
#print("{0}".format(message), file=sys.stderr)
last_num = ""
strike = 0
for letter in message:    
    nums = str(string2bits(letter))
    nums = ("0"*(7-len(nums)))+nums
    print("NUMBERS: {0}".format(nums), file=sys.stderr)    
    for i in range(0, len(nums)):
        if last_num != nums[i]:
            print("STRIKE: {0}".format(strike), file=sys.stderr)
            if strike>0:
                omessage.append(form_words(last_num, strike))
            strike = 0            
        last_num = nums[i]
        strike = strike + 1
print("STRIKE: {0}".format(strike), file=sys.stderr)
if strike>0:
    omessage.append(form_words(last_num, strike))                        
print("{0}".format(" ".join(omessage)))    
# Write an action using printtgreev8 *
# To debug: print("Debug messages...", file=sys.stderr)

#print(omessage)

