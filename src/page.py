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

    :ivar str wikitext: wikitext
    """

    def __init__(self, title, id_, ns, revision_id, wikitext):
        """Initialize Wikipedia page.

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
            msg = "failed to initialize Wikipedia page\t: {}"
            raise RuntimeError(msg.format(exception))
        return

    def __getattr__(self, name):
        """Get attribute value.

        :param str name: name

        :returns: attribute value
        """
        if name == "sections":
            value = self._find_sections(self.wikitext)
        elif name == "paragraphs":
            sections = self._find_sections(self.wikitext)
            value = self._find_paragraphs(sections)
        else:
            raise AttributeError
        return value

    def _find_sections(self, wikitext):
        """Find sections.

        :param str wikitext: wikitext

        :returns: sections
        :rtype: list
        """
        return self.parser.find_sections(wikitext)

    def _find_paragraphs(self, sections):
        """Find paragraphs.

        :param list sections: sections

        :returns: paragraphs
        :rtype: list
        """
        try:
            paragraphs = [
                self._find_paragraphs(section)
                if isinstance(section, list)
                else self.parser.find_paragraphs(section)
                for section in sections
            ]
        except Exception as exception:
            msg = "failed to find paragraphs\t: {}"
            raise RuntimeError(msg.format(exception))
        return paragraphs
