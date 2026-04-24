from collections.abc import Mapping
from configparser import ConfigParser
from pathlib import Path

import attr

from .constants import Position
from .hand import Range


@attr.s(slots=True)
class _Situation:
    utg = attr.ib()
    utg1 = attr.ib()
    utg2 = attr.ib()
    utg3 = attr.ib()
    utg4 = attr.ib()
    co = attr.ib()
    btn = attr.ib()
    sb = attr.ib()
    bb = attr.ib()
    inaction = attr.ib()
    outaction = attr.ib()
    comment = attr.ib()


@attr.s(slots=True)
class _Spot:
    position = attr.ib()
    range = attr.ib()
    posindex = attr.ib()


_POSITIONS = {"utg", "utg1", "utg2", "utg3", "utg4", "co", "btn", "sb", "bb"}


class Strategy(Mapping):
    def __init__(self, strategy, source="<string>"):
        raise NotImplementedError

    @classmethod
    def from_file(cls, filename):
        raise NotImplementedError

    def __getattr__(self, name):
        # Strategy uses only _Situation._fields, but this way .strategy files are more flexible,
        # because can contain extra values without breaking anything
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def items(self):
        pass

    def keys(self):
        pass

    def get(self, key, default=None):
        pass

    def __getitem__(self, key):
        raise NotImplementedError

    def values(self):
        pass

    def __contains__(self, key):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def get_first_spot(self, situation=0):
        pass
