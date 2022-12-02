def is_null_or_whitespace(string:str) -> bool:
    if string == None:
        return True
    return not string.strip()

def print_list(list:list) -> None:
    for ele in list:
        print(ele)
