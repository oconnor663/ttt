#! /usr/bin/python3

import sys


LOSE = "LOSE"
DRAW = "DRAW"
WIN = "WIN"


def new_board(height, width):
    return ((None,) * width,) * height


def get_height(board):
    return len(board)


def get_width(board):
    return len(board[0])


def make_move(board, player, row, col):
    # Boards are tuples, so they're immutable. To make a move, we create a new
    # board with the move made and return that.
    return tuple(tuple(player if r == row and c == col else board[r][c]
                       for c in range(get_width(board)))
                 for r in range(get_height(board)))


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


def get_winner(board):
    lines = get_victory_lines(board)
    # Check to see if anyone has N-in-a-row.
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
    # Check to see whether the board is totally full.
    for row in range(get_height(board)):
        for col in range(get_width(board)):
            if board[row][col] is None:
                return None
    return DRAW


def possible_moves(board, player_to_move):
    moves = []
    for row in range(get_height(board)):
        for col in range(get_width(board)):
            if board[row][col] is None:
                moves.append((row, col))
    return moves


def best_move(board, player_to_move, other_player):
    all_possible = possible_moves(board, player_to_move)
    assert all_possible, "there must be some possible moves"
    draw_moves = []
    for move in all_possible:
        # Look at each possible move.
        new_board = make_move(board, player_to_move, move[0], move[1])
        winner = get_winner(new_board)
        # If any move makes you win immediately, just return that.
        if winner == player_to_move:
            return (WIN, move)
        # Keep track of moves that are immediate draws too. That might end up
        # being the best option.
        elif winner == DRAW:
            draw_moves.append(move)
            continue

        # If the game is not yet decided, recursively call best_move from the
        # other player's perspective. THIS IS WHERE THE MAGIC HAPPENS! If the
        # other player has no winning response, then this is a good move.
        result, response = best_move(new_board, other_player, player_to_move)
        if result == LOSE:
            return (WIN, move)
        elif result == DRAW:
            draw_moves.append(move)

    # At this point, if we had found any winning moves, we would have already
    # returned them. So it looks like there's no winning move. If there's a
    # draw move, return that.
    if draw_moves:
        return (DRAW, draw_moves[0])

    # If there weren't any draw moves, looks like we're screwed.
    return (LOSE, None)


def print_best_move(board, player, other_player):
    # Finding the best move can take a while, so print something to let the
    # user know what we're doing.
    print("Finding best move... ", end="")
    # Because this is a partial line, we need to call flush() to make sure
    # it gets shown immediately.
    sys.stdout.flush()

    result, move = best_move(board, player, other_player)
    if result == LOSE:
        print("The computer says you're screwed :(")
    else:
        print("{} {} ({})".format(
            move[0], move[1], "win" if result == WIN else "tie"))


def main():
    height = 3
    width = 3
    if len(sys.argv) > 1:
        height = int(sys.argv[1])
        width = int(sys.argv[2])
    board = new_board(height, width)
    players = ('X', 'O')
    turn = 0
    print_board(board)
    while True:
        player = players[turn % 2]
        other_player = players[(turn + 1) % 2]
        print_best_move(board, player, other_player)
        move_str = input(player + "'s move: ")
        row, col = (int(i) for i in move_str.split())
        if row >= height or col >= width or board[row][col] is not None:
            print("Invalid move.")
            continue
        board = make_move(board, player, row, col)
        print_board(board)
        winner = get_winner(board)
        if winner == DRAW:
            print('Tie game!')
            return
        if winner is not None:
            print(winner, "wins!")
            return
        turn += 1


if __name__ == '__main__':
    main()
