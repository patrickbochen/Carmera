#Randomize output from database
#Better results for training 
#(same images not back to back, also randomizes order of tags)

import random

train_file_name = "trainAMI2.txt"
test_file_name = "testAMI2.txt"

lines = open(train_file_name).readlines()
random.shuffle(lines)
open(train_file_name, 'w').writelines(lines)

lines = open(test_file_name).readlines()
random.shuffle(lines)
open(test_file_name, 'w').writelines(lines)