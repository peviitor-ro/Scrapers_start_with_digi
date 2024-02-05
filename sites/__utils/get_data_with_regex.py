#
#
#
# Get data with regex expresions
#
#
import re


def get_data_with_regex(expression: str, text: str) -> str:
    '''
    ... this func return needed data with regex expresions
    '''
    match = re.search(expression, text)
    if match:
        return match.group(0)
    else:
        return ""
