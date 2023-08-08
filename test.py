from img_reader_util import findImage
from img_reader_util import findAllImages
import numpy as np
import os
import pyautogui
import cv2
import time
from ScreenReader import ScreenReader

needle_image = cv2.imread('troops/giant.png')
haystack_image = cv2.imread('redbounds/selection.PNG')

try:
    haystack_image = haystack_image[700:]
    start = time.time()
    image_locs, confidence = findAllImages(needle_image, haystack_image, grayscale=True)
    # print image_loc and confidence
    print(image_locs)
    print(confidence)

    # draw a rectangle around the image
    blank = np.zeros((haystack_image.shape[0], haystack_image.shape[1], 3), np.uint8)
    for image_loc in image_locs:
        cv2.rectangle(blank, (image_loc[0], image_loc[1]), (image_loc[0] + needle_image.shape[1], image_loc[1] + needle_image.shape[0]), (0, 255, 0), 2)
    end = time.time()
    print("Time elapsed: " + str(end - start))
    
    # show the image
    final = cv2.addWeighted(haystack_image, 0.8, blank, 1, 0)
    cv2.imshow('image', final)
    cv2.waitKey(0)
except RuntimeError:
    print("Image not found")