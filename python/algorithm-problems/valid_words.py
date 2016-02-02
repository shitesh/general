

def is_valid_word(string):
    word_list = ["mobile","samsung","sam","sung","man","mango","icecream","and","go","i","love","ice","cream"]
    if string in word_list:
        return True
    return False


def get_valid_strings(string, string_length, result):
    for index in xrange(0, string_length+1):
        if is_valid_word(string[:index]):
            if index == string_length:
                result += string[:index+1]
                print result
                return

            get_valid_strings(string[index:], len(string[index:]), result+string[:index]+" ")


get_valid_strings("ilovesamsungmobile", len("ilovesamsungmobile"),"")
get_valid_strings("cream", len("cream"),"")