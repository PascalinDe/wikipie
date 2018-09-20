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
#: https://en.wikipedia.org/wiki/Wikipedia:Article_titles


def _get_namespace(namespaces, flag=False):
    """Get namespace parser element.

    namespace = any namespace;

    :param bool flag: toggle debug messages on/off
    :param list namespaces: list of namespaces

    :returns: namespace
    :rtype: ParserElement
    """
    try:
        namespace = pyparsing.Or(
            pyparsing.CaselessLiteral(namespace)
            for namespace in namespaces
        )
        if flag:
            namespace.setDebug()
        namespace.setName("namespace")
        namespace = namespace.setResultsName("namespace")
    except Exception as exception:
        msg = "failed to get namespace parser element:{}".format(exception)
        raise RuntimeError(msg)
    return namespace


def _get_page_name(flag=False):
    """Get page_name parser element.

    :param bool flag: toggle debug messages on/off

    page_name = printable w/o "#:<>[]_{|}", { printable w/o "#<>[]_{|}" };

    :returns: page_name
    :rtype: ParserElement
    """
    try:
        initChars = "".join(
            char for char in string.printable if char not in "#:<>[]_{|}"
        )
        bodyChars = "".join(
            char for char in string.printable if char not in "#<>[]_{|}"
        )
        page_name = pyparsing.Word(
            initChars, bodyChars=bodyChars
        )
        page_name.leaveWhitespace()
        page_name.parseWithTabs()
        if flag:
            page_name.setDebug()
        page_name.setName("page_name")
        page_name = page_name.setResultsName("page_name")
    except Exception as exception:
        msg = "failed to get page_name parser element:{}".format(exception)
        raise RuntimeError(msg)
    return page_name


def _get_link_text(flag=False):
    """Get link_text parser element.

    :param bool flag: toggle debug messages on/off

    link_text = { printable w/o "#<>[]_{|}" }-;

    :returns: link_text parser element
    :rtype: ParserElement
    """
    try:
        initChars = "".join(
            char for char in string.printable if char not in "#<>[]_{|}"
        )
        link_text = pyparsing.Word(initChars)
        link_text.leaveWhitespace()
        link_text.parseWithTabs()
        if flag:
            link_text.setDebug()
        link_text.setName("link_text")
        link_text = link_text.setResultsName("link_text")
    except Exception as exception:
        msg = "failed to get link_text parser element:{}".format(exception)
        raise RuntimeError(msg)
    return link_text


def _get_word_ending(flag=False):
    """Get word_ending parser element.

    :param bool flag: toggle debug messages on/off

    word_ending = { ascii_letter }-;

    :returns: word_ending
    :rtype: ParserElement
    """
    try:
        word_ending = pyparsing.Word(
            string.ascii_letters
        )
        if flag:
            word_ending.setDebug()
        word_ending.setName("word_ending")
        word_ending = word_ending.setResultsName("word_ending")
    except Exception as exception:
        msg = "failed to get word_ending:{}".format(exception)
        raise RuntimeError(msg)
    return word_ending


def get_internal_link(namespaces, flag=False):
    """Get internal link parser element.

    internal_link =
    "[[", [ [ namespace ], ":" ], page_name, [ "|", [ link_text ] ], "]]",
    word_ending;

    :param list namespaces: namespaces
    :param bool flag: toggle debug messages on/off

    :returns: internal link
    :rtype: ParserElement
    """
    try:
        internal_link_opening = pyparsing.Literal("[[")
        namespace = _get_namespace(namespaces, flag=flag)
        colon = pyparsing.Literal(":")
        page_name = _get_page_name(flag=flag)
        pipe = pyparsing.Literal("|")
        link_text = _get_link_text(flag=flag)
        internal_link_closing = pyparsing.Literal("]]")
        word_ending = _get_word_ending(flag=flag)
        internal_link = pyparsing.Combine(
            internal_link_opening
            + pyparsing.Optional(pyparsing.Optional(namespace) + colon)
            + page_name
            + pyparsing.Optional(pipe + pyparsing.Optional(link_text))
            + internal_link_closing
            + pyparsing.Optional(word_ending)
        )
        internal_link.leaveWhitespace()
        internal_link.parseWithTabs()
        if flag:
            internal_link.setDebug()
        internal_link.setName("internal_link")
        internal_link = internal_link.setResultsName("internal_link")
    except Exception as exception:
        msg = "failed to return internal link:{}".format(exception)
        raise RuntimeError(msg)
    return internal_link


def get_redirect(namespaces, flag=False):
    """"Get redirect parser element.

    redirect = "#REDIRECT", space | tab, internal_link;

    :param list namespaces: namespaces
    :param bool flag: toggle debug messages on/off

    :returns: redirect
    :rtype: ParserElement
    """
    try:
        internal_link = get_internal_link(namespaces, flag=flag)
        redirect = pyparsing.Combine(
            pyparsing.Literal("#REDIRECT")
            + pyparsing.White(ws=" \t", exact=1)
            + internal_link
        )
        redirect.leaveWhitespace()
        redirect.parseWithTabs()
        if flag:
            redirect.setDebug()
        redirect.setName("redirect")
        redirect.setResultsName("redirect")
    except Exception as exception:
        msg = "failed to return redirect:{}".format(exception)
        raise RuntimeError(msg)
    return redirect
