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
:synopsis: Test mongoDB client.
"""


# standard library imports
import unittest

# third party imports

# library specific imports
import src.mongodb


class TestGetClient(unittest.TestCase):
    """Test get_client function."""

    def test_positional_arguments_00(self):
        """Test positional arguments."""
        config = {}
        with self.assertRaises(RuntimeError):
            src.mongodb.get_client(config)
        return
