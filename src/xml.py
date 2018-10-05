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


class ExportFileParser():
    """Wikipedia export file parser.

    (q.v. https://stackoverflow.com/questions/31250641/
    python-lxml-using-the-xmllang-attribute-to-retrieve-an-element)

    :cvar dict NSMAP: namespaces
    :ivar _ElementTree tree: tree
    """
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
            self._validate(xsd, tree)
            self.tree = tree
        except Exception as exception:
            msg = "failed to initialize export file parser\t: {}"
            raise RuntimeError(msg.format(exception))

    @staticmethod
    def _validate(xsd, tree):
        """Validate Wikipedia export file.

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

    def find_siteinfo_element(self):
        """Find siteinfo element.

        :returns: siteinfo element
        :rtype: Element
        """
        try:
            siteinfo_element = self.tree.find("{*}siteinfo")
        except Exception as exception:
            msg = "failed to find siteinfo element\t: {}".format(exception)
            raise RuntimeError(msg)
        return siteinfo_element

    def find_namespace_elements(self):
        """Find namespace elements.

        :returns: namespace elements
        :rtype: dict
        """
        try:
            siteinfo_element = self.find_siteinfo_element()
            namespaces_element = siteinfo_element.find("{*}namespaces")
            namespace_elements = {}
            for element in namespaces_element.iterfind("{*}namespace"):
                if element.text is not None:
                    namespace_elements[element.attrib["key"]] = element.text
                else:
                    namespace_elements[element.attrib["key"]] = "(Main)"
        except Exception as exception:
            msg = "failed to find namespace elements\t: {}".format(exception)
            raise RuntimeError(msg)
        return namespace_elements

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
            page_element["title"] = title_element.text or ""
        if "ns" in prop:
            ns_element = element.find("{*}ns")
            page_element["ns"] = ns_element.text or ""
        if "id" in prop:
            pageid_element = element.find("{*}id")
            page_element["id"] = pageid_element.text or ""
        if "redirect" in prop:
            redirect_element = element.find("{*}redirect")
            page_element["redirect"] = redirect_element.text or ""
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
            revision_element["id"] = id_element.text or ""
            parentid_element = element.find("{*}parentid")
            if parentid_element is not None:
                revision_element["parentid"] = parentid_element.text or ""
            else:
                revision_element["parentid"] = ""
            timestamp_element = element.find("{*}timestamp")
            revision_element["timestamp"] = timestamp_element.text or ""
            revision_element["contributor"] = self._find_contributor_element(
                element.find("{*}contributor")
            )
            minor_element = element.find("{*}minor")
            if minor_element is not None:
                revision_element["minor"] = minor_element.text or ""
            else:
                revision_element["minor"] = ""
            comment_element = element.find("{*}comment")
            if comment_element is not None:
                revision_element["comment"] = comment_element.text or ""
            else:
                revision_element["comment"] = ""
            model_element = element.find("{*}model")
            revision_element["model"] = model_element.text or ""
            format_element = element.find("{*}format")
            revision_element["format"] = format_element.text or ""
            text_element = element.find("{*}text")
            revision_element["text"] = self._find_text_element(text_element)
            sha1_element = element.find("{*}sha1")
            revision_element["sha1"] = sha1_element.text or ""
        except Exception as exception:
            msg = "failed to find revision element\t: {}"
            raise RuntimeError(msg.format(exception))
        return revision_element

    @staticmethod
    def _find_contributor_element(element):
        """Find contributor element.

        :param Element element: contributor element

        :returns: contributor element
        :rtype: dict
        """
        try:
            contributor_element = {}
            username_element = element.find("{*}username")
            if username_element is not None:
                contributor_element["username"] = username_element.text or ""
            else:
                contributor_element["username"] = ""
            id_element = element.find("{*}id")
            if id_element is not None:
                contributor_element["id"] = id_element.text or ""
            else:
                contributor_element["id"] = ""
            ip_element = element.find("{*}ip")
            if ip_element is not None:
                contributor_element["ip"] = ip_element.text or ""
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

    @staticmethod
    def _find_text_element(element):
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
