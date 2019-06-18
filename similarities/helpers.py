from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    line_a = set(a.splitlines())
    line_b = set(b.splitlines())
    lines_in_common = line_a.intersection(line_b)

    return list(lines_in_common)


def sentences(a, b):
    """Return sentences in both a and b"""
    sent_a = set(sent_tokenize(a))
    sent_b = set(sent_tokenize(b))
    sent_in_common = sent_a.intersection(sent_b)

    return list(sent_in_common)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    sub_a = extr_substr(a, n)
    sub_b = extr_substr(b, n)
    sub_in_common = sub_a.intersection(sub_b)

    return list(sub_in_common)


def extr_substr(string, n):
    """Extract substrings from string"""
    substr = set()
    for i in range(len(string) - n + 1):
        substr.add(string[i:i + n])

    return substr  # it's a set

