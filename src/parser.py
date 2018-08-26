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
import collections

# third party imports

# library specific imports
import pyparsing


Section = collections.namedtuple(
    "Section", ["level", "heading", "wikitext", "subsections"]
)
Paragraph = collections.namedtuple("Paragraph", ["index", "wikitext"])


class Parser(object):
    """Wikitext parser."""

    @staticmethod
    def find_sections(wikitext, level=2):
        """Find sections.

        :param str wikitext: wikitext
        :param int level: level

        :returns: section
        :rtype: Section
        """
        try:
            #: section_heading = ^, (2*6"=", unicode_char w/o "=",
            #: { unicode_char }-, 2*6"=" ) | ("<h[2-6]>", { unicode_char }-,
            #: "</h[2-6]>", $;
            format_string = (
                r"^(?:={{{0}}}([^=].*?)={{{0}}})|(?:<h{0}>(.+?)</h{0}>)$"
            )
            pattern = re.compile(format_string.format(level), re.MULTILINE)
            matches = [
                match[0] if match[0] else match[1]
                for match in pattern.findall(wikitext)
            ]
            if not matches:
                return Section(level-1, "", wikitext, [])
            else:
                format_string = (
                    r"^(?:={{{0}}}(?:[^=].*?)={{{0}}})|"
                    r"(?:<h{0}>(?:.+?)</h{0}>)$"
                )
                pattern = re.compile(
                    format_string.format(level), re.MULTILINE
                )
                splits = [
                    split for split in pattern.split(wikitext) if split
                ]
                msg = (
                    "number of section headings ({}) does not match "
                    "number of sections ({})"
                ).format(len(matches), len(splits)-1)
                assert len(matches) == len(splits)-1, msg
                if level == 6:
                    subsections = [
                        Section(level, heading, wikitext, [])
                        for heading, wikitext in zip(matches, splits[1:])
                    ]
                    section = Section(level-1, "", splits[0], subsections)
                    return section
                else:
                    section = Section(level-1, "", splits[0], [])
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
            #: paragraph = 2*newline | <br> | <br />;
            #: newline = U+000AU+000D | U+000DU+000A | U+000A | U+000D;
            pattern = r"(?:(?:\n\r)|(?:\r\n)|\n|\r){2}|(?:<br>)|(?:<br />)"
            paragraphs = [
                Paragraph(index, wikitext)
                for index, wikitext in enumerate(re.split(pattern, wikitext))
            ]
        except Exception as exception:
            msg = "failed to find paragraphs\t: {}"
            raise RuntimeError(msg.format(exception))
        return paragraphs
