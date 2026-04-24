import re
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import attr
import pytz
from lxml import etree
from zope.interface import implementer

from .. import handhistory as hh
from ..card import Card
from ..constants import Action, Currency, Game, GameType, Limit, MoneyType
from ..hand import Combo

__all__ = ["PokerStarsHandHistory", "Notes"]


@implementer(hh.IStreet)
class _Street(hh._BaseStreet):
    def _parse_cards(self, boardline):
        pass

    def _parse_actions(self, actionlines):
        pass

    def _parse_uncalled(self, line):
        pass

    def _parse_collected(self, line):
        pass

    def _parse_muck(self, line):
        pass

    def _parse_player_action(self, line):
        pass


@implementer(hh.IHandHistory)
class PokerStarsHandHistory(hh._SplittableHandHistoryMixin, hh._BaseHandHistory):
    """Parses PokerStars Tournament hands."""

    _DATE_FORMAT = "%Y/%m/%d %H:%M:%S ET"
    _TZ = pytz.timezone("US/Eastern")  # ET
    _split_re = re.compile(r" ?\*\*\* ?\n?|\n")
    _header_re = re.compile(
        r"""
                        ^PokerStars\s+                                # Poker Room
                        Hand\s+\#(?P<ident>\d+):\s+                   # Hand history id
                        (Tournament\s+\#(?P<tournament_ident>\d+),\s+ # Tournament Number
                         ((?P<freeroll>Freeroll)|(                    # buyin is Freeroll
                          \$?(?P<buyin>\d+(\.\d+)?)                   # or buyin
                          (\+\$?(?P<rake>\d+(\.\d+)?))?               # and rake
                          (\s+(?P<currency>[A-Z]+))?                  # and currency
                         ))\s+
                        )?
                        (?P<game>.+?)\s+                              # game
                        (?P<limit>(?:Pot\s+|No\s+|)Limit)\s+          # limit
                        (-\s+Level\s+(?P<tournament_level>\S+)\s+)?   # Level (optional)
                        \(
                         (((?P<sb>\d+)/(?P<bb>\d+))|(                 # tournament blinds
                          \$(?P<cash_sb>\d+(\.\d+)?)/                 # cash small blind
                          \$(?P<cash_bb>\d+(\.\d+)?)                  # cash big blind
                          (\s+(?P<cash_currency>\S+))?                # cash currency
                         ))
                        \)\s+
                        -\s+.+?\s+                                    # localized date
                        \[(?P<date>.+?)\]                             # ET date
                        """,
        re.VERBOSE,
    )
    _table_re = re.compile(
        r"^Table '(.*)' (\d+)-max Seat #(?P<button>\d+) is the button"
    )
    _seat_re = re.compile(
        r"^Seat (?P<seat>\d+): (?P<name>.+?) \(\$?(?P<stack>\d+(\.\d+)?) in chips\)"
    )  # noqa
    _hero_re = re.compile(r"^Dealt to (?P<hero_name>.+?) \[(..) (..)\]")
    _pot_re = re.compile(r"^Total pot (\d+(?:\.\d+)?) .*\| Rake (\d+(?:\.\d+)?)")
    _winner_re = re.compile(r"^Seat (\d+): (.+?) collected \((\d+(?:\.\d+)?)\)")
    _showdown_re = re.compile(r"^Seat (\d+): (.+?) showed \[.+?\] and won")
    _ante_re = re.compile(r".*posts the ante (\d+(?:\.\d+)?)")
    _board_re = re.compile(r"(?<=[\[ ])(..)(?=[\] ])")

    def parse_header(self):
        # sections[0] is before HOLE CARDS
        # sections[-1] is before SUMMARY
        pass

    def parse(self):
        """Parses the body of the hand history, but first parse header if not yet parsed."""
        pass

    def _parse_table(self):
        pass

    def _parse_players(self):
        pass

    def _parse_button(self):
        pass

    def _parse_hero(self):
        pass

    def _parse_preflop(self):
        pass

    def _parse_flop(self):
        pass

    def _parse_street(self, street):
        pass

    def _parse_showdown(self):
        pass

    def _parse_pot(self):
        pass

    def _parse_board(self):
        pass

    def _parse_winners(self):
        pass


@attr.s(slots=True)
class _Label:
    """Labels in Player notes."""

    id = attr.ib()
    color = attr.ib()
    name = attr.ib()


@attr.s(slots=True)
class _Note:
    """Player note."""

    player = attr.ib()
    label = attr.ib()
    update = attr.ib()
    text = attr.ib()


class NoteNotFoundError(ValueError):
    """Note not found for player."""


class LabelNotFoundError(ValueError):
    """Label not found in the player notes."""


class Notes:
    """Class for parsing pokerstars XML notes."""

    _color_re = re.compile("^[0-9A-F]{6}$")

    def __init__(self, notes: str):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    @classmethod
    def from_file(cls, filename):
        """Make an instance from a XML file."""
        raise NotImplementedError

    @property
    def players(self):
        """Tuple of player names."""
        pass

    @property
    def label_names(self):
        """Tuple of label names."""
        pass

    @property
    def notes(self):
        """Tuple of notes.."""
        pass

    @property
    def labels(self):
        """Tuple of labels."""
        pass

    def get_note_text(self, player):
        """Return note text for the player."""
        pass

    def get_note(self, player):
        """Return :class:`_Note` tuple for the player."""
        pass

    def add_note(self, player, text, label=None, update=None):
        """Add a note to the xml. If update param is None, it will be the current time."""
        pass

    def append_note(self, player, text):
        """Append text to an already existing note."""
        pass

    def prepend_note(self, player, text):
        """Prepend text to an already existing note."""
        pass

    def replace_note(self, player, text):
        """Replace note text with text. (Overwrites previous note!)"""
        pass

    def change_note_label(self, player, label):
        pass

    def del_note(self, player):
        """Delete a note by player name."""
        pass

    def _find_note(self, player):
        # if player name contains a double quote, the search phrase would be invalid.
        # &quot; entitiy is searched with ", e.g. &quot;bootei&quot; is searched with '"bootei"'
        pass

    def _get_note_data(self, note):
        pass

    def get_label(self, name):
        """Find the label by name."""
        pass

    def add_label(self, name, color):
        """Add a new label. It's id will automatically be calculated."""
        pass

    def del_label(self, name):
        """Delete a label by name."""
        pass

    def _find_label(self, name):
        pass

    def _get_label_id(self, name):
        pass

    def save(self, filename):
        """Save the note XML to a file."""
        pass
