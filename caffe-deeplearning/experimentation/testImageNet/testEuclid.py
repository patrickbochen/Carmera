#import analysis
from carmera import Carmera

cm          = Carmera(api_key="69d2724e760ab8756c4054a9b54d4b44ef6bc4fc")
cm.url_base = "http://192.168.60.2" # Note how this IP is Euclids Vagrant files private IP
im          = cm.Image()

try:

    res = im.search( {
        'address' : '120 S 2nd ST, Brooklyn, NY 11249',
        'radius'  : 500,
        'limit'   : 1
    } )

    data = res.json()

    if len(data['features']) == 1:

        # Find image id in properties
        image_id = data['features'][0]['properties']['image_id']
        #image_id = 69858
 
        # Create destination path were to download image to
        #dest = "/home/vagrant/caffe/Carmera-SceneDetection/images/tmp/{}.jpg".format(image_id)
        dest = "../images/crowdai/{}.jpg".format(image_id)

        # Download the image
        im.download(image_id, dest)

        # Run CV analysis on image
        #results = analysis.find_car_rois(dest)
        print ("Im the best")

        # Save ROI results to API
        #roi = cm.Roi()
        #roi.create(image_id, tag="car", roi=results['roi'], confidence=results['confidence'])

except Exception as e:

    print(e.code)  ## HTTP status code
    print(e.error) ## JSON error message
