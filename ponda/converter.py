# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from .data import Domain, Message

def converttocsv(fio, listdata):
    for row in listdata:
        line = "\t".join(map(unicode, row)) + "\n"
        fio.write(line)

def converttolist(objects, includecomment=True):
    res = []
    for obj in objects:
        res += convertobj(obj, includecomment=includecomment)

    return res

def convertobj(obj, includecomment=True):
    klass = obj.__class__
    if klass is str or klass is unicode:
        if includecomment:
            return [[obj]]
        else:
            return []
    elif klass is Domain:
        if includecomment:
            return [["# domain: {value}".format(value=obj.value)]]
        else:
            return []
    elif klass is Message:
        return convertmessage(obj, includecomment=includecomment)

def convertmessage(message, includecomment=True):
    res = []
    if message.prev and includecomment:
        vals = []
        if message.prev.ctxt:
            vals.append(['#| msgctxt {}'.format(message.prev.ctxt)])

        vals.append(['#| msgid {}'.format(message.prev.value)])
        res += vals

    if message.msgid.value=='' and not includecomment:
        pass
    elif not message.has_plural:
        res.append([message.msgid.value, message.msgstr.value])
    else:
        items = message.msgstr.items
        for num, msg in items:
            if num == 0:
                res.append([message.msgid.value, msg, num])
            else:
                res.append([message.msgid.pluralform, msg, num])

    return res
