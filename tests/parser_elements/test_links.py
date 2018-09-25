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
:synopsis: Links parser elements tests.
"""


# standard library imports
import csv
import unittest

# third party imports
import hypothesis
import hypothesis.strategies

# library specific imports
from src.parser_elements import links
from tests.parser_elements import strategies


class TestLinks(unittest.TestCase):
    """Links parser elements tests."""

    @staticmethod
    def _get_namespaces():
        """Get namespaces.

        :returns: namespaces
        :rtype: list
        """
        with open("tests/parser_elements/data/namespaces.csv") as fp:
            reader = csv.reader(fp)
            namespaces = next(reader)
        return namespaces

    @hypothesis.given(strategies.links.namespace())
    def test_namespace_00(self, namespace):
        """Test namespace parser element.

        :param str namespace: namespace
        """
        namespaces = self._get_namespaces()
        parser_element = links._get_namespace(namespaces)
        parse_results = parser_element.parseString(namespace)
        self.assertEqual(namespace, parse_results["namespace"])
        return

    @hypothesis.given(strategies.links.page_name(1, 16))
    def test_page_name_00(self, page_name):
        """Test page_name parser element.

        :param str page_name: page_name
        """
        parser_element = links._get_page_name()
        parse_results = parser_element.parseString(page_name)
        self.assertEqual(page_name, parse_results["page_name"])
        return

    @hypothesis.given(strategies.layout.heading_text(1, 16))
    def test_anchor_00(self, heading_text):
        """Test anchor parser element.

        :param str heading_text: heading_text

        anchor = "#", heading_text;
        """
        anchor = strategies.links.anchor(heading_text=heading_text)
        parser_element = links._get_anchor()
        parse_results = parser_element.parseString(anchor)
        self.assertEqual(heading_text, parse_results["anchor"]["heading_text"])
        return

    def test_anchor_01(self):
        """Test anchor parser element.

        anchor = "#", "top";
        """
        anchor = strategies.links.anchor()
        parser_element = links._get_anchor()
        parse_results = parser_element.parseString(anchor)
        self.assertEqual("top", parse_results["anchor"]["heading_text"])
        return

    @hypothesis.given(strategies.links.link_text(1, 16))
    def test_link_text_00(self, link_text):
        """Test link_text parser element.

        :param str link_text: link_text
        """
        parser_element = links._get_link_text()
        parse_results = parser_element.parseString(link_text)
        self.assertEqual(link_text, parse_results["link_text"])
        return

    @hypothesis.given(strategies.links.word_ending(1, 16))
    def test_word_ending_00(self, word_ending):
        """Test word_ending parser element.

        :param str word_ending: word_ending
        """
        parser_element = links._get_word_ending()
        parse_results = parser_element.parseString(word_ending)
        self.assertEqual(word_ending, parse_results["word_ending"])
        return

    @hypothesis.given(strategies.links.page_name(1, 16))
    def test_internal_link_00(self, page_name):
        """Test internal_link parser element.

        :param str page_name: page_name

        internal_link = "[[", page_name, "]]";
        """
        internal_link = strategies.links.internal_link(page_name)
        namespaces = self._get_namespaces()
        parser_element = links.get_internal_link(namespaces)
        parse_results = parser_element.parseString(internal_link)
        self.assertEqual(
            page_name, parse_results["internal_link"]["page_name"]
        )
        return

    @hypothesis.given(strategies.links.page_name(1, 16))
    def test_internal_link_01(self, page_name):
        """Test internal_link parser element.

        :param str page_name: page_name

        internal_link = "[[", ":", page_name, "]]";
        """
        internal_link = strategies.links.internal_link(
            page_name, namespace_prefix=":"
        )
        namespaces = self._get_namespaces()
        parser_element = links.get_internal_link(namespaces)
        parse_results = parser_element.parseString(internal_link)
        self.assertNotIn("namespace", parse_results)
        self.assertEqual(
            page_name, parse_results["internal_link"]["page_name"]
        )
        return

    @hypothesis.given(
        strategies.links.namespace(),
        strategies.links.page_name(1, 16)
    )
    def test_internal_link_02(self, namespace, page_name):
        """Test internal_link parser element.

        :param str namespace: namespace
        :param str page_name: page_name

        internal_link = "[[", namespace, ":", page_name, "]]";
        """
        namespace_prefix = namespace + ":"
        internal_link = strategies.links.internal_link(
            page_name, namespace_prefix=namespace_prefix
        )
        namespaces = self._get_namespaces()
        parser_element = links.get_internal_link(namespaces)
        parse_results = parser_element.parseString(internal_link)
        self.assertEqual(
            namespace, parse_results["internal_link"]["namespace"]
        )
        self.assertEqual(
            page_name, parse_results["internal_link"]["page_name"]
        )
        return

    @hypothesis.given(
        strategies.links.namespace(),
        strategies.links.page_name(1, 16)
    )
    def test_internal_link_03(self, namespace, page_name):
        """Test internal_link parser element.

        :param str namespace: namespace
        :param str page_name: page_name

        internal_link = "[[", namespace, ":", page_name, "|", "]]";
        """
        namespace_prefix = namespace + ":"
        piped = "|"
        internal_link = strategies.links.internal_link(
            page_name, namespace_prefix=namespace_prefix, piped=piped
        )
        namespaces = self._get_namespaces()
        parser_element = links.get_internal_link(namespaces)
        parse_results = parser_element.parseString(internal_link)
        self.assertEqual(
            namespace, parse_results["internal_link"]["namespace"]
        )
        self.assertEqual(
            page_name, parse_results["internal_link"]["page_name"]
        )
        self.assertNotIn("link_text", parse_results["internal_link"])
        return

    @hypothesis.given(
        strategies.links.namespace(),
        strategies.links.page_name(1, 16),
        strategies.links.link_text(1, 16)
    )
    def test_internal_link_04(self, namespace, page_name, link_text):
        """Test internal_link parser element.

        :param str namespace: namespace
        :param str page_name: page_name
        :param str link_text: link_text

        internal_link = "[[", namespace, ":", page_name, "|", link_text, "]]";
        """
        namespace_prefix = namespace + ":"
        piped = "|" + link_text
        internal_link = strategies.links.internal_link(
            page_name, namespace_prefix=namespace_prefix, piped=piped
        )
        namespaces = self._get_namespaces()
        parser_element = links.get_internal_link(namespaces)
        parse_results = parser_element.parseString(internal_link)
        self.assertEqual(
            namespace, parse_results["internal_link"]["namespace"]
        )
        self.assertEqual(
            page_name, parse_results["internal_link"]["page_name"]
        )
        self.assertEqual(
            link_text, parse_results["internal_link"]["link_text"]
        )
        return

    @hypothesis.given(
        strategies.links.namespace(),
        strategies.links.page_name(1, 16),
        strategies.links.link_text(1, 16),
        strategies.links.word_ending(1, 16)
    )
    def test_internal_link_05(
            self, namespace, page_name, link_text, word_ending
    ):
        """Test internal_link parser element.

        :param str namespace: namespace
        :param str page_name: page_name
        :param str link_text: link_text
        :param str word_ending: word_ending

        internal_link = "[[", namespace, ":", page_name, "|", link_text, "]]",
        word_ending;
        """
        namespace_prefix = namespace + ":"
        piped = "|" + link_text
        internal_link = strategies.links.internal_link(
            page_name,
            namespace_prefix=namespace_prefix,
            piped=piped,
            word_ending=word_ending
        )
        namespaces = self._get_namespaces()
        parser_element = links.get_internal_link(namespaces)
        parse_results = parser_element.parseString(internal_link)
        self.assertEqual(
            namespace, parse_results["internal_link"]["namespace"]
        )
        self.assertEqual(
            page_name, parse_results["internal_link"]["page_name"]
        )
        self.assertEqual(
            link_text, parse_results["internal_link"]["link_text"]
        )
        self.assertEqual(
            word_ending, parse_results["internal_link"]["word_ending"]
        )
        return

    @hypothesis.given(
        strategies.layout.heading_text(1, 16),
        strategies.links.link_text(1, 16),
        strategies.links.word_ending(1, 16)
    )
    def test_internal_link_06(self, heading_text, link_text, word_ending):
        """Test internal_link parser element.

        :param str heading_text: heading_text
        :param str link_text: link_text
        :param str word_ending: word_ending

        internal_link = "[[", anchor, "|", link_text, "]]", word_ending;
        """
        anchor = strategies.links.anchor(heading_text=heading_text)
        piped = "|" + link_text
        internal_link = strategies.links.internal_link(
            anchor,
            piped=piped,
            word_ending=word_ending
        )
        namespaces = self._get_namespaces()
        parser_element = links.get_internal_link(namespaces)
        parse_results = parser_element.parseString(internal_link)
        self.assertEqual(
            heading_text,
            parse_results["internal_link"]["anchor"]["heading_text"]
        )
        self.assertEqual(
            link_text, parse_results["internal_link"]["link_text"]
        )
        self.assertEqual(
            word_ending, parse_results["internal_link"]["word_ending"]
        )
        return

    @hypothesis.given(
        strategies.links.namespace(),
        strategies.links.page_name(1, 16),
        strategies.layout.heading_text(1, 16)
    )
    def test_internal_link_07(self, namespace, page_name, heading_text):
        """Test internal_link parser element.

        :param str namespace: namespace
        :param str page_name: page_name
        :param str heading_text: heading_text

        internal_link = "[[", namespace, ":", page_name, anchor, "]]";
        """
        pass

    @hypothesis.given(
        hypothesis.strategies.data(),
        strategies.links.page_name(1, 16)
    )
    def test_redirect_00(self, data, page_name):
        """Test redirect parser element.

        :param str page_name: page_name
        """
        internal_link = strategies.links.internal_link(page_name)
        redirect = data.draw(strategies.links.redirect(internal_link))
        namespaces = self._get_namespaces()
        parser_element = links.get_redirect(namespaces)
        parse_results = parser_element.parseString(redirect)
        self.assertEqual(internal_link, parse_results["internal_link"][0])
        return
