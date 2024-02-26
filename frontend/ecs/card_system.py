import os 
import pygame

rank_to_name_dict = {
    1: "ace", 
    2: "two", 
    3: "three", 
    4: "four", 
    5: "five", 
    6: "six", 
    7: "seven", 
    8: "eight", 
    9: "nine", 
    10: "ten", 
    11: "jack", 
    12: "queen", 
    13: "king"
}

CARD_MAX_WIDTH = 125
CARD_MAX_HEIGHT = 200

def resizeCard(filepath, scale=1):
    image = pygame.image.load(filepath).convert_alpha()
    resized = pygame.transform.scale(image, (CARD_MAX_WIDTH * scale, CARD_MAX_HEIGHT * scale))
    return resized

class Deck: 
    def __init__(self): 
        # Cards should be an array of data type card
        self.cards = []
        self.cardsDict = {}
    
    def create_deck(self):
        # Loop for actual deck
        for suit in ["hearts", "diamonds", "clubs", "spades"]:
            for rank in range(1, 14):
                card = Card(rank, suit, self.cardsDict[rank_to_name_dict[rank] + "_" + suit])
                self.cards.append(card)
        
        return self.cards
    
    def load_images(self):
        cards = {}
        for suit in ["hearts", "diamonds", "clubs", "spades"]:
            suit_path = os.path.join("frontend/assets/suits", suit + ".jpg")

            for rank in range(1, 14):
                num = f"{rank_to_name_dict[rank]}.jpg"
                num_path = os.path.join("frontend/assets/numbers", num)

                if os.path.exists(num_path) and os.path.exists(suit_path):
                    cards[rank_to_name_dict[rank] + "_" + suit] = [resizeCard(num_path), resizeCard(suit_path)]
                else: 
                    print("Card Image Error for: " + num_path + " and " + suit_path)
        
        self.cardsDict = cards

class Card:
    def __init__(self, rank, suit, images):
        self.rank = rank 
        self.suit = suit
        self.images = images
        self.shown = True

    def createCard(self, x, y, screen, scale=1): 
        radius = 10
        scaling_const = 3.5
        suit_offset = scaling_const * 2.5

        cardSurface = pygame.Surface((CARD_MAX_WIDTH * scale, CARD_MAX_HEIGHT * scale), pygame.SRCALPHA) 
        if self.shown == True: 
            pygame.draw.rect(cardSurface, (255, 255, 255), cardSurface.get_rect(), border_radius=radius)
            rankImg = pygame.transform.scale(self.images[0], (CARD_MAX_WIDTH / scaling_const, CARD_MAX_HEIGHT / scaling_const))
            suitImg = pygame.transform.scale(self.images[1], (CARD_MAX_WIDTH / scaling_const, CARD_MAX_HEIGHT / (scaling_const + 1)))

            cardSurface.blits((
                (rankImg, (radius / 2, radius / 2)), 
                (suitImg, (rankImg.get_width() + radius / 4, suit_offset + radius / 2)),
            ))
            
        else: 
            cardBack = resizeCard("frontend/assets/card_back.png", scale=0.75)
            cardSurface.blit(cardBack, (0, 0))

        screen.blit(cardSurface, (x, y))
        
    def get_card_value(self):
        return self.rank
