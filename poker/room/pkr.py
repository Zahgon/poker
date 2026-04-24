import re
from decimal import Decimal

import pytz
from zope.interface import implementer

from .. import handhistory as hh
from ..constants import Action, Currency, Game, GameType, Limit, MoneyType
from ..hand import Card, Combo

__all__ = ["PKRHandHistory"]


@implementer(hh.IStreet)
class _Street(hh._BaseStreet):
    def _parse_cards(self, boardline):
        pass

    def _parse_actions(self, actionlines):
        pass

    def _parse_pot(self, line):
        pass

    def _parse_player_action(self, line):
        pass


@implementer(hh.IHandHistory)
class PKRHandHistory(hh._SplittableHandHistoryMixin, hh._BaseHandHistory):
    """Parses PKR hand histories."""

    currency = Currency.USD
    tournament_ident = None
    tournament_name = None
    tournament_level = None

    _DATE_FORMAT = "%d %b %Y %H:%M:%S"
    _TZ = pytz.UTC
    _SPLIT_CARD_SPACE = slice(0, 3, 2)
    _STREET_SECTIONS = {"flop": 2, "turn": 3, "river": 4}
    _split_re = re.compile(r"Dealing |\nDealing Cards\n|Taking |Moving |\n")
    _blinds_re = re.compile(r"^Blinds are now \$([\d.]*) / \$([\d.]*)$")
    _hero_re = re.compile(r"^\[(. .)\]\[(. .)\] to (?P<hero_name>.*)$")
    _seat_re = re.compile(r"^Seat (\d\d?): (.*) - \$([\d.]*) ?(.*)$")
    _sizes_re = re.compile(r"^Pot sizes: \$([\d.]*)$")
    _card_re = re.compile(r"\[(. .)\]")
    _rake_re = re.compile(r"Rake of \$([\d.]*) from pot \d$")
    _win_re = re.compile(r"^(.*) wins \$([\d.]*) with: ")

    def parse_header(self):
        # sections[1] is after blinds, before preflop
        # section[2] is before flop
        # sections[-1] is before showdown
        pass

    def parse(self):
        """Parses the body of the hand history, but first parse header if not yet parsed."""
        pass

    def _parse_players(self):
        # In hh there is no indication of max_players,
        # so init for 10, as there are 10 player tables on PKR.
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

    def _parse_extra(self):
        pass
