#For train01 - network 1
#Shows network results on 5 testing images, directory /images_test/ is now in /sceneTagging/finetune_setup/
#Simple guide to giving presentation, for a more visual approach change how you choose coordinates/image_ids

# set up Python environment: numpy for numerical routines, and matplotlib for plotting
import numpy as np

# The caffe module needs to be on the Python path;
#  we'll add it here explicitly.
import sys
caffe_root = '../../../../'  # this file should be run from {caffe_root}/examples (otherwise change this line) (aka caffe)
sys.path.insert(0, caffe_root + 'python')

file_path = 'Carmera-SceneDetection/sceneTagging/finetune_results/train01/'

import caffe
# If you get "No module named _caffe", either you have not built pycaffe or you have the wrong path.

caffe.set_mode_cpu()
#gpu settings
#caffe.set_mode_gpu()
#caffe.set_device(0)

model_def = caffe_root + file_path + 'deploy.prototxt'
model_weights = caffe_root + file_path + 'snapshots_iter_100000.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)


# load the mean ImageNet image (as distributed with Caffe) for subtraction
mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
print ('mean-subtracted values:', zip('BGR', mu))
# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR
# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
net.blobs['data'].reshape(50,        # batch size
                          3,         # 3-channel (BGR) images
                          227, 227)  # image size is 227x227


#Somehow choose images
#Link from Carmera map (AOI) to this file
listTest = ['133228', '146202', '162005', '199691', '299650']

#Verification (hand labeled images)
dictTest = {'133228': 'Residential, Outside Venue, Construction',
            '146202': 'Safe, Commercial',
            '162005': 'Safe, Tourist, Rich, Commercial',
            '199691': 'Residential, Outside Venue',
            '299650': 'Old, Commercial'}

#Tags for the first network, in order of output nodes
tags = ['Safe', 'Residential', 'Outside Venue', 'Tourist',
    'Old', 'Rich', 'Construction', 'Commercial']

for im in listTest[0:5]:

    print('\nImage: ' + im)
    tag = dictTest.get(im)
    print('Actual Labels: ' + tag)


    image = caffe.io.load_image(caffe_root + 'data/scene/images_test/' + im + '.jpg')
    transformed_image = transformer.preprocess('data', image)
    # copy the image data into the memory allocated for the net
    net.blobs['data'].data[...] = transformed_image
    ### perform classification
    output = net.forward()
    output_prob = output['prob'][0]  # the output probability vector for the first image in the batch
    labels_file = caffe_root + file_path + 'label_names.txt'
    labels = np.loadtxt(labels_file, str, delimiter='\t')
    # sort top five predictions from softmax output
    top_inds = output_prob.argsort()[::-1][:5]  # reverse sort and take 5 largest items

    print ('probabilities and labels:')
    print (zip(output_prob[top_inds], labels[top_inds]))

