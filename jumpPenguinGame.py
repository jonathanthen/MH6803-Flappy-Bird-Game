import sys
import pygame
import random
from pygame.locals import *
import flyPenguinGame

# INITIALIZE MODULES
pygame.init()
framepersecond_clock = pygame.time.Clock()

# GAME WINDOW SETTINGS
screen_width, screen_height = 696, 522
window = pygame.display.set_mode((screen_width, screen_height))   
elevation = screen_height * 0.8

# IMAGE SETTINGS
game_images = {}      
framepersecond = 60

# SOUNDS
flap_fx = pygame.mixer.Sound('images/birdflap.wav')
die_fx = pygame.mixer.Sound('images/die.wav')
hurt_fx = pygame.mixer.Sound('images/hurt.wav')

# FONT SETTINGS
myFont = pygame.font.SysFont('Raleway', 40, bold=True, italic=True)
black=(0,0,0)

# MAIN GAME FUNCTION
def game():
    score = 0
    health = 3
    horizontal = int(screen_width/6)
    vertical = int((screen_height - game_images['penguin'].get_height())/2)

    lastFrame = pygame.time.get_ticks()
    obsX = screen_width # need to randomly
    ice_X = screen_width + 400
    obsY = elevation - game_images['lodge'].get_height()
    ice_Y = elevation - game_images['iceberg'].get_height()
    collision_immune = False
    collision_time = 0

    # PENGUIN VELOCITY
    penguin_velocity_y = 0

    while True:

        t = pygame.time.get_ticks() # get the time in milliseconds
        deltaTime = (t-lastFrame)/1000.0 # Find difference in time and then convert it to seconds
        lastFrame = t # set lastFrame as the current time for next frame.

        window.blit(game_images['background'], (0, 0))
        window.blit(game_images['icefloor'], (0, elevation))
        window.blit(game_images['penguin'], (horizontal, vertical))
        window.blit(game_images['heart'], (20,20))
         
        # KEY PRESSES WHILE IN GAME
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical == elevation-20:
                    flap_fx.play()
                    penguin_velocity_y = -600

        # COLLISION IMMUNITY
        if pygame.time.get_ticks() - collision_time > 1500:
            collision_immune = False
        else:
            window.blit(game_images['shield'], (horizontal-20, vertical-40))
            window.blit(game_images['penguin'], (horizontal, vertical))

        # PENGUIN MOVEMENT
        penguin_velocity_y += 17 # Simulates Gravity
        vertical += penguin_velocity_y * deltaTime

        if vertical > elevation-20: # Sets user back to ground level if drops below ground
            vertical = elevation-20
            penguin_velocity_y = elevation

        # OBSTACLE MOVEMENT
        obsX -= 280 * deltaTime
        ice_X -= 280 * deltaTime
        if 3<= score <10:
             obsX -= 25 * deltaTime
             ice_X -= 25 * deltaTime
        elif 10<= score <20:
              obsX -= 50 * deltaTime
              ice_X -= 50 * deltaTime
        elif 20 <= score:
              obsX -= 100 * deltaTime
              ice_X -= 100 * deltaTime

        window.blit(game_images['lodge'], (obsX, obsY))
        window.blit(game_images['iceberg'], (ice_X, ice_Y))

        if obsX < - game_images['lodge'].get_width():
            score += 1
            obsX = screen_width

        if ice_X < - game_images['iceberg'].get_width():
            score += 1
            ice_X = obsX + random.randrange(350, 480)

        # COLLISION FUNCTION
        if ((vertical + game_images['penguin'].get_height() > obsY or vertical + game_images['penguin'].get_height() > ice_Y) and collision_immune == False):
            if (obsX < horizontal < obsX + game_images['lodge'].get_width() or ice_X < horizontal < ice_X + game_images['iceberg'].get_width()):
                collision_immune = True
                health -= 1
                collision_time = pygame.time.get_ticks()
                if health != 0:
                    hurt_fx.play()

        health_font = myFont.render(str(health), True, (255, 255, 255))
        window.blit(health_font, (55, 20.1))

        # GAME OVER
        if collision_immune == True and health == 0:
            game_over(score)
            return

        # Score Display
        score_font = pygame.font.SysFont('Raleway', 64)
        score_txt = score_font.render(str(score), True, black)
        scoreRect = score_txt.get_rect()
        scoreRect.center = [screen_width * 0.9, screen_height - 480]
        window.blit(score_txt, scoreRect)

        pygame.display.update()
        framepersecond_clock.tick(framepersecond)


def game_start(x, y):

    while True:
        window.blit(game_images['background'], (0, 0))
        window.blit(game_images['penguin'], (horizontal, vertical))
        window.blit(game_images['title'], (45, 100))
        window.blit(game_images['instructions'], (100, screen_height // 2 + 50))
        window.blit(game_images['lodge'], (600, 318))
        window.blit(game_images['iceberg'], (20, 318))
        window.blit(game_images['icefloor'], (0, elevation))

        for event in pygame.event.get():
            # USER CLICKS ON ESCAPE KEY - GAME CLOSES
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                # EXIT PROGRAM
                sys.exit()

                # SPACE KEY TO START - GAME STARTS
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                game()

            # If the user presses other keys
            elif event.type == KEYDOWN:
               flyPenguinGame.handleInvalidKey()

            # STARTING SCREEN
            else:
                # REFRESHES THE SCREEN
                pygame.display.update()
                # SET RATE OF FRAME PER SECOND
                framepersecond_clock.tick(framepersecond)


def game_over(final_score):
    die_fx.play()
    font = pygame.font.SysFont('Raleway', 70, bold=True, italic=True)  # use to display text on the screen
    snd_font = pygame.font.SysFont('None', 35, italic=True)
    third_font = pygame.font.SysFont('Raleway', 30)
    text = font.render("Game Over", True, (255, 255, 255))
    snd_txt = snd_font.render("Please press space or up keyboard to restart ~", True, black)
    third_txt = third_font.render('Your final score: ' + str(final_score), True, black)
    textRect = text.get_rect()
    textRect_snd = snd_txt.get_rect()
    textRect_third = third_txt.get_rect()
    textRect.center = [screen_width / 2, screen_height / 2 - 50]
    textRect_snd.center = [screen_width / 2 + 2, screen_height / 2 + 5]
    textRect_third.center = [screen_width - 100, 20]
    window.blit(text, textRect)
    window.blit(snd_txt, textRect_snd)
    window.blit(third_txt, textRect_third)


# MAIN GAME
if __name__ == "__main__":
    # Initializing pygame module
    pygame.init()
    framepersecond_clock = pygame.time.Clock()

    # GAME TITLE & IMAGES
    pygame.display.set_caption('Jump Penguin')

    game_images['background'] = pygame.image.load('images/background.jpg').convert_alpha()
    game_images['penguin'] = pygame.image.load('images/penguin.png').convert_alpha()
    game_images['title'] = pygame.image.load("images/title.png").convert_alpha()
    game_images['instructions'] = pygame.image.load("images/instructions.png").convert_alpha()
    game_images['icefloor'] = pygame.image.load("images/icefloor.jpg").convert_alpha()
    game_images['lodge'] = pygame.image.load("images/lodge.png").convert_alpha()
    game_images['iceberg'] = pygame.image.load("images/iceberg.png").convert_alpha()
    game_images['heart'] = pygame.image.load("images/heart.png").convert_alpha()
    game_images['shield'] = pygame.image.load("images/shield.png").convert_alpha()

    # SET COORDINATE OF PLAYER
    horizontal = int(screen_width / 6)
    vertical = int((screen_height - game_images['penguin'].get_height()) / 2)
    game_start(horizontal, vertical)
