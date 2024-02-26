import pygame

# Consts; these will be set via config
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
gameName = "Blackjack"
x_spacing = 105
y_spacing = 50
button_width = 100
button_height = 50
x_card = 50
y_card = 150
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (210, 210, 210)
GREEN = (0, 128, 0)
HOVER_GREEN = (0, 64, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Render Text 
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Button Class
class Button: 
    def __init__(self, x, y, width, height, text, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = None
        self.width = width 
        self.height = height
        self.buttonSurface = pygame.Surface((width, height)) 
        self.font_size = font_size

        self.fillColors = {
            'normal': GREEN, 
            'hover': HOVER_GREEN, 
            'pressed': BLACK
        }

    def draw(self, screen):
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, BLACK)
        self.buttonSurface.blit(text_surface, [
            self.rect.width/2 - text_surface.get_rect().width/2,
            self.rect.height/2 - text_surface.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.rect)

    def setAction(self, func): 
        self.action = func

    def handle_event(self, event):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.rect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.action != None:
                    # Pass in button function args here
                    self.action(self.text) 
                    # Will also have to set game effect and game action state here


class GameOver: 
    def __init__(self, font_size, winner, loser, width, height, is_tie):
        self.font_size = font_size
        self.winner = winner
        self.loser = loser
        self.textSurface = pygame.Surface((width, height))
        self.width = width
        self.height = height
        self.is_tie = is_tie

    def drawEndScene(self, screen):
        font = pygame.font.Font(None, self.font_size)

        winner_str = self.winner 
        if (not self.is_tie): 
            winner_str += " is the winner!"
        winner_text = font.render(winner_str, True, WHITE)
        winner_rect = winner_text.get_rect(center = (self.width / 2, self.height / 2 - 50))
        
        loser_str = self.loser
        if (not self.is_tie): 
            loser_str += " lost. Woof."
        loser_text = font.render(loser_str, True, WHITE)
        loser_rect = loser_text.get_rect(center = (self.width / 2, self.height / 2))

        self.textSurface.blit(winner_text, winner_rect)
        self.textSurface.blit(loser_text, loser_rect)
        screen.blit(self.textSurface, (0, 0))

class Turn:
    def __init__(self, font_size, text, width, height, x, y):
        self.font_size = font_size
        self.text = text
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.textSurface = pygame.Surface((width, height))

    def drawTurnMarker(self, screen):
        font = pygame.font.Font(None, self.font_size)
        self.textSurface.fill(GREY)

        turn_str = self.text
        turn_text = font.render(turn_str, True, BLACK)
        turn_rect = turn_text.get_rect()

        self.textSurface.blit(turn_text, turn_rect)
        screen.blit(self.textSurface, (self.x, self.y))


