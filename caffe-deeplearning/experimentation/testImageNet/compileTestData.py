from carmera import Carmera

cm = Carmera(api_key="69d2724e760ab8756c4054a9b54d4b44ef6bc4fc")
cm.url_base = "http://192.168.60.2"
im = cm.Image()

f = open("crowdAIExp.txt",'r')

for line in f:
    line = line.replace("\n", "")
    ## Download image by id and save to disk
    print(line)
    try:
        res = im.download(line, "../images/crowdai/{}.jpg".format(line))
        ## Do stuff with response
    except Exception as e:
        print(e)
        # print(e.code)  ## HTTP status code
        # print(e.error) ## JSON error message
