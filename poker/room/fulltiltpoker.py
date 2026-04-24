import re
from decimal import Decimal

import pytz
from zope.interface import implementer

from .. import handhistory as hh
from .._common import _make_int
from ..card import Card
from ..constants import Action, Currency, Game, GameType, Limit
from ..hand import Combo

__all__ = ["FullTiltPokerHandHistory"]


@implementer(hh.IStreet)
class _Street(hh._BaseStreet):
    def _parse_cards(self, boardline):
        pass

    def _parse_actions(self, actionlines):
        pass

    def _parse_uncalled(self, line):
        pass

    def _parse_raise(self, line):
        pass

    def _parse_win(self, line):
        pass

    def _parse_muck(self, line):
        pass

    def _parse_think(self, line):
        pass

    def _parse_player_action(self, line):
        pass


@implementer(hh.IHandHistory)
class FullTiltPokerHandHistory(hh._SplittableHandHistoryMixin, hh._BaseHandHistory):
    """Parses Full Tilt Poker hands the same way as PokerStarsHandHistory class."""

    rake = None
    tournament_level = None

    _DATE_FORMAT = "%H:%M:%S ET - %Y/%m/%d"
    _TZ = pytz.timezone("US/Eastern")  # ET
    _split_re = re.compile(r" ?\*\*\* ?\n?|\n")
    _header_re = re.compile(
        r"""
        ^Full[ ]Tilt[ ]Poker[ ]                                 # Poker Room
        Game[ ]\#(?P<ident>\d*):[ ]                             # Hand history id
        (?P<tournament_name>                                    # Tournament name
            \$?(?P<buyin>\d*)?                                  # buyin, not always there,
                                                                # part of tournament_name
        .*)[ ]                                                  # end of tournament_name
        \((?P<tournament_ident>\d*)\),[ ]                       # Tournament Number
        Table[ ](?P<table_name>\d*)[ ]-[ ]                      # Table name
        (?P<limit>NL|PL|FL|No Limit|Pot Limit|Fix Limit)[ ]     # limit
        (?P<game>.*?)[ ]-[ ]                                    # game
        (?P<sb>\d*)/(?P<bb>\d*)[ ]-[ ].*                        # blinds
        \[(?P<date>.*)\]$                                       # date in ET
        """,
        re.VERBOSE,
    )
    _seat_re = re.compile(r"^Seat (\d): (.*) \(([\d,]*)\)$")
    _button_re = re.compile(r"^The button is in seat #(\d)$")
    _hero_re = re.compile(r"^Dealt to (?P<hero_name>.*) \[(..) (..)\]$")
    _street_re = re.compile(r"\[([^\]]*)\] \(Total Pot: (\d*)\, (\d) Players")
    _pot_re = re.compile(r"^Total pot ([\d,]*) .*\| Rake (\d*)$")
    _winner_re = re.compile(r"^Seat (?P<seat>\d): (?P<name>.*?) .*collected \((\d*)\),")
    _showdown_re = re.compile(r"^Seat (\d): (.*) showed .* and won")
    _board_re = re.compile(r"(?<=[\[ ])(..)(?=[\] ])")

    def parse_header(self):
        # sections[0] is before HOLE CARDS
        # sections[-1] is before SUMMARY
        pass

    def parse(self):
        """Parses the body of the hand history, but first parse header if not yet parsed."""
        pass

    def _parse_players(self):
        # In hh there is no indication of max_players, so init for 9.
        pass

    def _parse_button(self):
        # one line before the first split.
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

    def _parse_extra(self):
        # tournament name already parsed in header
        pass

    def _parse_streetline(self, start, street):
        """Parse pot, num players."""
        pass
