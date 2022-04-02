def hash_encode(str):
    hashed_str = ""
    for element in str[::-1]:
        hashed_str += (element + 'o72i01m')
    return hashed_str

def hash_decode(hashed_str):
    str = ""
    for element in hashed_str[::-1]:
        str += (element)

    str = str.replace("m10i27o", "")
    return str
