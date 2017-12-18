File Details-
	train_pong1p.py --> train the pong game
	test_pre_trained.py --> test game on pre computed q-value model
	test_new.py --> test game on recently trained model
	readq.py --> read q_values form file
	pre_trained_qval.pkl --> pre computed q-value model

NOTE: training takes ~100 Minutes of time for NUM_TRAIN = 1000000, but you will find better results than pre-trained model.
After the model is trained, program is tested for 5 games.

* There is a Maximum Score that can be attained(30). This is done in order to avoid it for playing infinitely. 
