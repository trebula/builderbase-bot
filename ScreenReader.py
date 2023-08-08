from distutils.filelist import findall
import cv2
import numpy as np
import pyautogui
from AttackStrategy.AttackStrategyType import AttackStrategy
import AttackStrategy.Troops as Troops
from img_reader_util import findImage, findAllImages

# handles initial screen reading (builder hall detection, border detection...)
class ScreenReader:
    image = None
    def __init__(self, _image=None):
        # initialize image
        if _image is None:
            self.getScreenImage()
        else:
            self.image = _image

    def setScreenImage(self, image):
        self.image = image

    def getScreenImage(self):
        return self.image

    def refreshScreenImage(self):
        # get image of screen and convert to np array
        ss = pyautogui.screenshot()
        self.image = np.array(ss)

    # returns the pixel location of the builder hall
    def getBuilderHallLoc(self):
        bh_image = cv2.imread('scaled/testcropped100.png')
        bh_loc, _ = findImage(bh_image, self.image, maximize_confidence=True)
        return bh_loc

    def getLineMap(self):
        # gaussian blur
        postimage = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        blur = cv2.GaussianBlur(postimage, (5,5), 0, 0)

        # red threshold mask
        lower = np.uint8([10, 0, 0])
        upper = np.uint8([35, 255, 255])
        red_mask = cv2.inRange(blur, lower, upper)

        # Hough transform for lines
        rho = 1  # distance resolution in pixels of the Hough grid
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 20  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 10  # minimum number of pixels making up a line
        max_line_gap = 5  # maximum gap in pixels between connectable line segments

        # lines is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(red_mask, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
        
        return lines

    def getTroopSelectionLoc(self, strategy: AttackStrategy):
        """
        Finds the location of troops on the deployment bar
        
        Arguments:
            strategy (strat.AttackStrategy): The strategy to use for finding the troops
            
        Returns:
            (dict): The troop type and its pixel location
        """
        # get troop composition
        troop_comp = strategy.getTroopComposition()

        # dict to store locations - TroopType -> [(x, y), ...]
        troop_locs = {} 

        # loop through dictionary
        for key, freq in troop_comp.items():
            # get actual troop name
            troop_name = Troops.TROOPS[key]

            # get image of troop
            image_name = 'troops/' + troop_name + '.png'
            troop_image = cv2.imread(image_name)

            # get locations of troop
            locs = findAllImages(troop_image, self.image)

            conf = 0.75
            while len(locs) > freq and conf < 0.9:
                locs = findAllImages(troop_image, self.image, stop_confidence=conf)
                conf += 0.1

            if (len(locs) != freq):
                raise RuntimeError("Could not find troop " + troop_name)

            # convert each element of locs to (x, y)
            locs = [((loc[0] + loc[2]) / 2, (loc[1] + loc[3]) / 2) for loc in locs]

            # add to troop_locs
            troop_locs[key] = locs

    def getArrowLocations(self):
        """
        Returns:
            (list): Arrow locations (x1, y1, x2, y2)
        """
        arrow_image = cv2.imread('troops/arrows.png')
        arrow_locs, _ = findAllImages(arrow_image, self.image, stop_confidence=0.75)
        return arrow_locs