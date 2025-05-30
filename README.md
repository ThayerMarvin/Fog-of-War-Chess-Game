ChessVar: Fog of War Chess Variation
ChessVar is a Python class that implements a simplified variation of chess called Fog of War. In this variation, players only see their own pieces and empty squares, while opponent pieces are hidden and shown as *. The class supports basic chess mechanics, move validation, and tracking game state.

Features
Standard chess starting setup with lowercase letters for Black and uppercase letters for White.

Turn-based moves alternating between White and Black.

Move validation for all standard pieces (King, Queen, Rook, Bishop, Knight, Pawn).

Enforces turn order and legal moves.

Detects win conditions by checking if either King is missing.

Provides board views from three perspectives:

White: Shows all White pieces, hides Black pieces as *.

Black: Shows all Black pieces, hides White pieces as *.

Audience: Shows full board with all pieces visible.

Coordinates in standard chess notation (e.g. "a1", "e4") converted internally.

Class and Methods Overview
Initialization
__init__(): Sets up the initial chessboard and starts the game with White's turn.

Game State
get_game_state(): Returns the current game state:

"UNFINISHED" if both Kings are present.

"WHITE_WON" if Black's King is captured.

"BLACK_WON" if White's King is captured.

Board Views
get_board(perspective): Returns the board from the requested perspective ("white", "black", or "audience"). Opponent pieces are replaced by '*' in player views.

print_board(perspective): Prints the board neatly from the given perspective.

Moves
make_move(moved_from, moved_to): Attempts to move a piece from one coordinate to another.

Validates if the game is ongoing.

Checks that the piece belongs to the current player.

Validates the move legality by piece type and path.

Updates the board and switches turns if the move is valid.

Returns True if the move succeeded, False otherwise.

Utilities
get_turn(): Returns the player whose turn it is ("white" or "black").

labels(notation): Converts chess notation like "a1" to board indices (row, col).

legal_move(piece, from_row, from_col, to_row, to_col): Validates if the attempted move is legal based on piece rules, movement, and path.

Usage Example
python
Copy
game = ChessVar()

# White moves pawn from d2 to d4
game.make_move('d2', 'd4')

# Black moves pawn from d7 to d6
game.make_move('d7', 'd6')

# White moves bishop from c1 to g5
game.make_move('c1', 'g5')

# Print board from audience perspective
game.print_board('audience')

# Print board from black's perspective (white pieces hidden)
game.print_board('black')
Notes and Limitations
Castling, en passant, and promotion are not implemented.

The Fog of War effect is limited to hiding opponent pieces as '*'.

No check or checkmate detection beyond king capture.

Assumes valid notation input; no input error handling for invalid formats.

Pawn capture logic may be simplified and may need adjustment for edge cases.

How to run
Simply instantiate the ChessVar class and call the methods as shown in the usage example to play the game programmatically.
