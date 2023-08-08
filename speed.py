#include <cmath>
#include <iostream>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>
from turtle import Screen
import numpy as np

def getLineIntersection(p0_x, p0_y, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y):
    s1_x = p1_x - p0_x
    s1_y = p1_y - p0_y
    s2_x = p3_x - p2_x
    s2_y = p3_y - p2_y
    divisor = (-s2_x * s1_y + s1_x * s2_y)
    if divisor == 0:
        return None, None
    s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / divisor
    t = (s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / divisor
    if (s >= 0 and s <= 1 and t >= 0 and t <= 1):
        x = p0_x + (t * s1_x)
        y = p0_y + (t * s1_y)
        return x, y
    return None, None
# bool getLineIntersection(double p0_x, double p0_y, double p1_x, double p1_y, 
#     double p2_x, double p2_y, double p3_x, double p3_y, double &i_x, double &i_y)
# {
#     double s1_x, s1_y, s2_x, s2_y;
#     s1_x = p1_x - p0_x;     s1_y = p1_y - p0_y;
#     s2_x = p3_x - p2_x;     s2_y = p3_y - p2_y;

#     double s, t;
#     double divisor = (-s2_x * s1_y + s1_x * s2_y);
#     s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / divisor;
#     t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / divisor;

#     if (s >= 0 && s <= 1 && t >= 0 && t <= 1)
#     {
#         // Collision detected
#         i_x = p0_x + (t * s1_x);
#         i_y = p0_y + (t * s1_y);
#         return true;
#     }

#     return false; // No collision
# }

# // returns the distance squared between two integer points (for faster computation)
# int getDistanceSquared(const coord &p1, const coord &p2)
# {
#     int dx = (p1.x - p2.x);
#     int dy = (p1.y - p2.y);
#     int dist = dx*dx + dy*dy;
#     return dist;
# }
def getDistanceSquared(p1, p2):
    dx = (p1[0] - p2[0])
    dy = (p1[1] - p2[1])
    dist = dx*dx + dy*dy
    return dist

# // lines is a numpy array of shape (n, 1, 4) where n is the number of lines
# // loc is a tuple (x, y) of the builder hall location
# // angleIncrementDeg is the angle increment in degrees
# // returns a vector of intersects consisting of an even number of elements, 
# // where each even index is an x coordinate and each odd index is a y coordinate
# // vector is in the form [x1, y1, x2, y2, x3, y3, ...]
# std::vector<int> getFarthestIntersects(const py::array_t<int> &lines, const std::vector<int> &loc, const int angleIncrementDeg=45, const bool sorted=true) {
#     py::buffer_info buf = lines.request();
#     int *data = (int *) buf.ptr;

#     // lines shape is (n, 1, 4)
#     int n = buf.shape[0];
#     int m = buf.shape[2];
#     coord locCoord1{loc[0], loc[1]};
    
#     // get farthest line on various angles
#     const double angleIncrement = angleIncrementDeg * M_PI / 180;

#     std::vector<coord> farthestIntersects;
#     for (double angle = 0; angle < 2 * M_PI; angle += angleIncrement) {
#         // farthest intersect set at max in case of no intersections, so when selecting closest wall to place troops at, no intersect-lines will not contribute to selection
#         coord farthestIntersect{std::numeric_limits<int>::max(), std::numeric_limits<int>::max()};
#         int farthestIntersectDistSquared = 0;

#         // first calculate line segment starting from loc and extending to farthest point
#         coord locCoord2;
#         locCoord2.x = locCoord1.x + (int) (std::cos(angle) * 50000); // x
#         locCoord2.y = locCoord1.y + (int) (std::sin(angle) * 50000); // y
        
#         // now find the farthest point on the line segment
#         for (int i = 0; i < n; i++) {
#             int x1 = data[i * m + 0];
#             int y1 = data[i * m + 1];
#             int x2 = data[i * m + 2];
#             int y2 = data[i * m + 3];
#             double intersectionX, intersectionY;

#             if (getLineIntersection(x1, y1, x2, y2, locCoord1.x, locCoord1.y, locCoord2.x, locCoord2.y, intersectionX, intersectionY)) {
#                 // get distance squared between intersection and builder hall location
#                 coord intersectCoord{(int) intersectionX, (int) intersectionY};
#                 int currDisSquared = getDistanceSquared(intersectCoord, locCoord1);

#                 if (currDisSquared > farthestIntersectDistSquared) {
#                     farthestIntersectDistSquared = currDisSquared;
#                     farthestIntersect.x = (int) intersectionX;
#                     farthestIntersect.y = (int) intersectionY;
#                 }
#             }
#         }
#         farthestIntersects.push_back(farthestIntersect);
#     }

#     if (sorted) {
#         // sort farthestIntersects by distance from builder hall location
#         std::sort(farthestIntersects.begin(), farthestIntersects.end(), [locCoord1](const coord &a, const coord &b) {
#             int aDist = getDistanceSquared(a, locCoord1);
#             int bDist = getDistanceSquared(b, locCoord1);
#             return aDist < bDist;
#         });
#     }

#     // unpack farthestIntersects into primitive int vector
#     std::vector<int> farthestIntersectsPrimitive;
#     for (coord c : farthestIntersects) {
#         farthestIntersectsPrimitive.push_back(c.x);
#         farthestIntersectsPrimitive.push_back(c.y);
#     }

#     return farthestIntersectsPrimitive;
# }

def getFarthestIntersects(lines, loc, angleIncrementDeg=45, sorted=True):
    # lines shape is (n, 1, 4)
    n = lines.shape[0]
    m = lines.shape[2]
    locCoord1 = loc

    # get farthest line on various angles
    angleIncrement = angleIncrementDeg * np.pi / 180

    farthestIntersects = []
    for angle in np.arange(0, 2 * np.pi, angleIncrement):
        # farthest intersect set at max in case of no intersections, so when selecting closest wall to place troops at, no intersect-lines will not contribute to selection
        farthestIntersect = (np.iinfo(np.int32).max, np.iinfo(np.int32).max)
        farthestIntersectDistSquared = 0

        # first calculate line segment starting from loc and extending to farthest point
        locCoord2 = (locCoord1[0] + int(np.cos(angle) * 50000), locCoord1[1] + int(np.sin(angle) * 50000))

        # now find the farthest point on the line segment
        for i in range(n):
            x1 = lines[i, 0, 0]
            y1 = lines[i, 0, 1]
            x2 = lines[i, 0, 2]
            y2 = lines[i, 0, 3]
            intersectionX, intersectionY = getLineIntersection(x1, y1, x2, y2, locCoord1[0], locCoord1[1], locCoord2[0], locCoord2[1])

            if intersectionX is not None and intersectionY is not None:
                # get distance squared between intersection and builder hall location
                intersectCoord = (intersectionX, intersectionY)
                currDisSquared = getDistanceSquared(intersectCoord, locCoord1)

                if currDisSquared > farthestIntersectDistSquared:
                    farthestIntersectDistSquared = currDisSquared
                    farthestIntersect = (intersectionX, intersectionY)
        farthestIntersects.append(farthestIntersect)

    if sorted:
        # sort farthestIntersects by distance from builder hall location
        farthestIntersects.sort(key=lambda x: getDistanceSquared(x, locCoord1))

    # unpack farthestIntersects into primitive int vector
    farthestIntersectsPrimitive = []
    for coord in farthestIntersects:
        farthestIntersectsPrimitive.append(coord[0])
        farthestIntersectsPrimitive.append(coord[1])

    return farthestIntersectsPrimitive

# // loc1 and loc2 are two-integer tuples (x, y)
# // returns the angle in degrees between the two locations (0 is east, 90 is north, etc)
# double getAngle(const std::vector<int> &loc1, const std::vector<int> &loc2) {
#     double dx = loc2[0] - loc1[0];
#     double dy = loc2[1] - loc1[1];
#     double angle = std::atan2(dy, dx);
#     return angle;
# }
def getAngle(loc1, loc2):
    dx = loc2[0] - loc1[0]
    dy = loc2[1] - loc1[1]
    angle = np.arctan2(dy, dx)
    return angle

import build.LineComputation
from ScreenReader import ScreenReader
import cv2
import time

img = cv2.imread('redbounds/redbounds2.png')
screenreader = ScreenReader(img)
lines = screenreader.getLineMap()
bh_loc = screenreader.getBuilderHallLoc()
# get center of builder hall
bh_loc = (bh_loc[0] + int(bh_loc[2] / 2), bh_loc[1] + int(bh_loc[3] / 2))

start = time.time()
getFarthestIntersects(lines, bh_loc)
end = time.time()
print(end - start)
time1 = end-start
start = time.time()
build.LineComputation.getFarthestIntersects(lines, bh_loc, 45, True)
end = time.time()
print(end - start)
time2 = end-start
speedup = time1/time2
print(speedup)