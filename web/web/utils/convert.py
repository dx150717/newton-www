# -*- coding: utf-8 -*-

def get_value_from_choice(key, choice):
    for i in choice:
        if i[0] == key:
            return i[1]
    