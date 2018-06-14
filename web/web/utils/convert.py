# -*- coding: utf-8 -*-

print "convert utils"
def get_value_from_choice(key, choice):
    for i in choice:
        if i[0] == key:
            return i[1]
    