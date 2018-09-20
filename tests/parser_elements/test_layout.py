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
:synopsis: Layout parser elements tests.
"""


# standard library imports
import unittest

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
from src.parser_elements import layout
from tests.parser_elements import strategies


class TestLayout(unittest.TestCase):
    """Layout parser elements tests."""

    @hypothesis.given(strategies.layout.heading_text(1, 16))
    def test_heading_text_00(self, heading_text):
        """Test heading_text parser element.

        :param str heading_text: heading_text
        """
        parser_element = layout.get_heading_text()
        parse_results = parser_element.parseString(heading_text)
        self.assertEqual(heading_text, parse_results["heading_text"])
        return
