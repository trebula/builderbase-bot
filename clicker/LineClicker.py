import pyautogui
import numpy as np

class LineClicker:
    """A class to randomly click on points in a line following a normal distribution.

    Attributes:
        point1 (tuple): (x,y) The first point in the line.
        point2 (tuple): (x,y) The second point in the line.
        numClicks (int, optional): The number of clicks to make. Defaults to 100.
    """
    def __init__(self, point1: tuple, point2: tuple, num_clicks: int = 100):
        self.point1: tuple = point1
        self.point2: tuple = point2
        self.num_clicks: int = num_clicks


    def set_click_location(self, point1: tuple, point2: tuple):
        """Set the first and second points in a line. """
        self.point1 = point1
        self.point2 = point2


    def start_clicking(self):
        """Continually click on random points on a line. """
        # get the x and y coordinates of the line
        x1, y1 = self.point1
        x2, y2 = self.point2

        # prevent division by zero
        if x1 == x2:
            x2 += 1

        # get the slope of the line
        slope = (y2 - y1) / (x2 - x1)

        # get the y-intercept of the line
        y_intercept = y1 - (slope * x1)

        # create a random array of x coordinates following a bell curve around the x mean
        x_coordinates = np.random.normal(loc=(x1 + x2) / 2, scale=abs(x1 - x2) / 2, size=self.num_clicks)
        y_coordinates = slope * x_coordinates + y_intercept

        # combine the x and y coordinates into an array of tuples
        coordinates = np.array(list(zip(x_coordinates, y_coordinates)))

        # remove any coordinates whose x coordinate lies outside the range of min(x1, x2) and max(x1, x2)
        coordinates = coordinates[(coordinates[:, 0] >= min(x1, x2)) & (coordinates[:, 0] <= max(x1, x2))]

        # click on each coordinate
        for coordinate in coordinates:
            pyautogui.click(coordinate[0], coordinate[1])
