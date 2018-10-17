# wikipie
[![Build Status](https://www.travis-ci.org/PascalinDe/wikipie.svg?branch=master)](https://www.travis-ci.org/PascalinDe/wikipie)

Wikitext parser.

## Usage
The input are an XML document output by [Special:Export](https://en.wikipedia.org/wiki/Special:Export) and its corresponding
[XML Schema Definition](https://www.mediawiki.org/xml/export-0.10.xsd). The output file can be specified using the `-o` option.
In case no output file has been specified, the output is printed to stdout.

### Example
Running `python3 main.py examples/Wikipedia-20180812145957.xml examples/export-0.10.xsd` shows the current features. In the order
of the output

* table of contents (in JSON)
* table of contents (in plaintext)
* dividing Wikipedia pages into sections and selecting them by heading
* finding internal and external links (wikitext)
* creating [pagelinks table](https://www.mediawiki.org/wiki/Special:MyLanguage/Manual:Pagelinks_table) rows

## Dependencies
The XML document and its corresponding XML Schema Definition are processed with the help of [lxml](https://lxml.de/).
The wikitext parser itself uses [PyParsing](https://github.com/pyparsing/pyparsing).
[Hypothesis](https://hypothesis.readthedocs.io/en/master/index.html) is used to generate test cases.
