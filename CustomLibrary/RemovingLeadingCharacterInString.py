def remove_leading_character_in_string(string, char):
    if string.startswith(char):
        string = string[1:]
        print(string)
        return string

def verify_leading_character_in_string(string):
    print(string)
    if string.startswith('0'):
        return True
    else:
        return False
