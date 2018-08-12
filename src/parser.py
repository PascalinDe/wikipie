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
:synopsis: Wikitext parser.
"""


# standard library imports
import re
# third party imports
# library specific imports
import pyparsing


class Parser(object):
    """Wikitext parser."""

    def __init__(self):
        """Initialize wikitext parser."""
        return

    @staticmethod
    def _find_paragraphs(wikitext):
        """Find paragraphs.

        :param str wikitext: wikitext

        :returns: paragraphs
        :rtype: list
        """
        try:
            #: paragraph = 2*newline;
            #: newline = U+000AU+000D | U+000DU+000A | U+000A | U+000D;
            pattern = "(?:(?:\n\r)|(?:\r\n)|\n|\r){2}"
            paragraphs = [
                paragraph
                for paragraph in re.split(pattern, wikitext) if paragraph
            ]
        except Exception as exception:
            msg = "failed to find paragraphs\t: {}"
            raise RuntimeError(msg.format(exception))
        return paragraphs

    def parse_wikitext(self, wikitext):
        """Parse wikitext.

        :param str wikitext: wikitext

        :returns: wikitext
        :rtype: dict
        """
        paragraphs = self._find_paragraphs(wikitext)
        return paragraphs
