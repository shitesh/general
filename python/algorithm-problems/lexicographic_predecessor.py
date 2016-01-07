

def get_lex_predecessor(input_list):
    max_index = -1*len(input_list) -1
    current_index, next_index = None, None
    for index in xrange(-1, max_index, -1):
        next_index = index - 1
        if next_index == max_index:
            print 'not possible'
            return None
        if input_list[next_index] < input_list[index]:
            current_index = index
            break

    input_list[current_index], input_list[next_index] = input_list[next_index], input_list[current_index]
    input_list = input_list[:next_index+1]+input_list[next_index+1:][::-1]
    return input_list




if __name__ == '__main__':
    input_str = raw_input('Enter the string')
    input_list = list(input_str)
    input_list = [ord(x) for x in input_list]
    #input_list.sort()

    input_list = get_lex_predecessor(input_list)
    if input_list:
        out_str = ''.join([chr(i) for i in input_list])
        print out_str