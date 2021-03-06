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
from src.parser_elements import layout


#: https://www.mediawiki.org/wiki/Help:Interwiki_linking
#: https://www.mediawiki.org/wiki/Special:MyLanguage/Markup_spec/BNF/Links#External_links
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

    page_name = unicode w/o "\n\r#:<>[]_{|}",
    { unicode w/o "\n\r#<>[]_{|}" };

    :returns: page_name
    :rtype: ParserElement
    """
    try:
        page_name = pyparsing.Regex(
            r"[^{0}][^{1}]*".format(r"\n\r#:<>\[\]_{|}", r"\n\r#<>\[\]_{|}")
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


def _get_anchor(flag=False):
    """Get anchor parser element.

    :param bool flag: toggle debug messages on/off

    anchor = "#", heading_text | "top";

    :returns: anchor
    :rtype: ParserElement
    """
    try:
        heading_text = layout.get_heading_text(flag=flag)
        top = pyparsing.Literal("top")
        anchor = pyparsing.Combine(
            pyparsing.Literal("#")
            + pyparsing.Or((heading_text, top))
        )
        anchor.leaveWhitespace()
        anchor.parseWithTabs()
        if flag:
            anchor.setDebug()
        anchor.setName("anchor")
        anchor = anchor.setResultsName("anchor")
    except Exception as exception:
        msg = "failed to get anchor parser element:{}".format(exception)
        raise RuntimeError(msg)
    return anchor


def _get_link_text(flag=False):
    """Get link_text parser element.

    :param bool flag: toggle debug messages on/off

    link_text = { unicode w/o "\n\r#<>[]_{|}" }-;

    :returns: link_text parser element
    :rtype: ParserElement
    """
    try:
        link_text = pyparsing.Regex(r"[^{0}]+".format(r"\n\r#<>\[\]_{|}"))
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
    "[[", [ [ namespace ], ":" ], ( anchor | page_name, [ anchor ] ),
    [ "|", [ link_text ] ], "]]", [ word_ending ];

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
        anchor = _get_anchor(flag=flag)
        pipe = pyparsing.Literal("|")
        link_text = _get_link_text(flag=flag)
        internal_link_closing = pyparsing.Literal("]]")
        word_ending = _get_word_ending(flag=flag)
        internal_link = pyparsing.Combine(
            internal_link_opening
            + pyparsing.Optional(pyparsing.Optional(namespace) + colon)
            + pyparsing.Or(
                (
                    anchor,
                    pyparsing.Combine(page_name + pyparsing.Optional(anchor))
                )
            )
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


def _get_url(flag=False):
    """Get URL parser element.

    url = { any of "+-.0-9A-Za-z" }-, "://", { printable w/o "\t\n\r []" }-;

    :param bool flag: toggle debug messages on/off

    :returns: URL parser element
    :rtype: ParserElement
    """
    try:
        url = pyparsing.Regex(
            r"[+\-.0-9A-Za-z]+://[^{0}]+".format(r"\t\n\r \[\]")
        )
        url.leaveWhitespace()
        url.parseWithTabs()
        if flag:
            url.setDebug()
        url.setName("url")
        url = url.setResultsName("url")
    except Exception as exception:
        msg = "failed to get URL parser element:{}".format(exception)
        raise RuntimeError(msg)
    return url


def get_external_link(flag=False):
    """Get external_link parser element.

    external_link = "[", url, [ space | tab, link_text ], "]";

    :param bool flag: toggle debug messages on/off

    :returns: external_link parser element
    :rtype: ParserElement
    """
    try:
        external_link_opening = pyparsing.Literal("[")
        url = _get_url(flag=flag)
        space_tab = pyparsing.Regex(r" |\t")
        link_text = _get_link_text(flag=flag)
        external_link_closing = pyparsing.Literal("]")
        external_link = pyparsing.Combine(
            external_link_opening
            + url
            + pyparsing.Optional(pyparsing.Combine(space_tab + link_text))
            + external_link_closing
        )
        external_link.leaveWhitespace()
        external_link.parseWithTabs()
        if flag:
            external_link.setDebug()
        external_link.setName("external_link")
        external_link = external_link.setResultsName("external_link")
    except Exception as exception:
        msg = "failed to get external_link parser element:{}".format(exception)
        raise RuntimeError(msg)
    return external_link


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
