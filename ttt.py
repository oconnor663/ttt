def new_board(height, width):
    return [[None] * width for i in range(height)]


def get_height(board):
    return len(board)


def get_width(board):
    return len(board[0])


def format_board(board):
    row_separator = "\n" + "┼".join(["───"] * get_width(board)) + "\n"
    return row_separator.join(
        " " + " │ ".join(char or " " for char in row)
        for row in board)


def print_board(board):
    print(format_board(board))


def get_victory_lines(board):
    lines = []
    # Add in all the rows.
    for row in range(get_height(board)):
        lines.append([(row, col) for col in range(get_width(board))])
    # And all the columns.
    for col in range(get_width(board)):
        lines.append([(row, col) for row in range(get_height(board))])
    lines.extend(get_diagonal_victory_lines(board))
    return lines


def get_diagonal_victory_lines(board):
    # We want this to work on non-square boards too! There are several ways we
    # could define it. To keep things simple, I want all diagonal lines to go
    # at 45 degrees, rather than trying to figure out weird slants. So in a
    # non-square board, the diagonals won't actually go from corner to corner.
    # We'll still say they have to *start* in a corner, again to keep things
    # simple.
    height = get_height(board)
    width = get_width(board)
    diag_len = min(height, width)
    # Note that we double count diagonals for square boards. Thats ok.
    return [[(i, i) for i in range(diag_len)],
            [(height - 1 - i, i) for i in range(diag_len)],
            [(i, width - 1 - i) for i in range(diag_len)],
            [(height - 1 - i, width - 1 - i) for i in range(diag_len)]]


def debug_print_victory_lines(height, width):
    for line in get_victory_lines(new_board(height, width)):
        dummy_board = new_board(height, width)
        for row, col in line:
            dummy_board[row][col] = 'x'
        print_board(dummy_board)
        print()


def get_winner(board):
    lines = get_victory_lines(board)
    for line in lines:
        startrow, startcol = line[0]
        startval = board[startrow][startcol]
        if startval is None:
            continue
        for row, col in line:
            if board[row][col] != startval:
                break
        else:
            return startval
    return None
