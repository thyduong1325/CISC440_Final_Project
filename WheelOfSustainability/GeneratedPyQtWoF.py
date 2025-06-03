import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QInputDialog
from WheelOfFortune import WOFHumanPlayer, WOFComputerPlayer, obscurePhrase, spinWheel, takeTurn


class WheelOfFortuneGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wheel of Fortune")
        self.setGeometry(100, 100, 600, 400)

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout()

        # Label to display game status
        self.status_label = QLabel("Welcome to Wheel of Fortune!")
        self.layout.addWidget(self.status_label)

        # Button to start the game
        self.start_button = QPushButton("Start Game")
        self.start_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_button)

        # Button to spin the wheel
        self.spin_button = QPushButton("Spin the Wheel")
        self.spin_button.clicked.connect(self.spin_wheel)
        self.layout.addWidget(self.spin_button)

        # Set layout
        self.central_widget.setLayout(self.layout)

        # Game state
        self.players = []
        self.current_player_index = 0
        self.phrase = "EXAMPLE PHRASE"  # Replace with actual phrase logic
        self.guessed = set()
        self.obscured = obscurePhrase(self.phrase, self.guessed)

    def start_game(self):
        # Initialize players and game state
        self.players = [WOFHumanPlayer("Player 1"), WOFComputerPlayer("AI", difficulty=5)]
        self.current_player_index = 0
        self.status_label.setText("Game Started! Player 1's turn.")
        self.obscured = obscurePhrase(self.phrase, self.guessed)
        # More initialization logic as needed

    def spin_wheel(self):
        # Logic to spin the wheel and update game state
        current_player = self.players[self.current_player_index]
        spun_value = spinWheel()  # Ensure this function returns a value
        self.status_label.setText(f"{current_player.name} spun {spun_value}!")

        # Prompt player for input
        self.get_player_input(current_player, spun_value)

    def get_player_input(self, player, spun_value):
        # Get player input for guessing a letter or phrase
        move, ok = QInputDialog.getText(self, "Player Move", f"{player.name}, enter your guess:")
        if ok and move:
            move = move.strip().upper()
            if move == 'EXIT':
                self.status_label.setText(f"{player.name} exited the game.")
                self.players.pop(self.current_player_index)
            elif move == 'PASS':
                self.status_label.setText(f"{player.name} passed.")
            else:
                # Handle the player's move
                if takeTurn(player, move, self.guessed, self.obscured, self.phrase, spun_value):
                    self.obscured = obscurePhrase(self.phrase, self.guessed)
                    self.status_label.setText(f"Phrase: {self.obscured}")
                else:
                    self.status_label.setText("Invalid move or letter already guessed.")

            # Move to the next player
            self.current_player_index = (self.current_player_index + 1) % len(self.players)


def main():
    app = QApplication(sys.argv)
    window = WheelOfFortuneGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()