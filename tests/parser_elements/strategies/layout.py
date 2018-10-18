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
:synopsis: Layout wikitext generation.
"""


# standard library imports

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports


@hypothesis.strategies.composite
def heading_text(draw, min_size, max_size):
    """Return heading_text.

    :param int min_size: minimum size
    :param int max_size: maximum size

    heading_text = { unicode_char w/o "\n\r#<=>[]_{|}" }-;

    :returns: heading_text
    :rtype: str
    """
    characters = hypothesis.strategies.characters(
        blacklist_characters="\n\r#<=>[]_{|}"
    )
    heading_text_ = draw(
        hypothesis.strategies.text(
            alphabet=characters, min_size=min_size, max_size=max_size
        )
    )
    return heading_text_


@hypothesis.strategies.composite
def section(draw, heading_text_, level):
    """Return section.

    :param str heading_text_: heading_text
    :param int level: level

    :returns: section
    :rtype: str
    """
    elements = (
        "{0}{1}{0}".format(level*"=", heading_text_),
        "<h{0}>{1}</h{0}>".format(level, heading_text_)
    )
    section_ = draw(hypothesis.strategies.sampled_from(elements))
    return section_


@hypothesis.strategies.composite
def line_break(draw):
    """Return line_break.

    :returns: line_break
    :rtype: str
    """
    elements = (
        draw(hypothesis.strategies.from_regex(r"(?:\n|(?:\r\n)){2}")),
        "<br>",
        "<br \>"
    )
    line_break_ = draw(hypothesis.strategies.sampled_from(elements))
    return line_break_
