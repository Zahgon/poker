import secrets

from .card import Card


class Deck:
    def __init__(self):
        raise NotImplementedError

    def shuffle(self):
        """Shuffles the deck."""
        pass

    def __len__(self):
        raise NotImplementedError

    def draw(self):
        """Draws a card from the top of the deck."""
        pass
