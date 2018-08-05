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
:synopsis: XML parser.
"""


# standard library imports

# third party imports
import lxml.etree

# library specific imports


def _validate(xml, xsd, tree):
    """Validate.

    :param str xml: XML file
    :param str xsd: XSD
    :param _ElementTree tree: tree
    """
    try:
        xmlschema = lxml.etree.XMLSchema(file=xsd)
        xmlschema.assertValid(tree)
    except lxml.etree.DocumentInvalid:
        raise RuntimeError("{} does not comply with {}".format(xml, xsd))
    except Exception:
        raise
    return


def parse_xml(xml, xsd):
    """Parse XML.

    :param str xml: XML file
    :param str xsd: XSD

    :returns: tree
    :rtype: _ElementTree tree: tree
    """
    try:
        tree = lxml.etree.parse(xml)
        if xsd:
            _validate(xml, xsd, tree)
    except Exception:
        raise
    return tree
