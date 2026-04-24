"""
    Poker hand history parser module.
"""

import io
import itertools
from datetime import datetime

import attr
import pytz
from cached_property import cached_property
from zope.interface import Attribute, Interface

from .card import Rank


@attr.s(slots=True)
class _Player:
    """Player participating in the hand history."""

    name = attr.ib()
    stack = attr.ib()
    seat = attr.ib()
    combo = attr.ib()


@attr.s(slots=True)
class _PlayerAction:
    """Player actions on the street."""

    name = attr.ib()
    action = attr.ib()
    amount = attr.ib()


class IStreet(Interface):
    actions = Attribute("_StreetAction instances.")
    cards = Attribute("Cards.")
    pot = Attribute("Pot size after actions.")


class IHandHistory(Interface):
    """Interface for all hand histories. Not all attributes are available in all room's hand
    histories, missing attributes are always None. This contains the most properties, available in
    any pokerroom hand history, so you always have to deal with None values.
    """

    # parsing information
    header_parsed = Attribute("Shows wheter header is parsed already or not.")
    parsed = Attribute("Shows wheter the whole hand history is parsed already or not.")
    date = Attribute("Date of the hand history.")

    # Street informations
    preflop = Attribute("_Street instance for preflop actions.")
    flop = Attribute("_Street instance for flop actions.")
    turn = Attribute("_Street instance for turn actions.")
    river = Attribute("_Street instance for river actions.")
    show_down = Attribute("_Street instance for showdown.")

    # Player informations
    table_name = Attribute("Name of")
    max_players = Attribute("Maximum number of players can sit on the table.")
    players = Attribute("Tuple of player instances.")
    hero = Attribute("_Player instance with hero data.")
    button = Attribute("_Player instance of button.")
    winners = Attribute("Tuple of _Player instances with winners.")

    # Game informations
    game_type = Attribute("GameType enum value (CASH, TOUR or SNG)")
    sb = Attribute("Small blind size.")
    bb = Attribute("Big blind size.")
    buyin = Attribute("Buyin with rake.")
    rake = Attribute("Rake only.")
    game = Attribute("Game enum value (HOLDEM, OMAHA? OHILO, RAZZ or STUD)")
    limit = Attribute("Limit enum value (NL, PL or FL)")
    ident = Attribute("Unique id of the hand history.")
    currency = Attribute("Currency of the hand history.")
    total_pot = Attribute("Total pot Decimal.")

    tournament_ident = Attribute("Unique tournament id.")
    tournament_name = Attribute("Name of the tournament.")
    tournament_level = Attribute("Tournament level.")

    def parse_header():
        """Parses only the header of a hand history. It is used for quick looking into the hand
        history for basic informations:
            ident, date, game, game_type, limit, money_type, sb, bb, buyin, rake, currency
        by parsing the least lines possible to get these.
        """

    def parse():
        """Parses the body of the hand history, but first parse header if not yet parsed."""


class _BaseStreet:
    def __init__(self, flop):
        self.pot = None
        self.actions = None
        self.cards = None
        self._parse_cards(flop[0])
        self._parse_actions(flop[1:])
        self._all_combinations = itertools.combinations(self.cards, 2)

    @cached_property
    def is_rainbow(self):
        pass

    @cached_property
    def is_monotone(self):
        pass

    @cached_property
    def is_triplet(self):
        pass

    @cached_property
    def has_pair(self):
        pass

    @cached_property
    def has_straightdraw(self):
        pass

    @cached_property
    def has_gutshot(self):
        pass

    @cached_property
    def has_flushdraw(self):
        pass

    @cached_property
    def players(self):
        pass

    def _get_differences(self):
        pass


class _BaseHandHistory:
    """Abstract base class for *all* kinds of parser."""

    def __init__(self, hand_text):
        """Save raw hand history."""
        self.raw = hand_text.strip()
        self.header_parsed = False
        self.parsed = False

    @classmethod
    def from_file(cls, filename):
        with io.open(filename, "rt", encoding="utf-8-sig") as f:
            return cls(f.read())

    def __str__(self):
        return f"<{self.__class__.__name__}: #{self.ident}>"

    @property
    def board(self):
        """Calculates board from flop, turn and river."""
        pass

    def _parse_date(self, date_string):
        """Parse the date_string and return a datetime object as UTC."""
        pass

    def _init_seats(self, player_num):
        pass

    def _get_hero_from_players(self, hero_name):
        pass


class _SplittableHandHistoryMixin:
    """Class for PokerStars and FullTiltPoker type hand histories, where you can split the hand
    history into sections.
    """

    def _split_raw(self):
        """Split hand history by sections."""
        pass

    def _del_split_vars(self):
        pass
