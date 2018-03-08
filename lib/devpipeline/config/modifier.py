#!/usr/bin/python3


def _prepend(separator, old_value, new_value):
    if old_value:
        return "{}{}{}".format(new_value, separator, old_value)
    else:
        return new_value


def _append(separator, old_value, new_value):
    if old_value:
        return "{}{}{}".format(old_value, separator, new_value)
    else:
        return new_value


def _set(separator, old_value, new_value):
    return new_value


def _delete(separator, old_value, new_value):
    return None


_modifiers = [
    ("prepend", _prepend),
    ("append", _append),
    ("override", _set),
    ("erase", _delete)
]


def modify(value, config, key, separator):
    for modifier, fn in _modifiers:
        mod_key = "{}.{}".format(key, modifier)
        if mod_key in config:
            value = fn(separator, value, config.get(mod_key))
    return value
