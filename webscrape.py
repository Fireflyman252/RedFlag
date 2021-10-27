
# This is the main file for the webscraper
# usage information can be found in help.txt


from requests_html import HTMLSession
import keras
from PIL import Image
import numpy as np
import urllib.request
import cv2
import json
import sys
import validators
import shutil
import tensorflow
from keras.backend import manual_variable_initialization
manual_variable_initialization(True)

URL = "https://www.deviantart.com/"
IMG_PX_SIZE = 224

# This method reads the dognames from a json file and returns them in a python list.  The dognames will match the output
# of the model.
def getDogNames():
    dognames = ["None"]
    with open('dognames.json', "r") as f:
        dognames = json.load(f)
    return dognames

# This method will classify the dog breeds from the image links that are in the input argument.  The method will load
# the saved model, grab the images from the website, resize the images for the model and them run a prediction on each
# of the images.  The results will be returned in a json format
# Arguments:
#       imageurls - a list of urls to www.deviantart.com photos or local images.
# Returns:
#       - prints out the classification of images in json format
def classifyImages(imageurls):
    # create a request_html session
    session = HTMLSession()
    # the dictionary that will contain the return values
    dictrv = {}
    # load the tensorflow model
    #my_model = keras.models.load_model("test_model")
    #my_model = tensorflow.saved_model.load("test_model")
    my_model = keras.models.load_model("dog_model.h5")

    batch = []

    # process each of the images and create a batch array for the prediction
    for url in imageurls:
        print("url",url)

        # Check if the input is a url
        if(validators.url(url)):
            # Use the object above to connect to needed webpage
            imagePage = session.get(url)

            # Run JavaScript code on webpage
            imagePage.html.render()

            # the page file contains the name of the file we want
            title_tags = imagePage.html.find("title")

            title = title_tags[0].text

            # this tag will have the picture we want
            formatedstring = "meta[content='" + title + "']"

            # find the tag with the meta tag
            test = imagePage.html.find("meta[property='og:image']")
            # extract the content, this is the direct link to the picture
            content = test[0].attrs["content"]

            # doenload the picture and save it locally.
            urllib.request.urlretrieve(content,"test.jpg")
        else:
            #if the file is a local file, just copy it so we can process it
            shutil.copy(url,"test.jpg")

        #resize the image to the size that model needs
        image = Image.open("test.jpg")
        nparray = np.asarray(image)
        resized_img = cv2.resize(nparray, (IMG_PX_SIZE, IMG_PX_SIZE), interpolation=cv2.INTER_CUBIC)
        #convert values from 0 and 255 to float 0.0 to 1.0
        resized_img = resized_img.astype(np.float)/255.0

        batch.append(resized_img)

    # change the batch to numpy so it can be used
    npbatch = np.asarray(batch)
    print("batch size", npbatch.shape)

    # set up the batch
    # TODO: set this up as a real batch so you don't have to look through
    #img_batch = np.expand_dims(resized_img, axis=0)

    # run the model
    answers = my_model.predict(npbatch)
    #print(answers)

    # count which image we are on, used for formatting in dictrv
    count = 0

    # get the answer (and the dogname associated with that answer) for each entry and add them to the dictionary.
    for answer in answers:
        val, idx = max((val, idx) for (idx, val) in enumerate(answer))
        print("val ", val, " idx ", idx)
        dognames=getDogNames()
        print("dog type:", dognames[idx])
        dicturl = {}
        dicturl["file"] = imageurls[count]
        dicturl["classification"] = dognames[idx].split('-')[1]
        entrystring = "file {}".format(count)
        count += 1
        dictrv[entrystring] = dicturl

    #convert dictionary to json
    json_object = json.dumps(dictrv, indent=4)
    print(json_object)

# Scrape the addresses of 5 photos from www.deviantart.com and send them to classifyImages to classify for the breed of
# dog.  This method uses request_html to send a query to www.deviantart.com.  It will then pull the first 5 images that are
# returned and put them into a list that is sent to classify images.
# Arguments:
#       keyword - this is a word (string), that will be used to format the query string for www.deviantart.com
# Returns:
#       The results from classifyImages (json)
def scrape(keyword):

    # create an HTML Session object
    session = HTMLSession()

    # create the query string based on the input keyword
    querystring = "{}?q={} photo".format(URL,keyword)
    print(querystring)
    resp = session.get(querystring)

    # render the page to resolve any javascript
    resp.html.render()

    # find all the links on the page
    a_href_tags = resp.html.find("a")
    links = resp.html.absolute_links

    # request_html uses sets, so we will create one to use
    htmlset = set()

    # search the link tags for ones with the arguments containing "deviation_link", this indicates a direct link to
    # the picture
    for tag in a_href_tags:
        if(tag.html.__contains__("deviation_link")):
            htmlset.add(list(tag.absolute_links)[0])
            # keep collecting until we get 5
            if len(htmlset) > 4:
                break;

    htmllist = list(htmlset)
    # lets classify these images now
    classifyImages(htmllist)

#  This will display the help file (help.txt).  This will print out the entire file to the screen.
def printHelp():
    with open('help.txt', "r") as f:
        #read the whole file at once and print it to the screen
        file_contents = f.read()
        print(file_contents)

#  This will classify a single url.
def classifysingle(url):
    #create a list and add the url to the list and then call the main classify method
    imageURLs = []
    imageURLs.append(url)
    classifyImages(imageURLs)

# declare the main for this program
if __name__ == '__main__':
    args = sys.argv[1:]
    print(args)

    # check that there are arguments
    if len(args) == 0:
        printHelp()

    # classify the argument url as a dog breed type
    elif args[0] == "-c":
        if len(args) == 2:
            classifysingle(args[1])
        else:
            printHelp()
    elif args[0] == "--class":
        if len(args) == 2:
            classifysingle(args[1])
        else:
            printHelp()
    # scrape an image with the argument keyword
    elif args[0] == "-s":
        if len(args) == 2:
            scrape(args[1])
        else:
            printHelp()
    elif args[0] == "--scrape":
        if len(args) == 2:
            scrape(args[1])
        else:
            printHelp()
    #otherwise print help
    else:
        printHelp()

