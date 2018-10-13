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
    # pylint: disable=invalid-name
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

    page_name = unicode w/o "\n\r#:<>[]_{|}",
    { unicode w/o "\n\r#<>[]_{|}" };

    :returns: page_name
    :rtype: str
    """
    init_char = draw(
        hypothesis.strategies.characters(
            blacklist_characters="\n\r#:<>[]_{|}"
        )
    )
    alphabet = draw(
        hypothesis.strategies.characters(
            blacklist_characters="\n\r#<>[]_{|}"
        )
    )
    if min_size > 1:
        page_name_ = init_char + draw(
            hypothesis.strategies.text(
                alphabet=alphabet, min_size=min_size, max_size=max_size-1
            )
        )
    else:
        page_name_ = init_char
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

    link_text = { unicode w/o "\n\r#<>[]_{|}" }-;

    :returns: link_text
    :rtype: str
    """
    alphabet = hypothesis.strategies.characters(
        blacklist_characters="\n\r#<>[]_{|}"
    )
    link_text_ = draw(
        hypothesis.strategies.text(
            alphabet=alphabet, min_size=min_size, max_size=max_size
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


def internal_link(page_name_, namespace_prefix="", piped="", word_ending_=""):
    """Return internal_link.

    :param str page_name_: page_name (contains anchor if so)
    :param str namespace_prefix: namespace prefix
    :param str piped: piped
    :param str word_ending_: word_ending

    namespace_prefix = [ namespace ], ":";
    piped = "|", [ link_text ];

    internal_link =
    "[[", [ namespace_prefix ], ( anchor | page_name, [ anchor ] ),
    [ piped ], "]]", [ word_ending ];

    :returns: internal_link
    :rtype: str
    """
    internal_link_ = (
        "[[{namespace_prefix}{page_name}{piped}]]{word_ending}"
    )
    internal_link_ = internal_link_.format(
        namespace_prefix=namespace_prefix,
        page_name=page_name_,
        piped=piped,
        word_ending=word_ending_
    )
    return internal_link_


@hypothesis.strategies.composite
def redirect(draw, internal_link_):
    """Return redirect.

    :param str internal_link_: internal_link

    redirect = "#REDIRECT", space | tab, internal_link;

    :returns: redirect
    :rtype: str
    """
    space_tab = draw(hypothesis.strategies.sampled_from(" \t"))
    redirect_ = "#REDIRECT" + space_tab + internal_link_
    return redirect_
