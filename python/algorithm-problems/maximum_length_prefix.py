def max_length_prefix(string_list):

    current_string = string_list[0]
    count = 0
    for index in xrange(1, len(string_list)):
        next_string = string_list[index]

        str_len = min(len(current_string), len(next_string))
        count = 0
        for index1 in xrange(0, str_len):
            if current_string[index1] != next_string[index1]:
                break
            count += 1
        current_string = next_string[:count]

    if count > 0:
        return current_string[:count]
    return 'None'

print max_length_prefix(['hello', 'help'])


