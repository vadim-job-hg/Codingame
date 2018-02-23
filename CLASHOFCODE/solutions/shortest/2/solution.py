r=input
n,l,w = int(r()),'',{5:'methane',8:'ethane',11:'propane',14:'butane',17:'pentane'}
for i in range(n):l+=r()
print(w.get(l.count('C')+l.count('H'), 'NONE'))