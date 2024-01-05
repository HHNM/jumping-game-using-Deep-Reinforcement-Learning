import pygame
import sys 
from pygame.locals import *
from setting import *
import random

from sprites import *

pygame.init()

# Global constants
score_scroll = 0

# clean and fix the game collect ur input in a data struc
# see what needed for CGP 
font = pygame.font.SysFont("Lucia Sans", 30)

clock = pygame.time.Clock()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.font = pygame.font.SysFont('Futura', 30)

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def score(self, scroll):
        global score_scroll
        score_scroll += scroll
        score = score_scroll//10
        pygame.draw.rect(self.screen, 'White', (0, 0, SCREEN_WIDTH, 20))
        self.draw_text("SCORE: " + str(int(score)), font, 'Black', 0, 0)
        
    def run(self):
        platform = Platform(SCREEN_WIDTH//2 -90, SCREEN_HEIGHT -50, 2)
        platform_list = []
        platform_list.append(platform)
        self.player = Player()
        while True:

            scroll = self.player.move(0,platform_list)

            self.screen.fill('BLUE')

            if len(platform_list) < MAX_PLATFORM:
                # platform scale width
                p_w = random.randint(1, 2)
                # define the min and max horizontal position
                x_min = max(0, platform.rect.x - MIN_PLATFORM_LENGTH * p_w - MAX_PLATFORM_GAP)
                x_max = min(SCREEN_WIDTH - MIN_PLATFORM_LENGTH * p_w, platform.rect.x + platform.rect.width+MAX_PLATFORM_GAP)
                # platform position
                p_x = random.uniform(x_min, x_max)
                p_y = platform.rect.y - random.randint(80, 100) 
                
                platform = Platform(p_x, p_y, p_w)
                platform_list.append(platform)

            if self.player.rect.top > SCREEN_HEIGHT:
                break

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.player.get_input()

            
            self.player.draw(self.screen)

            for plat in platform_list:
                plat.draw(self.screen)
                plat.update(platform_list, scroll)

            self.score(scroll)
            pygame.display.update()
            clock.tick(60)



game = Game()
game.run()
