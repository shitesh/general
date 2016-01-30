# string_matrix[i][j] represents maximum palindromic subsequence length using characters from ith to jth index

def longest_palindromic_subsequence(string):
    length = len(string)
    string_matrix = [[0 for x in xrange(0, len(string))] for i in xrange(0, len(string))]

    for index in xrange(0, len(string)):
        string_matrix[index][index] = 1

    for column in xrange(2, len(string)+1):
        for index in xrange(len(string) - column + 1):
            index2 = index + column - 1
            if string[index] == string[index2] and column == 2:
                string_matrix[index][index2] = 2
            elif string[index] == string[index2]:
                string_matrix[index][index2] = 2 + string_matrix[index+1][index2-1]
            else:
                string_matrix[index][index2] = max(string_matrix[index][index2-1], string_matrix[index+1][index2])

    return string_matrix[0][len(string)-1]

print longest_palindromic_subsequence("abcddcb")



# can print substring easily
def longest_palindromic_substring(string):
    length = len(string)
    string_matrix = [[False for x in xrange(0, len(string))] for i in xrange(0, len(string))]

    for index in xrange(0, len(string)):
        string_matrix[index][index] = 1

    max_length = 1
    for column in xrange(2, len(string)+1):
        for index in xrange(len(string) - column + 1):
            index2 = index + column - 1
            if string[index] == string[index2] and column == 2:
                string_matrix[index][index2] = True
            elif string[index] == string[index2] and string_matrix[index+1][index2-1]:
                string_matrix[index][index2] = True
                if(column> max_length):
                    max_length = column
                    start_index = index

    return string[start_index: start_index+max_length]

print longest_palindromic_substring("forgeeksskeegfor")