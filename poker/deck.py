import secrets

from .card import Card


class Deck:
    def __init__(self):
        self._cards = list(Card)
        self._drawn = []

    def shuffle(self):
        """Shuffles the deck."""
        pass

    def __len__(self):
        return len(self._cards)

    def draw(self):
        """Draws a card from the top of the deck."""
        pass
