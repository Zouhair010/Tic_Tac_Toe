import tkinter as tk
from tkinter import messagebox


# Define all possible winning combinations (rows, columns, diagonals)
# Each set represents positions that form a winning line
win_cases = [
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},# Horizontal wins
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},# Vertical wins
        {0, 4, 8}, {2, 4, 6}# Diagonal wins
    ]
# Track available positions for each winning case
# This helps the computer determine which moves to prioritize
available_cases = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
# Store all Entry widgets for the 3x3 grid
listEntries = []
# Flag to track if the game has ended
gameOver = False
# Sets to track moves made by computer and player
computer_moves = set()
player_moves = set()

# Handle player's move when they click on a cell
def player_move(event):
    global player_moves,available_cases,listEntries
    # Get the currently focused Entry widget
    active = game_frame.focus_get()
    
    if active not in listEntries:
        return
    
    # Find the index of this widget in our list (0-8 for the 3x3 grid)
    player_choice = listEntries.index(active)
    # Check if the chosen cell is already occupied or if game is over
    if int(player_choice) in computer_moves or int(player_choice) in player_moves:
        return
    # Record the player's move
    player_moves.add(int(player_choice))

    # Remove chosen cell from available cases
    for case in available_cases:
        if int(player_choice) in case:
            case.remove(int(player_choice))
    # Update the visual representation of the move
    listEntries[int(player_choice)].config(state='normal') # Allow editing
    listEntries[int(player_choice)].config(fg='black') # Set text color
    listEntries[int(player_choice)].insert(0," x") # Insert 'x' symbol
    listEntries[int(player_choice)].config(state='readonly') # Make read-only again
    # Check if player won with this move
    check_winner(player_moves, "x",player_choice)
    # If game is still ongoing, let computer make its move
    if not gameOver:
        computer_move()
    else:
        restart()
        
# Handle computer's move
def computer_move():
    global player_moves,available_cases,computer_moves,listEntries
    """
    Determine the computer's next move:
    - Try to block or win if possible.
    - Otherwise, pick the best available option.
    """
    min_length = 3 # Start with maximum case length
    computer_choice = None
    # Strategy 1: Pick move from smallest available winning case to block player
    # This prioritizes moves that can block multiple potential winning paths
    for case in available_cases:
        if 0 < len(case) <= min_length:
            for i in range(len(case)):
                if case[i] not in computer_moves:
                    min_length = len(case)
                    computer_choice = case[i]
    # Strategy 2: Check if computer can win in this turn (highest priority)
    # Look for cases where computer has 2 moves and can complete the third
    for case in win_cases:
        count = sum(1 for i in case if i in computer_moves)
        if count == 2: # Computer has 2 out of 3 positions
            for i in case:
                # Find the empty position to complete the win
                if i not in computer_moves and i not in player_moves:
                    computer_choice = i
    # Execute the computer's move if a valid choice was found
    if computer_choice is not None:
        print(computer_choice)# Debug output
        # Update visual representation
        listEntries[int(computer_choice)].config(state='normal')
        listEntries[int(computer_choice)].config(fg='gray')# Different color for computer
        listEntries[int(computer_choice)].insert(0," o")# Insert 'o' symbol
        listEntries[int(computer_choice)].config(state='readonly')
        # Record the computer's move
        computer_moves.add(int(computer_choice))
    # Check if computer won with this move
    check_winner(computer_moves, "o",computer_choice)
    if gameOver:
        restart()

# Check for win conditions or draw
def check_winner(player_moves, symbol,player_turn):
    global gameOver
    """
    Check if there is a winner or a draw.
    - win_cases: possible winning combinations.
    - player_moves: current player's moves.
    - symbol: 'X' or 'O'.
    - player_turn: True if it's the human player, otherwise computer.
    """   
    # Check for draw condition (no more moves available) 
    if player_turn is None:  # no more moves left
        print("It's a draw!")
        # Highlight all cells in blue for draw
        for ent in listEntries:
            ent.config(fg='blue')
        messagebox.showinfo("","It's a draw!")
        gameOver = True
        return
    # Check each winning case to see if current player has achieved it
    for case in win_cases:
        if case <= player_moves:  # check if all elements of case are in player_moves
            if symbol == 'x': # Player wins
                print("You win!")
                # Highlight winning combination in green
                for i in case:
                    listEntries[i].config(fg='green')
                messagebox.showinfo("","You win!")

            else: # Computer wins
                print("You lose!")
                # Highlight winning combination in red
                for i in case:
                    listEntries[i].config(fg='red')
                messagebox.showinfo("","You lose!")
            # End the game
            gameOver = True       
            return

# Create and display the 3x3 game board     
def display_board():
    global listEntries
    for row in range(3):
        for col in range(3):
            ent = tk.Entry(game_frame,font=("Arial",60,"bold"),borderwidth=1,relief="solid",width=2)
            ent.config(state='readonly') # Make it read-only initially
            ent.bind("<FocusIn>",player_move) # Bind click event to player_move function
            listEntries.append(ent) # Add to list for later reference
            ent.grid(row=row,column=col) # Place in grid

def restart():
    global player_moves,available_cases,computer_moves,listEntries,gameOver
    while len(listEntries):
        listEntries[0].grid_forget()
        listEntries.pop(0)
    display_board()
    available_cases = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    gameOver = False
    computer_moves = set()
    player_moves = set()
        
# Create main window
window = tk.Tk()
window.title("tic_tac_toe")# Note: Title doesn't match the game content
window.resizable(False, False)# Disable window resizing
# Create frame to contain the game board
game_frame = tk.Frame(window,background='#80bfff',highlightbackground='#800080',border=1,relief="solid")
game_frame.pack()

# Initialize and display the game board
display_board()

# Start the GUI event loop
window.mainloop()