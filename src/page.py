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


class Page():
    """Wikipedia page.

    :ivar str title: title
    :ivar str id_: id
    :ivar str ns: ns
    :ivar str revision_id: revision id
    :ivar str wikitext: wikitext
    :ivar Parser parser: wikitext parser
    """

    def __init__(self, title, id_, ns, revision_id, wikitext, parser):
        # pylint: disable=too-many-arguments
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
            self.ns = ns    # pylint: disable=invalid-name
            self.revision_id = revision_id
            self.wikitext = wikitext
            self.parser = parser
        except Exception as exception:
            msg = "failed to initialize root:{}".format(exception)
            raise RuntimeError(msg)

    @staticmethod
    def _search_depth_first(section):
        """Depth-first search.

        :param Section section: section

        :returns: iterator object
        """
        try:
            stack = [section]
            while stack:
                section = stack.pop(0)
                for subsection in section.subsections[::-1]:
                    stack.insert(0, subsection)
                yield section
        except Exception as exception:
            msg = "failed to do depth-first search:{}".format(exception)
            raise RuntimeError(msg)

    @property
    def section(self):
        """(Root) section.

        :returns: section
        :rtype: Section
        """
        try:
            section = self.parser.find_sections(self.wikitext, level=2)
            section = section._replace(heading=self.title)
        except Exception as exception:
            msg = "failed to find section:{}".format(exception)
            raise RuntimeError(msg)
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
            paragraphs = [
                self.parser.find_paragraphs(value.wikitext)
                for value in self._search_depth_first(section)
            ]
        except Exception as exception:
            msg = "failed to find paragraphs:{}".format(exception)
            raise RuntimeError(msg)
        return paragraphs

    def find_prettyprint(self, section):
        """Find prettyprint.

        :param Section section: section

        :returns: prettyprint
        :rtype: str
        """
        try:
            prettyprint = ""
            for value in self._search_depth_first(section):
                if value.level > 1:
                    prettyprint += "|{} {}\n".format(
                        value.level*"-", value.heading
                    )
                else:
                    prettyprint += "{} {}\n".format("-", value.heading)
        except Exception as exception:
            msg = "failed to find prettyprint:{}".format(exception)
            raise RuntimeError(msg)
        return prettyprint

    def _find_toc(self, section, level=1):
        """Find table of contents.

        :param Section section: section
        :param int level: level

        :returns: table of contents
        :rtype: dict
        """
        try:
            if level == 5:
                toc = {
                    section.heading: [
                        {subsection.heading: []}
                        for subsection in section.subsections
                    ]
                }
            else:
                subsections = [
                    self._find_toc(subsection, level=level+1)
                    for subsection in section.subsections
                ]
                toc = {section.heading: subsections}
        except Exception as exception:
            msg = "failed to find table of contents:{}"
            raise RuntimeError(msg.format(exception))
        return toc

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
                msg = "{} file format is not supported".format(file_format)
                raise RuntimeError(msg)
        except RuntimeError:
            raise
        except Exception as exception:
            msg = "failed to find table of contents:{}".format(exception)
            raise RuntimeError(msg)
        return toc

    def find_section(self, heading):
        """Find section.

        :param str heading: heading

        :returns: section
        :rtype: Section or None
        """
        try:
            for section in self._search_depth_first(self.section):
                if section.heading == heading:
                    break
            else:
                section = None
        except Exception as exception:
            msg = "failed to find section:{}".format(exception)
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
            msg = "failed to find internal links:{}".format(exception)
            raise RuntimeError(msg)
        return internal_links

    def create_pagelinks_table_rows(self, wikitext):
        """Create pagelinks table rows
        (q.v. https://www.mediawiki.org/wiki/Special:MyLanguage/
        Manual:Pagelinks_table).

        :param str wikitext: wikitext

        :returns: pagelinks table rows
        :rtype: list
        """
        try:
            internal_links = self.find_internal_links(wikitext)
            pl_from = self.id_
            pl_from_namespace = self.ns
            rows = []
            for internal_link in internal_links:
                pl_namespace = internal_link.namespace
                pl_title = internal_link.page_name
                row = (pl_from, pl_from_namespace, pl_namespace, pl_title)
                rows.append(row)
        except Exception as exception:
            msg = "failed to create pagelinks table rows:{}".format(exception)
            raise RuntimeError(msg)
        return rows

    def create_pagelinks_table(self):
        """Create pagelinks table
        (q.v. https://www.mediawiki.org/wiki/Special:MyLanguage/
        Manual:Pagelinks_table).

        :returns: pagelinks table
        :rtype: list
        """
        try:
            pagelinks_table = []
            for section in self._search_depth_first(self.section):
                pagelinks_table += self.create_pagelinks_table_rows(
                    section.wikitext
                )
        except Exception as exception:
            msg = "failed to create pagelinks table:{}".format(exception)
            raise RuntimeError(msg)
        return pagelinks_table

    def find_external_links(self, wikitext):
        """Find external links.

        :param str wikitext: wikitext

        :returns: external links
        :rtype: list
        """
        try:
            external_links = self.parser.find_external_links(wikitext)
        except Exception as exception:
            msg = "failed to find external_links:{}".format(exception)
            raise RuntimeError(msg)
        return external_links
