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
