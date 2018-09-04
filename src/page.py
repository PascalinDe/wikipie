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
import json

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

    def __init__(self, title, id_, ns, revision_id, wikitext, parser):
        """Initialize root.

        :param str title: title
        :param str id_: id
        :param str ns: ns
        :param str revision_id: revision id
        :param str wikitext: wikitext
        :param Parser parser: wikitext parser
        """
        try:
            self.title = title
            self.id_ = id_
            self.ns = ns
            self.revision_id = revision_id
            self.wikitext = wikitext
            self.parser = parser
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
            value = self.find_pretty()
        elif name == "toc":
            section = self.sections
            value = self.find_toc(section)
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

    def find_pretty(self):
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

    def _find_toc(self, section, level=1):
        """Find table of contents.

        :param Section section: section
        :param int level: level

        :returns: table of contents
        :rtype: str
        """
        try:
            if level == 5:
                toc = {
                    section.heading: [
                        {subsection.heading: []}
                        for subsection in section.subsections
                    ]
                }
                return toc
            else:
                subsections = [
                    self._find_toc(subsection, level=level+1)
                    for subsection in section.subsections
                ]
                toc = {section.heading: subsections}
                return toc
        except Exception as exception:
            msg = "failed to find table of contents\t: {}"
            raise RuntimeError(msg.format(exception))

    def find_toc(self, section, level=1, file_format="json"):
        """Find table of contents.

        :param Section section: section
        :param int level: level
        :param str file_format: file format

        :returns: table of contents
        :rtype: str
        """
        try:
            toc = self._find_toc(section, level=level)
            if file_format == "json":
                toc = json.dumps(toc)
            else:
                msg = "file format {} is not supported".format(file_format)
                raise RuntimeError(msg)
        except RuntimeError:
            raise
        except Exception as exception:
            msg = "failed to find table of contents {}".format(exception)
            raise RuntimeError(msg)
        return toc

    def find_section(self, heading):
        """Find section.

        :param str heading: heading

        :returns: section
        :rtype: Section
        """
        try:
            section = self.sections
            stack = [section]
            while stack:
                section = stack.pop(0)
                if section.heading == heading:
                    break
                else:
                    for subsection in section.subsections:
                        stack.insert(0, subsection)
            else:
                section = None
        except Exception as exception:
            msg = "failed to find section\t: {}".format(exception)
            raise RuntimeError(msg)
        return section

    def find_internal_links(self, wikitext):
        """Find internal links.

        :param str wikitext: wikitext

        :returns: internal links
        :rtype: list
        """
        try:
            internal_links = self.parser.find_internal_links(wikitext)
        except Exception as exception:
            msg = "failed to find internal links\t: {}".format(exception)
            raise RuntimeError(msg)
        return internal_links
