import re
from datetime import datetime

import attr
import parsedatetime
import requests
from dateutil.tz import tzoffset
from lxml import etree
from pytz import UTC

from .._common import _make_int

__all__ = [
    "search_userid",
    "ForumMember",
    "FORUM_URL",
    "FORUM_MEMBER_URL",
    "AJAX_USERSEARCH_URL",
]


FORUM_URL = "http://forumserver.twoplustwo.com"
FORUM_MEMBER_URL = FORUM_URL + "/members"
AJAX_USERSEARCH_URL = FORUM_URL + "/ajax.php?do=usersearch"


class AmbiguousUserNameError(Exception):
    """Exception when username is not unique, there are more starting with the same."""


class UserNotFoundError(Exception):
    """User cannot be found."""


@attr.s(slots=True)
class _ExtraUser:
    id = attr.ib()
    name = attr.ib()


def search_userid(username):
    pass


class ForumMember:
    """Download and store a member data from the Two Plus Two forum."""

    _tz_re = re.compile("GMT (.*?)\.")
    _attributes = (
        ("username", '//td[@id="username_box"]/h1/text()', str),
        ("rank", '//td[@id="username_box"]/h2/text()', str),
        ("profile_picture", '//td[@id="profilepic_cell"]/img/@src', str),
        ("location", '//div[@id="collapseobj_aboutme"]/div/ul/li/dl/dd[1]/text()', str),
        (
            "total_posts",
            '//div[@id="collapseobj_stats"]/div/fieldset[1]/ul/li[1]/text()',
            _make_int,
        ),  # noqa
        (
            "posts_per_day",
            '//div[@id="collapseobj_stats"]/div/fieldset[1]/ul/li[2]/text()',
            float,
        ),
        ("public_usergroups", '//ul[@id="public_usergroup_list"]/li/text()', tuple),
        ("avatar", '//img[@id="user_avatar"]/@src', str),
    )

    def __init__(self, username):
        self.id = search_userid(username)
        self._download_and_parse()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.username}>"

    @classmethod
    def from_userid(cls, userid: str):
        pass

    def _download_and_parse(self):
        pass

    @property
    def profile_url(self):
        pass

    def _download_page(self):
        pass

    def _parse_attributes(self, root):
        pass

    def _get_timezone(self, root):
        """Find timezone informatation on bottom of the page."""
        pass

    def _parse_last_activity(self, root, tz):
        pass

    def _parse_join_date(self, root):
        pass

    @staticmethod
    def _parse_date(date_str, tz):
        pass
