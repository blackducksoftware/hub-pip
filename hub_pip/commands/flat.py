
from json import dumps

from .base import Base


class Flat(Base):
    """Say hello, world!"""

    def run(self):
        print('You supplied the following options:', dumps(
            self.options, indent=2, sort_keys=True))
