# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
import testbase
testbase

from ponda import parser
parser.debug = 1
data0 = ur"""

msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"POT-Creation-Date: 2014-09-18 14:34+JST\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"

#: path/to/somecode.py:105
msgid "こんにちは"
msgstr "hello"

"""

data1 = ur"""
#: path/to/somecode.py:105
#| msgctxt "previous-context"
#| msgid "previous-untranslated-string"
msgctxt "context"
msgid "untranslated-string"
msgstr "translated-string"
"""

data2 = ur"""
#: path/to/somecode.py:105
#| msgid "previous-untranslated-string"
msgid "untranslated-string"
msgstr "translated-string"
"""

data3 = ur"""
#: path/to/somecode.py:105
#| msgctxt "previous-context"
#| msgid "previous-untranslated-string"
msgid "this is a pen"
msgid_plural "these are pens"
msgstr[0] "これはペンです"
msgstr[1] "これは1本のペンです"
msgstr[2] "これは2本のペンです"
"""

data4 = ur"""
domain "domain"
#: path/to/somecode.py:105
#| msgctxt "previous-context"
#| msgid "previous-untranslated-string"
msgid "this is a pen"
msgstr "これはペンです"
"""

def test_lexer():
    lexer = parser.lexer
    lexer.input(data0)
    tokens = []
    while True:
        tok = lexer.token()
        if tok is None: break
        tokens.append(tok)

    assert 12 == len(tokens)
    assert 'msgid'==tokens[0].value

def test_parser():
    ps = parser.parser
    result = ps.parse(data0)
    assert 3 == len(result)
    assert ''==result[0].msgid.value
    assert result[1].startswith('#')
    assert 'こんにちは'==result[2].msgid.value
    assert 'hello'==result[2].msgstr.value

    result = ps.parse(data1)
    assert 2 == len(result)
    assert result[0].startswith('#')
    assert 'untranslated-string'==result[1].msgid.value
    assert 'translated-string'==result[1].msgstr.value
    assert 'context' == result[1].msgid.ctxt

    prev = result[1].prev
    assert prev
    assert "previous-untranslated-string"==prev.value
    assert "previous-context"==prev.ctxt

    result = ps.parse(data2)
    assert 2 == len(result)
    assert result[0].startswith('#')
    assert 'untranslated-string'==result[1].msgid.value
    assert 'translated-string'==result[1].msgstr.value
    assert result[1].msgid.ctxt is None

    prev = result[1].prev
    assert prev
    assert "previous-untranslated-string"==prev.value
    assert prev.ctxt is None

def test_parser2():
    ps = parser.parser
    result = ps.parse(data3)
    assert 2 == len(result)
    assert result[0].startswith('#')
    assert 'this is a pen'==result[1].msgid.value
    assert 'these are pens'==result[1].msgid.pluralform

    prev = result[1].prev
    assert prev
    assert "previous-untranslated-string"==prev.value
    assert "previous-context"==prev.ctxt

    assert "これはペンです"==result[1].plural(0).msgstr.value
    assert "これは2本のペンです"==result[1].plural(2).msgstr.value


def test_parser3():
    ps = parser.parser
    result = ps.parse(data4)
    assert 3 == len(result)
    assert "domain"==result[0].value
    assert result[1].startswith('#')

    assert 'this is a pen'==result[2].msgid.value
    assert "これはペンです"==result[2].msgstr.value


