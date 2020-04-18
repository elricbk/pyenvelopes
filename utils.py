# encoding: utf-8

def formatValue(value):
    # Can't use space directly as a separator, so `replace` is used
    return "{:,}\u2009₽".format(int(value)).replace(",", "\u2009")
