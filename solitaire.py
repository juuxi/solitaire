#Косынка
import pygame, random, games, cards

class Solitaire_card(pygame.sprite.Sprite, cards.Card):

    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", \
             "J", "Q", "K"]
    SUITS = ["c", "d", "h", "s"]

    def __init__(self, rank, suit):
        cards.Card(rank, suit)
        self.image = pygame.image.load("Cards/" + str(rank) + str(suit) + ".png")
        self.rect = self.image.get_rect()

class Solitaire_hand(cards.Hand):
    def add(self, card):
        self.cards.append(card)

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
    pygame.display.set_caption("Solitaire")
    main_deck = cards.Deck()
    main_deck.populate()
    main_deck.shuffle()
    first_deck = Solitaire_hand()
    #main_deck.deal([first_deck])
    first_deck.add(Solitaire_card("2", "h"))
    running = True
    while running:
        for card in first_deck.cards:
            screen.blit(card.image, (screen.get_width()/2, screen.get_height()/2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    
        pygame.display.update()   
        Time_var.tick(FPS)     
    pygame.quit()

main()