def get_last_index_of(string:str, character:str) -> int:
    reversed_str = string[::-1]
    return len(string) - reversed_str.index(character) - 1

def is_null_or_whitespace(string:str) -> bool:
    if string == None:
        return True
    return not string.strip()

def print_list(list:list) -> None:
    for ele in list:
        print(ele)

"""
Remove all non-numerical from string
"""
def filter_non_digits_for(string: str) -> str:
    # NOTE: Could make one to accept decimal points
    # but yuyutei doesn't deal with decimal numbers, so no need as of this writing.
    result = ''
    for char in string:
        if char in '0123456789':
            result += char
    return result 
