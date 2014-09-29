# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import codecs
import io
import sys
from .. import parser
from .. import converter

def convert(input_, output, includecomment=False, sep="\t"):
    data = parser.parse(input_)
    converted = converter.converttolist(data, includecomment)
    converter.converttocsv(output, converted, sep=sep)

def _open(path, mode='r', encoding='utf_8'):
    if path is None:
        if 'r' in mode:
            if sys.version_info >= (3, 0):
                return io.TextIOWrapper(sys.stdin.buffer, encoding=encoding)
            else:
                return codecs.getreader(encoding)(sys.stdin)
        elif 'w' in mode:
            if sys.version_info >= (3, 0):
                return io.TextIOWrapper(sys.stdout.buffer, encoding=encoding)
            else:
                return codecs.getwriter(encoding)(sys.stdout)
    else:
        return io.open(path, encoding=encoding)

def main():
    parser = argparse.ArgumentParser(description='Convert PO File To CSV.')
    parser.add_argument('-o', '--output')
    parser.add_argument('--includecomment', action='store_true')
    parser.add_argument('--encoding', default='utf_8')
    parser.add_argument('--sep', default='\t')
    parser.add_argument('input')
    args = parser.parse_args()
    input_ = _open(args.input, mode='r', encoding=args.encoding)
    output = _open(args.output, mode='w', encoding=args.encoding)
    convert(input_, output, args.includecomment, args.sep)

if __name__=='__main__':
    main()
