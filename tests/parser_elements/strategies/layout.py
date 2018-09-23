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
import string

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports


@hypothesis.strategies.composite
def heading_text(draw, min_size, max_size):
    """Return heading_text.

    :param int min_size: minimum size
    :param int max_size: maximum size

    heading_text = { printable w/o "#<=>[]_{|}" }-;

    :returns: heading_text
    :rtype: str
    """
    alphabet = "".join(
        char for char in string.printable if char not in "#<=>[]_{|}"
    )
    heading_text_ = draw(
        hypothesis.strategies.text(
            alphabet=alphabet, min_size=min_size, max_size=max_size
        )
    )
    return heading_text_
