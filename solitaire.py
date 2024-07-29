#Косынка
import pygame, random, games, cards

class Solitaire_card(pygame.sprite.Sprite, cards.Card):

    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", \
             "J", "Q", "K"]
    SUITS = ["c", "d", "h", "s"]

    def __init__(self, rank, suit, face_up = True):
        cards.Card(rank, suit)
        self.is_face_up = face_up
        self.image = pygame.image.load("Cards/" + str(rank) + str(suit) + ".png")
        self.rect = self.image.get_rect()

class Solitaire_hand(cards.Hand):
    def __init__(self, deck_num):
        cards.Hand.__init__(self)
        self.width = 100 + (deck_num - 1) * 125

class Solitaire_deck(cards.Deck):
    def populate(self):
        for suit in Solitaire_card.SUITS:
            for rank in Solitaire_card.RANKS:
                self.add(Solitaire_card(rank, suit))

def main():
    pygame.init()
    FPS = 50
    Time_var = pygame.time.Clock()
    screen = pygame.display.set_mode()
    MAIN_HEIGHT = screen.get_height()/4
    pygame.display.set_caption("Solitaire")
    main_deck = cards.Deck()
    main_deck.populate()
    main_deck.shuffle()
    first_deck = Solitaire_hand(1)
    second_deck = Solitaire_hand(2)
    third_deck = Solitaire_hand(3)
    forth_deck = Solitaire_hand(4)
    fifth_deck = Solitaire_hand(5)
    sixth_deck = Solitaire_hand(6)
    decks = [first_deck, second_deck, third_deck, forth_deck, fifth_deck, sixth_deck]
    #main_deck.deal([first_deck])
    for deck in decks:
        deck.add(Solitaire_card("2", "h"))
        if deck != first_deck:
            deck.cards[0].flip()
    running = True
    while running:
        for deck in decks:
            for card in deck.cards:
                screen.blit(card.image, (deck.width, MAIN_HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    
        pygame.display.update()   
        Time_var.tick(FPS)     
    pygame.quit()

main()