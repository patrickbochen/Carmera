#Downloads the training and testing images
#Need to update to production SDK
import os
from carmera import Carmera

cm = Carmera(api_key="69d2724e760ab8756c4054a9b54d4b44ef6bc4fc")
cm.url_base = "http://192.168.60.2"
im = cm.Image()

train_file_name = "train_2.txt"
test_file_name = "test_2.txt"

#Downloads images for training and testing sets
f = open(train_file_name,'r')
for line in f:
    get_imageId = line.split(" ")
    line = get_imageId[0]

    file_exists = "./images/" + line
    line = line.replace(".jpg", "")

    if os.path.isfile(file_exists):
        continue
    else:
        try:
            print (line)
            res = im.download(line, "./images/{}.jpg".format(line))
        except Exception as e:
            print(e)
f.close()

f = open(test_file_name,'r')
for line in f:
    get_imageId = line.split(" ")
    line = get_imageId[0]

    file_exists = "./images/" + line
    line = line.replace(".jpg", "")

    if os.path.isfile(file_exists):
        continue
    else:
        try:
            print(line)
            res = im.download(line, "./images/{}.jpg".format(line))
        except Exception as e:
            print(e)
            # print(e.code)  ## HTTP status code
            # print(e.error) ## JSON error message
f.close()

# #image counter to determine number of unique images in training and testing sets for validation
# image_counter = 0
# image_tracker = {}
# f = open("train_1.txt",'r')
# for line in f:
#     get_imageId = line.split(" ")
#     line = get_imageId[0]
#     line = line.replace(".jpg", "")
#     if(line in image_tracker):
#         continue
#     else:
#         image_tracker.update({line:image_counter})
#         image_counter += 1
# f.close()
# print (image_counter)

# image_counter = 0
# image_tracker = {}
# f = open("test_1.txt",'r')
# for line in f:
#     get_imageId = line.split(" ")
#     line = get_imageId[0]
#     line = line.replace(".jpg", "")
#     if(line in image_tracker):
#         continue
#     else:
#         image_tracker.update({line:image_counter})
#         image_counter += 1
# print (image_counter)
# f.close()

# Random testing images
# try:
#     res = im.download('146202', "./images_test/{}.jpg".format('146202'))
#     res = im.download('199691', "./images_test/{}.jpg".format('199691'))
#     res = im.download('299650', "./images_test/{}.jpg".format('299650'))
#     res = im.download('133228', "./images_test/{}.jpg".format('133228'))
#     res = im.download('162005', "./images_test/{}.jpg".format('162005'))
# except Exception as e:
#     print(e)