# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

u"""
Classes Holding Data
"""
from __future__ import unicode_literals

class ValueHolder(object):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return "<{klass}: {value}>".format(klass=self.__class__, value=self.value)

class Message(object):
    u"""
    """
    def __init__(self, msgid, msgstr, prev=None):
        self.msgid = msgid
        self.msgstr = msgstr
        self.prev = prev
        self.has_plural = isinstance(msgstr, MsgStrList)
    def plural(self, length=0):
        """
        get plural form

        Arguments:
          length: the number of expression
        """
        if not self.has_plural:
            return self
        elif length==0:
            return Message(self.msgid, self.msgstr.get(length), prev=self.prev)
        else:
            return Message(self.msgid.pluralform, self.msgstr.get(length), prev=self.prev)
    def __repr__(self):
        return "<Message: {id}, {str}>".format(id=self.msgid, str=self.msgstr)

class MsgCtxt(ValueHolder):
    pass

class Domain(ValueHolder):
    pass

class MsgId(ValueHolder):
    def __init__(self, value, ctxt=None, pluralform=None):
        self.value = value
        self.ctxt = ctxt
        self.pluralform = pluralform

class MsgStr(ValueHolder):
    def __init__(self, value, plurallist=None):
        self.value = value
        self.plurallist = plurallist

class MsgStrList(MsgStr):
    def __init__(self, valuelist):
        items = []
        for msgstr in valuelist:
            items.append((msgstr.number, msgstr))

        items.sort()
        dic = dict(items)
        self.items = items
        self.value = dic
    def get(self, num):
        return self.value.get(num, None)

class MsgStrPlural(MsgStr):
    def __init__(self, value, number):
        self.value = value
        self.number = number
    def __repr__(self):
        return "<MsgStr[{num}]: {value}>".format(num=self.number, value=self.value)

