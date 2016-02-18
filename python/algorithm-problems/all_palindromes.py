def all_palindromes(text):
    length = len(text)
    all_palindrome_set = set()

    for index, char in enumerate(text):
        all_palindrome_set.add(char)

        # find all odd length palindrome
        high = index + 1
        low = index - 1
        while low >= 0 and high < length and text[low] == text[high]:
            all_palindrome_set.add(text[low:high+1])
            low -= 1
            high += 1

        # find all even length palindrome
        high = index + 1
        low = index
        while low >=0 and high < length and text[low] == text[high]:
            all_palindrome_set.add(text[low: high+1])
            low -= 1
            high += 1

    print all_palindrome_set
    return len(all_palindrome_set)


print all_palindromes('aba')
print all_palindromes('aaa')