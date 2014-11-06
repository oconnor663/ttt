def new_board(height, width):
    return [[None] * width for i in range(height)]


def get_height(board):
    return len(board)


def get_width(board):
    return len(board[0])


def get_victory_lines(board):
    lines = []
    # Add in all the rows.
    for row in range(get_height(board)):
        lines.append([(row, col) for col in range(get_width(board))])
    # And all the columns.
    for col in range(get_width(board)):
        lines.append([(row, col) for row in range(get_height(board))])
    # At some point figure out diagonals.
    return lines


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
