from typing import Any
import build.LineComputation
import numpy as np

from AttackStrategy.Troops import ETroops
from utils.MathUtils import calculateAngleBetweenPoints, calculateDistanceBetweenPoints, calculatePointShift

from AttackStrategy.AttackStrategyType import AttackStrategy

class GiantCannon(AttackStrategy):
    line_map = None
    builder_hall_loc = None
    possible_drop_locations = []

    def __init__(self, line_map, builder_hall_loc) -> None:
        self.line_map = line_map
        self.builder_hall_loc = builder_hall_loc

    def get_troop_comp(self) -> Any:
        # 2 giant slots and 4 cannon slots
        troop_comp = {ETroops.GIANT.value: 2, 
                      ETroops.CANNON.value: 4}
        return troop_comp

    def get_troop_drop_locations(self):
        # get the farthest lines
        ANGLE_INCR = 22 # direction look angle increment (degrees)
        IS_SORTED = True # whether lines sorted by distance from builder hall
        farthest_intersects = build.LineComputation.getFarthestIntersects(self.line_map, self.builder_hall_loc, ANGLE_INCR, IS_SORTED)

        # reshape farthestIntersects to have (n/2,2) shape
        self.possible_drop_locations = np.reshape(farthest_intersects, (int(len(farthest_intersects)/2), 2))

        # closest is first element because of sorting
        closest_intersect = self.possible_drop_locations[0]

        # remove closest intersect from possible drop locations (in case it's not a valid drop location)
        self.possible_drop_locations = np.delete(self.possible_drop_locations, 0, 0)

        # troops should be dropped in a perpendicular line slightly farther away from the intersect
        angle = calculateAngleBetweenPoints(self.builder_hall_loc, closest_intersect)

        hypot_length = calculateDistanceBetweenPoints(self.builder_hall_loc, closest_intersect)
        hypot_length += self.builder_hall_loc[2] # add width of builder hall

        drop_location_center_X, drop_location_center_Y = calculatePointShift(self.builder_hall_loc, hypot_length, angle)

        perpangle = angle + np.pi/2 # perpendicular angle

        # line length will be five times the builder hall's width on either side of the center
        half_scaled_line_length = 5 * self.builder_hall_loc[2]

        # calculate line endpoints
        line_endpoint1 = (int(drop_location_center_X + half_scaled_line_length * np.cos(perpangle)), 
                          int(drop_location_center_Y + half_scaled_line_length * np.sin(perpangle)))
        line_endpoint2 = (int(drop_location_center_X - half_scaled_line_length * np.cos(perpangle)), 
                          int(drop_location_center_Y - half_scaled_line_length * np.sin(perpangle)))
        
        # for giant cannon attack strategy, all troops should be dropped within the range of the line
        # create dictionary of troop type and its drop location
        troop_drop_locations = [{
            ETroops.GIANT.value: [line_endpoint1, line_endpoint2]
        }, 
        {
            ETroops.CANNON.value: [line_endpoint1, line_endpoint2]
        }]
        return troop_drop_locations
