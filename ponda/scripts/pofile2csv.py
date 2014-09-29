# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
from . import parser
from . import converter

def convert(input_, output, includecomment=False):
    data = parser.parse(input_)
    converted = converter.converttolist(data, includecomment)
    converter.converttocsv(output, converted)

def main():
    parser = argparse.ArgumentParser(description='Convert PO File To CSV.')
    args = parser.parse_args()
    parser.add_argument('-o', '--output', type=argparse.FileType('wb', 0))
    parser.add_argument('-i', '--input', type=argparse.FileType('r'))
    parser.add_argument('--includecomment', action='store_true')
    convert(args.input, args.output, args.includecomment)

if __name__=='__main__':
    main()
