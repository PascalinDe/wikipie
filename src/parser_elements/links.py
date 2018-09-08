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
:synopsis: Links parser elements.
"""


# standard library imports
import string

# third party imports
import pyparsing

# library specific imports


#: https://www.mediawiki.org/wiki/Help:Interwiki_linking
#: https://en.wikipedia.org/wiki/Wikipedia:Namespace
def internal_link(namespaces, flag=False):
    """Returns internal link parser element.

    internal_link =
    "[[", [ [ namespace ], ":" ], page_name, [ [ "|" ], anchor ], "]]",
    word_ending;
    namespace = any namespace;
    page_name = { printable w/o "#<>[]_{|}" }-;
    anchor = { printable w/o "#<>[]_{|}" }-;
    word_ending = { ascii_letter }-;

    :param list namespaces: namespaces
    :param bool flag: toggle debug messages on/off

    :returns: internal link
    :rtype: ParserElement
    """
    try:
        printable = "".join(
            char for char in string.printable if char not in "#<>[]_{|}"
        )
        internal_link_opening = pyparsing.Literal("[[")
        colon = pyparsing.Literal(":")
        namespace = pyparsing.Or(
            pyparsing.CaselessKeyword(namespace) for namespace in namespaces
        ).setResultsName("namespace")
        namespace.setName("namespace")
        page_name = pyparsing.Word(printable).setResultsName("page_name")
        page_name.setName("page_name")
        pipe = pyparsing.Literal("|")
        anchor = pyparsing.Word(printable).setResultsName("anchor")
        anchor.setName("anchor")
        internal_link_closing = pyparsing.Literal("]]")
        word_ending = pyparsing.Word(
            string.ascii_letters
        ).setResultsName("word_ending")
        word_ending.setName("word_ending")
        internal_link = pyparsing.Combine(
            internal_link_opening
            + pyparsing.Optional(colon + pyparsing.Optional(namespace))
            + page_name
            + pyparsing.Optional(pyparsing.Optional(pipe) + anchor)
            + internal_link_closing
            + pyparsing.Optional(word_ending)
        ).setResultsName("internal_link", listAllMatches=True)
        internal_link.setName("internal_link")
        if flag:
            internal_link.setDebug()
    except Exception as exception:
        msg = "failed to return internal link\t: {}"
        raise RuntimeError(msg.format(exception))
    return internal_link
