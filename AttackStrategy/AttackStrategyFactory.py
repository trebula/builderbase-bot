from AttackStrategy.AttackStrategyType import AttackStrategy
from AttackStrategy.GiantCannon import GiantCannon
from AttackStrategy.Strategies import EStrategies

class AttackStrategyFactory:
    def __init__(self):
        pass

    def generate(attack_strategy_type: EStrategies, line_map, builder_hall_loc) -> AttackStrategy:
        """
        Generates an attack strategy. 
        Returns None if an invalid attack strategy is specified.

        Args:
            attackStrategyType (EStrategies): Specifies the strategy to generate
            lineMap (np.ndarray): Line map representing the attack borders
            builderHallLoc (tuple): (x, y, w, h) of builder hall location
        """
        if attack_strategy_type == EStrategies.GIANT_CANNON:
            return GiantCannon(line_map, builder_hall_loc)
        return None
