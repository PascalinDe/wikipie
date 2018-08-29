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
:synopsis:
"""


# standard library imports
import string

# third party imports
import pyparsing

# library specific imports


#: https://www.mediawiki.org/wiki/Help:Interwiki_linking


#: internal_link = "[[", target, [ "|", anchor ], "]]";
#: target = { printables }-;
#: anchor = { anchor }-;
INTERNAL_LINK_OPENING = pyparsing.Literal("[[")

TARGET = pyparsing.Word(
    string.printable.replace("[\\]", "").replace("|", "")
).setResultsName("target")
TARGET.setName("target")

ANCHOR = pyparsing.Word(
    string.printable.replace("[\\]", "")
).setResultsName("anchor")
ANCHOR.setName("anchor")

INTERNAL_LINK_CLOSING = pyparsing.Literal("]]")

INTERNAL_LINK = pyparsing.Combine(
    INTERNAL_LINK_OPENING
    + TARGET
    + pyparsing.Optional(pyparsing.Literal("|") + ANCHOR)
    + INTERNAL_LINK_CLOSING
).setResultsName("internal_link", listAllMatches=True)
INTERNAL_LINK.setName("internal_link")
