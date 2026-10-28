import time
import logging

from src.player import Player
from src.base_entity import BaseEntity

logger = logging.getLogger(__name__)

MAX_FRAMERATE = 240
MIN_FRAMETIME = 1 / MAX_FRAMERATE

class MainGame:

    player: Player
    obstacles: list[BaseEntity]

    def __init__(self):
        ...

    def run(self):
        self.initialize()
        self.render()
        frametime = 0
        counter = 1
        while True:
            frametime_start = time.monotonic()
            self.handle_movement(frametime)
            self.handle_interactions()
            self.render()
            frametime = frametime_start - time.monotonic()
            logger.debug(f"Frame {counter} took {round(frametime, 5)}s to render")
            counter += 1
            if frametime < MIN_FRAMETIME:
                time.sleep(MIN_FRAMETIME - frametime)

    def initialize(self):
        ...

    def handle_movement(self, frametime):
        ...

    def handle_interactions(self):
        ...

    def render(self):
        ...
