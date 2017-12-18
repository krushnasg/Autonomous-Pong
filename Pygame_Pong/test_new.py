import pygame
import sys
import random
import pickle
import math
import numpy as np
import json

SCORE_MAX = 30
NUM_TEST = 5


LEFTMOST = 1
RIGHTMOST = 89
numTraining = 100
LENGTH = 100
HEIGHT = 60
max_score = 0
posq = 0
nonvis = 0
# Initial Conditions.

white=(255,255,255)
black=(0,0,0)
green=(0,255,0)
red=(255,0,0)
blue=(0,0,255)
gray=(128,128,128)
size=[100,60]
ball_centre_y=30
ball_centre_x=(int((random.random()*100000)%(size[0]-20)))+10
#ball_centre_x = 90
ball_radius=3
ball_direction='UP_LEFT'
ball_speed=  1        # Ball speed.
hit_bar_speed=2       # Hit Bar Speed.18
hit_bar_length=10
hit_bar_height=3
hit_bar_left=int(size[0]/2)-int(hit_bar_length/2)
time1=pygame.time.get_ticks()
can_accel_left=False
can_accel_right=False

game_over=False
paused_game=False
set_actions=['UP_LEFT','UP_RIGHT','DOWN_LEFT','DOWN_RIGHT']
bar_set_actions=['RIGHT','LEFT']
bar_action=np.random.choice(bar_set_actions)
score=0
epsilon=0.3 			
gamma=0.6
alpha=0.5	
discount=1

randomcnt = 0
state = []
next_state=[]

pkl_file = open('q_val.pkl', 'rb')
q_values = pickle.load(pkl_file)
pkl_file.close()
visited = []





# Function to reset the game.

def reset_game() :
	global ball_centre_y
	global ball_centre_x
	global ball_direction
	global hit_bar_left
	global time1
	global can_accel_left
	global can_accel_right
	global game_over
	global paused_game
	global score
	ball_centre_y=30
	ball_centre_x=(int((random.random()*100000)%(size[0]-20)))+10
	#ball_centre_x = 50
	ball_direction='UP_LEFT'
	hit_bar_left=int(size[0]/2)-int(hit_bar_length/2)
	time1=pygame.time.get_ticks()
	can_accel_left=False
	can_accel_right=False
	game_over=False
	paused_game=False
	score=0




# Function to Draw Initial Screen.

def draw_initial_screen() :
	state = play(True)
	draw_screen()
	font=pygame.font.Font(None,22)
	gameText = font.render("Start", True, white)
#	overText = font.render('Pong', True, white)
	over1Text = font.render('Game', True, white)
	gameRect = gameText.get_rect()
	#overRect = overText.get_rect()
	over1Rect = over1Text.get_rect()
	gameRect.centerx=(size[0]/2)
	gameRect.centery=(size[1]/2)-15
	#overRect.centerx=(size[0]/2)
	#overRect.centery=(size[1]/2)
	over1Rect.centerx=(size[0]/2)
	over1Rect.centery=(size[1]/2+15)
	screen.blit(gameText, gameRect)
	#screen.blit(overText, overRect)
	screen.blit(over1Text, over1Rect)
	print_press_any_key()
	pygame.display.update()







# Function to wait for any key press.

def wait_for_any_key() :
	while True :
		for event in pygame.event.get() :
			if event.type==pygame.QUIT :
				sys.exit()
				pygame.quit()
			if event.type == pygame.KEYDOWN :
				return True








# Function to print Game Over.

def print_game_over() :
	font=pygame.font.Font(None,260)
	font1=pygame.font.Font(None,50)
	gameText = font.render('Game', True, white)
	overText = font.render('Over', True, white)
	sc="Your Score : "+str(score)
	scoreText = font1.render(sc, True, white)
	gameRect = gameText.get_rect()
	overRect = overText.get_rect()
	scoreRect = scoreText.get_rect()
	gameRect.centerx=(size[0]/2)
	gameRect.centery=(size[1]/2)-150
	overRect.centerx=(size[0]/2)
	overRect.centery=(size[1]/2)
	scoreRect.centerx=(size[0]/2)
	scoreRect.centery=(size[1]/2)+120
	screen.blit(gameText, gameRect)
	screen.blit(overText, overRect)
	screen.blit(scoreText, scoreRect)










# Function to print paused game.

def print_paused_game() :
	font=pygame.font.Font(None,230)
	overText = font.render('Paused', True, white)
	overRect = overText.get_rect()
	overRect.centerx=(size[0]/2)
	overRect.centery=(size[1]/2)
	screen.blit(overText, overRect)
	print_press_any_key()







# Function to print press any key.

def print_press_any_key() :
	global paused_game
	font=pygame.font.Font(None,30)
	if paused_game :
		text = font.render("Press Escape key to continue", True, gray)
	else :
		text = font.render("Press any key to continue", True, gray)
	rect = text.get_rect()
	rect.centerx=size[0]-150
	rect.centery=size[1]-50
	screen.blit(text, rect)






# Function to draw screen.

def draw_screen() :
	screen.fill(black)
	font=pygame.font.Font(None,10)
	scoreText = font.render(str(score), True, white)
	scoreRect = scoreText.get_rect()
	scoreRect.centerx=size[0]-10
	scoreRect.centery=10
	screen.blit(scoreText,scoreRect)
	pygame.draw.circle(screen,red,(ball_centre_x,ball_centre_y),ball_radius)
	pygame.draw.rect(screen,blue,(hit_bar_left,(size[1]-hit_bar_height),hit_bar_length,hit_bar_height))
	pygame.display.update()







# Main Game Play Function.

def play(view) :
	global hit_bar_left
	global time1
	global ball_direction
	global ball_centre_x
	global ball_centre_y
	global score
	global game_over

	global state
	if pygame.time.get_ticks() > (time1+11) and view :
		# Code to control movement of ball.
		if ball_direction=='UP_LEFT' :
			if (ball_centre_x-ball_speed)>ball_radius and (ball_centre_y-ball_speed)>ball_radius :
				ball_centre_x-=ball_speed
				ball_centre_y-=ball_speed
			elif (ball_centre_y-ball_speed)>ball_radius :      # Ball exceeds left side of screen.
				ball_direction='UP_RIGHT'
			elif (ball_centre_x-ball_speed)>ball_radius :      # Ball exceeds top of screen.
				ball_direction='DOWN_LEFT'
			else :                                             # Ball exceeds both left and top of screen.
				ball_direction='DOWN_RIGHT'
		if ball_direction=='UP_RIGHT' :
			if (ball_centre_x+ball_speed)<(size[0]-ball_radius) and (ball_centre_y-ball_speed)>ball_radius :
				ball_centre_x+=ball_speed
				ball_centre_y-=ball_speed
			elif (ball_centre_y-ball_speed)>ball_radius :      # Ball exceeds right side of screen.
				ball_direction='UP_LEFT'
			elif (ball_centre_x+ball_speed)<(size[0]-ball_radius)  :  # Ball exceeds bottom of screen.
				ball_direction='DOWN_RIGHT'
			else :                                             # Ball exceeds both right side and bottom of screen.
				ball_direction='DOWN_LEFT'
		if ball_direction=='DOWN_LEFT' :
			if (ball_centre_x-ball_speed)>ball_radius and (ball_centre_y+ball_speed)<(size[1]-ball_radius) :
				if (ball_centre_x+ball_radius)>=hit_bar_left and (ball_centre_x-ball_radius)<=(hit_bar_left+hit_bar_length) :
					if (ball_centre_y+ball_speed)<(size[1]-(ball_radius+hit_bar_height)) :
						ball_centre_x-=ball_speed
						ball_centre_y+=ball_speed
					else :                             # Condition of scoring.
						ball_direction='UP_LEFT'
						score+=1
				elif ((ball_centre_x+ball_radius)<hit_bar_left or (ball_centre_x-ball_radius)>(hit_bar_left+hit_bar_length)) :
					if(ball_centre_y+ball_radius)>(size[1]-hit_bar_height) :   # Condition of game over.
						ball_centre_y=size[1]-ball_radius
						game_over=True
					else :
						ball_centre_x-=ball_speed
						ball_centre_y+=ball_speed
				else :
					ball_centre_x-=ball_speed
					ball_centre_y+=ball_speed
			
			elif (ball_centre_x-ball_speed)>ball_radius :
				ball_direction='UP_LEFT'
			elif  (ball_centre_y+ball_speed)<(size[1]-ball_radius) :
				ball_direction='DOWN_RIGHT'
			else :
				direction='UP_RIGHT'
		if ball_direction=='DOWN_RIGHT' :
			if (ball_centre_x+ball_speed)<(size[0]-ball_radius) and (ball_centre_y+ball_speed)<(size[1]-ball_radius) :
				if (ball_centre_x+ball_radius)>=hit_bar_left and (ball_centre_x-ball_radius)<=(hit_bar_left+hit_bar_length) :
					if (ball_centre_y+ball_speed)<(size[1]-(ball_radius+hit_bar_height)) :
						ball_centre_x+=ball_speed
						ball_centre_y+=ball_speed
					else :                                 # Condition of scoring.
						ball_direction='UP_RIGHT'
						score+=1           
				elif ((ball_centre_x+ball_radius)<hit_bar_left or (ball_centre_x-ball_radius)>(hit_bar_left+hit_bar_length)) :
					if (ball_centre_y+ball_radius)>(size[1]-hit_bar_height) :      # Condition of game over.
						ball_centre_y=size[1]-ball_radius
						game_over=True     
					else :
						ball_centre_x+=ball_speed
						ball_centre_y+=ball_speed
				else :
					ball_centre_x+=ball_speed
					ball_centre_y+=ball_speed
			elif (ball_centre_x+ball_speed)<(size[0]-ball_radius) :
				ball_direction='UP_RIGHT'
			elif  (ball_centre_y+ball_speed)<(size[1]-ball_radius) :
				ball_direction='DOWN_LEFT'
			else :
				direction='UP_LEFT'
		# Code to control Hit Bar Position.

		if can_accel_left :
			if (hit_bar_left-hit_bar_speed)>=0 :
				hit_bar_left-=hit_bar_speed
		if can_accel_right :
			if (hit_bar_left+hit_bar_length+hit_bar_speed)<=size[0] :
				hit_bar_left+=hit_bar_speed
		
		time1=pygame.time.get_ticks()

	

	ball_hit_pos = getExpectedHitPos(ball_centre_x,ball_centre_y,ball_direction)
	return (hit_bar_left,ball_centre_x,ball_centre_y,ball_direction)






def wallHit(ball_centre_x,ball_centre_y,ball_direction):
	
	if(ball_direction == 'UP_LEFT'):
		if(ball_centre_x > ball_centre_y):
			return (ball_centre_x - ball_centre_y + ball_radius+1,ball_radius+1,'DOWN_LEFT')
		else:
			return (ball_radius+1,ball_centre_y - ball_centre_x + ball_radius+1, 'UP_RIGHT')
	elif(ball_direction == 'UP_RIGHT'):
		if(LENGTH - ball_centre_x > ball_centre_y):
			return (ball_centre_x + ball_centre_y - ball_radius-1,ball_radius+1,'DOWN_RIGHT')
		else:
			return (LENGTH - ball_radius-1, ball_centre_y - LENGTH + ball_centre_x + ball_radius+1, 'UP_LEFT')

	elif(ball_direction == 'DOWN_LEFT'):
		if(ball_centre_x > HEIGHT - ball_centre_y):
			return (ball_centre_x - HEIGHT + ball_centre_y + ball_radius+1 + hit_bar_height,HEIGHT - ball_radius-1 - hit_bar_height,'UP_LEFT')
		else:
			return (ball_radius+1,ball_centre_y + ball_centre_x - ball_radius-1, 'DOWN_RIGHT')

	elif(ball_direction == 'DOWN_RIGHT'):
		if(LENGTH - ball_centre_x > HEIGHT - ball_centre_y):
			return (ball_centre_x + HEIGHT - ball_centre_y - ball_radius-1 - hit_bar_height,HEIGHT - ball_radius-1 -  hit_bar_height,'UP_RIGHT')
		else:
			return (LENGTH - ball_radius-1, ball_centre_y + LENGTH - ball_centre_x - ball_radius-1 , 'DOWN_LEFT')


def getExpectedHitPos(ball_centre_x,ball_centre_y,ball_direction):
	x = ball_centre_x
	y = ball_centre_y
	direct = ball_direction
	while y != HEIGHT - ball_radius -hit_bar_height -1 :
		(x,y,direct) = wallHit(x,y,direct)
		print(x,y,direct)
	return x


def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)



pygame.init()
screen=pygame.display.set_mode(size,0,32)
pygame.display.set_caption("Pong 1P")

def getQValue(state, action):
    global q_values, posq
    if (state,action) in q_values:
    	return(q_values[(state,action)])
    else:
    	posq = posq +1
    	q_values.update({(state,action):0.0})
    	return 0.0


def computeActionFromQValues( state):
    global q_values,randomcnt
    max_action=-100000
    action = None
    if(getLegalActions(state)==None):
    	#print("nonr ala")
    	return None
    #print("--------------------------")
    for i in getLegalActions(state):
    	#print(str(i)+":" +str(getQValue(state,i)))
    	if max_action<getQValue(state,i):
    		max_action=getQValue(state,i)
    		action=i
    	elif max_action==getQValue(state,i):
    		#print("random"+str(i)+"\t"+str(randomcnt))
    		randomcnt +=1
    		r = random.random()
    		choice=r < 0.5
    		if choice:
        		max_action=getQValue(state,i)
        		action=i
    #print(action)
    return action

def computeActionFromQValues2( state):
    global q_values,randomcnt
    max_action=-100000
    action = None
    if(getLegalActions(state)==None):
    	print("nonr ala")
    	return None
    #if debug ==1:
    print("--------------------------")
    print("ball x =" + str(ball_centre_x) + "  y = " + str(ball_centre_y))
    print(state)


    for i in getLegalActions(state):
    	#if debug == 1:
    	print(str(i)+":" +str(getQValue(state,i)))
    	if max_action<getQValue(state,i):
    		max_action=getQValue(state,i)
    		action=i
    	elif max_action==getQValue(state,i):
    		print("random"+str(i)+"\t"+str(randomcnt))
    		randomcnt +=1
    		r = random.random()
    		choice=r < 0.5
    		if choice:
        		max_action=getQValue(state,i)
        		action=i
    print(action)
    return action



def getLegalActions(state):
	if state[0]=='TERMINAL':
		return None
	elif state[0]==1:
		return ["RIGHT"]
	elif state[0]==9:
		return ["LEFT"]
	else:
		return ["LEFT","RIGHT"]





ball_hit_pos = getExpectedHitPos(ball_centre_x,ball_centre_y,ball_direction)
state=(hit_bar_left,ball_centre_x,ball_centre_y,ball_direction)

draw_initial_screen()

reset_game()
num_test=NUM_TEST
max_score=-1
num_games=0
total_score=0
while num_test:
	

	draw_screen()

	ball_hit_pos = getExpectedHitPos(ball_centre_x,ball_centre_y,ball_direction)
	state=(hit_bar_left,ball_centre_x,ball_centre_y,ball_direction)
	action=computeActionFromQValues(state)
	bar_action=action
	if(bar_action==None):
		bar_action=np.random.choice(bar_set_actions)
	if bar_action == 'LEFT' :
		can_accel_left=True
		can_accel_right=False
	elif bar_action == 'RIGHT' :
		can_accel_right=True
		can_accel_left=False
	
	next_state=play(True)
	if(score>max_score):
		max_score=score
	if(score>SCORE_MAX):
		game_over=True
	if(game_over==True):
		print("Game over!!!!!,Score: %d" %(score))
		total_score+=score
		num_games+=1
		num_test-=1
	
		reset_game()
	state=next_state

	

print("Maximum Score: %d"%(max_score))
print("Average Score= %d / %d" %(total_score,num_games))

pygame.display.quit()
pygame.quit()