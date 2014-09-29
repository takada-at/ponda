# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .. import converter
from .. import parser
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

#: path/to/somecode.py:106
msgid "こんばんは"
msgstr "good night"

"""

data1 = ur"""
#: path/to/somecode.py:105
#| msgctxt "previous-context"
#| msgid "previous-untranslated-string"
msgctxt "context"
msgid "untranslated-string"
msgstr "translated-string"
"""

def test_converttolist():
    ps = parser.parser
    result = ps.parse(data0)
    listdata = converter.converttolist(result, False)
    print(listdata)
    assert listdata
    assert 2 == len(listdata)

    listdata = converter.converttolist(result, True)
    print(listdata)
    assert listdata
    assert 5 == len(listdata)


    result = ps.parse(data1)
    listdata = converter.converttolist(result, True)
    print(listdata)
    assert listdata
    assert 4 == len(listdata)
    assert ['untranslated-string', 'translated-string'] == listdata[-1]
