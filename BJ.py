import sys
import random
from colorama import Fore, Back, Style, init
init(autoreset=True)

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

# CLASSES

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_has = ''
        for card in self.deck:
            deck_has += '\n' + card.__str__()
        return 'The deck has:' + deck_has

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Money:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total = self.total + self.bet

    def lose_bet(self):
        self.total = self.total - self.bet

# FUNCTIONS

def take_bet(money):
    while True:
        try:
            money.bet = int(input('Make a bet:\n'))
        except ValueError:
            print(Fore.RED + 'Sorry, a bet must be an integer!')
        else:
            if money.bet > money.total:
                print(Fore.RED + 'Not enough money')
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.for_ace()

def hit_or_stand(deck,hand):
    global playing

    while True:
        x = input('Would you like to hit or stand? Enter "H" or "S"\n')

        if x[0].lower() == 'h':
            hit(deck,hand)

        elif x[0].lower() == 's':
            print('Player is stand. Dealer is playing')
            playing = False

        else:
            print('Incorrect value. Please enter "H" or "S" to continue')
            continue
        break

def show_some(player, dealer):
    print("\nDealer's hand:")
    print('///card hidden///')
    print(dealer.cards[1])
    print("\nPlayer's hand", *player.cards, sep = '\n')

def show_all(player, dealer):
    print("\nDealer's hand:", *dealer.cards, sep ='\n')
    print("Dealer's hand =", dealer.value)
    print("\nPlayer's hand:", *player.cards, sep = '\n')
    print("Player's hand = ", player.value)

def player_busts(player, dealer, money):
    print(Fore.RED + '\nPlayer busts!')
    money.lose_bet()

def player_wins(player, dealer, money):
    print(Fore.GREEN + '\nPlayer win!')
    money.win_bet()

def dealer_busts(player, dealer, money):
    print(Fore.GREEN +'\nDealer busts!')
    money.win_bet()

def dealer_wins(player, dealer, money):
    print(Fore.RED +'\nDealer wins!')
    money.lose_bet()

def push(player, dealer):
    print(Fore.BLUE + '\nDealer and Player tie!')

def wrong_rerun():
    while True:
        rerun = input(Fore.YELLOW + 'Would you like to play again? Enter Y or N\n')
        if rerun[0].upper() == 'Y':
            break
        elif rerun[0].upper() == 'N':
            sys.exit(Fore.CYAN + 'Thank you for playing! We hope to see you again soon!')
        else:
            continue

# THE ENTIRE GAME

player_money = Money()

print(Fore.YELLOW + 'Welcome to Black Jack game!')
print('Your start bank is ' + str(player_money.total))

while True:

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    take_bet(player_money)

    show_some(player_hand,dealer_hand)

    while playing:

        hit_or_stand(deck,player_hand)

        show_some(player_hand,dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_money)

        elif player_hand.value == 21:
            print(Fore.RED + Style.BRIGHT + '\nBlack Jack!')
            player_wins(player_hand,dealer_hand,player_money)
        break

    if player_hand.value < 21:

        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        show_all(player_hand,dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_money)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_money)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_money)
        else:
            push(player_hand,dealer_hand)

    print("\nPlayer's value is ", player_money.total)

    if player_money.total > 0:
        rerun = input(Fore.YELLOW + 'Would you like to play again? Enter Y or N\n')
        if rerun[0].upper() != 'Y' and rerun[0].upper() != 'N':
            wrong_rerun()
        else:
            if rerun[0].upper() == 'Y':
                playing = True
                continue
            elif rerun[0].upper() == 'N':
                print(Fore.CYAN + 'Thank you for playing! We hope to see you again soon!')
                break
    else:
        print(Fore.RED + 'You lost all your money as always, ahahhah')
        break