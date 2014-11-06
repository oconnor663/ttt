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
    # And now all the diagonals. Note that the board might not be square!
    for 
    return lines


def get_winner(board):
    # Check the rows.
    for row in range(get_height(board)):
        first = board[row][0]
        if first is None:
            continue
        for col in range(get_width(board)):
            if board[row][col] != first:
                break
        else:
            return first

    # Check the cols.
    for col in range(get_width(board)):
        first = board[0][col]
        if first is None:
            continue
        for row in range(get_height(board)):
            if board[row][col] != first:
                break
        else:
            return first
