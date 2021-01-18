#Started: Nov, 2019
#Last modified: Jan.20, 2020
#First iteration of the pygame project

##########
#THINGS TO WORK ON:
# - add smoother jump/physics
# - remove shaking when adding or colliding with a platform

##########

import pygame, sys, random, time
from pygame.locals import *

#
# FONCTIONS
#
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, (255,255,255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    pygame.quit()
                    sys.exit()
                return

#set up pygame
pygame.init()
mainClock = pygame.time.Clock()
pygame.display.set_caption('Leaper Frogger')
pygame.mouse.set_visible(False)

#
# INITIAL VARIABLES
#
#TIME VARIBALES
#frames per second
FPS = 60
#initialize clock
clock = pygame.time.Clock()

#MOVEMENT VARIABLES
# set up movement variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
#left/right/up/down speed
MOVESPEED = 4.5
#initilize jump time duration
ACCEL = 0.5
GRAVITY = 0
#duration of jump
JUMPTIME = 65
jumpTime = JUMPTIME

#SIZE VARIABLES
PLAYERSIZE = 75
WINDOWWIDTH = 960
WINDOWHEIGHT = 640

# COLLISION AND PLATFORM VARIABLES
# direction of the platforms, 1= up, 2=left, 3=right, 4= up
gravDirection = random.randint(1,3)

# PLATFORM DATA VARIABLES
#platform detection
platform = False
# platform speed increase
BLOCKSPEED = 1
blockCounter = 0
speedCounter = 0
gravCounter = 0
# amount of time before the next platform spawns (1 = FPS)
NEWBLOCK = 160
# amount of time before the next platform speeds up (1 = FPS)
BLOCKINCREASE = 1000
BLOCKSIZE = 30

# set up the colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# VISUAL / AUDIO

# set up sounds
pygame.mixer.music.load('background.mp3')

#set up images
background = pygame.image.load('background.jpg')
platformImage = pygame.image.load('platform.png')
playerNo = pygame.image.load('Sprite (Neutral).png')
playerDown = pygame.image.load('Sprite (Down).png')
playerLR = pygame.image.load('Sprite (Right Left).png')
playerAirUp = pygame.image.load('Sprite (Down Air).png')
playerUp = pygame.image.load('Sprite (Up Air).png')

#acale and transfer images to rects
background = pygame.transform.scale(background, (WINDOWWIDTH*2,WINDOWHEIGHT*2))
platformImage = pygame.transform.scale(platformImage, (BLOCKSIZE*int(4.9),BLOCKSIZE))
playerNo = pygame.transform.scale(playerNo, (PLAYERSIZE,PLAYERSIZE))
playerNoL = playerNo
playerNoR = pygame.transform.flip(playerNoL, True, False)
playerDown = pygame.transform.scale(playerDown, (PLAYERSIZE,PLAYERSIZE))
playerDownL = playerDown
playerDownR = pygame.transform.flip(playerDown, True, False)
playerLR = pygame.transform.scale(playerLR, (PLAYERSIZE,PLAYERSIZE))
playerAirUp = pygame.transform.scale(playerAirUp, (PLAYERSIZE,PLAYERSIZE))
playerAirUpL = playerAirUp
playerAirUpR = pygame.transform.flip(playerAirUp, True, False)
playerUp = pygame.transform.scale(playerUp, (PLAYERSIZE,PLAYERSIZE))
playerUpL = playerUp
playerUpR = pygame.transform.flip(playerUp, True, False)

#set background and image for player
backgroundRect = background.get_rect()
backgroundRect.left = 0
backgroundRect.top = 0
playerImage = playerNo
player = playerNo.get_rect()
platform = platformImage.get_rect()

#block list
blocks = []
# number of blocks initially to begin with
for x in range (0):
    blocks.append(platform (WINDOWWIDTH, random.randint(4*BLOCKSIZE,WINDOWHEIGHT-(3*BLOCKSIZE)), BLOCKSIZE*5, BLOCKSIZE/2))

# set up the window
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Input')

#font
font = pygame.font.SysFont(None, 48)
font2 = pygame.font.SysFont(None, 30)

#show the "Start" screen
drawText('Leaper Frogger', font, windowSurface,(WINDOWWIDTH/3),(WINDOWHEIGHT/4))
drawText('Press a key to start', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 4) + 50)
drawText('Controls: hold arrow keys or a/s/d/f to move up/down/left/or right', font2, windowSurface, (WINDOWWIDTH/7), (WINDOWHEIGHT/2))
drawText('Objective: endless 2D platformer, try to survive as long as possible', font2, windowSurface, (WINDOWWIDTH/8), (WINDOWHEIGHT/2)+50)
drawText('by jumping on the platforms that vary in speed and change direction', font2, windowSurface, (WINDOWWIDTH/8), (WINDOWHEIGHT/2)+80)
pygame.display.update()
waitForPlayerToPressKey()

#play song
pygame.mixer.music.play(-1, 0.0)

#define score
score = 0
#
# run the game loop
#
while True:
    # increase score
    score += 1
    # check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # moment keyboard variables 
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == ord('w'):
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == ord('s'):
                moveUp = False
                moveDown = True

         # non-movement keyboard variables           
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()              
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
            if event.key == K_UP or event.key == ord('w'):
                moveUp = False
            if event.key == K_DOWN or event.key == ord('s'):
                moveDown = False
            #if event.key == ord('x'):
                #player.top = random.randint(0, WINDOWHEIGHT - player.height)
                #player.left = random.randint(0, WINDOWWIDTH - player.width)

                
    # move down
    if moveDown:    
        player.top += MOVESPEED
            
    #jump duration/action (move up)
    if moveUp:
        if jumpTime > 0:
            GRAVITY += 0.1
            player.top -= ((2*MOVESPEED) - GRAVITY)
            jumpTime -=1
            ACCEL = 0.7           
    if jumpTime == 0:
        GRAVITY = 0

    #move left     
    if moveLeft :
        player.left -= MOVESPEED

    #move right
    if moveRight  :
        player.right += MOVESPEED

    #gravity check
    if  (platform == False):
        player.top += ACCEL
        ACCEL += 0.2

    # add initial starting block
    if blockCounter == 0:
        blocks.append(pygame.Rect(0, WINDOWHEIGHT/2, BLOCKSIZE*4, BLOCKSIZE/2))  
        gravDirection = 3
    #add blocks
    if gravDirection != 1:
        blockCounter += 1
    else:
        blockCounter += 2
        
    if blockCounter >= NEWBLOCK:
        #add new block
        blockCounter = 1
        if gravDirection == 1:
            blocks.append(pygame.Rect (random.randint(BLOCKSIZE,WINDOWWIDTH-(BLOCKSIZE)), 0, BLOCKSIZE*4, BLOCKSIZE/2))
        if gravDirection == 2:
            blocks.append(pygame.Rect (WINDOWWIDTH, random.randint(4*BLOCKSIZE,WINDOWHEIGHT-(3*BLOCKSIZE)), BLOCKSIZE*4, BLOCKSIZE/2))
        if gravDirection == 3:
            blocks.append(pygame.Rect (0-(3*BLOCKSIZE), random.randint(4*BLOCKSIZE,WINDOWHEIGHT-(3*BLOCKSIZE)), BLOCKSIZE*4, BLOCKSIZE/2))
        # IMPLEMENT IN THE FUTURE
        #if gravDirection == 4:
            #blocks.append(pygame.Rect (random.randint(BLOCKSIZE,WINDOWWIDTH-(BLOCKSIZE)), WINDOWHEIGHT, BLOCKSIZE*3, BLOCKSIZE/2))
    # constantly move the platforms to the up/left/right
    for block in blocks[:]:
        if gravDirection == 4:
            block.top -= BLOCKSPEED
            if block.top <= 0:
                blocks.remove(block)
        if gravDirection == 3:
            block.left += BLOCKSPEED
            if block.left >= WINDOWWIDTH:
                blocks.remove(block)
        if gravDirection == 2:
            block.left -= BLOCKSPEED
            if block.right <= 0:
                blocks.remove(block)
        if gravDirection == 1:
            block.top += BLOCKSPEED
            if block.top >= WINDOWHEIGHT:
                blocks.remove(block)
            
    #increase block speed and block spawn frequency
    speedCounter += 1
    if speedCounter >= BLOCKINCREASE:       
        speedCounter = 0
        BLOCKSPEED += 0.5
        NEWBLOCK -= 2
        
    #change direction of platforms
    gravCounter += 1
    if gravCounter >= BLOCKINCREASE/2:
        gravDirection = random.randint(1,3)
        gravCounter = 0

            
            
    # check if the player has collided with platforms
    for block in blocks[:]:
        if player.colliderect(block):
            GRAVITY = 0
            # player moving down
            if moveDown:
                player.top -= MOVESPEED
            # player colliding with block bottom
            if moveUp :
                if (player.right > block.left) and (player.left < block.right):
                    #player.top += (2*MOVESPEED)
                    jumpTime = 0        
            if moveLeft:
                # player colliding with block bottom
                if player.bottom > (block.top - GRAVITY): 
                    player.right += MOVESPEED

                
            if moveRight:
                # player colliding with the block left   
                if player.bottom > block.top:
                    player.left -= MOVESPEED

            # when player is on top of a block, allow player to move left/right/up
            if player.bottom <= (block.top+(2*ACCEL)):
                jumpTime = JUMPTIME
                player.bottom = block.top 
                platform = True
                ACCEL = 0.7
                # player moves with the block
                #player.left -= 2.5*BLOCKSPEED 
    # detect when no longer on a platform         
    else:
        platform = False
        MOVESPEED = 4
    
    
            
    # draw the black background onto the surface
    windowSurface.fill(BLACK)
    windowSurface.blit(background, backgroundRect)

    # Draw the score and top score.
    drawText('Score: %s' % (score), font, windowSurface, 10, 0)


    
    #neutral sprite no inputs
    playerImage = playerNo   
    if moveLeft:
        playerImage = playerLR
        playerNo = playerNoL
        playerDown = playerDownL
        playerUp = playerUpL
        playerAirUp = playerAirUpL
    if moveRight:
        playerImage = pygame.transform.flip(playerLR, True, False)
        playerNo = playerNoR
        playerDown = playerDownR
        playerUp = playerUpR
        playerAirUp = playerAirUpR
    if moveDown:
        playerImage = playerDown
    if moveUp:
        playerImage = playerUp
    if jumpTime == 0:
        playerImage = playerAirUp
        
    # draw the player onto the surface
    windowSurface.blit(playerImage, player)


    # draw the blocks one at a time
    for i in range (len(blocks)):
        #pygame.draw.rect(windowSurface, GREEN, blocks[i])
        windowSurface.blit(platformImage, blocks[i])
        

    pygame.display.update()

    # lose condition: if the player has went out of bounds
    if (player.right < 0) or (player.left > WINDOWWIDTH) or (player.top > WINDOWHEIGHT) or (player.bottom < 0):
        break
        
    clock.tick(FPS)

# Stop the game and show the "Game Over" screen.
pygame.mixer.music.stop()
drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3),(WINDOWHEIGHT / 3))
pygame.display.update()
waitForPlayerToPressKey()
# gameOverSound.stop()

    
