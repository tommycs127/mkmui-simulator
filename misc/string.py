import unicodedata


def not_same_width(s1: str, s2: str) -> bool:
    _ = unicodedata.east_asian_width
    return _(s1[-1]) != _(s2[0])

def both_ascii(s1: str, s2: str) -> bool:
    _ = unicodedata.east_asian_width
    # Ref for east_asian_width's results:
    # https://www.unicode.org/reports/tr44/#Validation_of_Enumerated
    matches = ('F', 'W', 'A')
    return _(s1[-1]) not in matches and _(s2[0]) not in matches

def join_string(s1: str, s2: str, condition=both_ascii) -> str:
    return s1 + ' ' + s2 if condition(s1, s2) else s1 + s2

def normalize_ascii_cjk_spacing(string: str) -> str:
    if not string:
        return string
    
    normalized_string = string[0]
    for idx in range(1, len(string)):
        normalized_string = join_string(
            normalized_string, string[idx], not_same_width
        )
    return normalized_string
