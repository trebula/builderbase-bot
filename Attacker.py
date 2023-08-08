import pyautogui
from time import sleep
from ScreenReader import ScreenReader
from clicker import (
    LineClicker,
)
from AttackStrategy import (
    AttackStrategy,
    AttackStrategyFactory,
    EStrategies,
)

class Attacker:
    attack_strat: AttackStrategy = None
    screen_reader: ScreenReader = None
    arrow_locations: list = None
    def __init__(self, strategy: EStrategies, screenReader: ScreenReader = None):
        if screenReader is None:
            self.screen_reader = ScreenReader()
        else:
            self.screen_reader = screenReader

        # initiate attack strategy
        builder_hall_loc = self.screen_reader.getBuilderHallLoc()
        while builder_hall_loc is None:
            sleep(1)
            self.screen_reader.refreshScreenImage()
            builder_hall_loc = self.screen_reader.getBuilderHallLoc()

        lineMap = self.screen_reader.getLineMap()
        self.arrow_locations = self.screen_reader.getArrowLocations()
        while self.arrow_locations is None:
            sleep(1)
            self.screen_reader.refreshScreenImage()
            builder_hall_loc = self.screen_reader.getBuilderHallLoc()
            lineMap = self.screen_reader.getLineMap()
            self.arrow_locations = self.screen_reader.getArrowLocations()

        factory = AttackStrategyFactory()
        self.attack_strat = factory.generate(strategy, lineMap, builder_hall_loc)

    def select_troops(self):
        troop_comp = self.attack_strat.get_troop_comp()
        # click all arrow locations
        for loc in self.arrow_locations:
            pyautogui.click(loc)
            # select troops
            


    # def performAttack():
