# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from ..scripts import pofile2csv
import io
from mock import patch, Mock
data0 = ur"""
msgid "こんにちは"
msgstr "hello"
"""

def test_main():
    import argparse
    out = io.StringIO()
    inp = io.StringIO(data0)
    pofile2csv._open= Mock(side_effect=[inp, out])
    dummyargs = argparse.Namespace(output=None, encoding='utf_8', input=None, includecomment=False, sep="\t")
    with patch.object(argparse.ArgumentParser, 'parse_args', return_value=dummyargs) as m:
        pofile2csv.main()
        assert "こんにちは\thello\n" == out.getvalue()

