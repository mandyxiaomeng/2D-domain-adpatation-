import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import os

def Matching (method, match, lowe_ratio):
    if method   == 'ORB':
        finder = cv.ORB_create()
    elif method == 'SIFT':
        finder = cv.SIFT_create()

    # BFMatcher with default params
    if match  == 'bf':
        matcher = cv.BFMatcher()

    queryKeypoints, queryDescriptors = finder.detectAndCompute(query_image,None)
    trainKeypoints, trainDescriptors = finder.detectAndCompute(train_image,None)

    matches = matcher.knnMatch(queryDescriptors,trainDescriptors,k=2)

    # Apply ratio test
    good_matches= []

    for m,n in matches:
        if m.distance < lowe_ratio*n.distance:
            good_matches.append([m])
    
    return queryKeypoints, trainKeypoints, matches, good_matches


#read images------------------------------------------
query_image = cv.imread('./input/cam1.jpg',0)          # queryImage
train_image = cv.imread('./input/cad1.png',0)          # trainImage


# rize images-------------------------------------------
#print(query_image.shape)
#print(train_image.shape)
#print(query_image.size)
#print(train_image.size)
scale_percent = ((train_image.shape[1])/(query_image.shape[1]))/(50/100)

width = int(query_image.shape[1] * scale_percent)
height = int(query_image.shape[0] * scale_percent)

query_image = cv.resize(query_image,(width,height))
#print(query_image.shape)
#print(query_image.size)


#Matching images------------------------------------------
method = 'ORB'  # 'SIFT'
match = 'bf'
lowe_ratio = 0.80

kp1, kp2, matches, good_matches = Matching (method, match, lowe_ratio)


#Result----------------------------------------------------------
message_1 = 'using %s with lowe_ratio %.2f' % (method, lowe_ratio)
message_2 = 'there are %d good matches' % (len(good_matches))

print(message_1)
print(message_2)

output_image = cv.drawMatchesKnn(query_image,kp1,train_image,kp2,good_matches, None, flags=2)

#print txt on the result image, save and plot result image
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(output_image,message_1,(10, 250), font, 0.8,(255,0,255),1,cv.LINE_AA)
cv.putText(output_image,message_2,(10, 270), font, 0.8,(255,0,255),1,cv.LINE_AA)
fname = 'output_%s_%.2f.jpg' % (method, lowe_ratio)
cv.imwrite(os.path.join('./output', fname), output_image)

plt.imshow(output_image),plt.show()