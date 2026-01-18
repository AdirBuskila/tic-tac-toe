import random
import os
import time

symbols = [
    "X", "O", "@", "#", "$", "%", "&", "*", "+", "=", "!", "?",
    "❤", "★", "☀", "☁", "☂", "☕", "☘", "♠", "♣", "♥", "♦", "♟",
    "⚡", "🔥", "💎", "🌙", "🌸", "🍀", "🍎", "🍕", "🎵", "🎯", "🚀", "🪐"
]

board = [
    [0,0,0],
    [0,0,0],
    [0, 0, 0]
]
BOARD_SIZE = 3
MODE_PVP = "PVP"
MODE_PVC = "PVC"

game_state = {}

def clear_console():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def select_mode() -> str:
    while True:
        c = input("Please select the game mode:\n(1) PVP (Player vs Player)\n(2) PVC (PLAYER VS COMPUTER)\n")
        c = c.strip()
        if not (c == "1" or c == "2"):
            print("Please enter a valid choice, 1 or 2")
            continue
        if c == "1":
            return MODE_PVP
        else:
            return MODE_PVC

def get_player_name(prompt: str) -> str:
    while True:
        name = input(f"{prompt}\n")
        name = name.strip()
        if name.isdigit():
            print("Please enter a valid name, not a number.")
            continue
        if len(name) < 2:
            print("Please enter a valid name, must be at least 2 characters.")
            continue
        return name

def random_symbol(symbols:list[str])-> str:
    return random.choice(symbols)

def choose_symbols(name1: str, name2: str) -> tuple[str, str]:
    """Let players choose their symbols, with random fallback"""
    while True:
        symb1 = input(f"{name1}, Please enter Your Symbol:\ni.e:(X,$,❤)\nPress Enter for random selection.\n")
        symb2 = input(f"{name2}, Please enter Your Symbol:\ni.e:(X,$,❤)\nPress Enter for random selection.\n")
        symb1 = symb1.strip()
        symb2 = symb2.strip()
        
        # Use random symbols if empty input
        if symb1 == "":
            symb1 = random_symbol(symbols)
        if symb2 == "":
            symb2 = random_symbol(symbols)
        
        # Ensure symbols are different
        if symb1 == symb2:
            print("The symbols must be different.")
            continue
        
        # Validate symbol length and content
        if len(symb1) > 1 or len(symb2) > 1:
            print("Symbols must be single character.")
            continue
        
        if symb1 != '0' and symb2 != '0':
            print(f"Symbols chosen: {name1} = {symb1}, {name2} = {symb2}")
            return symb1, symb2
        
        print("Please enter a valid symbol.")

def make_board(size=BOARD_SIZE) -> list[list]:
    return [[0 for row in range(size)] for column in range(size)]

def print_board(board: list[list]) -> None:
    """Print the game board with clear console for better UX"""
    clear_console()
    print("\n   1   2   3")
    print("  -----------")
    for i, row in enumerate(board):
        row_display = " | ".join(str(cell) if cell != 0 else " " for cell in row)
        print(f"{i+1} | {row_display} |")
        print("  -----------")

def is_cell_empty(board: list[list], row: int, col: int) -> bool:
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        raise IndexError("Please enter valid row and column number (0-2).")
    return board[row][col] == 0


def board_full(board: list[list]) -> bool:
    """
    Return True if the board is completely filled (i.e., there are no 0 cells left).
    Each cell that is still 0 means an empty spot
    """
    return all(cell != 0 for row in board for cell in row)

def board_empty(board: list[list]) -> bool:
    return all(cell == 0 for row in board for cell in row)

def place_symbol(board: list[list], row: int, col: int, symbol: str) -> bool:
    try:
        if is_cell_empty(board, row, col):
            board[row][col] = symbol
            return True
    except IndexError as e:
        print(e)
        return False



def read_move(player_name: str) -> tuple[int, int]:
    while True:
        try:
            move_input = input(f"{player_name}, Please enter row and column number (1-3), i.e: 2 3\n")
            move_input = move_input.strip()
            
            # Split the input and convert to integers
            parts = move_input.split()
            if len(parts) != 2:
                print("Please enter exactly two numbers separated by a space.")
                continue
                
            row = int(parts[0])
            col = int(parts[1])
            
            # Convert from 1-based to 0-based indexing
            row -= 1
            col -= 1
            
            # Validate range
            if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
                print(f"Please enter numbers between 1 and {BOARD_SIZE}.")
                continue
                
            return row, col
            
        except ValueError:
            print("Please enter valid numbers.")
        except Exception as e:
            print(f"Invalid input: {e}")



def has_winner(board: list[list], symbol: str) -> bool:
    # Check rows
    for row in board:
        if all(cell == symbol for cell in row):
            return True
    
    # Check columns
    for col in range(BOARD_SIZE):
        if all(board[row][col] == symbol for row in range(BOARD_SIZE)):
            return True
    
    # Check main diagonal (top-left to bottom-right)
    if all(board[i][i] == symbol for i in range(BOARD_SIZE)):
        return True
    
    # Check anti-diagonal (top-right to bottom-left)
    if all(board[i][BOARD_SIZE-1-i] == symbol for i in range(BOARD_SIZE)):
        return True
    
    return False


def is_tie(board: list[list], symb1: str, symb2: str) -> bool:
    """Check if the game is a tie (board full and no winner)"""
    if board_full(board):
        if has_winner(board, symb1) or has_winner(board, symb2):
            return False
        else:
            return True
    return False

# ============================================================================
# CORE GAME FUNCTIONS
# ============================================================================

def switch_turn(turn_idx: int) -> int:
    """Switch between players (0 and 1)"""
    return 1 - turn_idx

def announce_result(winner_name: str = None) -> None:
    """Print the game result"""
    clear_console()
    print("\n" + "="*50)
    if winner_name:
        print(f"🎉 Congratulations! {winner_name} wins! 🎉")
    else:
        print("🤝 It's a tie! Great game! 🤝")
    print("="*50)

def ask_play_again() -> bool:
    """Ask if players want to play another game"""
    while True:
        choice = input("\nWould you like to play again? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def computer_move_random(board: list[list]) -> tuple[int, int]:
    """Generate a random move for the computer"""
    empty_cells = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                empty_cells.append((row, col))
    
    if empty_cells:
        return random.choice(empty_cells)
    else:
        return (0, 0)  # Fallback (shouldn't happen if called correctly)

def welcome_message(players: list[dict]) -> None:
    """Display welcome message and game rules"""
    clear_console()
    print("\n" + "="*50)
    print("🎮 Welcome to Tic-Tac-Toe! 🎮")
    print("="*50)
    print(f"Mode: {'Player vs Player' if not players[1]['is_computer'] else 'Player vs Computer'}")
    print(f"Players: {players[0]['name']} ({players[0]['symbol']}) vs {players[1]['name']} ({players[1]['symbol']})")
    print("\nRules:")
    print("• Get 3 in a row (horizontal, vertical, or diagonal) to win!")
    print("• Enter row and column numbers (1-3) for your move")
    print("• Example: '2 3' means row 2, column 3")
    print("="*50)
    input("\nPress Enter to start the game...")


def init_game() -> tuple[list[list], list[dict]]:
    """Initialize a fresh game session (selects mode, gets player names, symbols, resets board & game_state)"""
    
    # --- Step 1: Select Mode ---
    game_mode = select_mode()
    game_state['mode'] = game_mode

    # --- Step 2: Initialize Players ---
    p1_name = get_player_name("Player 1, please enter your name.")
    if game_mode == MODE_PVP:
        p2_name = get_player_name("Player 2, please enter your name.")
    else:
        p2_name = "Computer"

    (symb1, symb2) = choose_symbols(p1_name, p2_name)
    p1 = {'name': p1_name, 'symbol': symb1, 'is_computer': False}
    p2 = {'name': p2_name, 'symbol': symb2, 'is_computer': game_mode == MODE_PVC}
    players = [p1, p2]

    # --- Step 3: Initialize Board and Game State ---
    board = make_board()
    game_state['cur_player_index'] = 0
    game_state['move_count'] = 0

    return board, players

def play_turn(board: list[list], player: dict) -> bool:
    """Handle a single turn for a player"""
    if player['is_computer']:
        print(f"\n{player['name']} is thinking...")
        time.sleep(1)  # Small delay to make it feel more natural
        row, col = computer_move_random(board)
    else:
        row, col = read_move(player['name'])
    
    if place_symbol(board, row, col, player['symbol']):
        print(f"{player['name']} placed {player['symbol']} at position ({row+1}, {col+1})")
        return True
    else:
        if not player['is_computer']:
            print("That position is already taken! Please try again.")
        return False

def play_game() -> None:
    """Main game loop"""
    board, players = init_game()
    welcome_message(players)
    
    current_player_idx = 0
    move_count = 0
    
    while True:
        print_board(board)
        
        current_player = players[current_player_idx]
        
        # Play turn until successful
        while not play_turn(board, current_player):
            if not current_player['is_computer']:
                continue  # Human player will be asked again
            else:
                break  # Computer should always find a valid move
        
        move_count += 1
        
        # Check for winner
        if has_winner(board, current_player['symbol']):
            print_board(board)
            announce_result(current_player['name'])
            break
        
        # Check for tie
        if is_tie(board, players[0]['symbol'], players[1]['symbol']):
            print_board(board)
            announce_result()
            break
        
        # Switch to next player
        current_player_idx = switch_turn(current_player_idx)

def main() -> None:
    """Main program entry point with replay loop"""
    clear_console()
    print("Welcome to Tic-Tac-Toe!")
    
    while True:
        play_game()
        
        if not ask_play_again():
            clear_console()
            print("Thanks for playing! Goodbye! 👋")
            break

# Run the game when the script is executed
if __name__ == "__main__":
    main()

