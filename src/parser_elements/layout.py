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
:synopsis: Layout parser elements.
"""


# standard library imports
import string

# third party imports
import pyparsing

# library specific imports


#: https://en.wikipedia.org/wiki/Help:Wikitext#Layout


def get_heading_text(flag=False):
    """Get heading_text parser element.

    :param bool flag: toggle debug messages on/off

    heading_text = { printable w/o "=" }-;

    :returns: heading_text
    :rtype: ParserElement
    """
    try:
        initChars = "".join(
            char for char in string.printable if char not in "="
        )
        heading_text = pyparsing.Word(initChars)
        heading_text.leaveWhitespace()
        heading_text.parseWithTabs()
        if flag:
            heading_text.setDebug()
        heading_text.setName("heading_text")
        heading_text = heading_text.setResultsName("heading_text")
    except Exception as exception:
        msg = "failed to get heading_text parser element:{}".format(exception)
        raise RuntimeError(msg)
    return heading_text
