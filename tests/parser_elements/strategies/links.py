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
:synopsis: Links wikitext generation.
"""


# standard library imports
import csv
import string

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports


@hypothesis.strategies.composite
def namespace(draw):
    """Return namespace.

    namespace = any namespace;

    :returns: namespace
    :rtype: str
    """
    with open("tests/parser_elements/data/namespaces.csv") as fp:
        reader = csv.reader(fp)
        namespaces = next(reader)
    namespace_ = draw(hypothesis.strategies.sampled_from(namespaces))
    return namespace_


@hypothesis.strategies.composite
def page_name(draw, min_size, max_size):
    """Return page_name.

    :param int min_size: minimum size
    :param int max_size: maximum size

    page_name = printable w/o "#:<>[]_{|}", { printable w/o "#<>[]_{|}" };

    :returns: page_name
    :rtype: str
    """
    initChars = "".join(
        char for char in string.printable if char not in "#:<>[]_{|}"
    )
    initChar = draw(hypothesis.strategies.sampled_from(initChars))
    bodyChars = "".join(
        char for char in string.printable if char not in "#<>[]_{|}"
    )
    body = draw(
        hypothesis.strategies.text(
            alphabet=bodyChars, min_size=min_size, max_size=max_size
        )
    )
    page_name_ = initChar + body
    return page_name_


def anchor(heading_text=""):
    """Return anchor.

    anchor = "#", heading_text | "top";

    :returns: anchor
    :rtype: str
    """
    if heading_text:
        anchor_ = "#" + heading_text
    else:
        anchor_ = "#" + "top"
    return anchor_


@hypothesis.strategies.composite
def link_text(draw, min_size, max_size):
    """Return link_text.

    :param int min_size: minimum size
    :param int max_size: maximum size

    link_text = { printable w/o "#<>[]_{|}" }-;

    :returns: link_text
    :rtype: str
    """
    bodyChars = "".join(
        char for char in string.printable if char not in "#<>[]_{|}"
    )
    link_text_ = draw(
        hypothesis.strategies.text(
            alphabet=bodyChars,
            min_size=min_size,
            max_size=max_size
        )
    )
    return link_text_


@hypothesis.strategies.composite
def word_ending(draw, min_size, max_size):
    """Return word_ending.

    :param int min_size: minimum size
    :param int max_size: maximum size

    word_ending = { ascii_letter }-;

    :returns: word_ending
    :rtype: str
    """
    word_ending_ = draw(
        hypothesis.strategies.text(
            alphabet=string.ascii_letters,
            min_size=min_size,
            max_size=max_size
        )
    )
    return word_ending_


def internal_link(page_name, namespace_prefix="", piped="", word_ending=""):
    """Return internal_link.

    :param str page_name: page_name (contains anchor if so)
    :param str namespace_prefix: namespace prefix
    :param str piped: piped
    :param str word_ending: word_ending

    namespace_prefix = [ namespace ], ":";
    piped = "|", [ link_text ];

    internal_link =
    "[[", [ namespace_prefix ], ( anchor | page_name, [ anchor ] ),
    [ piped ], "]]", [ word_ending ];

    :returns: internal_link
    :rtype: str
    """
    internal_link = (
        "[[{namespace_prefix}{page_name}{piped}]]{word_ending}"
    )
    internal_link = internal_link.format(
        namespace_prefix=namespace_prefix,
        page_name=page_name,
        piped=piped,
        word_ending=word_ending
    )
    return internal_link


@hypothesis.strategies.composite
def redirect(draw, internal_link):
    """Return redirect.

    :param str internal_link: internal_link

    redirect = "#REDIRECT", space | tab, internal_link;

    :returns: redirect
    :rtype: str
    """
    space_tab = draw(hypothesis.strategies.sampled_from(" \t"))
    redirect = "#REDIRECT" + space_tab + internal_link
    return redirect
