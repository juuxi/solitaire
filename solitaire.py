#Косынка
import pygame, random, games, cards
from pygame.locals import *

pygame.init()
all_sprites = pygame.sprite.Group()
screen = pygame.display.set_mode()
MAIN_HEIGHT = screen.get_height()/4 + screen.get_height()/16
FACE_UP_DOWN_HEIGHT = screen.get_height()/8
SUIT_HEIGHT = screen.get_height()/2 + screen.get_height()/8

class Solitaire_card(pygame.sprite.Sprite, cards.Card):

    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", \
             "J", "Q", "K"]
    SUITS = ["c", "d", "h", "s"]

    def __init__(self, rank, suit, face_up = True):
        pygame.sprite.Sprite.__init__(self)
        self.rank = rank
        self.suit = suit
        self.is_face_up = face_up
        self.image = pygame.image.load("Cards/" + str(rank) + str(suit) + ".png")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.moving = False

    def get_image (self):
        if self.is_face_up:
            self.image = pygame.image.load("Cards/" + str(self.rank) + str(self.suit) + ".png")
        else:
            self.image = pygame.image.load("Cards/XX.png")
        return self.image

class Solitaire_hand(cards.Hand):
    def __init__(self, deck_num, height):
        cards.Hand.__init__(self)
        self.deck_num = deck_num
        self.width = 150 + (deck_num - 1) * 150
        self.height = height
    
    def give(self, card, other_hand):
        if other_hand.cards[0].rank == "Bla":
            other_hand.cards[0].kill()
            other_hand.clear()
        other_hand.add(card)
        self.cards.remove(card)
        if not self.cards:
            self.add(Solitaire_card("Bla", "nk"))
            self.cards[0].rect.x = self.width
            self.cards[0].rect.y = self.height
            all_sprites.add(self.cards[0])
        else:
            self.flip_main()

    def flip_main(self):
        if self.height == MAIN_HEIGHT:
            self.cards[-1].is_face_up = True

class Solitaire_deck(cards.Deck):
    def populate(self):
        for suit in Solitaire_card.SUITS:
            for rank in Solitaire_card.RANKS:
                self.add(Solitaire_card(rank, suit))

    def deal(self, hands, per_hand = 1):
        for rounds in range(per_hand):
            for hand in hands:
                if self.cards:
                    top_card = self.cards[0]
                    self.give(top_card, hand)
                    return 0
                else:
                    return 1

def decks_population(decks, main_deck, screen, all_sprites):
    populate_main(decks, main_deck)
    populate_up_down(decks, main_deck)
    populate_with_blank(decks)
    for deck in decks[1:6]:
        for card in deck.cards:
            card.flip()

def populate_main(decks, main_deck):
    for deck in decks[:6]:
        for i in range(0, deck.deck_num):    
            if (i == deck.deck_num-1 and i != 0):
                main_deck.cards[0].flip()
            main_deck.deal([deck])
            deck.cards[-1].rect.x = deck.width + deck.cards.index(deck.cards[-1])*2 
            deck.cards[-1].rect.y = MAIN_HEIGHT + (deck.cards.index(deck.cards[-1]))*15

def populate_up_down(decks, main_deck):
    to_ret = 0
    while (not to_ret):
        if (main_deck.cards):
            main_deck.cards[0].flip()
        to_ret = main_deck.deal([decks[6]])
        decks[6].cards[-1].rect.x = decks[6].width
        decks[6].cards[-1].rect.y = FACE_UP_DOWN_HEIGHT

def populate_with_blank(decks):
    for deck in decks[7:]:
        deck.add(Solitaire_card("Bla", "nk"))
        all_sprites.add(deck.cards[-1])
        deck.cards[-1].rect.x = deck.width
        if deck in decks[8:]:
            deck.cards[-1].rect.y = SUIT_HEIGHT
        else: 
            deck.cards[-1].rect.y = FACE_UP_DOWN_HEIGHT

def is_near_deck(card, decks):
    for deck in decks:
        if not deck.cards[-1].moving:
            if card.rect.x in range(deck.cards[-1].rect.x - 10, deck.cards[-1].rect.x + 11):
                return True, deck.deck_num
    return False, 0

def blit_decks(decks):
    for deck in decks[:6]:
            for card in deck.cards:
                screen.blit(card.get_image(), (card.rect.x, card.rect.y))
    for deck in decks[6:8]:
        for card in deck.cards:
            screen.blit(card.get_image(), (card.rect.x, card.rect.y))
    for deck in decks[8:]:
        for card in deck.cards:
            screen.blit(card.get_image(), (card.rect.x, card.rect.y))

def deal_to_closest(card, deck, decks, num_of_deck, was_x, was_y):
    for check_deck in decks[:6]:
        if card.rect.y in range(int(check_deck.height), int(check_deck.height) + len(check_deck.cards)*15 + 20):
            deal_to_main(card, deck, decks, num_of_deck, was_x, was_y)
            return

    if card.rect.y in range(int(SUIT_HEIGHT)-20, int(SUIT_HEIGHT)+21):
        deal_to_suits(card, deck, decks, num_of_deck, was_x, was_y)
        return
    else:
        card.rect.x, card.rect.y = was_x, was_y

def deal_to_main(card, deck, decks, num_of_deck, was_x, was_y):
    for give_deck in decks[0:6]:
        if give_deck.width == 150 + (num_of_deck - 1) * 150:
            if is_dealable_main(card, give_deck):
                for cards in deck.cards[deck.cards.index(card):]:
                    deck.give(cards, give_deck)
                    cards.rect.x = give_deck.width + give_deck.cards.index(cards)*2 
                    cards.rect.y = MAIN_HEIGHT + (give_deck.cards.index(cards))*15  
                    cards.moving = False
            else:
                if deck in decks[:6]:
                    for back_cards in deck.cards[deck.cards.index(card):]:
                            back_cards.rect.x = deck.width + deck.cards.index(back_cards)*2 
                            back_cards.rect.y = MAIN_HEIGHT + (deck.cards.index(back_cards))*15  
                            back_cards.moving = False
                else:
                    card.rect.x, card.rect.y = was_x, was_y  

def is_dealable_main(card, give_deck):
    blacks = ["c", "s"]
    reds = ["h", "d"]
    if card.rank == "A":
        return False
    if give_deck.cards[0].rank == "Bla":
        if card.rank == "K":
            return True
        else:
            return False
    if card.suit in blacks and give_deck.cards[-1].suit in blacks:
        return False
    if card.suit in reds and give_deck.cards[-1].suit in reds:
        return False
    if card.RANKS.index(card.rank) == card.RANKS.index(give_deck.cards[-1].rank) - 1:
        return True
    return False

def deal_to_suits(card, deck, decks, num_of_deck, was_x, was_y):
    if num_of_deck == 2 and is_dealable_suits(card, decks[8]):
        deck.give(card, decks[8])
        card.rect.x = decks[8].width
        card.rect.y = SUIT_HEIGHT
    elif num_of_deck == 3 and is_dealable_suits(card, decks[9]):
        deck.give(card, decks[9])
        card.rect.x = decks[9].width
        card.rect.y = SUIT_HEIGHT
    elif num_of_deck == 4 and is_dealable_suits(card, decks[10]):
        deck.give(card, decks[10])
        card.rect.x = decks[10].width
        card.rect.y = SUIT_HEIGHT
    elif num_of_deck == 5 and is_dealable_suits(card, decks[11]):
        deck.give(card, decks[11])
        card.rect.x = decks[11].width
        card.rect.y = SUIT_HEIGHT
    else:
        card.rect.x, card.rect.y = was_x, was_y

def is_dealable_suits(card, give_deck):
    if card.rank == "A":
        return True
    if card.suit != give_deck.cards[-1].suit:
        return False
    if card.RANKS.index(card.rank) == card.RANKS.index(give_deck.cards[-1].rank) + 1:
        return True
    return False

def is_win(decks):
    if len(decks[8].cards) == 13 and len(decks[9].cards) == 13:
        if len(decks[10].cards) == 13 and len(decks[11].cards) == 13:
            return True
    return False

def deal_up_down(event, card, decks, to_face_up):
    if card.rect.collidepoint(event.pos) and to_face_up == True:
            if (decks[6].cards[0].rank != "Bla"):
                card.is_face_up = True 
                card.rect.x = decks[7].width   
                decks[6].give(card, decks[7])  
            else:
                while decks[7].cards[0].rank != "Bla":
                    decks[7].cards[0].is_face_up = False
                    decks[7].cards[0].rect.x = decks[6].width   
                    decks[7].give(decks[7].cards[0], decks[6])  

def main():
    pygame.font.init()
    my_font = pygame.font.SysFont("Times New Roman", 20)
    FPS = 50
    Time_var = pygame.time.Clock()
    screen.fill([150,255,255])
    pygame.display.set_caption("Solitaire")
    main_deck = Solitaire_deck()
    main_deck.populate()
    for card in main_deck.cards:
        all_sprites.add(card)
    main_deck.shuffle()
    first_deck = Solitaire_hand(1, MAIN_HEIGHT)
    second_deck = Solitaire_hand(2, MAIN_HEIGHT)
    third_deck = Solitaire_hand(3, MAIN_HEIGHT)
    forth_deck = Solitaire_hand(4, MAIN_HEIGHT)
    fifth_deck = Solitaire_hand(5, MAIN_HEIGHT)
    sixth_deck = Solitaire_hand(6, MAIN_HEIGHT)
    #2 decks that are higher than main
    face_down_deck = Solitaire_hand(1, FACE_UP_DOWN_HEIGHT)
    face_up_deck = Solitaire_hand (5, FACE_UP_DOWN_HEIGHT)
    #4 decks for each suit
    hearts_deck = Solitaire_hand(2, SUIT_HEIGHT)
    diamonds_deck = Solitaire_hand(3, SUIT_HEIGHT)
    clubs_deck = Solitaire_hand(4, SUIT_HEIGHT)
    spades_deck = Solitaire_hand(5, SUIT_HEIGHT)
    decks = [first_deck, second_deck, third_deck, forth_deck, fifth_deck, sixth_deck, \
             face_down_deck, face_up_deck, hearts_deck, diamonds_deck, clubs_deck, spades_deck]
    decks_population(decks, main_deck, screen, all_sprites)
    running = True
    was_x = None
    was_y = None
    to_face_up = False
    while running:
        screen.fill([155, 255, 255]) 
        blit_decks(decks)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    
            elif event.type == MOUSEBUTTONDOWN:
                for deck in decks[6:]:
                    if (to_face_up):
                        break
                    for card in deck.cards:
                        to_face_up = False
                        if card.rect.collidepoint(event.pos) and deck == decks[6]:
                            to_face_up = True
                            break
                        if card.rect.collidepoint(event.pos) and card.is_face_up and card.rank != "Bla":
                            if (deck == face_up_deck or deck in decks[8:]):
                                if card != deck.cards[-1]:
                                    continue
                            if deck == face_up_deck:
                                card.moving = True
                                was_x = card.rect.x
                                was_y = card.rect.y
                for deck in decks[:6]:
                    for card in reversed(deck.cards):
                        if card.rect.collidepoint(event.pos) and deck.cards[-1].moving == False:
                            for cards in deck.cards[deck.cards.index(card):]:
                                cards.moving = True
                            was_x = card.rect.x
                            was_y = card.rect.y

            elif event.type == MOUSEBUTTONUP:
                for deck in decks:
                    for card in deck.cards:
                        if(card.moving):
                            is_near, num_of_deck = is_near_deck(card, decks)
                            card.moving = False
                            if not is_near:
                                if deck in decks[:6]:
                                    for back_cards in deck.cards[deck.cards.index(card):]:
                                            back_cards.rect.x = deck.width + deck.cards.index(back_cards)*2 
                                            back_cards.rect.y = MAIN_HEIGHT + (deck.cards.index(back_cards))*15  
                                            back_cards.moving = False
                                else:
                                    card.rect.x, card.rect.y = was_x, was_y
                            else:
                                deal_to_closest(card, deck, decks, num_of_deck, was_x, was_y)
                        elif deck == decks[6] and to_face_up:
                            deal_up_down(event, card, decks, to_face_up)
                            to_face_up = False

            elif event.type == MOUSEMOTION:
                for deck in decks:
                    for card in deck.cards:
                        if(card.moving):
                            card.rect.move_ip(event.rel)
        if (is_win(decks)):
            text_surface = my_font.render('You won!', False, (0, 0, 0))
            screen.blit(text_surface, (screen.get_width()/2, 0))
        pygame.display.update()   
        Time_var.tick(FPS)     
    pygame.quit()

main()