#Outputs summary statistics about testing on 'safe' tags

network_output_file = 'safe_comparison.txt'

read = open(network_output_file,'r')

numMatch = 0 #Matches
numSafeMismatch = 0 #Streetscore classified as safe
numUnsafeMismatch = 0 #Streetscore classified as unsafe
numCoord= 0 #Total number of coordinates covered

#Number of safe and unsafe coordinates
numSafeStreet = 0
numUnsafeStreet = 0


for line in read:
    if line == '\n':
    	continue
    else:

    	line = line.split()

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


read.close()


print ('Number of coordinates covered: {}'.format(numCoord))

print ('Number of matches: {}'.format(numMatch))
print ('Percentage of matches: {}'.format(float(numMatch)/numCoord))

print ('\nNumber of safe, miscategorized coordinates: {}'.format(numSafeMismatch))
print ('Number of unsafe, miscategorized coordinates: {}'.format(numUnsafeMismatch))

print ('\nNumber of safe images: {}'.format(numSafeStreet))
print ('Number of unsafe images: {}'.format(numUnsafeStreet))


