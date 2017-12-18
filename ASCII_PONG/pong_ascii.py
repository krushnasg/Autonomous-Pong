import numpy as np
import random,math


SCORE_MAX = 30
NUM_TEST = 10
NUM_TRAIN = 10000

# Initial Conditions.
q_values={}

randomcnt =0

game_over=False
score=0
epsilon=0.3 			
gamma=0.6
alpha=0.5	
discount=1

set_actions=['UP_LEFT','UP_RIGHT','DOWN_LEFT','DOWN_RIGHT']
set_actions_game=['UP_LEFT','UP_RIGHT']

bar_set_actions=['RIGHT','LEFT']
ball_pos_x=(int((random.random()*1000)%10))
ball_pos_y=(int((random.random()*1000)%10))
ball_direction=np.random.choice(set_actions)
bar_action=np.random.choice(bar_set_actions)
bar_pos_x=5
bar_length=2
env = [['*' for x in range(10)] for y in range(10)]
state=[]




def reset_pong():
	global score
	global ball_pos_y,ball_pos_x,ball_direction,bar_pos_x,game_over
	score=0
	game_over=False
	ball_pos_x=(int((random.random()*1000)%10))
	ball_pos_y=(int((random.random()*1000)%10))
	ball_direction=np.random.choice(set_actions)
	bar_action=np.random.choice(bar_set_actions)
	bar_pos_x=5




def display_pong(env):
	env=ascii_pong()
	global bar_pos_x,ball_pos_x,ball_pos_y
	env[9][bar_pos_x-1]='-'
	env[9][bar_pos_x]='-'
	print("%d,%d"%(ball_pos_x,ball_pos_y))
	env[ball_pos_y][ball_pos_x]='@'
	print(env[0])
	print(env[1])
	print(env[2])
	print(env[3])
	print(env[4])
	print(env[5])
	print(env[6])
	print(env[7])
	print(env[8])	
	print(env[9])

def ascii_pong():
	global env
	env = [['*' for x in range(10)] for y in range(10)]
	return env


def play_pong():
	global state
	global game_over,score
	global ball_pos_y,ball_pos_x,bar_pos_x,ball_direction
	if(bar_action=='LEFT'):
		if(bar_pos_x>1):
			bar_pos_x=bar_pos_x-1
		else:
			bar_pos_x=bar_pos_x
	elif(bar_action=='RIGHT'):
		if(bar_pos_x<=8):
			bar_pos_x=bar_pos_x+1
		else:
			bar_pos_x=bar_pos_x

	if(ball_pos_x>0 and ball_pos_x<9):
		if(ball_pos_y>0 and ball_pos_y<9):
			if(ball_direction=='UP_LEFT'):
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='UP_RIGHT'):
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='DOWN_LEFT'):
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y+1
			elif(ball_direction=='DOWN_RIGHT'):
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y+1
		elif(ball_pos_y==0):
			if(ball_direction=='UP_LEFT'):
				ball_direction='DOWN_LEFT'
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y+1
			elif(ball_direction=='UP_RIGHT'):
				ball_direction='DOWN_RIGHT'
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y+1
			elif(ball_direction=='DOWN_LEFT'):
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y+1
			elif(ball_direction=='DOWN_RIGHT'):
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y+1
		elif(ball_pos_y==9 and (ball_pos_x==bar_pos_x or ball_pos_x==bar_pos_x-1)):
			score=score+1
			if(ball_direction=='UP_LEFT'):
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='UP_RIGHT'):
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='DOWN_LEFT'):
				ball_direction='UP_LEFT'
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='DOWN_RIGHT'):
				ball_direction='UP_RIGHT'
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y-1
		elif(ball_pos_y==9 ):
			game_over=True

	elif(ball_pos_x==0):
		if(ball_pos_y>0 and ball_pos_y<9):
			if(ball_direction=='UP_LEFT'):
				ball_direction='UP_RIGHT'
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='UP_RIGHT'):
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='DOWN_LEFT'):
				ball_direction='DOWN_RIGHT'
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y+1
			elif(ball_direction=='DOWN_RIGHT'):
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y+1
		elif(ball_pos_y==0):
			if(ball_direction=='UP_LEFT'):
				ball_direction='DOWN_RIGHT'
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y+1
			elif(ball_direction=='UP_RIGHT'):
				ball_direction='DOWN_RIGHT'
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y+1
			elif(ball_direction=='DOWN_LEFT'):
				ball_direction='DOWN_RIGHT'
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y+1
			elif(ball_direction=='DOWN_RIGHT'):
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y+1
		elif(ball_pos_y==9 and (ball_pos_x==bar_pos_x or ball_pos_x==bar_pos_x-1)):
			score=score+1
			if(ball_direction=='UP_LEFT'):
				ball_direction='UP_RIGHT'
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='UP_RIGHT'):
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='DOWN_LEFT'):
				ball_direction='UP_RIGHT'
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='DOWN_RIGHT'):
				ball_direction='UP_RIGHT'
				ball_pos_x=ball_pos_x+1
				ball_pos_y=ball_pos_y-1
		elif(ball_pos_y==9 and (ball_pos_x!=bar_pos_x and ball_pos_x!=bar_pos_x-1)):
			game_over=True
			



	elif(ball_pos_x==9):
		if(ball_pos_y>0 and ball_pos_y<9):
			if(ball_direction=='UP_LEFT'):
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='UP_RIGHT'):
				ball_direction='UP_LEFT'
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='DOWN_LEFT'):
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y+1
			elif(ball_direction=='DOWN_RIGHT'):
				ball_direction='DOWN_LEFT'
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y+1
		elif(ball_pos_y==0):
			if(ball_direction=='UP_LEFT'):
				ball_direction='DOWN_LEFT'
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y+1
			elif(ball_direction=='UP_RIGHT'):
				ball_direction='DOWN_LEFT'
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y+1
			elif(ball_direction=='DOWN_LEFT'):
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y+1
			elif(ball_direction=='DOWN_RIGHT'):
				ball_direction='DOWN_LEFT'
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y+1
		elif(ball_pos_y==9 and (ball_pos_x==bar_pos_x or ball_pos_x==bar_pos_x-1)):
			score=score+1

			if(ball_direction=='UP_LEFT'):
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y-1

			elif(ball_direction=='UP_RIGHT'):
				ball_direction='UP_LEFT'
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='DOWN_LEFT'):
				ball_direction='UP_LEFT'
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y-1
			elif(ball_direction=='DOWN_RIGHT'):
				ball_direction='UP_LEFT'
				ball_pos_x=ball_pos_x-1
				ball_pos_y=ball_pos_y-1
		elif(ball_pos_y==9 and (ball_pos_x!=bar_pos_x and ball_pos_x!=bar_pos_x-1)):
			game_over=True

	return (bar_pos_x,ball_pos_x,ball_pos_y,ball_direction)






def reset_pong2():
	global score
	global ball_pos_y,ball_pos_x,ball_direction,bar_pos_x,game_over
	score=0
	game_over=False
	ball_pos_x=(int((random.random()*1000)%10))
	ball_pos_y=5
	ball_direction=np.random.choice(set_actions_game)
	bar_action=np.random.choice(bar_set_actions)
	bar_pos_x=5


def getQValue(state, action):
    global q_values
    if (state,action) in q_values:
    	return(q_values[(state,action)])
    else:
    	q_values.update({(state,action):0.0})
    	return 0.0


def computeValueFromQValues(state):
    max_action=-100000
    for i in getLegalActions(state):
    	max_action=max(max_action,getQValue(state,i))
    if max_action==-100000:
    	max_action=0.0
    return max_action



def computeActionFromQValues( state):
    global q_values,randomcnt
    max_action=-100000
    action = None
    if(getLegalActions(state)==None):
    	return None
    for i in getLegalActions(state):
    	if max_action<getQValue(state,i):
    		max_action=getQValue(state,i)
    		action=i
    	elif max_action==getQValue(state,i):
    		randomcnt +=1
    		r = random.random()
    		choice=r < 0.5
    		if choice:
        		max_action=getQValue(state,i)
        		action=i
    return action

def computeActionFromQValues2( state):
    global q_values,randomcnt
    max_action=-100000
    action = None
    if(getLegalActions(state)==None):
    	print("nonr ala")
    	return None
    print("--------------------------")
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


def getAction( state):
    # Pick Action
    legalActions = getLegalActions(state)
    action = None
    r = random.random()
    choice=r<epsilon

    if legalActions==None:
    	return None

    if choice==True:
    	action=np.random.choice(legalActions)
    else:
    	action=computeActionFromQValues(state)


    return action

def update(state, action, nextState, reward):
	global q_values,score
	if(nextState[0]=='TERMINAL'):
		target=-100
		score=-100
		update_q=(1-alpha)*getQValue(state,action)+(alpha)*target
		q_values[(state,action)]=update_q
		return

	value_next=computeValueFromQValues(nextState)
	target=reward+discount*value_next
	update_q=(1-alpha)*getQValue(state,action)+(alpha)*target
	q_values[(state,action)]=update_q
	return


def getPolicy( state):
    return computeActionFromQValues(state)

def getValue( state):
    return scomputeValueFromQValues(state)



def getLegalActions(state):
	if state[0]=='TERMINAL':
		return None
	elif state[0]==1:
		return ["RIGHT"]
	elif state[0]==9:
		return ["LEFT"]
	else:
		return ["LEFT","RIGHT"]




#Training-------------------------------------------------------------------------------------------------------

state=(bar_pos_x,ball_pos_x,ball_pos_y,ball_direction)

env=ascii_pong()
#display_pong(env)
num_training=NUM_TRAIN
while num_training:
	old_score=score
	action=getAction(state)
	bar_action=action
	next_state=play_pong()
	reward=(score-old_score)*10



	if(game_over==True):
		next_state=('TERMINAL',ball_pos_x,ball_pos_y,ball_direction)
		update(state,action,next_state,reward)
		num_training=num_training-1
		reset_pong()
	else:
		update(state,action,next_state,reward)

	old_score=score
	state=next_state
	




ctr=0
for key, value in q_values.items():
	if(value!=0):
		ctr+=1

print("The count of non-zero states is:%d"%(ctr))
print("The number of states encountered: %d\n\n"%(len(q_values)))




#TEST--------------------------------------------------------------------------------------------------------------------


reset_pong2()
num_test=NUM_TEST
max_score=-1
num_games=0
total_score=0
while num_test:
	display_pong(env)
	
	action=computeActionFromQValues(state)
	bar_action=action
	print("move : " + str(action))
	if(bar_action==None):
		bar_action=np.random.choice(bar_set_actions)
	next_state=play_pong()
	if(score>max_score):
		max_score=score
	if(score>SCORE_MAX):
		game_over=True
	if(game_over==True):
		print("Game over!!!!!,Score: %d" %(score))
		#max_score=-1
		total_score+=score
		num_games+=1
		num_test-=1
		reset_pong2()
	state=next_state
	print("==================================================\n")

	

print("Maximum Score: %d"%(max_score))
print("Average Score= %d / %d" %(total_score,num_games))
