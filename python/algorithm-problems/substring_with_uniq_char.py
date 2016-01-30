def substring_with_uniq_char(string):
    dict_character_index = {}
    current_max_length = 0
    max_length = 0
    start_index = -1
    end_index = -1
    for index in xrange(0, len(string)):
        if dict_character_index.has_key(string[index]):
            prev_index = dict_character_index[string[index]]
            dict_character_index[string[index]] = index

            if index - current_max_length > prev_index:
                current_max_length += 1
            else:
                current_max_length = index - prev_index
        else:
            dict_character_index[string[index]] = index
            current_max_length += 1

        if current_max_length > max_length:
            end_index = index
            max_length = current_max_length
            start_index = index - max_length
    return string[start_index+1:end_index+1], max_length

print substring_with_uniq_char('geeksforgeeks')
#eksforg