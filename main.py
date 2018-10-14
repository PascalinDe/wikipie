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
import src.xml
import src.page
import src.parser


def main():     # pylint: disable=too-many-locals
    """main function."""
    try:
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(name=main.__name__)
        argument_parser = src.cli.get_argument_parser()
        args = argument_parser.parse_args()
        logger.info("input file:%s", args.input)
        if args.output:
            logger.info("output file:%s", args.output)
        else:
            logger.info("output:stdout")
        logger.info("parse wikitext")
        time0 = time.time()
        export_file_parser = src.xml.ExportFileParser(args.input, args.xsd)
        language_attrib = export_file_parser.find_language_attrib()
        logger.info("Wikipedia export file language:%s", language_attrib)
        namespace_elements = export_file_parser.find_namespace_elements()
        logger.info(
            "namespaces:%s", ", ".join(
                "'%s'" % value for value in namespace_elements.values()
            )
        )
        parser = src.parser.Parser(namespace_elements)
        prop = ("title", "id", "ns", "revision")
        pages = []
        for page_element in export_file_parser.find_page_elements(prop=prop):
            for revision_element in page_element["revision"]:
                page = src.page.Page(
                    page_element["title"],
                    page_element["id"],
                    page_element["ns"],
                    revision_element["id"],
                    revision_element["text"]["text"],
                    parser
                )
                pages.append(page)
        for page in pages:
            if page.ns == "0":
                print(page.find_toc(page.section))
                print(page.find_prettyprint(page.section))
                section = page.find_section("Adversaries")
                print(section)
                internal_links = page.find_internal_links(section.wikitext)
                print(internal_links)
                rows = page.create_pagelinks_table()
                print(rows)
        time1 = time.time()
        logger.info("parsed wikitext (%f sec)", time1 - time0)
    except Exception as exception:
        msg = "failed to parse wikitext:{}".format(exception)
        raise RuntimeError(msg)
    return


if __name__ == "__main__":
    main()
