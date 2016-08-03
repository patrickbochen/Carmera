#Outputs statistics on the culmulative network output
#for each image examined during validation testing on 'safe' tag

network_output_file = 'sNetworkOutput.txt' #File containing network probabilities outputs

probabilities = [0] * 10 #Vector containing probabilities in increments of .1
read = open(network_output_file,'r')

number_output= 0 #Total number of images covered

for line in read:
    if line == '\n':
    	continue
    else:
    	line = line.split()

    	try:
    		line = line[2]
    	except Exception as e:
    		continue

    	if line ==  'Ids':
    		continue
    	else:
    		number_output += 1
    		line = float(line)
    		if line < .1:
    			probabilities[0] += 1
    		elif line < .2:
    			probabilities[1] += 1
    		elif line < .3:
    			probabilities[2] += 1
    		elif line < .4:
    			probabilities[3] += 1
    		elif line < .5:
    			probabilities[4] += 1
    		elif line < .6:
    			probabilities[5] += 1
    		elif line < .7:
    			probabilities[6] += 1
    		elif line < .8:
    			probabilities[7] += 1
    		elif line < .9:
    			probabilities[8] += 1
    		else:
    			probabilities[9] += 1
read.close()

print ('Number of images covered: {}'.format(number_output))

print ('\nNetwork Probability Totals')
print (probabilities)

print ('\nPercentage of images in every .1 probability distribution')
for prob in probabilities:
    print (float(prob)/number_output)

