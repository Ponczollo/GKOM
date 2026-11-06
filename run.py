"""Application entry point."""

from src.game import MainGame

import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    MainGame().run()
