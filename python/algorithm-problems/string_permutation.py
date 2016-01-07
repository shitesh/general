# given an input string, this will generate all permutations of the string
def swap(input_str, index1, index2):
    temp = input_str[index1]
    input_str[index1] = input_str[index2]
    input_str[index2] = temp


def permute(input_str, start_index, end_index):
    if start_index == end_index:
        print ''.join([str(x) for x in input_str])

    else:
        for index in xrange(start_index, end_index):
            swap(input_str, index, start_index)
            permute(input_str, start_index+1, end_index)
            swap(input_str, index, start_index)

input_str = 'ABC'
input_str_list = list(input_str)


permute(input_str_list, 0, len(input_str_list))
