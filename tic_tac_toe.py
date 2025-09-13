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
available_cases = [0,1,2,3,4,5,6,7,8]
# Store all Entry widgets for the 3x3 grid
listEntries = []

# Flag to track if the game has ended
gameOver = False

# Sets to track moves made by computer and player
player1_moves = set()
player2_moves = set()

player1_symbol = "x"
player2_symbol = "o"

turn = player1_symbol

def display_board():
    global listEntries
    for row in range(3):
        for col in range(3):
            ent = tk.Entry(game_frame,font=("Arial",60,"bold"),borderwidth=1,relief="solid",width=2)
            ent.config(state='readonly') # Make it read-only initially
            ent.bind("<FocusIn>",player_move) # Bind click event to player_move function
            listEntries.append(ent) # Add to list for later reference
            ent.grid(row=row,column=col) # Place in grid

def player_move(event):
    global turn,available_cases,listEntries

    active = game_frame.focus_get()
    
    if active not in listEntries or gameOver:
        return
    # Find the index of this widget in our list (0-8 for the 3x3 grid)
    player_choice = listEntries.index(active)
    # Check if the chosen cell is already occupied or if game is over
    # if int(player_choice) not in available_cases :
    #     return
    if turn == player1_symbol and int(player_choice) in available_cases:
        player1_moves.add(int(player_choice))
        # Update the visual representation of the move
        listEntries[int(player_choice)].config(state='normal') # Allow editing
        listEntries[int(player_choice)].config(fg='black') # Set text color
        listEntries[int(player_choice)].insert(0," x") # Insert 'x' symbol
        listEntries[int(player_choice)].config(state='readonly') # Make read-only again
        check_winner(player1_symbol)
        turn = player2_symbol
        # Remove chosen cell from available cases
        available_cases.remove(int(player_choice))
        return

    elif turn == player2_symbol and int(player_choice) in available_cases:
        player2_moves.add(int(player_choice))
        # Update the visual representation of the move
        listEntries[int(player_choice)].config(state='normal') # Allow editing
        listEntries[int(player_choice)].config(fg='gray') # Set text color
        listEntries[int(player_choice)].insert(0," o") # Insert 'x' symbol
        listEntries[int(player_choice)].config(state='readonly') # Make read-only again
        check_winner(player2_symbol)
        turn = player1_symbol
        # Remove chosen cell from available cases
        available_cases.remove(int(player_choice))
        return

def check_winner(player_symbol):
    global gameOver

    if player_symbol == player2_symbol:
        player_moves = player2_moves
    else:
        player_moves = player1_moves

    # Check each winning case to see if current player has achieved it
    for case in win_cases:
        if case <= player_moves:  # check if all elements of case are in player_moves
            print(f"{player_symbol} win!")
            # Highlight winning combination in green
            for i in case:
                listEntries[i].config(fg='green')
            gameOver = True
            messagebox.showinfo("",f"{player_symbol} win!")


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