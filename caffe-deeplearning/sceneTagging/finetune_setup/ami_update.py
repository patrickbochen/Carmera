#updates path names in environment for given image ids
#Entire path names needed for caffe training
pathname = "/home/scene/caffe/data/scene/images/"

#Input files
train_file_name = "train_2.txt"
test_file_name = "test_2.txt"

#Output files
updated_train_file = "trainAMI2.txt"
updated_test_file = "testAMI2.txt"

read = open(train_file_name,'r')
write = open(updated_train_file, 'w+')
for line in read:
    line = pathname + line
    write.write(line)
read.close()
write.close()


read = open(test_file_name,'r')
write = open(updated_test_file, 'w+')
for line in read:
    line = pathname + line
    write.write(line)
read.close()
write.close()
