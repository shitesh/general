# gives a solution for n queens problem using backtracking algorithm


def is_safe(grid, row_num, column_number, max_row):
    # check only rows no need to check for column as we are incrementing column everytime
    for element in grid[row_num]:
        if element == 1:
            return False

    current_row = row_num-1
    current_column = column_number-1

    # upper left diagonal
    while current_column >=0 and current_row >= 0:
        if grid[current_row][current_column] == 1:
            return False
        current_column -= 1
        current_row -= 1

    # lower left diagonal
    current_row = row_num+1
    current_column = column_number-1

    while current_column >= 0 and current_row < max_row:
        if grid[current_row][current_column] == 1:
            return False
        current_column -= 1
        current_row += 1

    return True


def solve_n_queens(grid, column_num, max_columns):
    if column_num >= max_columns:
        return True

    for index in xrange(0, max_columns):
        if is_safe(grid, index, column_num, max_columns):
            grid[index][column_num] = 1
            if solve_n_queens(grid, column_num+1, max_columns):
                return True
            grid[index][column_num] = 0

    return False


def n_queens(count):
    grid = []
    column = 0
    for index in xrange(0, count):
        grid.append([0]*count)

    if solve_n_queens(grid, column, count):
        for x in grid:
            print x

    else:
        print 'no solution possible'


if __name__ == '__main__':
    n_queens(4)