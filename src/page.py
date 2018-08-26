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
:synopsis: Wikipedia page.
"""


# standard library imports

# third party imports

# library specific imports
import src.parser


class Page(object):
    """Wikipedia page.

    :ivar str title: title
    :ivar str id_: id
    :ivar str ns: ns
    :ivar str revision_id: revision id
    :ivar str wikitext: wikitext
    :ivar Parser parser: wikitext parser
    """

    def __init__(self, title, id_, ns, revision_id, wikitext):
        """Initialize root.

        :param str title: title
        :param str id_: id
        :param str ns: ns
        :param str revision_id: revision id
        :param str wikitext: wikitext
        """
        try:
            self.title = title
            self.id_ = id_
            self.ns = ns
            self.revision_id = revision_id
            self.wikitext = wikitext
            self.parser = src.parser.Parser()
        except Exception as exception:
            msg = "failed to initialize root\t: {}"
            raise RuntimeError(msg.format(exception))
        return

    def __getattr__(self, name):
        """Get attribute.

        :param str name: name

        :returns: attribute value
        """
        if name == "sections":
            value = self.find_sections(self.wikitext)
        elif name == "paragraphs":
            section = self.sections
            value = self.find_paragraphs(section=section)
        elif name == "pretty":
            value = self._find_pretty()
        else:
            msg = "does not have attribute '{}'".format(name)
            raise RuntimeError(msg)
        return value

    def find_sections(self, wikitext, level=2):
        """Find sections.

        :param str wikitext: wikitext
        :param int level: level

        :returns: section
        :rtype: Section
        """
        try:
            section = self.parser.find_sections(self.wikitext, level=level)
            section = section._replace(heading=self.title)
        except Exception as exception:
            msg = "failed to find sections\t: {}"
            raise RuntimeError(msg.format(exception))
        return section

    def find_paragraphs(self, section=None):
        """Find paragraphs.

        :param Section section: section

        :returns: paragraphs
        :rtype: list
        """
        try:
            if not section:
                section = self.section
            stack = [section]
            paragraphs = []
            while stack:
                section = stack.pop(0)
                paragraphs.append(
                    (
                        section.heading,
                        self.parser.find_paragraphs(section.wikitext)
                    )
                )
                for subsection in section.subsections[::-1]:
                    stack.insert(0, subsection)
        except Exception as exception:
            msg = "failed to find paragraphs\t: {}"
            raise RuntimeError(msg.format(exception))
        return paragraphs

    def _find_pretty(self):
        """Find pretty print.

        :returns: pretty
        :rtype: str
        """
        try:
            section = self.find_sections(self.wikitext)
            stack = [section]
            pretty = ""
            while stack:
                section = stack.pop(0)
                if section.level > 1:
                    pretty += "|{} {}\n".format(
                        section.level*"-", section.heading
                    )
                else:
                    pretty += "{} {}\n".format("-", section.heading)
                for subsection in section.subsections[::-1]:
                    stack.insert(0, subsection)
        except Exception as exception:
            msg = "failed to find pretty print\t: {}"
            raise RuntimeError(msg.format(exception))
        return pretty
