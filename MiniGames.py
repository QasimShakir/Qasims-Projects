import random

# Define the card values
card_values = {
    2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,
    11: 11, 12: 12, 13: 13, 14: 14  
}

# Function to create a deck
def create_deck():
    deck = []
    for suit in ['Spades', 'Diamonds', 'Hearts', 'Clubs']:
        for rank in range(2, 15):
            deck.append({'suit': suit.capitalize(), 'rank': rank, 'points': card_values[rank]})
    return deck

# Function to shuffle the deck
def shuffle_deck(deck):
    random.shuffle(deck)

# Function to draw a card from the deck
def draw_card(deck):
    return deck.pop()

# Function to print cards
def Card_Printer(card):
    suits_name = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
    suits_symbols = ['♠', '♦', '♥', '♣']

    rank = card['rank']
    if rank == 11:
        rank = 'J'
    elif rank == 12:
        rank = 'Q'
    elif rank == 13:
        rank = 'K'
    elif rank == 14:
        rank = 'A'
    else:
        rank = str(rank)

    
    if card['rank'] == 10:
        rank_str = '10'
        space = ''
    else:
        rank_str = rank
        space = ' '

    suit = suits_name.index(card['suit'])
    suit = suits_symbols[suit]

    lines = [
        '┌─────────┐',
        '│{}{}       │'.format(rank_str, space),
        '│         │',
        '│         │',
        '│    {}    │'.format(suit),
        '│         │',
        '│         │',
        '│       {}{}│'.format(space, rank_str),
        '└─────────┘'
    ]

    return '\n'.join(lines)



# Function to display the cards
def show_hand(hand):
    for card in hand:
        print(Card_Printer(card))

# Function to bet
def bet(player_bankroll):
    while True:
        try:
            bet_size = int(input("How many coins would you like to bet? (Max: 5)\n"))
            if bet_size > player_bankroll:
                print("You can only bet the money you have.")
                bet_size = player_bankroll
            elif bet_size > 5:
                print("You can only bet 5 coins at most.")
                bet_size = 5
            player_bankroll -= bet_size
            print("You bet {} coins. Your current bankroll is {} coins.".format(bet_size, player_bankroll))
            return bet_size, player_bankroll
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Function to redraw cards
def redraw(hand, deck):
    while True:
        redraw_yn = input("Do you want to redraw any cards? Y/N \n").capitalize()
        if redraw_yn == "Y":
            try:
                redraw_num = int(input("How many cards do you want to redraw?\n"))
                if redraw_num > 1:
                    redraw_list = [int(x) - 1 for x in input("Which cards do you want to redraw? (Use commas to separate) \n").split(',')]
                    for i in redraw_list:
                        hand[i] = draw_card(deck)
                else:
                    redraw_index = int(input("Which card do you want to redraw? \n")) - 1
                    hand[redraw_index] = draw_card(deck)

                print("Your hand is now: \n")
                show_hand(hand)
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        elif redraw_yn == "N":
            break
        else:
            print("Invalid input. Please enter Y or N.")

# Function to score the cards
def score_hand(hand, bet_size, player_bankroll):
    points = sorted([card['points'] for card in hand])
    suits = [card['suit'] for card in hand]
    points_repeat = [points.count(i) for i in points]
    suits_repeat = [suits.count(i) for i in suits]
    diff = max(points) - min(points)
    hand_name = ""
    payoff = {
        "Royal Flush": 9,
        "Straight Flush": 8,
        "Flush": 7,
        "Full House": 6,
        "Four of a Kind": 5,
        "Three of a Kind": 4,
        "Two Pair": 3,
        "Straight": 2,
        "Pair": 1,
        "Bad Hand": 0,
    }

    if 5 in suits_repeat:
        if points == [10, 11, 12, 13, 14]:
            hand_name = "Royal Flush"
            player_bankroll += bet_size * payoff[hand_name] 
        elif diff == 4 and max(points_repeat) == 1:
            hand_name = "Straight Flush"
            player_bankroll += bet_size * payoff[hand_name] 
        elif diff == 12 and points[4] == 14:
            check = 0
            for i in range(1, 4):
                check += points[i] - points[i - 1]
            if check == 3:
                hand_name = "Straight Flush"
                player_bankroll += bet_size * payoff[hand_name] 
            else:
                hand_name = "Flush"
                player_bankroll += bet_size * payoff[hand_name] 
        else:
            hand_name = "Flush"
            player_bankroll += bet_size * payoff[hand_name] 
    elif sorted(points_repeat) == [2, 2, 3, 3, 3]:
        hand_name = "Full House"
        player_bankroll += bet_size * payoff[hand_name] 
    elif 4 in points_repeat:
        hand_name = "Four of a Kind"
        player_bankroll += bet_size * payoff[hand_name] 
    elif 3 in points_repeat:
        hand_name = "Three of a Kind"
        player_bankroll += bet_size * payoff[hand_name] 
    elif points_repeat.count(2) == 4:
        hand_name = "Two Pair"
        player_bankroll += bet_size * payoff[hand_name] 
    elif 2 in points_repeat:
        hand_name = "Pair"
        player_bankroll += bet_size * payoff[hand_name] 
    elif diff == 4 and max(points_repeat) == 1:
        hand_name = "Straight"
        player_bankroll += bet_size * payoff[hand_name] 
    elif diff == 12 and points[4] == 14:
        check = 0
        for i in range(1, 4):
            check += points[i] - points[i - 1]
            if check == 3:
                hand_name = "Straight"
                player_bankroll += bet_size * payoff[hand_name] 
            else:
                hand_name = "Bad Hand"
                player_bankroll += bet_size * payoff[hand_name]
    else:
        hand_name = "Bad Hand"
        player_bankroll += bet_size * payoff[hand_name]

    print("You have a {}. Your bankroll is now {} coins.".format(hand_name, player_bankroll))
    return player_bankroll

    

   
# Print Welcome Message to Start the Game
print("""
      WELCOME TO Game Zone 
      by: Qasim Shakir
          and
          Huzefa Soni
       """)
rules = """
Here are the rules of the game:
-------------------------------
You start off with 20 coins. 
Before you are dealt a hand, you have to decide how many coins 
you'd like to bet. The maximum bet is 5 coins per hand. 
With each hand, you'll have an opportunity to redraw as many cards 
in your hand as you'd like for no additional charge. If you wind up 
with a winning hand (anything from a pair to a royal flush), you'll 
get your bet back and more. You will receive a prompt with each 
hand asking if you'd like to keep going or if you'd like to stop playing.

Enjoy!
-------------------------------
"""

    

# Function for the Guess the Number game using recursion
def guess_the_number():
    target_number = random.randint(1, 100)
    attempts = 0

    def guess_game(attempts):
        while True:
            try:
                guess = int(input("Guess the number (between 1 and 100): "))
                if 1 <= guess <= 100:
                    break
                else:
                    print("Number out of range. Please enter a number between 1 and 100.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        if guess == target_number:
            print(f"Congratulations! You guessed the number {target_number} in {attempts} attempts.")
        elif guess < target_number:
            print("Too low! Try again.")
            guess_game(attempts + 1)
        else:
            print("Too high! Try again.")
            guess_game(attempts + 1)

    guess_game(attempts)




# Function for the "Rock, Paper, Scissors" game
def rock_paper_scissors():
    options = ["rock", "paper", "scissors"]
    
    while True:
        player_choice = input("Choose Rock, Paper, or Scissors: ").lower()
        if player_choice in options:
            break
        else:
            print("Invalid choice. Please choose Rock, Paper, or Scissors.")

    computer_choice = random.choice(options)

    if player_choice == computer_choice:
        print("It's a tie!")
    elif (
        (player_choice == "rock" and computer_choice == "scissors") or
        (player_choice == "paper" and computer_choice == "rock") or
        (player_choice == "scissors" and computer_choice == "paper")
    ):
        print("You win!")
    else:
        print("You lose!")


# Function to display the menu
def display_menu():
    print("\nMENU:")
    print("1. Play Poker")
    print("2. Play Guess the Number")
    print("3. Rock Paper Scissors")
    print("4. Quit")

# Main function
while True:
    display_menu()
    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        # Poker game
        print("Let's play Poker!\n")
        print(rules)
        # Print start message
        print("Let's get started! Good luck!")

        # Starting Tokens
        player_bankroll = 20

        # While loop for game play 
        while player_bankroll >= 0:
            if player_bankroll == 0:
                print("Looks like your luck has run short. Better luck next time.")
                break
            deck = create_deck()
            shuffle_deck(deck)
            bet_size, player_bankroll = bet(player_bankroll)

            # Draw cards, show hand, redraw, and score the cards
            player_hand = [draw_card(deck) for _ in range(5)]
            show_hand(player_hand)
            redraw(player_hand, deck)
            player_bankroll = score_hand(player_hand, bet_size, player_bankroll)

        

        # Stop condition for the loop 
            stop_yn = input("Do you want to stop playing now? [Y/N]\n").capitalize() 
            if stop_yn == "Y":
                print("Your final winnings today were {} coins. Good luck next time!".format(player_bankroll))
                break
    
    elif choice == "2":
        # Guess the Number game
        print("Let's play Guess the Number!\n")
        guess_the_number()
    elif choice == "3":
        # Rock Paper Scissors
        print("Let's play Rock Paper Scissors!\n")
        rock_paper_scissors()
    elif choice == "4":
        # Quit the game
        print("Thanks for playing! Goodbye.")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
      