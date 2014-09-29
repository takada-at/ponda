# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os
__DIR__ = os.path.abspath(os.path.dirname(__file__))

from ply import lex, yacc
from .data import Domain, MsgId, MsgStr, MsgStrPlural, MsgStrList, Message

class ParserException(Exception):
    pass

DEBUG = 0
tokens = (
    'COMMENT',
    'DOMAIN',
    'PREV_START',
    'PREV_MSGCTXT',
    'PREV_MSGID',
    'PREV_MSGID_PLURAL',
    'PREV_STRING',
    'MSGCTXT',
    'MSGID',
    'MSGID_PLURAL',
    'MSGSTR',
    'NUMBER',
    'STRING'
)

t_DOMAIN = r'domain'
t_MSGID = r'msgid'
t_MSGID_PLURAL = r'msgid_plural'
t_MSGSTR = r'msgstr'
t_MSGCTXT = r'msgctxt'

t_ignore = ' \t'
t_prev_ignore = t_ignore
literals = '[]'

states = (
    ('prev', 'exclusive'),
)

def t_PREV_START(t):
    r'\#\|'
    t.lexer.begin('prev')
    return t

def t_COMMENT(t):
    r'\#.*\n'
    t.value = t.value[:-1]
    return t

def t_STRING(t):
    r'\"(?P<content>([^\\\n]|(\\.))*?)\"'
    stval = t.lexer.lexmatch.group("content")
    t.value = stval if stval else ''
    return t

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

t_prev_NUMBER = t_NUMBER

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    raise SyntaxError("Illegal character %r on %d" % (t.value[0], t.lexer.lineno))

t_prev_error = t_error

def t_prev_MSGCTXT(t):
    r'msgctxt'
    t.type = 'PREV_MSGCTXT'
    return t

def t_prev_MSGID(t):
    r'msgid'
    t.type = 'PREV_MSGID'
    return t

def t_prev_MSGID_PLURAL(t):
    r'msgid_plural'
    t.type = 'PREV_MSGID_PLURAL'
    return t

def t_prev_STRING(t):
    r'\"(?P<content>([^\\\n]|(\\.))*?)\"'
    t.type = 'PREV_STRING'
    stval = t.lexer.lexmatch.group("content")
    t.value = stval if stval else ''
    return t

def t_prev_newline(t):
    r'\n+'
    t.lexer.begin('INITIAL')
    t.lexer.lineno += len(t.value)

def p_empty(p):
    "empty :"
    pass

def p_error(p):
    raise PerserException(str(p))

def p_po_file(p):
    """
    po_file : po_file comment
            | po_file domain
            | po_file message
            | po_file error
            | empty
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_comment(p):
    """
    comment : COMMENT
    """
    p[0] = p[1]

def p_dommain(p):
    """
    domain : DOMAIN STRING
    """
    p[0] = Domain(p[2])

## -- message -- ##
def p_message(p):
    """
    message : message_intro string_list MSGSTR string_list
    """
    if p[1] and isinstance(p[1], tuple):
        msgid = MsgId(p[2], ctxt=p[1][1])
        prev = p[1][0]
    else:
        msgid = MsgId(p[2], ctxt=p[1])
        prev = None

    msgstr = MsgStr(p[4])
    p[0] = Message(msgid, msgstr, prev=prev)

def p_message_plural(p):
    """
    message : message_intro string_list msgid_pluralform pluralform_list
    """
    if p[1] and isinstance(p[1], tuple):
        msgid = MsgId(p[2], ctxt=p[1][1], pluralform=p[3])
        prev = p[1][0]
    else:
        msgid = MsgId(p[2], ctxt=p[1], pluralform=p[3])
        prev = None

    msgstr = MsgStrList(p[4])
    p[0] = Message(msgid, msgstr, prev=prev)

def p_message_no_msgstrplural(p):
    """
    message : message_intro string_list msgid_pluralform
    """
    raise PercerException("missing 'msgstr[0]' section")

def p_message_no_msgidplural(p):
    """
    message : message_intro string_list pluralform_list
    """
    raise PercerException("missing 'msgid_plural' section")

def p_message_no_msgstr(p):
    """
    message : message_intro string_list
    """
    raise PercerException("missing 'msgstr' section")
## -- message end -- ##

def p_message_intro(p):
    """
    message_intro : msg_intro
                  | prev msg_intro
    """
    if len(p)==3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

def p_prev(p):
    """
    prev : prev_msg_intro prev_string_list
         | prev_msg_intro prev_string_list prev_msgid_pluralform
    """
    if len(p)==3:
        p[0] = MsgId(p[2], ctxt=p[1])
    else:
        p[0] = MsgId(p[2], pluralform=p[3], ctxt=p[1])

def p_msg_intro(p):
    """
    msg_intro : MSGID
              | MSGCTXT string_list MSGID
    """
    if len(p)==2:
        return
    else:
        p[0] = p[2]

def p_prev_msg_intro(p):
    """
    prev_msg_intro : PREV_START PREV_MSGID
                   | PREV_START PREV_MSGCTXT prev_string_list PREV_START PREV_MSGID
    """
    if len(p)==3:
        return
    else:
        p[0] = p[3]

def p_msgid_pluralform(p):
    """
    msgid_pluralform : MSGID_PLURAL string_list
    """
    p[0] = p[2]

def p_prev_msgid_pluralform(p):
    """
    prev_msgid_pluralform : PREV_MSGID_PLURAL prev_string_list
    """
    p[0] = p[2]

def p_pluralform_list(p):
    """
    pluralform_list : pluralform
                    | pluralform_list pluralform
    """
    if len(p)==2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_pluralform(p):
    """
    pluralform : MSGSTR '[' NUMBER ']' string_list
    """
    p[0] = MsgStrPlural(number=p[3], value=p[5])

def p_string_list(p):
    """
    string_list : STRING
                | string_list STRING
    """
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_prev_string_list(p):
    """
    prev_string_list : PREV_STRING
                     | prev_string_list PREV_STRING
    """
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

start = str('po_file')
lexer = lex.lex(debug=DEBUG)
parser = yacc.yacc(outputdir=__DIR__, debug=DEBUG, write_tables=False)

def parse(f):
    ret = parser.parse(f.read())
    parser.restart()
    return ret
