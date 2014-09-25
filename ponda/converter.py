# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .data import Domain, Message
def converttolist(objects, keepcomment=True):
    res = []
    for obj in objects:
        res += convertobj

def convertobj(obj, keepcomment=True):
    klass = obj.__class__
    if klass is str or klass is unicode:
        if keepcomment:
            return [[obj]]
        else:
            return []
    elif klass is Domain:
        if keepcomment:
            return [["# domain: {value}".format(value=obj.value)]]
        else:
            return []
    elif klass is Message:
        return convertmessage(obj, keepcomment=keepcomment)

def convertmessage(message, keepcomment=True):
    res = []
    if message.prev and keepcomment:
        vals = convertmsgid(message.prev)
        vals = [["# " + row[0]] for row in vals]
        res += vals

    if not message.has_plural:
        res.append([message.msgid.value, message.msgstr.value])
    else:
        items = message.msgstr.items
        for num, msg in items:
            if num == 0:
                res.append([message.msgid.value, msg, num])
            else:
                res.append([message.msgid.pluralform, msg, num])
