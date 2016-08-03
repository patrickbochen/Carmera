Train02

The files in this folder pertain to a network that has been trained on the following tags: safe, green, family friendly, beautiful, desolate, and vibrant. The output of the network is an array of probabilities that the image matches one of the following tags. The order of these probabilities is determined during training, where each distinct tag corresponds to a node in the output layer. There is a file in caffe/data/scene/train02 that lists the tags, whose physical order corresponds to the node position in the output layer.

The deploy.prototxt, train_val.prototxt, and solver.prototxt are files that are necessary for training and testing. They are the files that define the network structure and the solver parameters for training the network. Note I made a mistake during the training of the network. The output contains 8 nodes, but there are only 6 labels. However, because nothing was trained on the last two nodes they shouldn't be that consequently unless you are basing classification on the highest n scoring labels.

_iter_100000.caffemodel saves the weights of the model. This particular model has been trained over 10,000 iterations over a set of roughly 2000 distinct images and their corresponding tags.

streetscore_newyorkcity.csv is verification data for the safety scores of the network, based on the MIT streetscore paper.

safe_val.py is the verification program that tests on the safety scores. It outputs the following files: sComparison, sErrors.txt, sNetworkOutput.txt

sComparison.txt contains the coordinate, binary classification of the coordinate using both network and streetscore q-score value, a boolean that tells if the network and streetscore match, and the radius the program had to search in to find the cut off number of images necessary for testing (specified in safe_val.py)

sErrors.txt contains the coordinate and any errors that might have occured (relating to Carmera sdk, lack of images, corrupted files, etc) during the attempt to classify an image.

sNetworkOutput.txt contains the actual safety probability output of the network for each image for each coordinate. There are 15 randomly selected images within a maximum of 150 m radius of the coordinate right now (the cutOffImages variable in safe_val.py) that are considered in the classification of the coordinate. If the network determines that more than half of the images are safe (which is determined if the safety probability is above a certain threshold) then the coordinate is considered safe. The sNetworkOutput.txt file contains the coordinate, image id, and safety probability.  

Look at testim.py for a simple example of running images through the network.
presentation.py is also a simple example that can present results to investors.

Note: the testing process was often halted and restarted. Because I was just appending to the file, the header tags will appear randomly in the testing output files. Take this into consideration when trying to parse the data.
Last two nodes in output layer are not important, mistake during training.