
def display_board(board):
    """Display the current game board."""
    for row in board:
        print(row)
            
def update_board(choice, symbol, board):
    """Update the board with the player's or computer's symbol at the chosen position."""
    for row in board:
        for i in range(len(row)):
            if row[i].isdigit():
                if int(row[i]) == choice:
                    row[i] = symbol
                    

def check_winner(win_cases, player_moves, symbol, player_turn):
    """
    Check if there is a winner or a draw.
    - win_cases: possible winning combinations.
    - player_moves: current player's moves.
    - symbol: 'X' or 'O'.
    - player_turn: True if it's the human player, otherwise computer.
    """
    
    if player_turn is None:  # no more moves left
        print("It's a draw!")
        return True
    
    for case in win_cases:
        if case <= player_moves:  # check if all elements of case are in player_moves
            if symbol == 'X':
                print("You win!")
            else:
                print("You lose!")
            return True
    # return False
		
def computer_move(win_cases, available_cases, computer_moves, player_moves):
    """
    Determine the computer's next move:
    - Try to block or win if possible.
    - Otherwise, pick the best available option.
    """
    min_length = 3
    computer_choice = None

    # Pick the move from the smallest available winning case to block the player
    for case in available_cases:
        if 0 < len(case) <= min_length:
            for i in range(len(case)):
                if case[i] not in computer_moves:
                    min_length = len(case)
                    computer_choice = case[i]

    # Check if computer can win in this turn
    for case in win_cases:
        count = sum(1 for i in case if i in computer_moves)
        if count == 2:
            for i in case:
                if i not in computer_moves and i not in player_moves:
                    computer_choice = i

    print("Computer chooses:", computer_choice)
    return computer_moves, computer_choice

def player_move(player_moves, available_cases):
    """Get the player's input, update their moves and available winning cases."""
    player_choice = int(input("Your choice: "))
    player_moves.add(player_choice)

    # Remove chosen cell from available cases
    for case in available_cases:
        if player_choice in case:
            case.remove(player_choice)

    return player_moves, available_cases, player_choice


def tic_tac_toe():
    """Main function to run the Tic Tac Toe game."""
    win_cases = [
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
        {0, 4, 8}, {2, 4, 6}
    ]

    available_cases = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    board = [
        ['0', '1', '2'],
        ['3', '4', '5'],
        ['6', '7', '8']
    ]

    computer_moves = set()
    player_moves = set()

    game_over = False

    while not game_over:
        
        display_board(board)

        # Player move
        player_moves, available_cases, player_choice = player_move(player_moves, available_cases)
        update_board(player_choice, 'X', board)
        game_over = check_winner(win_cases, player_moves, 'X', True)

        if game_over:
            break

        # Computer move
        computer_moves, computer_choice = computer_move(win_cases, available_cases, computer_moves, player_moves)
        computer_moves.add(computer_choice)
        update_board(computer_choice, 'O', board)
        game_over = check_winner(win_cases, computer_moves, 'O', computer_choice)

    display_board(board)


tic_tac_toe()