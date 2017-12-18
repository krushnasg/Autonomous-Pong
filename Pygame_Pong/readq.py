import pickle
import numpy as np

cnt =0

pkl_file = open('q_val.pkl', 'rb')
mydict2 = pickle.load(pkl_file)

def getQValue(state, action):
    global mydict2
    if (state,action) in mydict2:
    	return(mydict2[(state,action)])
    else:
    	print("enla")
    	#q_values.update({(state,action):0.0})
    	return 0.0

def getLegalActions(state):
	if state[0]=='TERMINAL':
		return None
	elif state[0]==1:
		return ["RIGHT"]
	elif state[0]==9:
		return ["LEFT"]
	else:
		return ["LEFT","RIGHT"]



#with open('obj/q_values.pkl', 'rb') as f:
 #   data = pickle.load(f)

for key, value in mydict2.items():
	if(value==0):
		cnt+=1
		state = key[0]
		#print(state)
		# for i in getLegalActions(state):
		# 	print(str(i)+":" +str(getQValue(state,i)))
		# print(str(key)+":"+str(value) + "\n" +"\n----------------------")

#print (mydict2)
print("\n" + str(len(mydict2)) + "\t" + str(cnt))
pkl_file.close()
