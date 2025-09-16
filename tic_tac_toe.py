from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivymd.color_definitions import colors
from kivy.uix.popup import Popup

# Set a background color for the entire window
Window.clearcolor = (0.9, 0.9, 0.9, 1) # A light gray color
Window.size = (1000, 680) # Set the window size to 800x400 pixels

# This class defines the layout and functionality for the initial screen.
# It inherits from BoxLayout, arranging its children widgets vertically or horizontally.
class InitialScreen(BoxLayout):
    """
    The initial screen widget that presents the user with game mode choices:
    - Player vs. Computer
    - Player vs. Player
    """
    def __init__(self, switch_player_vs_player_mode, switch_player_computer_mode, **kwargs):
        super().__init__(**kwargs)

        # Set the main layout to be vertical with significant padding and spacing
        # to center the content.
        self.orientation = "vertical"
        self.padding = 250
        self.spacing = 100

        # Use an AnchorLayout to center the button grid within the available space.
        self.anchorlayout = AnchorLayout(anchor_x='center', anchor_y='center')

        # A GridLayout to hold the mode selection buttons.
        # It's configured with 3 columns to allow for spacing.
        self.buttons_gridlayout = GridLayout(cols=3, size_hint_y=None, spacing=30)

        # first button
        play_vs_computer_mode_button = Button(
            text="player vs compute",
            size_hint=(None, None),
            size=(140, 40),
            background_normal="",
            background_color=colors["Blue"]["500"]
        )
        # Binds the button's 'on_release' event to the function that switches to Player vs. Computer mode.
        play_vs_computer_mode_button.bind(on_release = switch_player_computer_mode)
        self.buttons_gridlayout.add_widget(play_vs_computer_mode_button)

        # An empty widget to create space between the two buttons.
        self.buttons_gridlayout.add_widget(Widget())

        # second button
        player_vs_player_mode_button = Button(
            text="player vs player",
            size_hint=(None, None),
            size=(140, 40),
            background_normal="",
            background_color=colors["Teal"]["700"] # A teal color for this button
        )
        # Binds the button's 'on_release' event to the function that switches to Player vs. Player mode.
        player_vs_player_mode_button.bind(on_release = switch_player_vs_player_mode)
        self.buttons_gridlayout.add_widget(player_vs_player_mode_button)

        # Add the grid of buttons to the anchor layout, and then the anchor layout to the main screen.
        self.anchorlayout.add_widget(self.buttons_gridlayout)
        self.add_widget(self.anchorlayout)



# This class defines the layout and game logic for the Player vs. Player mode.
class FirstScreen(BoxLayout):
    """
    The main game screen widget for a two-player (human vs. human) game.
    It handles the game board, player turns, win/draw detection, and game controls.
    """
    def __init__(self, switch_game, switch_back, **kwargs):
        super().__init__(**kwargs)

        # Set the main layout to be horizontal, allowing the game board and scoreboard to be side-by-side.
        self.orientation = "horizontal"
        self.padding = 20
        self.spacing = 10

        # A vertical BoxLayout to contain the game grid and the control buttons below it.
        self.game_boxlayout = BoxLayout(orientation = "vertical", padding = 50, spacing = 10)

        # GridLayout for the 3x3 Tic-Tac-Toe board cells.
        self.textInput_gridlayout = GridLayout(cols=3)
        self.game_boxlayout.add_widget(self.textInput_gridlayout)
        
        # GridLayout for the control buttons (restart, switch, back).
        # It's configured with 3 columns.
        self.buttons_gridlayout = GridLayout(cols=3, size_hint_y=None, height=50,padding=(30,10) ,spacing=10)

        # 'Restart' button to start a new game in the current mode.
        restart_button = Button(
            text="restart",
            size_hint=(None, None),
            size=(80, 40),
            background_normal="",
            background_color=colors["Red"]["500"]
        )
        # Binds the button's 'on_release' event to this class's 'restart' method.
        restart_button.bind(on_release = self.restart)
        self.buttons_gridlayout.add_widget(restart_button)

        # 'Switch' button to change to the other game mode (e.g., PvP to PvC).
        # The actual switch logic is handled by the main app class.
        switch_game_button = Button(
            text="switch",
            size_hint=(None, None),
            size=(80, 40),
            background_normal="",
            background_color=colors["Amber"]["700"]
        )
        # Binds the button's 'on_release' event to the switch_game function passed from the main app.
        switch_game_button.bind(on_release = switch_game)
        self.buttons_gridlayout.add_widget(switch_game_button)

        # 'Back' button to return to the initial mode selection screen.
        back_button = Button(
            text="back",
            size_hint=(None, None),
            size=(80, 40),
            background_normal="",
            background_color=colors["Gray"]["600"]
        )
        # Binds the button's 'on_release' event to the switch_back function passed from the main app.
        back_button.bind(on_release = switch_back)
        self.buttons_gridlayout.add_widget(back_button)
        # Add the grid of control buttons to the game layout.
        self.game_boxlayout.add_widget(self.buttons_gridlayout)
        self.add_widget(self.game_boxlayout)

        # An AnchorLayout to center the scoreboard on the right side of the screen.
        self.anchorlayout = AnchorLayout(anchor_x='center', anchor_y='center')
        # A BoxLayout to organize the score labels and text inputs vertically.
        self.scours_boxlayout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(250, 150), spacing=10)

        # Label and TextInput for Player 1's score.
        self.player1_scour_labe = Label(text="Player 1 (X) Score", color=(0,0,0,1),font_size=22)
        self.scours_boxlayout.add_widget(self.player1_scour_labe)
        self.player1_scour_textinput = TextInput(
                halign="center",
                # readonly=True,
                size_hint=(None,None),
                font_size=30,
                size=(70,50),
                background_normal='',
                background_active='',
                multiline=False,
                background_color=(.95, .95, .95, 1) # A very light gray
        )
        self.player1_scour_textinput.text = "0"
        self.scours_boxlayout.add_widget(self.player1_scour_textinput)

        # Label and TextInput for Player 2's score.
        self.player2_scour_labe = Label(text="Player 2 (O) Score", color=(0,0,0,1),font_size=22) # Black text
        self.scours_boxlayout.add_widget(self.player2_scour_labe)
        self.player2_scour_textinput = TextInput(
            halign="center",
                # readonly=True,
                size_hint=(None,None),
                font_size=30,
                size=(70,50),
                background_normal='',
                background_active='',
                multiline=False,
                background_color=(.95, .95, .95, 1) # A very light gray
        )
        self.player2_scour_textinput.text = "0"
        self.scours_boxlayout.add_widget(self.player2_scour_textinput)
        # Add the scoreboard layout to the anchor layout, and then to the main screen.
        self.anchorlayout.add_widget(self.scours_boxlayout)

        self.add_widget(self.anchorlayout)

        # Define all possible winning combinations (rows, columns, diagonals).
        # Each set represents positions that form a winning line
        self.win_cases = [
                     {0, 1, 2}, {3, 4, 5}, {6, 7, 8},# Horizontal wins
                     {0, 3, 6}, {1, 4, 7}, {2, 5, 8},# Vertical wins
                     {0, 4, 8}, {2, 4, 6}# Diagonal wins
                    ]
        # A list to track available positions on the board (0-8).
        # When a cell is taken, its number is removed from this list.
        self.available_cases = [0,1,2,3,4,5,6,7,8]
        # A list to hold the 9 TextInput widgets that form the game grid.
        self.listEntries = []
        # A boolean flag to prevent moves after the game has concluded.
        self.gameOver = False
        # Sets to track the moves made by each player.
        self.player1_moves = set()
        self.player2_moves = set()
        # Define symbols for each player.
        self.player1_symbol = "x"
        self.player2_symbol = "o"
        # Keep track of whose turn it is, starting with player 1.
        self.turn = self.player1_symbol

        # Initialize the game board by creating and adding the TextInput cells.
        self.display_board()


    def display_board(self):
        """
        Creates and populates the 3x3 grid with TextInput widgets.
        Each TextInput acts as a cell on the Tic-Tac-Toe board.
        """
        # Create 9 TextInput widgets for the 3x3 grid.
        for _ in range(9):
            txtInput = TextInput(
                halign="center",
                readonly=True,
                size_hint=(None,None),
                font_size=100,
                size=(160,160),
                background_color=(1, 1, 1, 1), # White background for cells
                multiline=False
                
            )
            # Binds the 'on_touch_down' event of each cell to the 'player_move' method.
            # This is how the game registers a player's click.
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
        # Also ensures the touch is within the widget's boundaries.
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
                 instance.foreground_color = colors["Blue"]["800"] # Player 1 color
                 instance.readonly=True
                 # Remove the chosen cell from the list of available spots.
                 self.available_cases.remove(int(player_choice))
                 # Check if this move results in a win.
                 self.check_winner(self.player1_symbol)
                 # Switch the turn to Player 2.
                 self.turn = self.player2_symbol
                 return

            # Handle Player 2's turn.
            if self.turn == self.player2_symbol and int(player_choice) in self.available_cases:
                 self.player2_moves.add(int(player_choice))
                 # Update the visual representation of the move
                 instance.readonly=False
                 instance.text = self.player2_symbol
                 instance.foreground_color = colors["Pink"]["800"] # Player 2 color
                 instance.readonly=True
                 # Remove the chosen cell from the list of available spots.
                 self.available_cases.remove(int(player_choice))
                 # Check if this move results in a win.
                 self.check_winner(self.player2_symbol)
                 # Switch the turn to Player 1.
                 self.turn = self.player1_symbol
                 return
            
    def check_winner(self,player_symbol):
        """
        Checks if the most recent move resulted in a win or a draw.
        - player_symbol: The symbol ('x' or 'o') of the player to check.
        """
        # Check for a draw condition: if no cells are available and no one has won yet.
        if len(self.available_cases) == 0:
            # Highlight all cells to indicate a draw.
            for ent in self.listEntries:
                ent.background_color = colors["LightGreen"]["200"] # Use a light green for draw
            popup = Popup(
                    title = "it's draw!",
                    size_hint=(None,None),
                    size=(200,100),
                    # auto_dismiss=False
            )
            popup.open()
            return
        # Determine which player's moves to check.
        if player_symbol == self.player2_symbol:
            player_moves = self.player2_moves
        else:
            player_moves = self.player1_moves
        # Iterate through all predefined winning combinations.
        for case in self.win_cases:
            # A win occurs if all positions in a winning case are in the player's moves.
            if case <= player_moves:  # check if all elements of case are in player_moves
                # Highlight the winning combination of cells.
                for i in case:
                    self.listEntries[i].background_color = colors["LightGreen"]["200"]
                # Set the game over flag to prevent further moves.
                self.gameOver = True
                # Show a popup message announcing the winner.
                popup = Popup(
                    title = f"{player_symbol} win!",
                    size_hint=(None,None),
                    size=(200,100),
                    # auto_dismiss=False
                )
                popup.open()
        
    def restart(self,event):
        """
        Resets the game to its initial state for a new match.
        - event: The event object passed from the button press.
        """
        # Clear the text from all cells on the board.
        for ent in self.listEntries:
            ent.text = '' # Clear the 'x' or 'o'
            ent.background_color = (1,1,1,1) # Reset cell background to white
        # Reset all game state variables to their initial values.
        # This includes available spots, game over status, player moves, and whose turn it is.
        self.available_cases = [0,1,2,3,4,5,6,7,8]
        # Reset the game over flag.
        self.gameOver = False
        # Clear the moves for both players.
        self.player1_moves = set()
        self.player2_moves = set()
        self.player1_symbol = "x"
        self.player2_symbol = "o"
        self.turn = self.player1_symbol



# This class defines the layout and game logic for the Player vs. Computer mode.
class SecondScreen(BoxLayout):
    """
    The main game screen widget for a single-player (human vs. computer) game.
    It handles the game board, player input, computer AI moves, win/draw detection,
    and game controls.
    """
    def __init__(self, switch_game, switch_back, **kwargs):
        super().__init__(**kwargs)

        # Set the main layout to be horizontal, allowing the game board and scoreboard to be side-by-side.
        self.orientation = "horizontal"
        self.padding = 20
        self.spacing = 10

        # A vertical BoxLayout to contain the game grid and the control buttons below it.
        self.game_boxlayout = BoxLayout(orientation = "vertical", padding = 50, spacing = 10)
        # GridLayout for the 3x3 Tic-Tac-Toe board cells.
        self.textInput_gridlayout = GridLayout(cols=3)
        self.game_boxlayout.add_widget(self.textInput_gridlayout)

        # GridLayout for the control buttons (restart, switch, back).
        # It's configured with 3 columns.
        self.buttons_gridlayout = GridLayout(cols=3, size_hint_y=None, height=50,padding=(30,10), spacing=10)

        # 'Restart' button to start a new game in this mode.
        restart_button = Button(
            text="restart",
            size_hint=(None, None),
            size=(80, 40),
            background_normal="",
            background_color=colors["Red"]["500"]
        )
        # Binds the button's 'on_release' event to this class's 'restart' method.
        restart_button.bind(on_release = self.restart)
        self.buttons_gridlayout.add_widget(restart_button)

        # 'Switch' button to change to the other game mode (e.g., PvC to PvP).
        # The actual switch logic is handled by the main app class.
        switch_game_button = Button(
            text="switch",
            size_hint=(None, None),
            size=(80, 40),
            background_normal="",
            background_color=colors["Amber"]["700"]
        )
        # Binds the button's 'on_release' event to the switch_game function from the main app.
        switch_game_button.bind(on_release = switch_game)
        self.buttons_gridlayout.add_widget(switch_game_button)

        # 'Back' button to return to the initial mode selection screen.
        back_button = Button(
            text="back",
            size_hint=(None, None),
            size=(80, 40),
            background_normal="",
            background_color=colors["Gray"]["600"]
        )
        # Binds the button's 'on_release' event to the switch_back function from the main app.
        back_button.bind(on_release = switch_back)
        self.buttons_gridlayout.add_widget(back_button)

        # Add the grid of control buttons to the game layout.
        self.game_boxlayout.add_widget(self.buttons_gridlayout)
        self.add_widget(self.game_boxlayout)


        # An AnchorLayout to center the scoreboard on the right side of the screen.
        self.anchorlayout = AnchorLayout(anchor_x='center', anchor_y='center')
        # A BoxLayout to organize the score labels and text inputs vertically.
        self.scours_boxlayout = BoxLayout(orientation='vertical', size_hint=(None, None), size=(250, 150), spacing=10)

        self.player_scour_labe = Label(text="Your Score", color=(0,0,0,1),font_size=22)
        self.scours_boxlayout.add_widget(self.player_scour_labe)
        self.player_scour_textinput = TextInput(
                halign="center",
                # readonly=True,
                size_hint=(None,None),
                font_size=30,
                size=(70,50),
                background_normal='',
                background_active='',
                multiline=False,
                background_color=(.95, .95, .95, 1) # A very light gray
        )
        self.player_scour_textinput.text = "0"
        self.scours_boxlayout.add_widget(self.player_scour_textinput)

        # Label and TextInput for the computer's score.
        self.computer_scour_labe = Label(text="Computer Score", color=(0,0,0,1),font_size=22) # Black text
        self.scours_boxlayout.add_widget(self.computer_scour_labe)
        self.computer_scour_textinput = TextInput(
            halign="center",
                # readonly=True,
                size_hint=(None,None),
                font_size=30,
                size=(70,50),
                background_normal='',
                background_active='',
                multiline=False,
                background_color=(.95, .95, .95, 1) # A very light gray
        )
        self.computer_scour_textinput.text = "0"
        self.scours_boxlayout.add_widget(self.computer_scour_textinput)
        # Add the scoreboard layout to the anchor layout, and then to the main screen.
        self.anchorlayout.add_widget(self.scours_boxlayout)

        self.add_widget(self.anchorlayout)
         

        # Define all possible winning combinations (rows, columns, diagonals).
        # Each set represents positions that form a winning line
        self.win_cases = [
                     {0, 1, 2}, {3, 4, 5}, {6, 7, 8},# Horizontal wins
                     {0, 3, 6}, {1, 4, 7}, {2, 5, 8},# Vertical wins
                     {0, 4, 8}, {2, 4, 6}# Diagonal wins
                    ]
        # Track available positions for each winning case
        # This nested list structure is used by the computer's AI to decide its moves.
        self.available_cases = [
                      [0, 1, 2], [3, 4, 5], [6, 7, 8],
                      [0, 3, 6], [1, 4, 7], [2, 5, 8],
                      [0, 4, 8], [2, 4, 6]
        ]
        # A list to hold the 9 TextInput widgets that form the game grid.
        self.listEntries = []
        # A boolean flag to prevent moves after the game has concluded.
        self.gameOver = False
        # Sets to track moves made by the computer and the human player.
        self.computer_moves = set()
        self.player_moves = set()

        # Initialize the game board by creating and adding the TextInput cells.
        self.display_board()

    def display_board(self):
        """
        Creates and populates the 3x3 grid with TextInput widgets for the game board.
        """
        # Create 9 TextInput widgets for the 3x3 grid.
        for _ in range(9):
            txtInput = TextInput(
                halign="center",
                readonly=True,
                size_hint=(None,None),
                font_size=100,
                size=(160,160),
                background_color=(1, 1, 1, 1), # White background for cells
                multiline=False
            )
            # Binds the 'on_touch_down' event of each cell to the 'player_move' method.
            txtInput.bind(on_touch_down=self.player_move)
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
            # The computer's AI uses 'available_cases' to make decisions.
            # We must remove the player's choice from these lists.
            for case in self.available_cases:
                if int(player_choice) in case:
                    case.remove(int(player_choice))

            # Update the visual representation of the move
            instance.readonly=False # Allow editing
            instance.foreground_color = colors["Blue"]["800"] # Player color
            instance.text = "x" # Insert 'x' symbol
            instance.readonly=True # Make read-only again
            # Check if player won with this move
            self.check_winner(self.player_moves, "x",player_choice)
            # If the game is still ongoing, let the computer make its move.
            if not self.gameOver:
                self.computer_move()

    # Handle computer's move
    def computer_move(self):
        """
        Determines and executes the computer's next move based on a simple AI strategy.
        The strategy has a flaw: it finds a blocking move first, but then overwrites
        it if a winning move is found, effectively prioritizing winning over blocking.
        """
        # Prioritize taking the center position if it's available.
        central_pos = 4
        if central_pos not in self.computer_moves and any(central_pos in case for case in self.available_cases):
            computer_choice = central_pos
        else:
            min_length = 3 # Start with maximum case length
            computer_choice = None
            
            # --- AI Strategy 1: Find a "good" defensive or offensive move ---
            # It iterates through the remaining possible win lines ('available_cases').
            # It prefers lines with fewer open spots, hoping to block the player.
            # This choice might be immediately overwritten by Strategy 2.
            for case in self.available_cases:
                if 0 < len(case) <= min_length:
                    for i in range(len(case)):
                        if case[i] not in self.computer_moves:
                            min_length = len(case)
                            computer_choice = case[i]
            
            # --- AI Strategy 2: Check for an immediate win ---
            # This is the highest priority. It checks if the computer has 2 out of 3 spots
            # in any winning line and takes the 3rd spot if it's available.
            for case in self.win_cases:
                count = sum(1 for i in case if i in self.computer_moves)
                if count == 2: # Computer has 2 out of 3 positions
                    for i in case:
                        # Find the empty position to complete the win
                        if i not in self.computer_moves and i not in self.player_moves:
                            computer_choice = i
        
        # --- Execute the chosen move ---
        if computer_choice is not None:
            # Update visual representation
            self.listEntries[int(computer_choice)].readonly=False # Allow editing
            self.listEntries[int(computer_choice)].foreground_color = colors["Pink"]["800"] # Computer color
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
        # Check for draw condition (no more moves available) 
        # This logic is flawed, as `player_turn` will rarely be None. A better check would be the number of total moves or if available_cases is empty.
        if player_turn is None:  # no more moves left
            # Highlight all cells to indicate a draw.
            for ent in self.listEntries:
                ent.background_color = colors["LightBlue"]["200"] # Set a light blue background for draw
            
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
        # Iterate through all predefined winning combinations.
        for case in self.win_cases:
            # A win occurs if all positions in a winning case are in the player's moves.
            if case <= player_moves:  # check if all elements of case are in player_moves
                if symbol == 'x': # Player wins
                    # Highlight winning combination with a light green background.
                    for i in case:
                        self.listEntries[i].background_color = colors["LightGreen"]["200"]
                    # Show a popup message for a player win.
                    popup = Popup(
                    title = "You win!",
                    size_hint=(None,None),
                    size=(200,100),
                    # auto_dismiss=False
                    )
                    popup.open()
                    # Update the player's score.
                    self.player_scour_textinput.readonly=False
                    self.player_scour_textinput.text = str(int(self.player_scour_textinput.text) + 1)
                    self.player_scour_textinput.readonly=True
                else: # Computer wins
                    # Highlight winning combination with a light red background.
                    for i in case:
                        self.listEntries[i].background_color = colors["Red"]["200"]
                    # Show a popup message for a computer win.
                    popup = Popup(
                    title = "You lose!",
                    size_hint=(None,None),
                    size=(200,100),
                    # auto_dismiss=False
                    )
                    popup.open()
                    # Update the computer's score.
                    self.computer_scour_textinput.readonly=False
                    self.computer_scour_textinput.text = str(int(self.computer_scour_textinput.text) + 1)
                    self.computer_scour_textinput.readonly=True
                # End the game
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
            ent.background_color = (1, 1, 1, 1) # Reset cell background color to white
        # Reset all game state variables to their initial values.
        # This includes the computer's AI state, game over status, and both players' moves.
        self.available_cases = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
        ]
        # Reset the game over flag and player move sets.
        self.gameOver = False
        self.computer_moves = set()
        self.player_moves = set()



# This is the main Kivy App class. It's the entry point of the application.
class MyKivyApp(App):
    """
    The main application class that orchestrates the different screens (widgets).
    It is responsible for building the initial UI and managing the transitions
    between the InitialScreen, FirstScreen (PvP), and SecondScreen (PvC).
    """
    def build(self):
        # Instantiate the different screens, passing the necessary screen-switching methods as callbacks.
        self.first_screen = FirstScreen(self.switch_second_screen,self.switch_back_initial_screen)
        self.second_screen = SecondScreen(self.switch_first_screen,self.switch_back_initial_screen)
        self.initial_screen = InitialScreen(self.switch_first_screen,self.switch_second_screen)
        # The root layout that will hold the currently active screen.
        self.root_layout = BoxLayout()
        # Start by showing the initial screen for mode selection.
        self.root_layout.add_widget(self.initial_screen)
        return self.root_layout
    
    def switch_first_screen(self,instance=None):
        """Clears the root layout and adds the Player vs. Player screen (FirstScreen)."""
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.first_screen)

    def switch_second_screen(self,instance=None):
        """Clears the root layout and adds the Player vs. Computer screen (SecondScreen)."""
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.second_screen)

    def switch_back_initial_screen(self,instance=None):
        """Clears the root layout and adds the initial mode selection screen (InitialScreen)."""
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.initial_screen)
    
# This is the standard Python entry point.
# If this script is run directly (not imported), it will create an instance
# of MyKivyApp and start the Kivy application event loop.
if __name__ == '__main__':
    MyKivyApp().run()