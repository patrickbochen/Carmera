#Outputs summary statistics about testing of 'safe' tag

network_output_file = 'sComparison.txt'

read = open(network_output_file,'r')

numMatch = 0 #Matches
numSafeMismatch = 0 #Streetscore classified as safe
numUnsafeMismatch = 0 #Streetscore classified as unsafe
numCoord= 0 #Total number of coordinates covered

#Number of safe and unsafe coordinates
numSafeStreet = 0
numUnsafeStreet = 0

#Radius assumptions
numMinRadius = 0
num100Radius = 0
num150Radius = 0

for line in read:
    if line == '\n':
    	continue
    else:

    	line = line.split()
        #print (line)

    	if line[3] ==  'Match':
            continue

        numCoord += 1
    	if line[3] == 'True':
            numMatch += 1
        else:
            if line[1] == 'Safe':
                numSafeMismatch += 1
            else:
                numUnsafeMismatch += 1

        if line[1] == 'Safe':
            numSafeStreet += 1
        else:
            numUnsafeStreet += 1

        if line[4] == '50':
            numMinRadius += 1
        elif float(line[4]) <= 100:
            num100Radius += 1
        else:
            num150Radius += 1


read.close()


print ('Number of coordinates covered: {}'.format(numCoord))

print ('Number of matches: {}'.format(numMatch))
print ('Percentage of matches: {}'.format(float(numMatch)/numCoord))

print ('\nNumber of safe, miscategorized coordinates: {}'.format(numSafeMismatch))
print ('Number of unsafe, miscategorized coordinates: {}'.format(numUnsafeMismatch))

print ('\nNumber of safe images: {}'.format(numSafeStreet))
print ('Number of unsafe images: {}'.format(numUnsafeStreet))

print ('\nNumber of coordinates with >= 15 images in 50 m radius: {}'.format(numMinRadius))
print ('Number of coordinates with >= 15 images in 100 m radius: {}'.format(num100Radius))
print ('Number of coordinates with >= 15 images in 150 m radius: {}'.format(num150Radius))



