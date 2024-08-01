#Косынка
import pygame, random, games, cards
from pygame.locals import *

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

    def get_image (self):
        if self.is_face_up:
            self.image = pygame.image.load("Cards/" + str(self.rank) + str(self.suit) + ".png")
        else:
            self.image = pygame.image.load("Cards/XX.png")
        return self.image

class Solitaire_hand(cards.Hand):
    def __init__(self, deck_num):
        cards.Hand.__init__(self)
        self.deck_num = deck_num
        self.width = 150 + (deck_num - 1) * 150

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

def decks_population(decks, main_deck, MAIN_HEIGHT, FACE_UP_DOWN_HEIGHT):
    for deck in decks[:7]:
        for i in range(0, deck.deck_num):    
            if (i == deck.deck_num-1 and i != 0):
                main_deck.cards[0].flip()
            main_deck.deal([deck])
            #change rect.x and rect.y of last card in list
            deck.cards[-1].rect.x = deck.width + deck.cards.index(deck.cards[-1])*2 
            deck.cards[-1].rect.y = MAIN_HEIGHT + (deck.cards.index(deck.cards[-1]))*15
    to_ret = 0
    while (not to_ret):
        if (main_deck.cards):
            main_deck.cards[0].flip()
        to_ret = main_deck.deal([decks[6]])
        decks[6].cards[-1].rect.x = decks[6].width
        decks[6].cards[-1].rect.y = FACE_UP_DOWN_HEIGHT
    for deck in decks[7:]:
        deck.add(Solitaire_card("Bla", "nk"))
    for deck in decks[1:6]:
        for card in deck.cards:
            card.flip()

def main():
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont("Times New Roman", 20)
    all_sprites = pygame.sprite.Group()
    FPS = 50
    Time_var = pygame.time.Clock()
    screen = pygame.display.set_mode()
    MAIN_HEIGHT = screen.get_height()/4 + screen.get_height()/16
    FACE_UP_DOWN_HEIGHT = screen.get_height()/8
    SUIT_HEIGHT = screen.get_height()/2 + screen.get_height()/8
    screen.fill([255,255,255])
    pygame.display.set_caption("Solitaire")
    main_deck = Solitaire_deck()
    main_deck.populate()
    for card in main_deck.cards:
        all_sprites.add(card)
    main_deck.shuffle()
    first_deck = Solitaire_hand(1)
    second_deck = Solitaire_hand(2)
    third_deck = Solitaire_hand(3)
    forth_deck = Solitaire_hand(4)
    fifth_deck = Solitaire_hand(5)
    sixth_deck = Solitaire_hand(6)
    #2 decks that are higher than main
    face_down_deck = Solitaire_hand(1)
    face_up_deck = Solitaire_hand (5)
    #4 decks for each suit
    hearts_deck = Solitaire_hand(2)
    diamonds_deck = Solitaire_hand(3)
    clubs_deck = Solitaire_hand(4)
    spades_deck = Solitaire_hand(5)
    decks = [first_deck, second_deck, third_deck, forth_deck, fifth_deck, sixth_deck, \
             face_down_deck, face_up_deck, hearts_deck, diamonds_deck, clubs_deck, spades_deck]
    decks_population(decks, main_deck, MAIN_HEIGHT, FACE_UP_DOWN_HEIGHT)
    running = True
    while running:
        for deck in decks[:6]:
            for card in deck.cards:
                screen.blit(card.get_image(), (deck.width + (deck.cards.index(card))*2, MAIN_HEIGHT + (deck.cards.index(card))*15))
        for deck in decks[6:8]:
            for card in deck.cards:
                screen.blit(card.get_image(), (deck.width, FACE_UP_DOWN_HEIGHT))
        for deck in decks[8:]:
            for card in deck.cards:
                screen.blit(card.get_image(), (deck.width, SUIT_HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    
            if event.type == MOUSEBUTTONDOWN:
                for deck in decks:
                    for card in deck.cards:
                        if card.rect.collidepoint(event.pos):
                            text_surface = my_font.render('Some Text', False, (0, 0, 0))
                            screen.blit(text_surface, (screen.get_width()/2, 0))
        pygame.display.update()   
        Time_var.tick(FPS)     
    pygame.quit()

main()