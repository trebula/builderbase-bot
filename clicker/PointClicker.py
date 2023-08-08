import pyautogui
import numpy as np

class PointClicker:
    """ 
    A class to click on a specified point on the screen.
    
    Attributes:
        point (tuple): The point to click at.
        numClicks (int, optional): The number of clicks to make. Defaults to 100.
    """
    def __init__(self, point: tuple, numClicks: int = 100):
        self.point: tuple = point
        self.numClicks: int = numClicks

    def set_click_location(self, point: tuple):
        """ Set the point. """
        self.point = point

    def start_clicking(self):
        """ Continually click on the point. """
        # get the x and y coordinates of the point
        x, y = self.point

        # click on the coordinate
        for _ in range(self.numClicks):
            pyautogui.click(x, y)
        