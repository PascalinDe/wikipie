#    This file is part of WikiPie 1.0.
#    Copyright (C) 2018  Carine Dengler
#
#    WikiPie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
:synopsis: Page elements.
"""


# standard library imports
import collections

# third party imports
# library specific imports


_Section = collections.namedtuple(
    "Section", ["level", "heading", "wikitext", "subsections"]
)


class Section(_Section):    # pylint: disable=missing-docstring
    __slots__ = ()

    def __repr__(self):
        return "{}\n{}".format(self.heading, self.wikitext)


_Paragraph = collections.namedtuple("Paragraph", ["index", "wikitext"])


class Paragraph(_Paragraph):    # pylint: disable=missing-docstring
    __slots__ = ()

    def __repr__(self):
        return " {}".format(self.wikitext)


_InternalLink = collections.namedtuple(
    "InternalLink", ["namespace", "page_name", "link_text"]
)


class InternalLink(_InternalLink):  # pylint: disable=missing-docstring
    __slots__ = ()

    def __repr__(self):
        return self.link_text

    def __format__(self, format_spec):
        return self.link_text
