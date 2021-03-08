import pygame
import random   #so that our enemy appears at random places
import math
from pygame import mixer


# initialise the pygame

pygame.init()

# create the screen

screen=pygame.display.set_mode((800,600))  # here the inside bracket is tuple

# Title and icon

pygame.display.set_caption("Space Rangers")
icon=pygame.image.load(r'Images-logos\asteroid_attack.png')
pygame.display.set_icon(icon)

#background

back=pygame.image.load(r'Images-logos\18731.jpg')

# Background Sound



#player

player_img=pygame.image.load(r'Images-logos\battleship.png')
playerX=370
playerY=480
player_change=0
def player(x,y):
    screen.blit(player_img,(x,y))

#alien

alien_img=[]
alienX=[]
alienY=[]
alien_changeX=[]
alien_changeY=[]
num_aliens=6
for i in range(num_aliens):
    if i<3:
        alien_img.append(pygame.image.load(r'Images-logos\alien2.png'))
    else:
        alien_img.append(pygame.image.load(r'Images-logos\monster.png'))
    alienX.append(random.randint(0,736))
    alienY.append(random.randint(15,75))
    alien_changeX.append(.15)
    alien_changeY.append(.05)


def alien(x,y,i):
    screen.blit(alien_img[i],(x,y))

#missile

missile_img=pygame.image.load(r'Images-logos\missile.png')
missileX=playerX+16
missileY=475
move=1.2
state="ready"
def missile(x,y):
    global state
    state="fire"
    screen.blit(missile_img,(x,y))
blast=pygame.image.load(r'Images-logos\blast.png')  

# score

score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=11
textY=11
def show_score(x,y):
    score=font.render("Score :"+ str(score_value),True,(255,255,255))
    screen.blit(score,(0,0))

#collision mechanism

def isCollision(alienX,alienY,missileX,missileY):
    distance=math.sqrt(((missileX-alienX)**2)+((missileY-alienY)**2))
    if distance<37:
        return True
    else:
        return False

#life text

life=5
l_font=pygame.font.Font('freesansbold.ttf',32)
l_textX=10
l_textY=10

#Game-over-Text

g_font=pygame.font.Font('freesansbold.ttf',50)
g_textX=30
g_textY=30


# Game over

def alien_collison_check(a,b,c,d,i):
    alien_collision=isCollision(a,b,c,d)
    if alien_collision:
        global life
        life-=1
        alienX[i]=random.randint(0,735)
        alienY[i]=random.randint(30,100) 
        collision_sound=mixer.Sound(r'Sound_effects\explosion.wav')
        collision_sound.play()
        
        #  game-Over-finally
        
        if life<=0:
            gameover_sound=mixer.Sound(r'Sound_effects\game_over_fast.wav')
            gameover_sound.play()
            for i in range(6):
                alienX[i]=2000
                alienY[i]=0
                alien_changeX[i]=0
                alien_changeY[i]=0



    l_score=l_font.render("Life :"+ str(life),True,(255,255,255))
    screen.blit(l_score,(680,0))
    if life<=0:
        g_score=g_font.render("Game Over",True,(255,255,255))
        screen.blit(g_score,(300,260))

# Game loop --------------------------------------------------------------------------------

running=True
while running:
    screen.fill((0,0,0))#r,g,b
    
    #background image
    
    screen.blit(back,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        # if a key stroke is pressed check wheather its right or left
        if event.type == pygame.KEYDOWN:#key down means we pressed key
            if event.key == pygame.K_LEFT:
                player_change=-0.3
            if event.key == pygame.K_RIGHT:
                player_change=0.3
            if event.key == pygame.K_SPACE:
                if state is "ready":
                    missile_sound=mixer.Sound(r'Sound_effects\beam_small.wav')
                    missile_sound.play() # this will play only when we press Space but i need continous
                    missileX=playerX+16
                    missile(missileX,475)

        if event.type == pygame.KEYUP:#key up means we released the key
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #player_change=0   so that the spaceship do not move further but i want it to move further 
                pass
            
    # if else conditions for boundaries
    playerX+=player_change     
    if playerX<0:
        playerX=0
    elif playerX>736:
        playerX=736   


    for i in range(num_aliens):
        
        #  Game Over
        alien_collison_check(playerX,playerY,alienX[i],alienY[i],i)
        # i increased the speeed of aliens if score is greater than 30
        if score_value>=30 and life!=0:
            alien_changeY[i]=.3
        elif life==0:
            alien_changeY[i]=0
        else:
            alien_changeY[i]=.05

        alienX[i]+=alien_changeX[i]  
        alienY[i]+=alien_changeY[i]  
        if alienX[i]<0 and life!=0:
            alien_changeX[i]=.15
        elif alienX[i]>736 and life!=0:
            alien_changeX[i]=-.15
        if alienY[i]<0 and life!=0:
            if score_value>=30:
                alien_changeY[i]=.1
            else:
                alien_changeY[i]=.05
        elif alienY[i]>600 and life!=0:
            alienX[i]=random.randint(0,736)
            alienY[i]=random.randint(30,100) 
        
        # alien hit by missile
        collision=isCollision(alienX[i],alienY[i],missileX,missileY)
        if collision:
            # missileY=475  if this is not commented we have to again press for space to fire beam
            #state="ready"  this too
            score_value+=1
            alienX[i]=random.randint(0,735)
            alienY[i]=random.randint(30,100) 
            collision_sound=mixer.Sound(r'Sound_effects\hit.wav')
            collision_sound.play()
        
        alien(alienX[i],alienY[i],i)


    # missile move
    if missileY<=0:
        missileX=playerX+16
        missileY=475

    #playing beam in a loop  (failed not worked well)
    #missile_sound=mixer.Sound(r'C:\files\VS code\py_game\Sound_effects\beam_small.wav')
    #missile_sound.play()
    
    player(playerX,playerY)
    show_score(textX,textY)
    if state is "fire":
        missile(missileX,missileY)
        missileY-=move
    pygame.display.update()#this will keep updating the screen





    # in this game i made the enemy move in random y we can also let them decrease y
    # axis on striking the boundary etc