import re


def variables(path):
    return re.findall(r"{([^}]+)}", path)
