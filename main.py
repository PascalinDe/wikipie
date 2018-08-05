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
:synopsis: Wikitext parser.
"""


# standard library imports
import time
import logging

# third party imports

# library specific imports
import src.cli
import src.parser


def main():
    """main function."""
    try:
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(name=main.__name__)
        argument_parser = src.cli.get_argument_parser()
        args = argument_parser.parse_args()
        logger.info("input\t: %s", args.input)
        if args.output:
            logger.info("output\t: %s", args.output)
            if args.mongoDB:
                logger.info("output\t: %s", args.mongoDB)
        else:
            logger.info("output\t: stdout")
            if args.mongoDB:
                logger.info("output\t: %s", args.mongoDB)
        logger.info("parse wikitext")
        time0 = time.time()
        parser = src.parser.Parser()
        parser.parse_wikitext()
        time1 = time.time()
        logger.info("parsed wikitext (%f sec)", time1 - time0)
    except Exception as exception:
        raise RuntimeError("failed to parse wikitext\t: {}".format(exception))
    return


if __name__ == "__main__":
    main()
