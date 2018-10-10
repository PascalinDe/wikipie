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

    # pylint: disable=no-value-for-parameter
    @hypothesis.given(strategies.layout.heading_text(1, 16))
    def test_heading_text_00(self, heading_text):
        """Test heading_text parser element.

        :param str heading_text: heading_text
        """
        parser_element = layout.get_heading_text()
        parse_results = parser_element.parseString(heading_text)
        self.assertEqual(heading_text, parse_results["heading_text"])
        return

    @hypothesis.given(
        hypothesis.strategies.data(), strategies.layout.heading_text(1, 16)
    )
    def test_section_regex_00(self, data, heading_text):
        """Test section regex (capturing).

        :param str heading_text: heading_text
        """
        level = data.draw(
            hypothesis.strategies.integers(min_value=2, max_value=6)
        )
        section = data.draw(strategies.layout.section(heading_text, level))
        section_regex = layout.get_section_regex(level=level)
        match = section_regex.match(section)
        if match.group(1):
            self.assertEqual(heading_text, match.group(1))
        else:
            self.assertEqual(heading_text, match.group(2))
        return

    @hypothesis.given(
        hypothesis.strategies.data(), strategies.layout.heading_text(1, 16)
    )
    def test_section_regex_01(self, data, heading_text):
        """Test section regex (non-capturing).

        :param str heading_text: heading_text
        """
        level = data.draw(
            hypothesis.strategies.integers(min_value=2, max_value=6)
        )
        section = data.draw(strategies.layout.section(heading_text, level))
        section_regex = layout.get_section_regex(
            level=level, non_capturing=True
        )
        match = section_regex.match(section)
        self.assertEqual(section, match[0])
        self.assertRaises(IndexError, match.group, 1)
        return
