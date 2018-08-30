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
def internal_link(name, results_name, list_all_matches=False, debug=False):
    """Returns internal link parser element.

    internal_link = "[[", target, [ [ "|" ], anchor ], "]]";
    target = { printable w/o "[]|" }-;
    anchor = { printable w/o "[]" }-;

    :param str name: name
    :param str results_name: results name
    :param bool debug: toggle debug messages on/off

    :returns: internal link
    :rtype: ParserElement
    """
    try:
        printable = string.printable.replace("[\\]", "")
        internal_link_opening = pyparsing.Literal("[[")
        target = pyparsing.Word(
            printable.replace("|", "")
        ).setResultsName("target")
        target.setName("target")
        if debug:
            target.setDebug()
        pipe = pyparsing.Literal("|")
        anchor = pyparsing.Word(printable).setResultsName("anchor")
        anchor.setName("anchor")
        if debug:
            anchor.setDebug()
        internal_link_closing = pyparsing.Literal("]]")
        internal_link = pyparsing.Combine(
            internal_link_opening
            + target
            + pyparsing.Optional(pyparsing.Optional(pipe) + anchor)
            + internal_link_closing
        ).setResultsName(results_name, listAllMatches=list_all_matches)
        internal_link.setName(name)
        if debug:
            internal_link.setDebug()
    except Exception as exception:
        msg = "failed to return internal link\t: {}"
        raise RuntimeError(msg.format(exception))
    return internal_link
