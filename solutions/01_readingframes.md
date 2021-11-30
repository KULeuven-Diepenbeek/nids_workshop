ex0101

# open the file
f = open ("data/test.txt", "r")

# loop over all the lines
for l in f:
    line = l[:-1]
    if(line == "Zzz"):
        print("")
    else:
        print(line, end='')

# close the file
f.close()



