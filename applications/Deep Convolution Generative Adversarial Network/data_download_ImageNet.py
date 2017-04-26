# -*- coding:utf-8 -*-
import numpy as np
import urllib
import urllib2
import requests
import cv2
import os
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

'''ImageNet data'''

path = "Imagenet/{}.jpg"
row_size = 10
column_size = 10
Normal_value = 200
MINIMUM_SIZE = 4096

'''address contents'''

url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n09903153'
url_face = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09618957'
url_cel= 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n10529231'
url_woman='http://image-net.org/api/text/imagenet.synset.geturls?wnid=n09619168'

'''crawling method1'''
def download_data_from_internet_in_urllib():

    data = urllib.urlopen(url_face)
    '''information for url'''
    #print temp.geturl() #return url
    #print data.getcode() #return code
    #print data.info() # return header
    #print data.read() # return data
    #soup = BeautifulSoup(data.read(), 'lxml')
    #print soup

    '''
    Points to note when downloading url 'ImageNet' data.
    1. Using urllib.urlopen().getcode(), check the connection state - must be 200
    2. Using os.path.getsize(), Find image data that has a value less than 4096.
    3. Find data of the form 'None'.
    '''
    i=0
    for t,line in enumerate(data.readlines()):
        print "Image_URL -> "+line
        try :
            code=urllib.urlopen(line).getcode() # Normal value must be 200.
            print "code : {}".format(code)
            if code != Normal_value:
                raise  # Errors of the current except statement are indicated.
        except:
            '''not reading Image data that has a value that is not '200'. '''
            print "error_URL"+line
            i+=(-1)
            continue
        else:
            if code == Normal_value:
                print "download..."+"<"+path.format(t+1+i)+">"

                '''In here,because all Image data(including null data) is saved
                We have to do post-processing. '''
                urllib.urlretrieve(line,path.format(t+1+i))
                img = cv2.imread(path.format(t+1+i), cv2.IMREAD_COLOR)

                '''post-processing, removing image data that has a value less than 4096 and removing data of the form 'None' '''
                if img != None and os.path.getsize(path.format(t+1+i)) > MINIMUM_SIZE:
                    resized_image = cv2.resize(img, (64, 64),interpolation=cv2.INTER_AREA)
                    cv2.imwrite(path.format(t+1+i), resized_image)
                else:
                    print "Erase data that does not satisfy the condition."
                    os.remove(path.format(t+1+i))
                    i += (-1)
    print "download completed"

'''crawling method2'''
def download_data_from_internet_in_requests():

    data=requests.get(url_face,stream=True)

    '''
    Points to note when downloading url 'ImageNet' data.
    1. Using urllib.urlopen().getcode(), check the connection state - must be 200
    2. Using os.path.getsize(), Find image data that has a value less than 4096.
    3. Find data of the form 'None'.
    '''
    i=0
    for t,line in enumerate(data.iter_lines()):
        print "Image_URL -> " + line
        try:
            code = urllib.urlopen(line).getcode()  # Normal value must be 200.
            print "code : {}".format(code)
            if code != Normal_value:
                raise  # Errors of the current except statement are indicated.
        except:
            '''not reading Image data that has a value that is not '200'. '''
            print "error_URL" + line
            i += (-1)
            continue
        else:
            if code == Normal_value:
                print "download..." + "<" + path.format(t + 1 + i) + ">"

                '''In here,because all Image data(including null data) is saved
                We have to do post-processing. '''
                urllib.urlretrieve(line, path.format(t + 1 + i))
                img = cv2.imread(path.format(t + 1 + i), cv2.IMREAD_COLOR)

                '''post-processing, removing image data that has a value less than 4096 and removing data of the form 'None' '''
                if img != None and os.path.getsize(path.format(t + 1 + i)) > MINIMUM_SIZE:
                    resized_image = cv2.resize(img, (64, 64), interpolation=cv2.INTER_AREA)
                    cv2.imwrite(path.format(t + 1 + i), resized_image)
                else:
                    print "Erase data that does not satisfy the condition."
                    os.remove(path.format(t + 1 + i))
                    i += (-1)
    print "download completed"

def read_data_from_file():
    return 0

if __name__ == "__main__":
    "download the ImageNet data from inside"
    '''method1'''
    download_data_from_internet_in_urllib() # using urllib1 or urllib2
    '''method2'''
    #download_data_from_internet_in_requests() # using requests module

    '''Load the ImageNet data from inside'''
    train_img=read_data_from_file()

    '''visualization'''
    fig ,  ax = plt.subplots(row_size, column_size, figsize=(column_size, row_size))
    fig.suptitle('MNIST')
    for j in xrange(row_size):
        for i in xrange(column_size):
            ax[j][i].set_axis_off()
            ax[j][i].imshow(train_img[i+j*column_size],cmap="gray")
    plt.show()

else:
    print "Load the ImageNet data from the outside"

