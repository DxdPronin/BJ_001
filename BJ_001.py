from random import shuffle
from dataclasses import dataclass

@dataclass
class Card:
    suit: str
    rank: str

class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

    def __init__(self):
        self.deck = []
        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(Card(suit, rank))

    def shuffle_deck(self):
        shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

@dataclass
class Player:
    name: str
    hand: list
    chips: int

    def add_card(self, card):
        self.hand.append(card)

    def calculate_hand_value(self):
        hand_value = 0
        aces = 0
        for card in self.hand:
            if card.rank == 'Ace':
                aces += 1
                hand_value += 11
            elif card.rank in ['Jack', 'Queen', 'King']:
                hand_value += 10
            else:
                hand_value += int(card.rank)
        while hand_value > 21 and aces:
            hand_value -= 10
            aces -= 1
        return hand_value

class BlackJack:
    def __init__(self, player_name, chips):
        self.player = Player(player_name, [], chips)
        self.dealer = Player('Dealer', [], 0)
        self.deck = Deck()
        self.deck.shuffle_deck()

    def reset_game(self):
        self.player.hand = []
        self.dealer.hand = []
        self.deck = Deck()
        self.deck.shuffle_deck()

    def place_bet(self, bet):
        if bet <= self.player.chips:
            self.player.chips -= bet
            self.dealer.chips += bet
            return True
        else:
            return False

    def deal_initial_cards(self):
        for _ in range(2):
            self.player.add_card(self.deck.deal_card())
            self.dealer.add_card(self.deck.deal_card())

    def player_turn(self):
        while self.player.calculate_hand_value() < 21:
            action = input('Would you like to hit or stand? ')
            if action == 'hit':
                self.player.add_card(self.deck.deal_card())
                print(f"{self.player.name}'s hand: {self.player.hand}")
            else:
                break

    def dealer_turn(self):
        while self.dealer.calculate_hand_value() < 17:
            self.dealer.add_card(self.deck.deal_card())
        print(f"Dealer's hand: {self.dealer.hand}")

    def determine_winner(self):
        if self.player.calculate_hand_value() > 21:
            return 'Dealer'
        elif self.dealer.calculate_hand_value() > 21:
            return self.player.name
        elif self.player.calculate_hand_value() > self.dealer.calculate_hand_value():
            return self.player.name
        elif self.dealer.calculate_hand_value() > self.player.calculate_hand_value():
            return 'Dealer'
        else:
            return 'Push'

class Simulation:
    def __init__(self):
        self.games_played = 0
        self.total_chips = 0

    def play_game(self):
        print('Welcome to BlackJack!')
        player_name = input('What is your name? ')
        starting_chips = int(input('How many chips would you like to start with? '))
        game = BlackJack(player_name, starting_chips)  #


        while True:
            bet = int(input(f"You have {game.player.chips} chips. How much would you like to bet? "))
            if game.place_bet(bet):
                game.reset_game()
                game.deal_initial_cards()
                print(f"{game.player.name}'s hand: {game.player.hand}")
                print(f"Dealer's hand: [{game.dealer.hand[0]}, *]")
                game.player_turn()
                game.dealer_turn()
                winner = game.determine_winner()
                if winner == game.player.name:
                    print(f"{game.player.name} wins!")
                    game.player.chips += bet * 2
                elif winner == 'Dealer':
                    print("Dealer wins!")
                else:
                    print("Push!")
                    game.player.chips += bet
                self.games_played += 1
                self.total_chips += game.player.chips
                play_again = input("Would you like to play again? (y/n) ")
                if play_again == 'y':
                    continue
                else:
                    break
            else:
                print("Not enough chips. Please place a valid bet.")

        print(f"\n{game.player.name}, you played {self.games_played} games and ended with {self.total_chips} chips.")

if __name__ == '__main__':
    simulation = Simulation()
    simulation.play_game()

