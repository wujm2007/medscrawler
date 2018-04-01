import re

hump_p = re.compile(r'([a-z]|\d)([A-Z])')


def decamelize(camel_str):
    return re.sub(hump_p, r'\1_\2', camel_str).lower()
