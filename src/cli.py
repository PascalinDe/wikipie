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
:synopsis: Command-line interface.
"""


# standard library imports
import os
import argparse

# third party imports
# library specific imports


def get_argument_parser():
    """Get argument parser.

    :returns: argument parser
    :rtype: ArgumentParser
    """
    try:
        argument_parser = argparse.ArgumentParser()
        argument_parser.add_argument(
            "input", help="XML document (output of Special:Export)"
        )
        argument_parser.add_argument("xsd", help="XML Schema Definition")
        argument_parser.add_argument("-o", "--output", help="output file")
        argument_parser.add_argument(
            "-p", "--processes",
            default=os.cpu_count(), type=int, help="number of processes"
        )
    except Exception as exception:
        raise RuntimeError(
            "failed to get argument parser\t: {}".format(exception)
        )
    return argument_parser
