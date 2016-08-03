#Counts number of unique image labels
unique_entries = {}
i = 0
f = open("unique.txt",'r')
for line in f:
    get_imageId = line.split(" ")
    line = get_imageId[0]
    line = line.replace(".jpg", "")
    line = int(line)
    
    if unique_entries.get(line):
        continue
    else:
        unique_entries.update({line:i})
        i += 1


for key in sorted(unique_entries):
    print ("%s: %s" % (key, unique_entries[key]))

print (i)

f.close()