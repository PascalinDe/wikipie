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
import re

# third party imports

# library specific imports
import src.page_elements
import src.parser_elements.links
import src.parser_elements.layout


class Parser():
    """Wikitext parser.

    :ivar dict namespaces: namespaces
    :ivar bool flag: toggle debug messages on/off
    """

    def __init__(self, namespaces, flag=False):
        """Initialize wikitext parser.

        :param dict namespaces: namespaces
        :param bool flag: toggle debug messages on/off
        """
        try:
            self.namespaces = namespaces
            self.flag = flag
        except Exception as exception:
            msg = "failed to initialize wikitext parser\t: {}"
            raise RuntimeError(msg.format(exception))

    @staticmethod
    def find_sections(wikitext, level=2):
        """Find sections.

        :param str wikitext: wikitext
        :param int level: level

        :returns: section
        :rtype: Section
        """
        try:
            pattern = src.parser_elements.layout.get_section_regex(
                level=level
            )
            matches = [
                match[0] if match[0] else match[1]
                for match in pattern.findall(wikitext)
            ]
            if not matches:     # pylint: disable=no-else-return
                return src.page_elements.Section(level-1, "", wikitext, [])
            else:
                pattern = src.parser_elements.layout.get_section_regex(
                    level=level, non_capturing=True
                )
                splits = [
                    split for split in pattern.split(wikitext) if split
                ]
                msg = (
                    "number of section headings ({}) does not match "
                    "number of sections ({})"
                ).format(len(matches), len(splits)-1)
                assert len(matches) == len(splits)-1, msg
                if level == 6:  # pylint: disable=no-else-return
                    subsections = [
                        src.page_elements.Section(level, heading, wikitext, [])
                        for heading, wikitext in zip(matches, splits[1:])
                    ]
                    section = src.page_elements.Section(
                        level-1, "", splits[0], subsections
                    )
                    return section
                else:
                    section = src.page_elements.Section(
                        level-1, "", splits[0], []
                    )
                    subsections = [
                        Parser.find_sections(split, level=level+1)
                        for split in splits[1:]
                    ]
                    subsections = [
                        subsection._replace(heading=heading)
                        for heading, subsection in zip(matches, subsections)
                    ]
                    return section._replace(subsections=subsections)
        except Exception as exception:
            msg = "failed to find sections\t: {}"
            raise RuntimeError(msg.format(exception))

    @staticmethod
    def find_paragraphs(wikitext):
        """Find paragraphs.

        :param str wikitext: wikitext

        :returns: paragraphs
        :rtype: list
        """
        try:
            pattern = src.parser_elements.layout.get_line_break_regex()
            paragraphs = [
                src.page_elements.Paragraph(index, wikitext)
                for index, wikitext in enumerate(pattern.split(wikitext))
            ]
        except Exception as exception:
            msg = "failed to find paragraphs\t: {}"
            raise RuntimeError(msg.format(exception))
        return paragraphs

    def find_internal_links(self, wikitext):
        """Find internal links.

        :param str wikitext: wikitext

        :returns: internal links
        :rtype: list
        """
        try:
            indexes = {v: k for k, v in self.namespaces.items()}
            parser_element = src.parser_elements.links.get_internal_link(
                [v for k, v in self.namespaces.items() if k != "0"],
                flag=self.flag
            )
            tokens = [
                tokens for tokens, _, _ in parser_element.scanString(wikitext)
            ]
            internal_links = []
            for token in tokens:
                if "namespace" in token:
                    namespace = indexes[token["internal_link"]["namespace"]]
                else:
                    namespace = indexes["(Main)"]
                if "anchor" in token["internal_link"]:
                    if "page_name" in token["internal_link"]:
                        page_name = (
                            token["internal_link"]["page_name"]
                            + token["internal_link"]["anchor"][0]
                        )
                    else:
                        page_name = token["internal_link"]["anchor"][0]
                else:
                    page_name = token["internal_link"]["page_name"]
                if "link_text" in token:
                    link_text = token["internal_link"]["link_text"]
                else:
                    link_text = page_name
                if "word_ending" in token:
                    link_text += token["internal_link"]["word_ending"]
                internal_links.append(
                    src.page_elements.InternalLink(
                        namespace, page_name, link_text
                    )
                )
        except Exception as exception:
            msg = "failed to find internal links\t: {}"
            raise RuntimeError(msg.format(exception))
        return internal_links
