# Author: Thayer Marvin
# GitHub username: ThayerMarvin
# Date: 12/04/2024
# Description: This program is a variant of chess called Fog of War. The pieces are invisible to each other but the
# board can be called from the audience's perspective. When the pieces are moved the moves are validated based on the
# turn order, the game state, and the individual pieces move set.
class ChessVar:
    """A class to play a variation of chess call Fog of War"""
    def __init__(self):
        self._board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
        self._game_state = "UNFINISHED"  # initialized game state
        self._turn = "white"  # white starts

    def get_game_state(self):
        """A method to announce the winner or if the game is still ongoing"""
        for row in self._board:  # checks for a white king to see if black won
            if "K" in row:
                break
        else:
            return "BLACK_WON"

        for row in self._board:  # checks for a black king to see if white won
            if "k" in row:
                break
        else:
            return "WHITE_WON"

        return "UNFINISHED"  # if both kings are present the game is unfinished

    def get_board(self, perspective):
        """A method to get the board from either white, black, or the audiences perspective"""
        if perspective == "black":
            black_board = []  # new empty board to store the black board
            for row in self._board:
                new_row = []  # new empty row to store each row of the new board in
                for piece in row:  # loops through the board checking for lowercase pieces and replaces them
                    if piece.isupper():
                        new_row.append('*')
                    else:
                        new_row.append(piece)
                black_board.append(new_row)
            return black_board

        elif perspective == "white":
            white_board = []  # new empty board to store the white board
            for row in self._board:
                new_row = []  # new empty row to store each row of the new board in
                for piece in row:  # loops through the board checking for uppercase pieces and replaces them
                    if piece.islower():
                        new_row.append('*')
                    else:
                        new_row.append(piece)
                white_board.append(new_row)
            return white_board

        elif perspective == "audience":  # shows the entire board
            return self._board

        else:
            print("Invalid perspective, please choose, white, black, or audience.")

    def make_move(self, moved_from, moved_to):
        """A method to make sure a turn is valid, move pieces and update the board and game state"""
        if self.get_game_state() != "UNFINISHED":
            return False

        from_row, from_col = self.labels(moved_from)  # converts chess notation to index using labels method
        to_row, to_col = self.labels(moved_to)

        piece = self._board[from_row][from_col]  # gets piece from starting postiong

        if not piece:  # makes sure it's not an empty space
            return False

        if (piece.isupper() and self._turn != "white") or (piece.islower() and self._turn != "black"):
            return False  # makes sure it's the correct players turn

        if not self.legal_move(piece, from_row, from_col, to_row, to_col):  # makes sure the move is legal
            return False

        self._board[to_row][to_col] = piece  # Make the move and update the board
        self._board[from_row][from_col] = " "

        self._turn = "black" if self._turn == "white" else "white"  # switches the turn
        return True

    def get_turn(self):
        """Gets the current turn"""
        return self._turn

    def labels(self, notation):
        """Converts chess notation to (row, column)"""
        col = ord(notation[0].lower()) - ord('a')  # Convert a-h to 0-7
        row = 8 - int(notation[1])  # Convert 1-8 to 7-0
        return row, col

    def legal_move(self, piece, from_row, from_col, to_row, to_col):
        """Validates if moves are legal by piece type"""

        if not (0 <= to_row <= 7 and 0 <= to_col <= 7):
            return False  # Invalid move if the destination is out of bounds

        target_piece = self._board[to_row][to_col]  # retrieves the piece on the destination square

        if target_piece != " " and (  # checks if the destination square is not empty and stops from moving if a friendly piece is there
                (piece.isupper() and target_piece.isupper()) or (piece.islower() and target_piece.islower())):
            return False

        if 'k' in piece.lower():
            row_diff = abs(from_row - to_row)
            col_diff = abs(from_col - to_col)

            if row_diff <= 1 and col_diff <= 1:  # king can move one space in any direction
                return True
            else:
                return False

        if 'q' in piece.lower():
            row_diff = abs(from_row - to_row)  # calculates move distance
            col_diff = abs(from_col - to_col)

            if from_row == to_row:  # validates if the queen can horizontal with no pieces in the way
                start_col, end_col = min(from_col, to_col) + 1, max(from_col, to_col)  # Define the range of columns
                for column in range(start_col, end_col):  # Loop through the columns between the start and end
                    if (piece.isupper() and self._board[from_row][column].isupper()) or \
                            (piece.islower() and self._board[from_row][column].islower()):  # Check if there's a friendly piece
                        return False
                    elif (piece.isupper() and self._board[from_row][column].islower()) or \
                            (piece.islower() and self._board[from_row][column].isupper()): # Check if there's an opponent's piece
                        return True
                return True

            elif from_col == to_col:  # validates if the queen can vertical with no pieces in the way
                start_row, end_row = min(from_row, to_row) + 1, max(from_row, to_row)  # Define the range of rows
                for row in range(start_row, end_row):  # Loop through the rows between the start and end
                    if (piece.isupper() and self._board[row][from_col].isupper()) or \
                            (piece.islower() and self._board[row][from_col].islower()):
                        return False
                    elif (piece.isupper() and self._board[row][from_col].islower()) or \
                            (piece.islower() and self._board[row][from_col].isupper()):
                        return True
                return True

            elif row_diff == col_diff:  # validates if queen is moving diagonally
                row_step = 1 if to_row > from_row else -1  # determine direction vertically
                col_step = 1 if to_col > from_col else -1  # determine direction horizontally

                # Iterate through all squares between the start and end
                row, col = from_row + row_step, from_col + col_step
                while row != to_row and col != to_col:
                    if self._board[row][col] != " ":  # If there is any piece in the way
                        if (piece.isupper() and self._board[row][col].isupper()) or \
                                (piece.islower() and self._board[row][col].islower()):  # Check if it's a friendly piece
                            return False
                        elif (piece.isupper() and self._board[row][col].islower()) or \
                                (piece.islower() and self._board[row][col].isupper()):  # Check if it's an opponent piece
                            return True
                    row += row_step  # move to the next row
                    col += col_step  # move to the next column
                return True
            else:
                return False

        if 'p' in piece.lower():
            first_move = False
            if piece == 'P' and from_row == 6:  # White pawns first move
                first_move = True
            elif piece == 'p' and from_row == 1:  # Black pawns first move
                first_move = True

            row_diff = abs(from_row - to_row)
            col_diff = abs(from_col - to_col)

            if row_diff == 1 and col_diff == 0:  # checks if pawn can move one space
                if self._board[to_row][to_col] == " ":
                    return True
                if piece == 'P' and to_row < 8 and to_col < 8:
                    if self._board[to_row][to_col].islower():  # checks to see if it can capture a black piece
                        return True
                if piece == 'p' and to_row < 8 and to_col < 8:
                    if self._board[to_row][to_col].isupper():  # checks to see if it can capture a white piece
                        return True

            if first_move and row_diff == 2 and col_diff == 0:
                if piece == 'P':  # White pawn moving up
                    if self._board[to_row][to_col] == " " and self._board[from_row - 1][from_col] == " ":
                        return True
                elif piece == 'p':  # Black pawn moving down
                    if self._board[to_row][to_col] == " " and self._board[from_row + 1][from_col] == " ":
                        return True

            if row_diff == 1 and col_diff == 1:  # Check if the pawn is capturing diagonally
                if piece == 'P' and to_row < 8 and to_col < 8:
                    if self._board[to_row][to_col].islower():  # White capturing black
                        return True
                if piece == 'p' and to_row < 8 and to_col < 8:
                    if self._board[to_row][to_col].isupper():  # Black capturing white
                        return True

        if piece.lower() == "b":
            row_diff = abs(from_row - to_row)  # calculate move distance
            col_diff = abs(from_col - to_col)
            if row_diff == col_diff:  # validates the bishop can move diagonally
                row_step = 1 if to_row > from_row else -1  # determines the direction of the movement
                col_step = 1 if to_col > from_col else -1

                row, col = from_row + row_step, from_col + col_step # Iterate through all squares between the start and end
                while row != to_row and col != to_col:
                    if self._board[row][col] != " ":  # If there is any friendly piece in the way
                        if (piece.isupper() and self._board[row][col].isupper()) or \
                                (piece.islower() and self._board[row][col].islower()):
                            return False
                        else:
                            return True
                    row += row_step
                    col += col_step
                return True
            else:
                return False

        if "r" in piece.lower():

            if from_row == to_row:  # validates if the rook can horizontal with no pieces in the way
                start_col, end_col = min(from_col, to_col) + 1, max(from_col, to_col)  # Define the range of columns

                for column in range(start_col, end_col):  # loop through the columns

                    if (piece.isupper() and self._board[from_row][column].isupper()) or \
                            (piece.islower() and self._board[from_row][column].islower()):
                        return False  # if there is a friendly piece in the way
                return True

            elif from_col == to_col:  # validates if the rook can vertically with no pieces in the way
                start_row, end_row = min(from_row, to_row) + 1, max(from_row, to_row)  # Define the range of columns

                for row in range(start_row, end_row):  # loop through the columns
                    if (piece.isupper() and self._board[row][from_col].isupper()) or \
                            (piece.islower() and self._board[row][from_col].islower()):
                        return False
                return True
            else:
                return False

        if "n" in piece.lower():
            row_diff = abs(from_row - to_row)
            col_diff = abs(from_col - to_col)
            if (col_diff == 2 and row_diff == 1) or (row_diff == 2 and col_diff == 1):
                if self._board[to_row][to_col] == " " or (
                        piece.isupper() and self._board[to_row][to_col].islower()) or (
                        piece.islower() and self._board[to_row][to_col].isupper()):
                    return True
                else:
                    return False  # validates if the knight can move in an L shape

            else:
                return False

    def print_board(self, perspective):
        """Method to print the board from either white, black, or the audience's perspective in a neater format"""
        board = self.get_board(perspective)

        for row in board:
            # Join each element in the row with a space and print the row
            print(" ".join(row))




game = ChessVar()
# print(game.make_move('f2', 'f3'))
# print(game.make_move('b7', 'b5'))
# print(game.make_move('g1', 'h3'))
# print(game.make_move('g7', 'g5'))
# print(game.make_move('h3', 'g5'))
print(game.make_move('d2', 'd4'))
#print(game.make_move('g7', 'g5'))
print(game.make_move('d7', 'd6'))
print(game.make_move('c1', 'g5'))
print(game.make_move('b7', 'b5'))
print(game.make_move('g5', 'd8'))
print(game.make_move('c8','a6'))
print(game.make_move('e2','e3'))
print(game.make_move('a7','a6 '))
print(game.print_board('audience'))
print(game.print_board('black'))
# print(game.get_board("audience"))
# print(game.get_board("white"))
# print(game.get_board("black"))
