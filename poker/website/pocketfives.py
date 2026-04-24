import attr
import requests
from lxml import etree

from .._common import _make_float

__all__ = ["get_ranked_players", "WEBSITE_URL", "RANKINGS_URL"]


WEBSITE_URL = "http://www.pocketfives.com"
RANKINGS_URL = WEBSITE_URL + "/rankings/"


@attr.s(slots=True)
class _Player:
    """Pocketfives player data."""

    name = attr.ib()
    country = attr.ib()
    triple_crowns = attr.ib(converter=int)
    monthly_win = attr.ib(converter=int)
    biggest_cash = attr.ib()
    plb_score = attr.ib(converter=_make_float)
    biggest_score = attr.ib(converter=_make_float)
    average_score = attr.ib(converter=_make_float)
    previous_rank = attr.ib(converter=_make_float)


def get_ranked_players():
    """Get the list of the first 100 ranked players."""
    pass
