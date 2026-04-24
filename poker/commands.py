import datetime as dt
import typing

import click
from dateutil import tz

LOCALTIMEZONE = tz.tzlocal()


def _print_header(title):
    pass


def _print_values(*args):
    pass


@click.group()
def poker():
    """Main command for the poker framework."""


@poker.command(
    "range", short_help="Prints the range in a formatted table in ASCII or HTML."
)
@click.argument("range")
@click.option("--no-border", is_flag=True, help="Don't show border.")
@click.option(
    "--html", is_flag=True, help="Output html, so you can paste it on a website."
)
def range_(range, no_border, html):
    """Prints the given range in a formatted table either in a plain ASCII or HTML.
    The only required argument is the range definition, e.g. "A2s+ A5o+ 55+"
    """
    pass


@poker.command(
    "2p2player", short_help="Get profile information about a Two plus Two member."
)
@click.argument("username")
def twoplustwo_player(username):
    """Get profile information about a Two plus Two Forum member given the username."""
    pass


@poker.command(short_help="List pocketfives ranked players (1-100).")
@click.argument("num", type=click.IntRange(1, 100), default=100)
def p5list(num):
    """List pocketfives ranked players, max 100 if no NUM, or NUM if specified."""
    pass


@poker.command(short_help="Show PokerStars status like active players.")
def psstatus():
    """Shows PokerStars status such as number of players, tournaments."""
    pass
