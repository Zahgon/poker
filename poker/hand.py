import functools
import itertools
import random
import re
from decimal import Decimal
from pathlib import Path

from cached_property import cached_property

from ._common import PokerEnum, _ReprMixin
from .card import BROADWAY_RANKS, Card, Rank

__all__ = [
    "Shape",
    "Hand",
    "Combo",
    "Range",
    "PAIR_HANDS",
    "OFFSUIT_HANDS",
    "SUITED_HANDS",
]


# pregenerated all the possible suit combinations, so we don't have to count them all the time
_PAIR_SUIT_COMBINATIONS = ("cd", "ch", "cs", "dh", "ds", "hs")
_OFFSUIT_SUIT_COMBINATIONS = (
    "cd",
    "ch",
    "cs",
    "dc",
    "dh",
    "ds",
    "hc",
    "hd",
    "hs",
    "sc",
    "sd",
    "sh",
)
_SUITED_SUIT_COMBINATIONS = ("cc", "dd", "hh", "ss")


class Shape(PokerEnum):
    OFFSUIT = "o", "offsuit", "off"
    SUITED = "s", "suited"
    PAIR = ("",)


class _HandMeta(type):
    """Makes Hand class iterable. __iter__ goes through all hands in ascending order."""

    def __new__(metacls, clsname, bases, classdict):
        """Cache all possible Hand instances on the class itself."""
        cls = super(_HandMeta, metacls).__new__(metacls, clsname, bases, classdict)
        cls._all_hands = tuple(cls._get_non_pairs()) + tuple(cls._get_pairs())
        return cls

    def _get_non_pairs(cls):
        pass

    def _get_pairs(cls):
        pass

    def __iter__(cls):
        return iter(cls._all_hands)

    def make_random(cls):
        pass


@functools.total_ordering
class Hand(_ReprMixin, metaclass=_HandMeta):
    """General hand without a precise suit. Only knows about two ranks and shape."""

    __slots__ = ("first", "second", "_shape")

    def __new__(cls, hand):
        if isinstance(hand, cls):
            return hand

        if len(hand) not in (2, 3):
            raise ValueError("Length should be 2 (pair) or 3 (hand)")

        first, second = hand[:2]

        self = object.__new__(cls)

        if len(hand) == 2:
            if first != second:
                raise ValueError(
                    "%r, Not a pair! Maybe you need to specify a suit?" % hand
                )
            self._shape = ""
        elif len(hand) == 3:
            shape = hand[2].lower()
            if first == second:
                raise ValueError(f"{hand!r}; pairs can't have a suit: {shape!r}")
            if shape not in ("s", "o"):
                raise ValueError(f"{hand!r}; Invalid shape: {shape!r}")
            self._shape = shape

        self._set_ranks_in_order(first, second)

        return self

    def __str__(self):
        return f"{self.first}{self.second}{self.shape}"

    def __hash__(self):
        return hash(self.first) + hash(self.second) + hash(self.shape)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        # AKs != AKo, because AKs is better
        return (
            self.first == other.first
            and self.second == other.second
            and self.shape.val == other.shape.val
        )

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        # pairs are better than non-pairs
        if not self.is_pair and other.is_pair:
            return True
        elif self.is_pair and not other.is_pair:
            return False
        elif (
            not self.is_pair
            and not other.is_pair
            and self.first == other.first
            and self.second == other.second
            and self._shape != other._shape
        ):
            # when Rank match, only suit is the deciding factor
            # so, offsuit hand is 'less' than suited
            return self._shape == "o"
        elif self.first == other.first:
            return self.second < other.second
        else:
            return self.first < other.first

    def _set_ranks_in_order(self, first, second):
        # set as Rank objects.
        pass

    def to_combos(self):
        pass

    @property
    def is_suited_connector(self):
        pass

    @property
    def is_suited(self):
        pass

    @property
    def is_offsuit(self):
        pass

    @property
    def is_connector(self):
        pass

    @property
    def is_one_gapper(self):
        pass

    @property
    def is_two_gapper(self):
        pass

    @property
    def rank_difference(self):
        """The difference between the first and second rank of the Hand."""
        pass

    @property
    def is_broadway(self):
        pass

    @property
    def is_pair(self):
        pass

    @property
    def shape(self):
        pass

    @shape.setter
    def shape(self, value):
        pass


PAIR_HANDS = tuple(hand for hand in Hand if hand.is_pair)
"""Tuple of all pair hands in ascending order."""

OFFSUIT_HANDS = tuple(hand for hand in Hand if hand.is_offsuit)
"""Tuple of offsuit hands in ascending order."""

SUITED_HANDS = tuple(hand for hand in Hand if hand.is_suited)
"""Tuple of suited hands in ascending order."""


@functools.total_ordering
class Combo(_ReprMixin):
    """Hand combination."""

    __slots__ = ("first", "second")

    def __new__(cls, combo):
        if isinstance(combo, Combo):
            return combo

        if len(combo) != 4:
            raise ValueError("%r, should have a length of 4" % combo)
        elif combo[0] == combo[2] and combo[1] == combo[3]:
            raise ValueError(f"{combo!r}, Pair can't have the same suit: {combo[1]!r}")

        self = super().__new__(cls)
        self._set_cards_in_order(combo[:2], combo[2:])
        return self

    @classmethod
    def from_cards(cls, first, second):
        pass

    def __str__(self):
        return f"{self.first}{self.second}"

    def __hash__(self):
        return hash(self.first) + hash(self.second)

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.first == other.first and self.second == other.second
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented

        # lookup optimization
        self_is_pair, other_is_pair = self.is_pair, other.is_pair
        self_first, other_first = self.first, other.first

        if self_is_pair and other_is_pair:
            if self_first == other_first:
                return self.second < other.second
            return self_first < other_first

        elif self_is_pair or other_is_pair:
            # Pairs are better than non-pairs
            return self_is_pair < other_is_pair

        else:
            if self_first.rank == other_first.rank:
                if self.second.rank == other.second.rank:
                    # same ranks, suited go first in order by Suit rank
                    if self.is_suited or other.is_suited:
                        return self.is_suited < other.is_suited
                    # both are suited
                    return self_first.suit < other_first.suit
                return self.second < other.second
            return self_first < other_first

    def _set_cards_in_order(self, first, second):
        pass

    def to_hand(self):
        """Convert combo to :class:`Hand` object, losing suit information."""
        pass

    @property
    def is_suited_connector(self):
        pass

    @property
    def is_suited(self):
        pass

    @property
    def is_offsuit(self):
        pass

    @property
    def is_connector(self):
        pass

    @property
    def is_one_gapper(self):
        pass

    @property
    def is_two_gapper(self):
        pass

    @property
    def rank_difference(self):
        """The difference between the first and second rank of the Combo."""
        pass

    @property
    def is_pair(self):
        pass

    @property
    def is_broadway(self):
        pass

    @property
    def shape(self):
        pass

    @shape.setter
    def shape(self, value):
        pass


class _RegexRangeLexer:
    _separator_re = re.compile(r"[,;\s]+")
    _rank = r"([2-9TJQKA])"
    _suit = r"[cdhs♣♦♥♠]"
    # the second card is not the same as the first
    # (negative lookahead for the first matching group)
    # this will not match pairs, but will match e.g. 86 or AK
    _nonpair1 = rf"{_rank}(?!\1){_rank}"
    _nonpair2 = rf"{_rank}(?!\2){_rank}"

    rules = (
        # NAME, REGEX, value extractor METHOD NAME
        ("ALL", r"XX", "_get_value"),
        ("PAIR", rf"{_rank}\1$", "_get_first"),
        ("PAIR_PLUS", rf"{_rank}\1\+$", "_get_first"),
        ("PAIR_MINUS", rf"{_rank}\1-$", "_get_first"),
        ("PAIR_DASH", rf"{_rank}\1-{_rank}\2$", "_get_for_pair_dash"),
        ("BOTH", rf"{_nonpair1}$", "_get_first_two"),
        ("BOTH_PLUS", rf"{_nonpair1}\+$", "_get_first_two"),
        ("BOTH_MINUS", rf"{_nonpair1}-$", "_get_first_two"),
        ("BOTH_DASH", rf"{_nonpair1}-{_nonpair2}$", "_get_for_both_dash"),
        ("SUITED", rf"{_nonpair1}s$", "_get_first_two"),
        ("SUITED_PLUS", rf"{_nonpair1}s\+$", "_get_first_two"),
        ("SUITED_MINUS", rf"{_nonpair1}s-$", "_get_first_two"),
        ("SUITED_DASH", rf"{_nonpair1}s-{_nonpair2}s$", "_get_for_shaped_dash"),
        ("OFFSUIT", rf"{_nonpair1}o$", "_get_first_two"),
        ("OFFSUIT_PLUS", rf"{_nonpair1}o\+$", "_get_first_two"),
        ("OFFSUIT_MINUS", rf"{_nonpair1}o-$", "_get_first_two"),
        ("OFFSUIT_DASH", rf"{_nonpair1}o-{_nonpair2}o$", "_get_for_shaped_dash"),
        ("X_SUITED", rf"{_rank}Xs$|X{_rank}s$", "_get_rank"),
        ("X_SUITED_PLUS", rf"{_rank}Xs\+$|X{_rank}s\+$", "_get_rank"),
        ("X_SUITED_MINUS", rf"{_rank}Xs-$|X{_rank}s-$", "_get_rank"),
        ("X_OFFSUIT", rf"{_rank}Xo$|X{_rank}o$", "_get_rank"),
        ("X_OFFSUIT_PLUS", rf"{_rank}Xo\+$|X{_rank}o\+$", "_get_rank"),
        ("X_OFFSUIT_MINUS", rf"{_rank}Xo-$|X{_rank}o-$", "_get_rank"),
        ("X_PLUS", rf"{_rank}X\+$|X{_rank}\+$", "_get_rank"),
        ("X_MINUS", rf"{_rank}X-$|X{_rank}-$", "_get_rank"),
        ("X_BOTH", rf"{_rank}X$|X{_rank}$", "_get_rank"),
        # might be anything, even pair
        # FIXME: 5s5s accepted
        ("COMBO", rf"{_rank}{_suit}{_rank}{_suit}$", "_get_value"),
    )
    # compile regexes when initializing class, so every instance will have them precompiled
    rules = [
        (name, re.compile(regex, re.IGNORECASE), method)
        for (name, regex, method) in rules
    ]

    def __init__(self, range=""):
        # filter out empty matches
        self.tokens = [token for token in self._separator_re.split(range) if token]

    def __iter__(self):
        """Goes through all the tokens and compare them with the regex rules. If it finds a match,
        makes an appropriate value for the token and yields them.
        """
        for token in self.tokens:
            for name, regex, method_name in self.rules:
                if regex.match(token):
                    val_method = getattr(self, method_name)
                    yield name, val_method(token)
                    break
            else:
                raise ValueError("Invalid token: %s" % token)

    @staticmethod
    def _get_value(token):
        pass

    @staticmethod
    def _get_first(token):
        pass

    @staticmethod
    def _get_rank(token):
        pass

    @classmethod
    def _get_in_order(cls, first_part, second_part, token):
        pass

    @classmethod
    def _get_first_two(cls, token):
        pass

    @classmethod
    def _get_for_pair_dash(cls, token):
        pass

    @classmethod
    def _get_first_smaller_bigger(cls, first_part, second_part, token):
        pass

    @staticmethod
    def _get_rank_in_order(token, first_part, second_part):
        pass

    @classmethod
    # for 'A5-AT'
    def _get_for_both_dash(cls, token):
        pass

    @classmethod
    # for 'A5o-ATo' and 'A5s-ATs'
    def _get_for_shaped_dash(cls, token):
        pass


@functools.total_ordering
class Range:
    """Parses a str range into tuple of Combos (or Hands)."""

    slots = ("_hands", "_combos")

    def __init__(self, range=""):
        self._hands = set()
        self._combos = set()

        for name, value in _RegexRangeLexer(range):
            if name == "ALL":
                for card in itertools.combinations("AKQJT98765432", 2):
                    self._add_offsuit(card)
                    self._add_suited(card)
                for rank in "AKQJT98765432":
                    self._add_pair(rank)

                # full range, no need to parse any more name
                break

            elif name == "PAIR":
                self._add_pair(value)

            elif name == "PAIR_PLUS":
                smallest = Rank(value)
                for rank in (rank.val for rank in Rank if rank >= smallest):
                    self._add_pair(rank)

            elif name == "PAIR_MINUS":
                biggest = Rank(value)
                for rank in (rank.val for rank in Rank if rank <= biggest):
                    self._add_pair(rank)

            elif name == "PAIR_DASH":
                first, second = Rank(value[0]), Rank(value[1])
                ranks = (rank.val for rank in Rank if first <= rank <= second)
                for rank in ranks:
                    self._add_pair(rank)

            elif name == "BOTH":
                self._add_offsuit(value[0] + value[1])
                self._add_suited(value[0] + value[1])

            elif name == "X_BOTH":
                for rank in (r.val for r in Rank if r < Rank(value)):
                    self._add_suited(value + rank)
                    self._add_offsuit(value + rank)

            elif name == "OFFSUIT":
                self._add_offsuit(value[0] + value[1])

            elif name == "SUITED":
                self._add_suited(value[0] + value[1])

            elif name == "X_OFFSUIT":
                biggest = Rank(value)
                for rank in (rank.val for rank in Rank if rank < biggest):
                    self._add_offsuit(value + rank)

            elif name == "X_SUITED":
                biggest = Rank(value)
                for rank in (rank.val for rank in Rank if rank < biggest):
                    self._add_suited(value + rank)

            elif name == "BOTH_PLUS":
                smaller, bigger = Rank(value[0]), Rank(value[1])
                for rank in (rank.val for rank in Rank if smaller <= rank < bigger):
                    self._add_suited(value[1] + rank)
                    self._add_offsuit(value[1] + rank)

            elif name == "BOTH_MINUS":
                smaller, bigger = Rank(value[0]), Rank(value[1])
                for rank in (rank.val for rank in Rank if rank <= smaller):
                    self._add_suited(value[1] + rank)
                    self._add_offsuit(value[1] + rank)

            elif name in ("X_PLUS", "X_SUITED_PLUS", "X_OFFSUIT_PLUS"):
                smallest = Rank(value)
                first_ranks = (rank for rank in Rank if rank >= smallest)

                for rank1 in first_ranks:
                    second_ranks = (rank for rank in Rank if rank < rank1)
                    for rank2 in second_ranks:
                        if name != "X_OFFSUIT_PLUS":
                            self._add_suited(rank1.val + rank2.val)
                        if name != "X_SUITED_PLUS":
                            self._add_offsuit(rank1.val + rank2.val)

            elif name in ("X_MINUS", "X_SUITED_MINUS", "X_OFFSUIT_MINUS"):
                biggest = Rank(value)
                first_ranks = (rank for rank in Rank if rank <= biggest)

                for rank1 in first_ranks:
                    second_ranks = (rank for rank in Rank if rank < rank1)
                    for rank2 in second_ranks:
                        if name != "X_OFFSUIT_MINUS":
                            self._add_suited(rank1.val + rank2.val)
                        if name != "X_SUITED_MINUS":
                            self._add_offsuit(rank1.val + rank2.val)

            elif name == "COMBO":
                self._combos.add(Combo(value))

            elif name == "OFFSUIT_PLUS":
                smaller, bigger = Rank(value[0]), Rank(value[1])
                for rank in (rank.val for rank in Rank if smaller <= rank < bigger):
                    self._add_offsuit(value[1] + rank)

            elif name == "OFFSUIT_MINUS":
                smaller, bigger = Rank(value[0]), Rank(value[1])
                for rank in (rank.val for rank in Rank if rank <= smaller):
                    self._add_offsuit(value[1] + rank)

            elif name == "SUITED_PLUS":
                smaller, bigger = Rank(value[0]), Rank(value[1])
                for rank in (rank.val for rank in Rank if smaller <= rank < bigger):
                    self._add_suited(value[1] + rank)

            elif name == "SUITED_MINUS":
                smaller, bigger = Rank(value[0]), Rank(value[1])
                for rank in (rank.val for rank in Rank if rank <= smaller):
                    self._add_suited(value[1] + rank)

            elif name == "BOTH_DASH":
                smaller, bigger = Rank(value[1]), Rank(value[2])
                for rank in (rank.val for rank in Rank if smaller <= rank <= bigger):
                    self._add_offsuit(value[0] + rank)
                    self._add_suited(value[0] + rank)

            elif name == "OFFSUIT_DASH":
                smaller, bigger = Rank(value[1]), Rank(value[2])
                for rank in (rank.val for rank in Rank if smaller <= rank <= bigger):
                    self._add_offsuit(value[0] + rank)

            elif name == "SUITED_DASH":
                smaller, bigger = Rank(value[1]), Rank(value[2])
                for rank in (rank.val for rank in Rank if smaller <= rank <= bigger):
                    self._add_suited(value[0] + rank)

    @classmethod
    def from_file(cls, filename):
        """Creates an instance from a given file, containing a range.
        It can handle the PokerCruncher (.rng extension) format.
        """
        range_string = Path(filename).open().read()
        return cls(range_string)

    @classmethod
    def from_objects(cls, iterable):
        """Make an instance from an iterable of Combos, Hands or both."""
        pass

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self._all_combos == other._all_combos
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return len(self._all_combos) < len(other._all_combos)
        return NotImplemented

    def __contains__(self, item):
        if isinstance(item, Combo):
            return item in self._combos or item.to_hand() in self._hands
        elif isinstance(item, Hand):
            return item in self._all_hands
        elif isinstance(item, str):
            if len(item) == 4:
                combo = Combo(item)
                return combo in self._combos or combo.to_hand() in self._hands
            else:
                return Hand(item) in self._all_hands

    def __len__(self):
        return self._count_combos()

    def __str__(self):
        return ", ".join(self.rep_pieces)

    def __repr__(self):
        range = " ".join(self.rep_pieces)
        return f"{self.__class__.__name__}('{range}')"

    def __hash__(self):
        return hash(self.combos)

    def to_html(self):
        """Returns a 13x13 HTML table representing the range.

        The table's CSS class is ``range``, pair cells (td element) are ``pair``, offsuit hands are
        ``offsuit`` and suited hand cells has ``suited`` css class.
        The HTML contains no extra whitespace at all.
        Calculating it should not take more than 30ms (which takes calculating a 100% range).
        """
        pass

    def to_ascii(self, border=False):
        """Returns a nicely formatted ASCII table with optional borders."""
        pass

    @property
    def rep_pieces(self):
        """List of str pieces how the Range is represented."""
        pass

    def _get_pieces(self, combos, combos_in_hand):
        pass

    def _shorten_pieces(self, pieces):
        pass

    def _get_format(self, first, last):
        pass

    def _add_pair(self, rank):
        pass

    def _add_offsuit(self, tok):
        pass

    def _add_suited(self, tok):
        pass

    @cached_property
    def hands(self):
        """Tuple of hands contained in this range. If only one combo of the same hand is present,
        it will be shown here. e.g. ``Range('2s2c').hands == (Hand('22'),)``
        """
        pass

    @cached_property
    def combos(self):
        pass

    @cached_property
    def percent(self):
        """What percent of combos does this range have compared to all the possible combos.

        There are 1326 total combos in Hold'em: 52 * 51 / 2 (because order doesn't matter)
        Precision: 2 decimal point
        """
        pass

    def _count_combos(self):
        pass

    @cached_property
    def _all_combos(self):
        pass

    @cached_property
    def _all_hands(self):
        pass


if __name__ == "__main__":
    import cProfile

    print("_all_COMBOS")
    cProfile.run("Range('XX')._all_combos", sort="tottime")
    print("COMBOS")
    cProfile.run("Range('XX').combos", sort="tottime")
    print("HANDS")
    cProfile.run("Range('XX').hands", sort="tottime")

    r = (
        "KK-QQ, 88-77, A5s, A3s, K8s+, K3s, Q7s+, Q5s, Q3s, J9s-J5s, T4s+, 97s, 95s-93s, 87s, "
        "85s-84s, 75s, 64s-63s, 53s, ATo+, K5o+, Q7o-Q5o, J9o-J7o, J4o-J3o, T8o-T3o, 96o+, "
        "94o-93o, 86o+, 84o-83o, 76o, 74o, 63o, 54o, 22"
    )
    print("R _all_COMBOS")
    cProfile.run("Range('%s')._all_combos" % r, sort="tottime")
    print("R COMBOS")
    cProfile.run("Range('%s').combos" % r, sort="tottime")
    print("R HANDS")
    cProfile.run("Range('%s').hands" % r, sort="tottime")
