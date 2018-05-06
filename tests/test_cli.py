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
:synopsis: Test command-line interface.
"""


# standard library imports
import unittest

# third party imports
# library specific imports
import src.cli


class TestGetArgumentParser(unittest.TestCase):
    """Test get_argument_parser function.

    :cvar str INPUT: input file
    :cvar str OUTPUT: output file
    :cvar str CONFIG: mongoDB configuration file
    """
    INPUT = "foo"
    OUTPUT = "bar"
    CONFIG = "baz"

    def test_positional_arguments_00(self):
        """Test positional arguments."""
        parser = src.cli.get_argument_parser()
        args = parser.parse_args([self.INPUT, self.CONFIG])
        self.assertEqual(
            self.INPUT,
            args.input,
            msg="{} != {}".format(self.INPUT, args.input)
        )
        self.assertEqual(
            self.CONFIG,
            args.config,
            msg="{} != {}".format(self.CONFIG, args.config)
        )
        return

    def test_optional_arguments_00(self):
        """Test optional arguments."""
        parser = src.cli.get_argument_parser()
        args = parser.parse_args([self.INPUT, self.CONFIG, "-o", self.OUTPUT])
        self.assertEqual(
            self.OUTPUT,
            args.output,
            msg="{} != {}".format(self.OUTPUT, args.output)
        )
        return

    def test_optional_arguments_01(self):
        """Test optional arguments."""
        parser = src.cli.get_argument_parser()
        args = parser.parse_args(
            [self.INPUT, self.CONFIG, "--output", self.OUTPUT]
        )
        self.assertEqual(
            self.OUTPUT,
            args.output,
            msg="{} != {}".format(self.OUTPUT, args.output)
        )
        return
