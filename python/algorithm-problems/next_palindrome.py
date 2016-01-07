def round_up(num):
    length = len(str(num))
    increment = pow(10, ((length/2)+1))
    return ((num/increment)+1)*increment


def get_middle_digit(num):
    return str(num)[(len(str(num))-1)/2]


def get_left_half(num):
    return str(num)[:len(str(num))/2]


def next_palindrome(num):
    length = len(str(num))
    is_odd = (length % 2 != 0)
    left_half = get_left_half(num)
    middle = get_middle_digit(num)
    if is_odd:
        increment = pow(10, length/2)
        new_number = int(left_half+middle+left_half[::-1])
    else:
        increment = int(1.1*pow(10, length/2))
        new_number = int(left_half+left_half[::-1])
    if new_number > num:
        return new_number
    if middle != '9':
        return new_number + increment
    else:
        return next_palindrome(round_up(num))

if __name__ == '__main__':
    number = raw_input('Enter the number')
    print next_palindrome(number)