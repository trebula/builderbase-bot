from typing import Any
from abc import ABC, abstractmethod

# attack strategy interface
class AttackStrategy(ABC):
    @abstractmethod
    def __init__(self, line_map, builder_hall_loc) -> None:
        """
        Initialize the attack strategy.
        """
        pass

    @abstractmethod
    def get_troop_comp(self) -> dict:
        """Returns the troop composition of the strategy
        
        Returns:
            (dict): The troop type and its quantity
                Key: 
                    (Troops): The troop type
                Value:
                    (int): The quantity of the troop type
        """
        pass
    
    @abstractmethod
    def get_troop_drop_locations(self) -> Any:
        """Returns a list of dictionaries representing the troops and its drop loc
        
        Returns:
            (list): A list of dictionaries representing the troops and its drop loc
                Key:
                    troop_type (Troops): The troop type
                Value:
                    (list): A list of tuples representing the x and y coordinates of the troop drop location
                    i.e. [(x1, y1), (x2, y2)]
        """
        pass
