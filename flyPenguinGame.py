# Import module
import random
import sys
import pygame
from pygame.locals import *
import jumpPenguinGame
import time

# GAME WINDOW SETTINGS
W, H = 696, 522
pygame.init()

window = pygame.display.set_mode((W, H)) # Set window based on width and height
# sea level position
# -y
# |
# 0 -------> +x
# |
# |
# |
# +y
elevation = H * 0.82

# FONT SETTINGS
myFont = pygame.font.SysFont("Times New Roman", 30)
black=(0,0,0)

# SOUNDS
flap_fx = pygame.mixer.Sound('images/birdflap.wav')
die_fx = pygame.mixer.Sound('images/die.wav')
hurt_fx = pygame.mixer.Sound('images/hurt.wav')

# IMAGES
game_images = {}
framepersecond = 32
pipeimage = 'images/pipe.png'
background_image = 'images/background.jpg'
penguinplayer_image = 'images/penguin.png'
sealevel_image = 'images/icefloor.jpg'
heart_image = 'images/heart.png'

def game():
    # Initialisation
    score = 0 # score obtained
    health = 3 # total health life

    # Penguin initial position
    horizontal = int(W / 5)
    vertical = int(H / 3)

    # Generating two pipes
    fst_pipe = createPipe()
    snd_pipe = createPipe()

    # List containing upper pipes
    up_pipes = [
        {'x': W + 100, 'y': fst_pipe[0]['y']}, # 'y': the height of fst upper pipe
        {'x': W + 400, 'y': snd_pipe[0]['y']}  # 'y': the height of snd upper pipe
    ]

    # List containing lower pipes
    down_pipes = [
        {'x': W + 100, 'y': fst_pipe[1]['y']}, # 'y': the height of fst down pipe
        {'x': W + 400, 'y': snd_pipe[1]['y']}  # 'y': the height of snd down pipe
    ]

    pipeVelX = -4 # pipe velocity along x: the speed of the pipe's movement to the left
    penguin_velocity_y = -9 # penguin velocity: the speed of the penguin's upward movement
    penguin_fly_velocity = -8  # velocity while flying
    penguin_Max_Vel_Y = 10 # penguin maximum velocity
    gravity = 1 # simulation of gravity

    # COLLISION TIME & IMMUNITY
    collision_immune = False
    collision_time = 0

    # Handle the keyboard events
    while True:
        # COLLISION IMMUNITY
        if pygame.time.get_ticks() - collision_time > 1500:
            collision_immune = False

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    flap_fx.play()
                    penguin_velocity_y = penguin_fly_velocity

        # When the penguin is crashed
        game_over = isGameOver(horizontal, vertical, game_images['pipeimage'], game_images['flypenguin'], up_pipes, down_pipes)

        if game_over and health == 0 and collision_immune == True:
            jumpPenguinGame.game_over(score)
            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN and event.key == K_SPACE:
                        return

        elif game_over and health > 0 and collision_immune == False:
            collision_immune = True
            health -= 1
            collision_time = pygame.time.get_ticks()
            hurt_fx.play()

        # Score calculation
        player_mid_pos = horizontal + game_images['flypenguin'].get_width()/2
        for pipe in up_pipes:
            pipe_mid_pos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
            if player_mid_pos + pipeVelX < pipe_mid_pos < player_mid_pos:
                score += 1

        # Penguin velocity changes with score
        if score < 3:
            pipeVelX = pipeVelX * 1
        elif 3 <= score <= 6:
            pipeVelX = -4 - 0.2 * score
        else:
            pipeVelX = -6

        # Simulate the state of penguin flying
        if penguin_velocity_y < penguin_Max_Vel_Y:
            penguin_velocity_y += gravity

        playerHeight = game_images['flypenguin'].get_height()
        vertical = vertical + min(penguin_velocity_y, elevation - vertical - playerHeight)

        # Move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to touch the leftmost of screen
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])

        # Once the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        # BUILD GAME IMAGES
        health_font = myFont.render(str(health), 1, black) # HEALTH BAR
        window.blit(game_images['background'], (0, 0))
        window.blit(game_images['flypenguin'], (horizontal, vertical))
        window.blit(game_images['heart'], (10, 10))
        window.blit(health_font, (40, 7))

        if collision_immune == True:
            window.blit(game_images['shield'], (horizontal-20, vertical-40))
            window.blit(game_images['flypenguin'], (horizontal, vertical))

        # Build up and down pipes
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0], (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1], (lowerPipe['x'], lowerPipe['y']))

        window.blit(game_images['sea_level'], (0, elevation))

        # Score Display
        score_font = pygame.font.SysFont('Raleway', 64)
        score_txt = score_font.render(str(score), True, black)
        scoreRect = score_txt.get_rect()
        scoreRect.center = [W * 0.9, H - 480]
        if health != 0: window.blit(score_txt, scoreRect)

        # Refresh the game window and display the score
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)


def handleInvalidKey():
    f = pygame.font.SysFont('Raleway', 50, italic=True)
    txt = f.render('Invalid Keyboard', True, (255, 255, 255))
    rect = txt.get_rect()
    rect.center = [215, 245]
    window.blit(txt, rect.center)
    pygame.display.update()
    time.sleep(1)


def createPipe():
    flyingArea = H - game_images['sea_level'].get_height()
    offset = flyingArea / 3
    pipeX = W + 8

    # Generating random height of pipes
    y2 = offset + random.randrange(0, int((flyingArea - 1.1* offset)))
    y1 = y2 - game_images['pipeimage'][0].get_height() - offset

    pipes = [{'x': pipeX, 'y': y1}, {'x': pipeX, 'y': y2}] # the coordinates of the upper and down pipes

    return pipes


def isGameOver(horizontal, vertical, pipeImage, penguinImage, up_pipes, down_pipes):
    # when the penguin touches the sky or ice level, then game over
    if vertical < 0 or vertical > elevation - 25 :
        return True

    # Check whether the penguin hits the upper pipe or not
    for pipe in up_pipes:
        pipeHeight = pipeImage[0].get_height() # get the pipe height, i.e. 320
        if (vertical < pipeHeight + pipe['y'] and abs(horizontal - pipe['x']) < penguinImage.get_width()):
            return True

    # Check whether the penguin hits the down pipe or not
    for pipe in down_pipes:
        if (vertical + penguinImage.get_height() > pipe['y']) and abs(horizontal - pipe['x']) < penguinImage.get_width():
            return True

    return False


def game_start(horizontal, vertical):

    while True:
        for event in pygame.event.get():
            # If user clicks on the cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                game()

            # If the user presses other keys
            elif event.type == KEYDOWN:
                handleInvalidKey()

            # If user does not press any keys, then nothing happens
            else:
                # build the game window
                window.blit(game_images['background'], (0, 0))
                window.blit(game_images['flypenguin'], (horizontal, vertical))
                window.blit(game_images['pipeimage'][0], (640, -200))
                window.blit(game_images['pipeimage'][1], (640, elevation - 150))
                window.blit(game_images['sea_level'], (0, elevation))
                window.blit(game_images['title'], (45, 100))
                window.blit(game_images['instructions'], (100, H // 2 + 50))
                pygame.display.update()
                framepersecond_clock.tick(framepersecond)


if __name__ == "__main__":

    # Initializing pygame modulee
    pygame.init()
    framepersecond_clock = pygame.time.Clock()

    # Sets the title on top of game window
    pygame.display.set_caption('Flying Penguin Game')

    # Load all the images which we will use in the game
    game_images['title'] = pygame.image.load("images/title.png").convert_alpha()
    game_images['instructions'] = pygame.image.load("images/instructions.png").convert_alpha()
    game_images['flypenguin'] = pygame.image.load(penguinplayer_image).convert_alpha()
    game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
    game_images['background'] = pygame.image.load(background_image).convert_alpha()
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180), pygame.image.load(pipeimage).convert_alpha())
    game_images['heart'] = pygame.image.load(heart_image).convert_alpha()
    game_images['shield'] = pygame.image.load("images/shield.png").convert_alpha()

    # Set the coordinates of flappy penguin
    horizontal = int(W / 5)
    vertical = int((H - game_images['flypenguin'].get_height()) / 2)
    game_start(horizontal, vertical)