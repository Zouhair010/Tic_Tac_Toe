from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivymd.color_definitions import colors
from kivy.uix.popup import Popup

# This class represents the initial screen where the user chooses the game mode.
class InitialScreen(BoxLayout):
    """
    The initial screen widget that presents the user with game mode choices:
    - Player vs. Computer
    - Player vs. Player
    """
    def __init__(self, switch_player_vs_player_mode, switch_player_computer_mode, **kwargs):
        super().__init__(**kwargs)

        # A grid layout to hold the mode selection buttons, with spacing.
        self.buttons_gridlayout = GridLayout(cols=3, size_hint_y=None, height=50, padding = (30,10), spacing=10)

        # first button
        play_vs_computer_mode_button = Button(
            text="player vs compute",
            size_hint=(None, None),
            size=(120, 40),
            background_normal="",
            background_color=(0, 0, 1, 1)  # blue
        )
        # Bind the button's release event to the function that switches to Player vs Computer mode.
        play_vs_computer_mode_button.bind(on_release = switch_player_computer_mode)
        self.buttons_gridlayout.add_widget(play_vs_computer_mode_button)

        #spacer
        self.buttons_gridlayout.add_widget(Widget())

        # first button
        player_vs_player_mode_button = Button(
            text="player vs player",
            size_hint=(None, None),
            size=(120, 40),
            background_normal="",
            background_color=(0, 0, 1, 1)  # blue
        )
        # Bind the button's release event to the function that switches to Player vs Player mode.
        player_vs_player_mode_button.bind(on_release = switch_player_vs_player_mode)
        self.buttons_gridlayout.add_widget(player_vs_player_mode_button)

        # Add the grid of buttons to the main layout of this screen.
        self.add_widget(self.buttons_gridlayout)



# This class represents the game screen for Player vs Player mode.
class FirstScreen(BoxLayout):
    """
    The main game screen widget for a two-player (human vs. human) game.
    It handles the game board, player turns, win/draw detection, and game controls.
    """
    def __init__(self, switch_game, switch_back, **kwargs):
        super().__init__(**kwargs)

        # Set the main layout to be vertical with padding and spacing.
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        # Create the grid that will hold the 3x3 game board cells.
        self.textInput_gridlayout = GridLayout(cols=3)
        self.add_widget(self.textInput_gridlayout)
        
        # Create a grid to hold the control buttons below the game board.
        self.buttons_gridlayout = GridLayout(cols=3, size_hint_y=None, height=50,padding=(30,10) ,spacing=10)

        # 'Restart' button to start a new game in the current mode.
        restart_button = Button(
            text="restart",
            size_hint=(None, None),
            size=(80, 40),
            background_normal="",
            background_color=(0, 0, 1, 1)  # blue
        )
        # Bind the button's release event to the restart method of this class.
        restart_button.bind(on_release = self.restart)
        self.buttons_gridlayout.add_widget(restart_button)

        # 'Switch' button to change to the other game mode (e.g., PvP to PvC).
        # The actual switch logic is handled by the main app class.
        switch_game_button = Button(
            text="switch",
            size_hint=(None, None),
            size=(80, 40),
            background_normal="",
            background_color=(0, 0, 1, 1)
        )
        # Bind the button's release event to the switch_game function passed from the main app.
        switch_game_button.bind(on_release = switch_game)
        self.buttons_gridlayout.add_widget(switch_game_button)

        # 'Back' button to return to the initial mode selection screen.
        back_button = Button(
            text="back",
            size_hint=(None, None),
            size=(80, 40),
            background_normal="",
            background_color=(0, 0, 1, 1)  # blue
        )
        # Bind the button's release event to the switch_back function passed from the main app.
        back_button.bind(on_release = switch_back)
        self.buttons_gridlayout.add_widget(back_button)

        # Add the grid of control buttons to the main layout.
        self.add_widget(self.buttons_gridlayout)

        # Define all possible winning combinations (rows, columns, diagonals)
        self.win_cases = [
                     {0, 1, 2}, {3, 4, 5}, {6, 7, 8},# Horizontal wins
                     {0, 3, 6}, {1, 4, 7}, {2, 5, 8},# Vertical wins
                     {0, 4, 8}, {2, 4, 6}# Diagonal wins
                    ]
        # A list to track available positions on the board (indices 0-8).
        self.available_cases = [0,1,2,3,4,5,6,7,8]
        # A list to store all the TextInput widgets for the 3x3 grid.
        self.listEntries = []
        # A flag to track if the game has ended, to prevent further moves.
        self.gameOver = False
        # Sets to track the moves made by each player.
        self.player1_moves = set()
        self.player2_moves = set()
        # Define symbols for each player.
        self.player1_symbol = "x"
        self.player2_symbol = "o"
        # Keep track of whose turn it is, starting with Player 1.
        self.turn = self.player1_symbol

        # Initialize the game board by creating and adding the TextInput cells.
        self.display_board()


    def display_board(self):
        """
        Creates and populates the 3x3 grid with TextInput widgets.
        Each TextInput acts as a cell on the Tic-Tac-Toe board.
        """
        # Loop 9 times to create each cell of the board.
        for _ in range(9):
            txtInput = TextInput(
                halign="center",
                readonly=True,
                size_hint=(None,None),
                font_size=100,
                size=(160,160),
                multiline=False
                
            )
            # Bind the touch event on each cell to the player_move method.
            txtInput.bind(on_touch_down=self.player_move) # Bind click event to player_move function
            self.listEntries.append(txtInput) # Add to list for later reference
            self.textInput_gridlayout.add_widget(txtInput)

    def player_move(self,instance,touch):
        """
        Handles the logic when a player clicks on a cell.
        - instance: The TextInput widget that was touched.
        - touch: The touch event information (e.g., position).
        """
        # Ignore clicks if the game is over or if the click is not on a cell.
        if instance not in self.listEntries or self.gameOver:
            return
        # Check if the touch event occurred within the bounds of the TextInput widget.
        if instance.collide_point(*touch.pos):
            # Find the index of this widget in our list (0-8 for the 3x3 grid)
            player_choice = self.listEntries.index(instance)
            # Ignore the move if the chosen cell is already taken.
            if int(player_choice) not in self.available_cases :
                return
            # Handle Player 1's turn.
            if self.turn == self.player1_symbol and int(player_choice) in self.available_cases:
                 self.player1_moves.add(int(player_choice))
                 # Update the visual representation of the move
                 instance.readonly=False
                 instance.text = self.player1_symbol
                 instance.foreground_color = colors["Gray"]["900"]
                 instance.readonly=True
                 # Check if this move results in a win.
                 self.check_winner(self.player1_symbol)
                 # It's now Player 2's turn.
                 self.turn = self.player2_symbol
                 # Remove the chosen cell from the list of available spots.
                 self.available_cases.remove(int(player_choice))
                 return
            
            # Handle Player 2's turn.
            if self.turn == self.player2_symbol and int(player_choice) in self.available_cases:
                 self.player2_moves.add(int(player_choice))
                 # Update the visual representation of the move
                 instance.readonly=False
                 instance.text = self.player2_symbol
                 instance.foreground_color = colors["Gray"]["600"]
                 instance.readonly=True
                 # Check if this move results in a win.
                 self.check_winner(self.player2_symbol)
                 # It's now Player 1's turn.
                 self.turn = self.player1_symbol
                 # Remove the chosen cell from the list of available spots.
                 self.available_cases.remove(int(player_choice))
                 return
            
    def check_winner(self,player_symbol):
        """
        Checks if the most recent move resulted in a win or a draw.
        - player_symbol: The symbol ('x' or 'o') of the player to check.
        """
        # Determine which player's moves to check.
        if player_symbol == self.player2_symbol:
            player_moves = self.player2_moves
        else:
            player_moves = self.player1_moves
        # Check each winning case to see if the current player has achieved it.
        for case in self.win_cases:
            # A win occurs if all positions in a winning case are in the player's moves.
            if case <= player_moves:  # check if all elements of case are in player_moves
                # print(f"{player_symbol} win!")
                # Highlight winning combination in green
                for i in case:
                    self.listEntries[i].foreground_color = colors["Green"]["800"]
                self.gameOver = True # End the game.
                # Show a popup message announcing the winner.
                popup = Popup(
                    title = f"{player_symbol} win!",
                    size_hint=(None,None),
                    size=(200,100),
                    # auto_dismiss=False
                )
                popup.open()
                # self.restart()
                # self.switch_game()
        
    def restart(self,event):
        """
        Resets the game to its initial state for a new match.
        - event: The event object passed from the button press.
        """
        # Clear the text from all cells on the board.
        for ent in self.listEntries:
            ent.text = ''
        # Reset all game state variables to their starting values.
        self.available_cases = [0,1,2,3,4,5,6,7,8]
        self.gameOver = False
        # Clear the moves for both players.
        self.player1_moves = set()
        self.player2_moves = set()
        self.player1_symbol = "x"
        self.player2_symbol = "o"
        self.turn = self.player1_symbol



# This class represents the game screen for Player vs Computer mode.
class SecondScreen(BoxLayout):
    """
    The main game screen widget for a single-player (human vs. computer) game.
    It handles the game board, player input, computer AI moves, win/draw detection,
    and game controls.
    """
    def __init__(self, switch_game, switch_back, **kwargs):
        super().__init__(**kwargs)

        # Set the main layout to be vertical with padding and spacing.
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        # Create the grid that will hold the 3x3 game board cells.
        self.textInput_gridlayout = GridLayout(cols=3)
        self.add_widget(self.textInput_gridlayout)

        # Create a grid to hold the control buttons below the game board.
        self.buttons_gridlayout = GridLayout(cols=3, size_hint_y=None, height=50,padding=(30,1), spacing=10)

        # 'Restart' button to start a new game in this mode.
        restart_button = Button(
            text="restart",
            size_hint=(None, None),
            size=(80, 40),
            background_normal="",
            background_color=(0, 0, 1, 1)  # bluerestart_button
        )
        # Bind the button's release event to the restart method.
        restart_button.bind(on_release = self.restart)
        self.buttons_gridlayout.add_widget(restart_button)

        # 'Switch' button to change to the other game mode (e.g., PvC to PvP).
        switch_game_button = Button(
            text="switch",
            size_hint=(None, None),
            size=(80, 40),
            background_normal="",
            background_color=(0, 0, 1, 1)
        )
        # Bind the button's release event to the switch_game function from the main app.
        switch_game_button.bind(on_release = switch_game)
        self.buttons_gridlayout.add_widget(switch_game_button)

        # 'Back' button to return to the initial mode selection screen.
        back_button = Button(
            text="back",
            size_hint=(None, None),
            size=(80, 40),
            background_normal="",
            background_color=(0, 0, 1, 1)  # bluerestart_button
        )
        # Bind the button's release event to the switch_back function from the main app.
        back_button.bind(on_release = switch_back)
        self.buttons_gridlayout.add_widget(back_button)

        # Add the grid of control buttons to the main layout.
        self.add_widget(self.buttons_gridlayout)

        # Define all possible winning combinations (rows, columns, diagonals)
        self.win_cases = [
                     {0, 1, 2}, {3, 4, 5}, {6, 7, 8},# Horizontal wins
                     {0, 3, 6}, {1, 4, 7}, {2, 5, 8},# Vertical wins
                     {0, 4, 8}, {2, 4, 6}# Diagonal wins
                    ]
        # Track available positions for each winning case
        # This helps the computer determine which moves to prioritize.
        self.available_cases = [
                      [0, 1, 2], [3, 4, 5], [6, 7, 8],
                      [0, 3, 6], [1, 4, 7], [2, 5, 8],
                      [0, 4, 8], [2, 4, 6]
        ]
        # A list to store all the TextInput widgets for the 3x3 grid.
        self.listEntries = []
        # A flag to track if the game has ended.
        self.gameOver = False
        # Sets to track moves made by the computer and the human player.
        self.computer_moves = set()
        self.player_moves = set()

        # Create and display the game board.
        self.display_board()

    def display_board(self):
        """
        Creates and populates the 3x3 grid with TextInput widgets for the game board.
        """
        # Create 9 TextInput widgets for the 3x3 grid.
        for _ in range(9): # Loop 9 times for each cell.
            txtInput = TextInput(
                halign="center",
                readonly=True,
                size_hint=(None,None),
                font_size=100,
                size=(160,160),
                multiline=False
            )
            # Bind the touch event on each cell to the player_move method.
            txtInput.bind(on_touch_down=self.player_move) # Bind click event to player_move function
            self.listEntries.append(txtInput) # Add to list for later reference
            self.textInput_gridlayout.add_widget(txtInput)

    def player_move(self,instance,touch):
        """
        Handles the logic when the human player clicks on a cell.
        After the player's move, it triggers the computer's move.
        - instance: The TextInput widget that was touched.
        - touch: The touch event information.
        """
        # Ignore clicks if the game is over or if the click is not on a cell.
        if instance not in self.listEntries or self.gameOver:
            return
        # Check if the touch event occurred within the bounds of the TextInput widget.
        if instance.collide_point(*touch.pos):
            # Find the index of this widget in our list (0-8 for the 3x3 grid)
            player_choice = self.listEntries.index(instance)
            # Ignore the move if the chosen cell is already taken by either player.
            if int(player_choice) in self.computer_moves or int(player_choice) in self.player_moves:
                return
            # Record the player's move
            self.player_moves.add(int(player_choice))
            # Remove the chosen cell from the computer's list of available cases.
            for case in self.available_cases:
                if int(player_choice) in case:
                    case.remove(int(player_choice))

            # Update the visual representation of the move
            instance.readonly=False # Allow editing
            instance.foreground_color = colors["Gray"]["900"] # Set text color
            instance.text = "x" # Insert 'x' symbol
            instance.readonly=True # Make read-only again
            # Check if player won with this move
            self.check_winner(self.player_moves, "x",player_choice)
            # If the game is not over, let the computer make its move.
            if not self.gameOver:
                self.computer_move()
            # else:
            #     self.restart()

    # Handle computer's move
    def computer_move(self):
        """
        Determines and executes the computer's next move based on a simple AI strategy.
        The strategy has a flaw: it finds a blocking move first, but then overwrites
        it if a winning move is found, effectively prioritizing winning over blocking.
        """
        min_length = 3 # Start with maximum case length
        computer_choice = None
        
        # Strategy 1: Pick a move from the smallest available winning case to block the player.
        # This prioritizes moves that are part of win lines with fewer open spots.
        for case in self.available_cases:
            if 0 < len(case) <= min_length:
                for i in range(len(case)):
                    if case[i] not in self.computer_moves:
                        min_length = len(case)
                        computer_choice = case[i]
        
        # Strategy 2: Check if the computer can win in this turn. This is the highest priority.
        # It looks for cases where the computer has 2 moves and can complete a winning line.
        for case in self.win_cases:
            # Count how many of the computer's moves are in this winning case.
            count = sum(1 for i in case if i in self.computer_moves)
            if count == 2: # Computer has 2 out of 3 positions
                for i in case:
                    # Find the empty position to complete the win
                    if i not in self.computer_moves and i not in self.player_moves:
                        computer_choice = i
        # --- Execute the chosen move ---
        if computer_choice is not None: # If a valid move was found...
            # print(computer_choice)# Debug output
            # Update visual representation
            self.listEntries[int(computer_choice)].readonly=False # Allow editing
            self.listEntries[int(computer_choice)].foreground_color = colors["Gray"]["600"] # Set text color
            self.listEntries[int(computer_choice)].text = "o" # Insert 'o' symbol
            self.listEntries[int(computer_choice)].readonly=True # Make read-only again
            # Record the computer's move
            self.computer_moves.add(int(computer_choice))
        # Check if computer won with this move
        self.check_winner(self.computer_moves, "o",computer_choice)
    
    # Check for win conditions or draw
    def check_winner(self,player_moves, symbol,player_turn):
        """
        Checks if the most recent move resulted in a win or a draw.
        - player_moves: A set of moves for the player being checked.
        - symbol: The symbol of the player ('x' or 'o').
        - player_turn: The specific cell index of the last move. Used here to detect a draw.
        """
        # Check for a draw. This logic is flawed because player_turn will rarely be None.
        # A better approach would be to check if all cells are filled.
        if player_turn is None:  # no more moves left
            # Highlight all cells in blue for draw
            for ent in self.listEntries:
                ent.foreground_color = colors["Blue"]["800"] # Set text color
            # Show a popup message for a draw.
            popup = Popup(
                    title = "It's a draw!",
                    size_hint=(None,None),
                    size=(200,100),
                    # auto_dismiss=False
                )
            popup.open()
            self.gameOver = True
            return
        # Check each winning case to see if the current player has achieved it.
        for case in self.win_cases:
            # A win occurs if all positions in a winning case are in the player's moves.
            if case <= player_moves:  # check if all elements of case are in player_moves
                if symbol == 'x': # Player wins
                    # Highlight winning combination in green
                    for i in case:
                        self.listEntries[i].foreground_color = colors["Green"]["800"] # Set text color
                    popup = Popup(
                    title = "You win!",
                    size_hint=(None,None),
                    size=(200,100),
                    # auto_dismiss=False
                    )
                    popup.open()
                else: # Computer wins
                    # Highlight winning combination in red
                    for i in case:
                        self.listEntries[i].foreground_color = colors["Red"]["800"] # Set text color
                    popup = Popup(
                    title = "You lose!",
                    size_hint=(None,None),
                    size=(200,100),
                    # auto_dismiss=False
                    )
                    popup.open()
                self.gameOver = True # End the game.
                self.gameOver = True       
                return
            
    def restart(self,event):
        """
        Resets the game to its initial state for a new match.
        - event: The event object passed from the button press.
        """
        # Clear the text from all cells on the board.
        for ent in self.listEntries:
            ent.text = ''
        # Reset all game state variables to their starting values.
        self.available_cases = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
        ]
        self.gameOver = False
        self.computer_moves = set()
        self.player_moves = set()



# The main application class that manages the different screens.
class MyKivyApp(App):
    """
    The main application class that orchestrates the different screens (widgets).
    It is responsible for building the initial UI and managing the transitions
    between the InitialScreen, FirstScreen (PvP), and SecondScreen (PvC).
    """
    def build(self):
        # Instantiate the different screens (widgets) of the application, passing the switch methods.
        self.first_screen = FirstScreen(self.switch_second_screen,self.switch_back_initial_screen)
        self.second_screen = SecondScreen(self.switch_first_screen,self.switch_back_initial_screen)
        self.initial_screen = InitialScreen(self.switch_first_screen,self.switch_second_screen)
        # The root layout that will hold the currently active screen widget.
        self.root_layout = BoxLayout()
        # Start by showing the initial screen to let the user choose a mode.
        self.root_layout.add_widget(self.initial_screen)
        return self.root_layout
    
    def switch_first_screen(self,instance=None):
        """Switches the view to the Player vs. Player game screen."""
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.first_screen)

    def switch_second_screen(self,instance=None):
        """Switches the view to the Player vs. Computer game screen."""
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.second_screen)

    def switch_back_initial_screen(self,instance=None):
        """Switches the view back to the initial mode selection screen."""
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.initial_screen)
    
# This is the standard Python entry point.
# If this script is run directly (not imported), it will create an instance
# of MyKivyApp and start the Kivy application event loop.
if __name__ == '__main__':
    MyKivyApp().run()