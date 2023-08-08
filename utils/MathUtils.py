import numpy as np

def calculateAngleBetweenPoints(point1: tuple, point2: tuple) -> float:
    """
    Calculate the angle between two points.
    
    Args:
        point1 (tuple): (x,y) The first point.
        point2 (tuple): (x,y) The second point.
    
    Returns:
        float: The angle between the two points.
    """
    x1, y1 = point1
    x2, y2 = point2
    return np.arctan2(y2 - y1, x2 - x1)

def calculateDistanceBetweenPoints(point1: tuple, point2: tuple) -> float:
    """
    Calculate the distance between two points.
    
    Args:
        point1 (tuple): (x,y) The first point.
        point2 (tuple): (x,y) The second point.
    
    Returns:
        float: The distance between the two points.
    """
    x1, y1 = point1
    x2, y2 = point2
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculatePointShift(startPoint: tuple, distance: float, angle: float) -> tuple:
    """
    Calculate the resulting point given a start point, distance between points, and angle.
    
    Args:
        startPoint (tuple): (x,y) The start point.
        distance (float): The length of the shift.
        angle (float): The angle of the shift.
    
    Returns:
        tuple: The new point.
    """
    x, y = startPoint
    return x + distance * np.cos(angle), y + distance * np.sin(angle)

def generateBoundedRandomNormalDistribution(numPoints: int, mean: float, stdDev: float, min: float, max: float) -> list:
    """
    Generate a random normal distribution with a bounded range.
    
    Args:
        numPoints (int): The number of points to generate.
        mean (float): The mean of the distribution.
        stdDev (float): The standard deviation of the distribution.
        min (float): The minimum value of the distribution.
        max (float): The maximum value of the distribution.
    
    Returns:
        list: A list of random points.
    """
    distribution = np.random.normal(loc=mean, scale=stdDev, size=numPoints) * (max - min) + min

    # remove any values that are outside the range
    distribution = distribution[(distribution >= min) & (distribution <= max)]

    return distribution