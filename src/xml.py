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
:synopsis: Wikipedia export file parser.
"""


# standard library imports
import logging

# third party imports
import lxml.etree

# library specific imports


class ExportFileParser(object):
    """Wikipedia export file parser.

    :cvar dict NSMAP: namespaces
    :ivar _ElementTree tree: tree
    """
    #: https://stackoverflow.com/questions/31250641/python-lxml-using-the-xmllang-attribute-to-retrieve-an-element
    NSMAP = {"xml": "http://www.w3.org/XML/1998/namespace"}

    def __init__(self, xml, xsd):
        """Initialize Wikipedia export file parser.

        :param str xml: XML file
        :param str xsd: XSD
        """
        try:
            logger = logging.getLogger().getChild(__name__)
            logger.info("initializing Wikipedia export file parser")
            tree = lxml.etree.parse(xml)
            self._validate(xml, xsd, tree)
            self.tree = tree
        except Exception as exception:
            msg = "failed to initialize export file parser\t: {}"
            raise RuntimeError(msg.format(exception))
        return

    @staticmethod
    def _validate(xml, xsd, tree):
        """Validate Wikipedia export file.

        :param str xml: XML file
        :param str xsd: XSD
        :param _ElementTree tree: tree
        """
        try:
            xmlschema = lxml.etree.XMLSchema(file=xsd)
            xmlschema.assertValid(tree)
        except lxml.etree.DocumentInvalid:
            msg = "Wikipedia export file does not comply with XSD"
            raise RuntimeError(msg)
        except Exception as exception:
            msg = "failed to validate Wikipedia export file\t:{}"
            raise RuntimeError(msg.format(exception))
        return

    def find_language_attrib(self):
        """Find language attribute.

        :returns: language attribute
        :rtype: str
        """
        try:
            attrib = "{{{}}}lang".format(self.NSMAP["xml"])
            language_attrib = self.tree.getroot().attrib[attrib]
        except Exception as exception:
            msg = "failed to find language attribute\t: {}".format(exception)
            raise RuntimeError(msg)
        return language_attrib

    def find_page_elements(self, prop=("title", "ns", "id")):
        """Find page elements.

        :param tuple prop: properties

        :returns: page elements
        :rtype: generator
        """
        try:
            elements = self.tree.iterfind("{*}page")
            generator = self._find_page_elements(prop, elements)
        except Exception as exception:
            msg = "failed to find page elements\t: {}".format(exception)
            raise RuntimeError(msg)
        return generator

    def _find_page_elements(self, prop, elements):
        """Find page elements.

        :param tuple prop: properties
        :param generator elements: page elements

        :returns: page elements
        :rtype: generator
        """
        for element in elements:
            yield self._find_page_element(prop, element)

    def _find_page_element(self, prop, element):
        """Find page element.

        :param tuple prop: properties
        :param Element page_element: page element

        :returns: page element
        :rtype: dict
        """
        page_element = {}
        if "title" in prop:
            title_element = element.find("{*}title")
            if title_element.text is not None:
                page_element["title"] = title_element.text
            else:
                page_element["title"] = ""
        if "ns" in prop:
            ns_element = element.find("{*}ns")
            if ns_element.text is not None:
                page_element["ns"] = ns_element.text
            else:
                page_element["ns"] = ""
        if "id" in prop:
            pageid_element = element.find("{*}id")
            if pageid_element.text is not None:
                page_element["id"] = pageid_element.text
            else:
                page_element["id"] = ""
        if "redirect" in prop:
            redirect_element = element.find("{*}redirect")
            if redirect_element is not None:
                page_element["redirect"] = redirect_element.attrib["title"]
            else:
                page_element["redirect"] = ""
        if "revision" in prop:
            elements = element.iterfind("{*}revision")
            page_element["revision"] = list(
                self._find_revision_elements(elements)
            )
        return page_element

    def _find_revision_elements(self, elements):
        """Find revision elements.

        :param generator elements: revision elements

        :returns: revision elements
        :rtype: generator
        """
        for element in elements:
            yield self._find_revision_element(element)

    def _find_revision_element(self, element):
        """Find revision element.

        :param Element element: revision element

        :returns: revision element
        :rtype: dict
        """
        try:
            revision_element = {}
            id_element = element.find("{*}id")
            if id_element.text is not None:
                revision_element["id"] = id_element.text
            else:
                revision_element["id"] = ""
            parentid_element = element.find("{*}parentid")
            if parentid_element is not None:
                if parentid_element.text is not None:
                    revision_element["parentid"] = parentid_element.text
                else:
                    revision_element["parentid"] = ""
            else:
                revision_element["parentid"] = ""
            timestamp_element = element.find("{*}timestamp")
            if timestamp_element.text is not None:
                revision_element["timestamp"] = timestamp_element.text
            else:
                revision_element["timestamp"] = ""
            contributor_element = element.find("{*}contributor")
            revision_element["contributor"] = self._find_contributor_element(
                contributor_element
            )
            minor_element = element.find("{*}minor")
            if minor_element is not None:
                if minor_element.text is not None:
                    revision_element["minor"] = minor_element.text
                else:
                    revision_element["minor"] = ""
            else:
                revision_element["minor"] = ""
            comment_element = element.find("{*}comment")
            if comment_element is not None:
                if comment_element.text is not None:
                    revision_element["comment"] = comment_element.text
                else:
                    revision_element["comment"] = ""
            else:
                revision_element["comment"] = ""
            model_element = element.find("{*}model")
            if model_element.text is not None:
                revision_element["model"] = model_element.text
            else:
                revision_element["model"] = ""
            format_element = element.find("{*}format")
            if format_element.text is not None:
                revision_element["format"] = format_element.text
            else:
                revision_element["format"] = ""
            text_element = element.find("{*}text")
            revision_element["text"] = self._find_text_element(text_element)
            sha1_element = element.find("{*}sha1")
            if sha1_element.text is not None:
                revision_element["sha1"] = sha1_element.text
            else:
                revision_element["sha1"] = ""
        except Exception as exception:
            msg = "failed to find revision element\t: {}"
            raise RuntimeError(msg.format(exception))
        return revision_element

    def _find_contributor_element(self, element):
        """Find contributor element.

        :param Element element: contributor element

        :returns: contributor element
        :rtype: dict
        """
        try:
            contributor_element = {}
            username_element = element.find("{*}username")
            if username_element is not None:
                if username_element.text is not None:
                    contributor_element["username"] = username_element.text
                else:
                    contributor_element["username"] = ""
            else:
                contributor_element["username"] = ""
            id_element = element.find("{*}id")
            if id_element is not None:
                if id_element.text is not None:
                    contributor_element["id"] = id_element.text
                else:
                    contributor_element["id"] = ""
            else:
                contributor_element["id"] = ""
            ip_element = element.find("{*}ip")
            if ip_element is not None:
                if ip_element.text is not None:
                    contributor_element["ip"] = ip_element.text
                else:
                    contributor_element["ip"] = ""
            else:
                contributor_element["ip"] = ""
            # attribute (optional)
            if "deleted" in element.attrib:
                contributor_element["deleted"] = element.attrib["deleted"]
            else:
                contributor_element["deleted"] = ""
        except Exception as exception:
            msg = "failed to find contributor element\t: {}"
            raise RuntimeError(msg.format(exception))
        return contributor_element

    def _find_text_element(self, element):
        """Find text element.

        :param Element element: text element

        :returns: text element
        :rtype: str
        """
        try:
            text_element = {}
            if element.text is not None:
                text_element["text"] = element.text
            else:
                text_element["text"] = ""
            # attribute (optional)
            if "deleted" in element.attrib:
                text_element["deleted"] = element.attrib["deleted"]
            else:
                text_element["deleted"] = ""
            # attribute (optional)
            if "id" in element.attrib:
                text_element["id"] = element.attrib["id"]
            else:
                text_element["id"] = ""
            # attribute (optional)
            if "bytes" in element.attrib:
                text_element["bytes"] = element.attrib["bytes"]
            else:
                text_element["bytes"] = ""
        except Exception as exception:
            msg = "failed to find text element\t: {}"
            raise RuntimeError(msg.format(exception))
        return text_element
