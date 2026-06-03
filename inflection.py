def pluralize(word):
    if word.endswith("y") and len(word) > 1 and word[-2].lower() not in "aeiou":
        return f"{word[:-1]}ies"
    if word.endswith(("s", "x", "z", "ch", "sh")):
        return f"{word}es"
    return f"{word}s"
