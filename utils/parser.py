from typing import List

from config import settings


def text_parser(text: str) -> List[str]:
    limit = settings.CHAR_LIMIT

    if len(text) <= limit:
        return [text]

    retval = []
    strings = text.split("\n")
    r_string = ""
    curr_len = 0
    for string in strings:
        l_string = len(string)
        if curr_len + l_string <= limit:
            r_string += string
            curr_len += l_string
        else:
            retval.append(r_string)
            r_string = ""
            r_string += string
            curr_len = l_string

    return retval


def zulu_to_gmt(zulu_time_str):
    # Преобразование времени из UTC в GMT
    gmt_time = zulu_time_str.strftime("%Y-%m-%d %H:%M:%S")
    return gmt_time
