# https://www.codingame.com/ide/puzzle/chuck-norris
def string2bits(st=''):
    return ' '.join(format(ord(x), 'b') for x in st)
     
def form_words(letter, strike):
    if letter == "1":
        result = "0 "
    else:
        result = "00 "
    return result + ("0"*strike)

omessage = []
message = input()
last_num = ""
strike = 0
for letter in message:    
    nums = str(string2bits(letter))
    nums = ("0"*(7-len(nums)))+nums
    for i in range(0, len(nums)):
        if last_num != nums[i]:
            if strike>0:
                omessage.append(form_words(last_num, strike))
            strike = 0            
        last_num = nums[i]
        strike = strike + 1
if strike>0:
    omessage.append(form_words(last_num, strike))                        
print("{0}".format(" ".join(omessage)))
