import pygame
import sys 
from pygame.locals import *
from setting import *
import random
import numpy as np
from sprites import *




class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.font = pygame.font.SysFont('Lucia Sans', 30)
        self.clock = pygame.time.Clock()

        self.platform_list = []
        platform = Platform(SCREEN_WIDTH//2 -90, SCREEN_HEIGHT -50, 2)
        self.platform_list.append(platform)

        self.player = Player()
        
        self.nearest_platform = platform
        # The number of platforms the player has jumped so far
        self.jumped_platforms = 0
        # timer variables, restart the game if the player doesn't
        # improve for a specific period of time(300 in our case)
        self.counter = 300
        self.check = 0
        # keep track of the current score and the best one scored 
        # by the player
        self.current_score = 0
        self.best_score = 0
        # Reset the game
        self.reset()


    def draw_text(self, text, text_col, x, y):
        """
        Draw text on the screen
        """
        img = self.font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def game_score(self, scroll):
        """
        Show the current and best score of the best player
        """
        global points
        self.current_score += int(scroll)
        points = self.current_score//10
        # show the current score
        pygame.draw.rect(self.screen, 'White', (0, 0, SCREEN_WIDTH, 20))
        self.draw_text("SCORE: " + str(self.score), 'Black', 0, 0)
        # show the best score so far
        if self.best_score < self.score:
            self.best_score = self.score
        self.draw_text("BEST SCORE: " + str(int(self.best_score)), 'Black', 250, 0)
        return int(points)
    
    def generate_platform(self):
        """
        Randomly generate platforms for the game
        """
        # Generate a random width for the platform
        p_w = random.randint(1, 2)
        
        # define the min and max horizontal position from the
        # first generated platform
        platform = self.platform_list[-1]

        x_min = max(0, platform.rect.x - MIN_PLATFORM_LENGTH * p_w - MAX_PLATFORM_GAP)
        x_max = min(SCREEN_WIDTH - MIN_PLATFORM_LENGTH * p_w, platform.rect.x + platform.rect.width+MAX_PLATFORM_GAP)
        # platform x and y position
        p_x = random.uniform(x_min, x_max)
        p_y = platform.rect.y - random.randint(80, 100) 
        # Create the platform and add it to the list of platforms
        platform = Platform(p_x, p_y, p_w)
        self.platform_list.append(platform)

    def reset(self):
        """
        Restart the game and initialize the player's variables
        to 0
        """
        self.max_score = 0
        self.frame_iteration = 0
        # empty all the current players if any
        # instantiate players
        
        platform = Platform(SCREEN_WIDTH//2 -90, SCREEN_HEIGHT -50, 2)
        self.platform_list.append(platform)

        self.player.kill()
        # Initialize player variables to 0
        self.player = Player()
        self.score = 0
        self.jumped_platforms = 0
        self.platform_list.clear()

        platform = Platform(SCREEN_WIDTH//2 -90, SCREEN_HEIGHT -50, 2)
        self.platform_list.append(platform)



    def play_step(self, action):
        """
        Play the game by taking the action input"action" and returning 
        the reward, the state of the game (game over or not) and the score of the player
        """
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        reward = 0
        game_over = False

        self.screen.fill('BLUE')
        if len(self.platform_list) < MAX_PLATFORM:
            self.generate_platform()

        self.player.draw(self.screen)
        self.player.update(self.platform_list)
        scroll = self.player.move(0, self.platform_list)
        
        self._move(action)
        

        for plat in self.platform_list:
            plat.draw(self.screen)
            plat.update(self.platform_list, scroll)

        

        for j, plat in enumerate(self.platform_list):
            hits = pygame.sprite.collide_rect(self.player, plat)
            if hits:
                if j > self.jumped_platforms:
                    self.jumped_platforms = j
        
        reward = self.jumped_platforms
        
        # If the player falls and disappear from the screen 
        if self.player.rect.top > SCREEN_HEIGHT: 
            reward = -1           
            game_over = True

        # The best score so far
        game_score = self.game_score(scroll)

        # Check if the generation is stuck and doesn't progress
        self.counter -=1
        if self.counter == 0:
            # If the best player score is not progressing for the duration specified
            # penalise the players and create a new generation
            if self.check == game_score:
                game_over = True
                self.counter = 300 
            else:
                # Reset the counter and set the check score to the game score                         
                self.check = game_score
                self.counter = 300 
        pygame.display.update()
        self.clock.tick(60)
        # the player score is the number of platforms jumped
        self.score = self.jumped_platforms
        return reward, game_over, self.score

    def _move(self, action):
        """
        Move the player based on the action received
        """
        if np.array_equal(action, [1, 0, 0]):
            # Jump Left
            self.player.jump = True
            self.player.moving_left = True
            self.player.moving_right = False
        elif np.array_equal(action, [0, 1, 0]):
            # Jump Right
            self.player.jump = True
            self.player.moving_left = False
            self.player.moving_right = True
        else:
            # Jump Up
            self.player.jump = True
            self.player.moving_left = False
            self.player.moving_right = False



                    



