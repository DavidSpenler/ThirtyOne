listt = []
nlist = []
while len(listt) != 0:
    grt = listt[0]
    for item in listt:
        if item > grt:
            grt = item
    listt.remove(grt)
    nlist.append(grt)
print(nlist)
    
