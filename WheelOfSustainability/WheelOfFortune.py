"""
AUTHORS: Uyen Thy Duong, Spencer Kubat
COURSE:  CISC 440
DATE:    05/13/2025

Wheel of Fortune – Sustainability Edition

This game is a sustainability-themed adaptation of Wheel of Fortune designed for both human and AI players.
Players take turns spinning a wheel and guessing letters to solve a hidden environmental phrase.

Key Features:
- Three play modes: Player vs Player, Player vs AI, and Player vs Random AI
- Difficulty levels dynamically adjust AI behavior and phrase complexity
- AI uses Constraint Satisfaction (CSP), Uniform Cost Search (UCS), and Greedy Search to make intelligent guesses
- Special wedges include JACKPOT, BANKRUPT, and 1/2 CAR, LOSE A TURN
- Players can buy vowels for a cost of $250
- Phrase bank is drawn from sustainability_words.txt

The game highlights how AI techniques can be applied to educational and environmentally focused gameplay.
"""


import random
import string
import time
from enum import Enum


VOWEL_COST = 250
VOWELS = 'AEIOU'
LETTERS = string.ascii_uppercase
PHRASES = []

# Load phrases from file
with open('./WheelOfSustainability/sustainability_words.txt') as f:
    PHRASES = [line.strip() for line in f if line.strip()]

# Define the wheel wedges
WHEEL = [
    '$500', '1/2 CAR', '$500', 'BANKRUPT', '$2500', '$600', '$500',
    'JACKPOT', '$500', '$500', 'BANKRUPT', '$1500', '$400', '$300',
    '1/2 CAR', '$300', '$300', 'LOSE A TURN', '$600',
    '$300', 'LOSE A TURN', '$800', '$800', '$900',
    '$700', '$600'
]

class Difficulty(Enum):
    EASY = 1
    MEDIUM = 5
    HARD = 8


# Part A: Base class for all players
class WOFPlayer:
    def __init__(self, name):
        self.name = name
        self.prizeMoney = 0
        self.prizes = []
        self.half_car_count = 0  # Tracks how many 1/2 CAR wedges they’ve earned

    def addMoney(self, amt):
        # Add money to the player's total
        self.prizeMoney += amt

    def goBankrupt(self):
        # Reset money and special items on bankruptcy
        self.prizeMoney = 0
        self.half_car_count = 0
        self.prizes = []  # Reset the player's prizes

    def addPrize(self, prize):
        # Add a prize to the player's prize list
        self.prizes.append(prize)

    def buyVowel(self, vowel):
        # Deduct cost of vowel from player's money
        if self.prizeMoney >= VOWEL_COST and vowel.upper() in VOWELS:
            self.prizeMoney -= VOWEL_COST
            print(f"{self.name} bought a vowel: {vowel.upper()} for ${VOWEL_COST}. Remaining money: ${self.prizeMoney}")
            return True
        else:
            print(f"{self.name} cannot afford to buy a vowel.")
            return False
    
    def __str__(self):
        return f"{self.name} (${self.prizeMoney})"

# Human player class inherits WOFPlayer
class WOFHumanPlayer(WOFPlayer):
    def getMove(self, obscured, guessed):
        # Prompt for human input during their turn
        prompt = f"""{self.name} has ${self.prizeMoney}
Current Phrase:  {obscured}
Guessed: {', '.join(sorted(guessed))}
Guess a letter, phrase, or type '_exit' or '_pass': """
        return input(prompt)

# Computer player class inherits WOFPlayer and adds decision-making logic
class WOFComputerPlayer(WOFPlayer):
    def __init__(self, name, difficulty):
        super().__init__(name)
        self.difficulty = difficulty

    def smartCoinFlip(self):
        old_difficulty = self.difficulty
        self.difficulty = random.randint(1, 10)
        return self.difficulty > old_difficulty

    def getPossibleLetters(self, guessed):
        possible = [l for l in LETTERS if l not in guessed]
        if self.prizeMoney < VOWEL_COST:
            possible = [l for l in possible if l not in VOWELS]
        return possible

    # Helper method to compare phrase to obscuredPhrase
    def checkMatch(self, obscured, guessed, phrase):
        for o, p in zip(obscured.upper(), phrase.upper()):
            if o != '_' and o != p:
                return False
            if o == '_' and p in guessed:
                return False
        return True
    
    # CSP filter to find matching phrases
    def cspFilter(self, obscured, guessed):
        """
        variables: obscuredPhrase, phrase
        domains = {
            obscuredPhrase: the phrase with unguessed letters as '_'
            PHRASES: the original phrase from the file sustainability_words.txt
        }
        constraints = {
            obscuredPhrase must match the phrase with guessed letters
        }
        Since we cannot change the obscuredPhrase, we don't need to work on a queue and 
        """
        constraints = lambda p: len(p) == len(obscured) and self.checkMatch(obscured, guessed, p)

        # Filter phrases based on constraints
        matches = []
        # Check if the phrase matches the obscuredPhrase
        for p in PHRASES:
            if constraints(p):
                matches.append(p)
        return matches

    def mismatchHeuristic(self, candidate, obscured):
        mismatches = 0
        for c, o in zip(candidate.upper(), obscured.upper()):
            if o != '_' and c != o:
                mismatches += 1
        return mismatches

    def letterFrequency(self, word, possible_letters):
        freq = {}
        for char in word.upper():
            if char in possible_letters:
                freq[char] = freq.get(char, 0) + 1
        return freq

    # Greedy search to find the most frequent letter
    def greedySearch(self, candidates, obscured, possible_letters):
        best_phrase = min(candidates, key=lambda p: self.mismatchHeuristic(p, obscured))
        freqs = self.letterFrequency(best_phrase, possible_letters)
        return max(freqs, key=freqs.get) if freqs else None


    # Uniform cost search to find the most frequent letter that is not vowel to optimal the budget of the player
    def uniformCostSearch(self, candidates, possible_letters):
        letter_cost = {}
        for phrase in candidates:
            for l in phrase.upper():
                if l in possible_letters and l not in VOWELS:
                    letter_cost[l] = letter_cost.get(l, 0) + 1

        if not letter_cost:
            return None
        return max(letter_cost, key=letter_cost.get)

    def getMove(self, obscured, guessed):
        print(f"""{self.name} has ${self.prizeMoney}
Current Phrase:  {obscured}
Guessed: {', '.join(sorted(guessed))}
Guess a letter, phrase, or type '_exit' or '_pass': """, end='')

        if obscured.count('_') == 0:
            print(obscured)
            return obscured
        
        possible_letters = self.getPossibleLetters(guessed)
        if not possible_letters:
            print("_pass")
            return "_pass"

        if self.smartCoinFlip():
            candidates = self.cspFilter(obscured, guessed)

            if candidates:
                if len(candidates) == 1 and self.difficulty == 10:
                    move = candidates[0]
                elif self.difficulty <= 5:
                    move = self.uniformCostSearch(candidates, possible_letters)
                else:
                    move = self.greedySearch(candidates, obscured, possible_letters)

                if move:
                    print(move)
                    return move

        move = random.choice(possible_letters)
        print(move)
        return move


# Helper function to obscure unguessed letters

def obscurePhrase(phrase, guessed):
    result = []
    for char in phrase:
        if not char.isalnum() or char.upper() in guessed:  
            result.append(char)
        else:
            result.append('_')
    return ''.join(result)


# Function to spin the wheel and return a result

def spinWheel():
    return random.choice(WHEEL)

# Main gameplay loop

def takeTurn(player, move, guessed, obscured, phrase, spun):
    """Handle a player's letter guess."""
    move = move.upper()
    if move in guessed:
            print("Letter already guessed.")
            return False  # Skip turn

    
    if move in VOWELS and not player.buyVowel(move):
        return False
    guessed.add(move)
    if move in phrase.upper():
        count = phrase.upper().count(move)
        if spun == 'JACKPOT':
            jackpot = 10000
            winnings = jackpot * count
            player.addMoney(winnings)
            print(f"{move} appears {count} time(s)! {player.name} hit the JACKPOT and won ${winnings}!")
        elif spun.startswith('$'):
            amt = int(spun.strip('$'))
            winnings = amt * count
            player.addMoney(winnings)
            print(f"{move} appears {count} time(s)! {player.name} won ${winnings}!")
        else:
            player.addPrize(spun)
            print(f"{player.name} won a prize: {spun}!")
    else:
        print(f"{move} is not in the phrase.")
        return False
    return True  # Turn completed


def guessPhrase(player, move, phrase):
    """Handle a player's full phrase guess."""
    if move.upper() == phrase.upper():
        print(f"{player.name} guessed the phrase! {player.name} win!")
        return True  # Game ends
    else:
        print(f"Incorrect Phrase guess.")
        return False  # Continue game


def playGame(mode):
    time.sleep(1)
    print()
    print("============================")
    print()

    # Initialize players based on the selected mode
    players = []
    if mode == "PVP":
        num_human = 2
        for i in range(num_human):
            name = input(f"Enter name for Player {i+1}: ")
            players.append(WOFHumanPlayer(name))
        while True:
            choice = input('\nChoose Difficulty (Easy, Medium, Hard): ').strip().upper()
            try:
                difficulty = Difficulty[choice].value
                break
            except KeyError:
                print("Invalid selection. Please try again.")
    elif mode == "PVA":
        name = input("Enter name for the human player: ")
        players.append(WOFHumanPlayer(name))
        while True:
            choice = input('\nChoose Difficulty (Easy, Medium, Hard): ').strip().upper()
            try:
                difficulty = Difficulty[choice].value
                break
            except KeyError:
                print("Invalid selection. Please try again.")
        players.append(WOFComputerPlayer("AI", difficulty))
    elif mode == "PVR":
        name = input("Enter name for the human player: ")
        players.append(WOFHumanPlayer(name))
        print("AI player will choose a random difficulty.")
        difficulty = random.randint(1, 10)
        players.append(WOFComputerPlayer("AI", difficulty))
    elif mode == "Custom":
        num_human = int(input("Enter number of human players: "))
        num_computer = int(input("Enter number of computer players: "))
        print()
        print("============================")
        if num_human < 0 or num_computer < 0:
            print("Invalid number of players.")
            return
        print()
        while True:
            choice = input('Choose Difficulty (Easy, Medium, Hard): ').strip().upper()
            try:
                difficulty = Difficulty[choice].value
                break
            except KeyError:
                print("Invalid selection. Please try again.")
        for i in range(num_human):
            name = input(f"Enter name for human player {i+1}: ")
            players.append(WOFHumanPlayer(name))
        for i in range(num_computer):
            name = f"Computer {i+1}"
            players.append(WOFComputerPlayer(name, difficulty))

    
    print()
    lengthLimit = 48
    if difficulty == Difficulty.EASY.value:
        lengthLimit = 12
    elif difficulty == Difficulty.MEDIUM.value:
        lengthLimit = 24

    subPhrases = [p for p in PHRASES if len(p) <= lengthLimit]
    if not subPhrases:
        print("Error: No phrases match the selected difficulty.")
        return

    phrase = random.choice(subPhrases)
    guessed = set()
    current_player = 0

       

    print()
    print("============================")
    print("       GAME START!")
    print("============================")
    obscured = obscurePhrase(phrase, guessed)
    print()
    print(f"The phrase is: {obscured}")
    # Game loop
    while True:
        print()
        print("============================")
        print()
        time.sleep(2)
        player = players[current_player]
        obscured = obscurePhrase(phrase, guessed)

        spun = spinWheel()
        print(f"{player.name} spun: {spun}")

        # Handle special wheel outcomes
        if spun == 'BANKRUPT':
            player.goBankrupt()
            print(f"{player.name} went bankrupt!")
            current_player = (current_player + 1) % len(players)
            continue
        elif spun == 'LOSE A TURN':
            print(f"{player.name} spun: LOSE A TURN and loses a turn.")
            current_player = (current_player + 1) % len(players)
            continue
        elif spun == '1/2 CAR':
            player.half_car_count += 1
            print(f"{player.name} collected a 1/2 CAR wedge! Total: {player.half_car_count}")
            if player.half_car_count >= 2:
                player.addPrize('Car')
                player.half_car_count -= 2
                print(f"{player.name} has won a CAR!")
            current_player = (current_player + 1) % len(players)
            continue

        while True:
            move = player.getMove(obscured, guessed)
            if not move:
                print("Invalid input. Please try again.")
                continue
            break

        if move == '_exit':
            print()
            print("============================\n")
            print(f"{player.name} exited the game.")
            print("Thank you for playing!")
            players.pop(current_player)
            if(len(players) > 0):
                current_player = current_player % len(players)
            else:
                print("============================")
                print("\nNo players left. Game over.")
                break
            continue
        elif move == '_pass':
            print(f"{player.name} passed.")

        elif len(move) == 1 and move.upper() in LETTERS:
            if takeTurn(player, move, guessed, obscured, phrase, spun):
                continue
        else:
            # Check for win
            if guessPhrase(player, move, phrase):
                print()
                print("============================")
                print(f"{player.name} wins! The phrase was: {phrase}")
                print("============================")
                break

        current_player = (current_player + 1) % len(players)

def mainMenu():
    """Display the main menu and handle user selection."""
    while True:
        print("============================")
        print("Welcome to Wheel of Fortune!")
        print("============================")
        print("1. Player vs Player")
        print("2. Player vs AI")
        print("3. Player vs Random")
        print("4. Custom Game")
        print("5. Exit")
        print("============================")
        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            playGame(mode="PVP")
            print()
        elif choice == '2':
            playGame(mode="PVA")
            print()
        elif choice == '3':
            playGame(mode="PVR")
            print()
        elif choice == '4':
            playGame(mode="Custom")
            print()
        elif choice == '5':
            print("Thank you for playing! Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")

# Entry point
if __name__ == "__main__":
    mainMenu()
