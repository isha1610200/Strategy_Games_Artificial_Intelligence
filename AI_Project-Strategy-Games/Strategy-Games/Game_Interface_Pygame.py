import math , time
from time import sleep
#from Game_Codes import *
#from Game_Codes_Modified import *
from Game_Logic import *
import pygame
from pygame.locals import*

SCREEN_HORIZONTAL = 600
SCREEN_VERTICAL = 600 


# Define a TicTacToeBoard object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of this object
class TicTacToeBoard(pygame.sprite.Sprite):
	def __init__(self):
		super(TicTacToeBoard, self).__init__()
		self.width = SCREEN_HORIZONTAL/2
		self.height = SCREEN_VERTICAL/2
		width = self.width
		height = self.height
		self.surf = pygame.Surface((width, height))
		self.surf.fill((255, 255, 255))
		self.rect = self.surf.get_rect()
		line_color = (0,0,0)
		# Drawing vertical lines
		pygame.draw.line(self.surf,line_color,(width/3,0),(width/3, height),7)
		pygame.draw.line(self.surf,line_color,(width/3*2,0),(width/3*2, height),7)
		# Drawing horizontal lines
		pygame.draw.line(self.surf,line_color,(0,height/3),(width, height/3),7)
		pygame.draw.line(self.surf,line_color,(0,height/3*2),(width, height/3*2),7)


	def update(self,symbol,row,col):
		#print("In upd:" , row, col)
		width = self.width
		height = self.height
		hor_diff = width/3
		vert_diff = height/3
		if symbol == 'X':
			pygame.draw.circle(self.surf,(255,0,0),( int((col*(width/3)) + ((width/3)/2)), int((row*(height/3)) + ((height/3)//2)) ),15)
		else:
			pygame.draw.circle(self.surf,(0,0,255),( int((col*(width/3)) + ((width/3)/2)), int((row*(height/3)) + ((height/3)//2)) ),15)
		pygame.display.flip()		


def Game_Over(screen,utility_value):

	if utility_value > 0:
		string = "You have Won!"
	elif utility_value <0:
		string = "AI has Won , You lost the game!"
	else:
		string = "Its a Draw!"
	Print_Text_On_Screen(screen,string,30,(0,0,0),500)
	pygame.display.update()
	sleep(5)
	#time.sleep(5)



def Play_TicTacToe(screen,Algorithm_choice):

	running = True
	GameObject = TicTacToe()
	Gamestate = GameObject.initialState
	screen.fill((255,192,203))
	TTTBoard = TicTacToeBoard()
	
	while running:

		pygame.display.update()
		Print_Text_On_Screen(screen,"Your Coin:",20,(0,100,0),45)
		pygame.draw.circle(screen,(255,0,0),(400,45),8)
		Print_Text_On_Screen(screen,"My Coin:",20,(0,100,0),70)
		pygame.draw.circle(screen,(0,0,255),(400,70),8)
		pygame.display.update()
		start_hor = SCREEN_HORIZONTAL/4
		start_vert = SCREEN_VERTICAL/4
		screen.blit(TTTBoard.surf, (start_hor, start_vert))



		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
			elif event.type == pygame.MOUSEBUTTONDOWN: # 1.Check if correct pos. click 2.Make action_by_max yourself instead of max_move fn 3.Update surface state
				if GameObject.PLAYER_TURN_DETECTOR(Gamestate) == 'MAX':
					x,y = pygame.mouse.get_pos() # print(x,y)
					hor_diff = (SCREEN_HORIZONTAL/2)/3
					vert_diff = (SCREEN_VERTICAL/2)/3
					Col = None
					Row = None

					if x>start_hor and x<hor_diff + start_hor:
						Col = 0
					elif x>start_hor + hor_diff and x < start_hor + 2*hor_diff:
						Col = 1
					elif start_hor + 2*hor_diff < x and x < start_hor + 3*hor_diff:
						Col = 2
					else:
						Col = None

					if y>start_vert and y < start_vert + vert_diff:
						Row = 0
					elif y>start_vert + vert_diff and y < start_vert + 2*vert_diff:
						Row = 1
					elif y > start_vert + 2*vert_diff and y < start_vert + 3*vert_diff:
						Row = 2
					else:
						Row = None

					if Row is not None and Col is not None and Gamestate[0][Row][Col] == '-':
						#print(Row , "," , Col)
						action_by_max = "Place X at ({},{})".format(Row,Col)   #action_by_max = MAX_MOVE(GameObject,Gamestate)  # Move by Human  NOTE:Here Gamestate indeed has 'MAX'
						Gamestate = GameObject.RESULT(Gamestate,action_by_max)
						TTTBoard.update('X',Row,Col) # And now discard rest of the events in the queue
						pygame.display.flip()
						screen.blit(TTTBoard.surf, (start_hor, start_vert))
						pygame.event.clear()
						break    # To ensure only 1 event of mouseclick type is processed at a time

		pygame.display.update()

		if GameObject.PLAYER_TURN_DETECTOR(Gamestate) == 'MIN':

			if GameObject.TERMINAL_TEST(Gamestate):
				utility_value = GameObject.UTILITY(Gamestate)
				running = False
				Game_Over(screen,utility_value)
				#time.sleep(5)
			else:
				action_by_min = GENERIC_GAME_PLAYING_AGENT(GameObject,Gamestate,Algorithm_choice)
				Gamestate = GameObject.RESULT(Gamestate,action_by_min)
				index = action_by_min.find("(")
				O_row = int(action_by_min[index + 1])
				O_col = int(action_by_min[index + 3])
				TTTBoard.update('O',O_row,O_col)
				screen.blit(TTTBoard.surf, (start_hor, start_vert))
				if GameObject.TERMINAL_TEST(Gamestate):
					utility_value = GameObject.UTILITY(Gamestate)
					running = False
					Game_Over(screen,utility_value)
					#time.sleep(5)

		pygame.display.flip()

	return



class OpenFieldTicTacToeBoard(pygame.sprite.Sprite):
	def __init__(self,dimension):
		super(OpenFieldTicTacToeBoard, self).__init__()
		self.width = (2/3)*SCREEN_HORIZONTAL
		self.height = (2/3)*SCREEN_VERTICAL
		self.dimension = dimension
		width = self.width
		height = self.height
		self.surf = pygame.Surface((width, height))
		self.surf.fill((255, 255, 255))
		self.rect = self.surf.get_rect()
		line_color = (0,0,0)

		for i in range(dimension):
			pygame.draw.line(self.surf,line_color,((width/dimension)*i,0),((width/dimension)*i,height),7) ##---> Vertical Line
			pygame.draw.line(self.surf,line_color,(0,(height/dimension)*i),(width,(height/dimension)*i),7) ##---> Horizonatal line

		


	def update(self,symbol,row,col):
		#print("In upd:" , row, col)
		dimension = self.dimension
		width = self.width
		height = self.height
		hor_diff = width/dimension
		vert_diff = height/dimension
		if symbol == 'X':
			pygame.draw.circle(self.surf,(255,0,0),( int((col*hor_diff) + (hor_diff/2)), int((row*vert_diff) + (vert_diff//2)) ),8)
		else:
			pygame.draw.circle(self.surf, (0,0,255),( int((col*hor_diff) + (hor_diff/2)), int((row*vert_diff) + (vert_diff//2)) ),8)
		
		pygame.display.flip()		




def Play_OpenFieldTicTacToeHelper(screen,Algorithm_choice,dimension,connecting_length):

	running = True
	GameObject = OpenFieldTicTacToe(dimension,connecting_length)
	Gamestate = GameObject.initialState
	screen.fill((255,192,203))
	OFTTTBoard = OpenFieldTicTacToeBoard(dimension)
	
	while running:

		pygame.display.update()

		Print_Text_On_Screen(screen,"Connecting Length required to win:" + str(connecting_length), 20,(0,0,0),25)
		Print_Text_On_Screen(screen,"Your Coin:",20,(0,100,0),45)
		pygame.draw.circle(screen,(255,0,0),(400,45),8)
		Print_Text_On_Screen(screen,"My Coin:",20,(0,100,0),70)
		pygame.draw.circle(screen,(0,0,255),(400,70),8)
		pygame.display.update()
		start_hor = SCREEN_HORIZONTAL/6   #Board---> 2/3 of total screen width
		start_vert = SCREEN_VERTICAL/6
		screen.blit(OFTTTBoard.surf, (start_hor, start_vert))



		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
			elif event.type == pygame.MOUSEBUTTONDOWN: # 1.Check if correct pos. click 2.Make action_by_max yourself instead of max_move fn 3.Update surface state
				if GameObject.PLAYER_TURN_DETECTOR(Gamestate) == 'MAX':
					x,y = pygame.mouse.get_pos() # print(x,y)
					hor_diff = ((2/3)*SCREEN_HORIZONTAL)/dimension  #---> bcoz board heer will be 2/3 of toatl screen width
					vert_diff = ((2/3)*SCREEN_VERTICAL)/dimension
					Col = None
					Row = None

					for i in range(dimension):
						if x>start_hor + i*hor_diff  and x < start_hor + (i+1)*hor_diff:
							Col = i
							break

					for j in range(dimension):
						if y>start_vert + j*vert_diff and y< start_vert + (j+1)*vert_diff:
							Row = j
							break


					if Row is not None and Col is not None and Gamestate[0][Row][Col] == '-':
						#print(Row , "," , Col)
						action_by_max = "Place X at ({},{})".format(Row,Col)   #action_by_max = MAX_MOVE(GameObject,Gamestate)  # Move by Human  NOTE:Here Gamestate indeed has 'MAX'
						Gamestate = GameObject.RESULT(Gamestate,action_by_max)
						OFTTTBoard.update('X',Row,Col) # And now discard rest of the events in the queue
						pygame.display.flip()
						screen.blit(OFTTTBoard.surf, (start_hor, start_vert))
						pygame.event.clear()
						break    # To ensure only 1 event of mouseclick type is processed at a time

		pygame.display.update()

		if GameObject.PLAYER_TURN_DETECTOR(Gamestate) == 'MIN':

			if GameObject.TERMINAL_TEST(Gamestate):
				utility_value = GameObject.UTILITY(Gamestate)
				running = False
				Game_Over(screen,utility_value)
				#time.sleep(5)
			else:
				action_by_min = GENERIC_GAME_PLAYING_AGENT(GameObject,Gamestate,Algorithm_choice)
				Gamestate = GameObject.RESULT(Gamestate,action_by_min)
				index = action_by_min.find("(")
				O_row = int(action_by_min[index + 1])
				O_col = int(action_by_min[index + 3])
				OFTTTBoard.update('O',O_row,O_col)
				screen.blit(OFTTTBoard.surf, (start_hor, start_vert))
				if GameObject.TERMINAL_TEST(Gamestate):
					utility_value = GameObject.UTILITY(Gamestate)
					running = False
					Game_Over(screen,utility_value)
					#time.sleep(5)

		pygame.display.flip()

	return

def ask(screen, question):
	# "ask(screen, question) -> answer"
	current_string = ""
	screen.fill((255,100,255))
	Print_Text_On_Screen(screen, question + ": " + str(current_string) , 20,(255,0,0),200)
	pygame.display.update()
	flag = 1
	while True:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == K_BACKSPACE:
					current_string = current_string[0:-1]
				elif event.key == K_RETURN:
					flag = 0
					break
				elif event.key == K_MINUS:
					current_string + "_"
				elif event.key <= 127:
					current_string =  current_string + chr(event.key)
			screen.fill((255,100,255))
			Print_Text_On_Screen(screen, question + ": " + str(current_string),20,(255,0,0),200)
			pygame.display.update()
		if flag == 0:
			screen.fill((255,100,255))
			Print_Text_On_Screen(screen, question + ": " + str(current_string),20,(255,0,0),200)
			pygame.display.update()
	        #time.sleep(1)
			return int(current_string)


def Play_OpenFieldTicTacToe(screen,Algorithm_choice):

	running = True

	while running:

		screen.fill((120,255,255))
		dimension = ask(screen,"Enter Board dimensions , then press Enter::")
		screen.fill((120,255,255))
		connecting_length = ask(screen,"Enter Connecting Length , then press Enter:")
		screen.fill((120,255,255))
		Play_OpenFieldTicTacToeHelper(screen,Algorithm_choice,dimension,connecting_length)
		running = False
		"""
		#Print_Text_On_Screen(screen,"Enter board dimensions and connecting length:",25,(250,0,250),SCREEN_VERTICAL/5)  # STUCK here
		#Print_Text_On_Screen(screen,"YET NOT IMPLEMENTED",25,(250,0,250),SCREEN_VERTICAL/5 + 100) 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				dimension = 5
				connecting_length = 4
				Play_OpenFieldTicTacToeHelper(screen,Algorithm_choice,dimension,connecting_length)
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					dimension = 5
					connecting_length = 4
					Play_OpenFieldTicTacToeHelper(screen,Algorithm_choice,dimension,connecting_length)
					running = False

		pygame.display.flip()
		"""
	return

def Print_Text_On_Screen(screen,text_string,font_size,color,Vertical_Placement):
	font = pygame.font.Font('freesansbold.ttf', font_size) 
	text = font.render(text_string,True,color)
	textRect = text.get_rect()
	textRect.center = (SCREEN_HORIZONTAL/2,Vertical_Placement)
	screen.blit(text,textRect)

def Choose_Algorithm(screen):
	Print_Text_On_Screen(screen,"Choose the algorithm/strategy to be used by AI game playing agent:",18,(0,0,255),SCREEN_VERTICAL/5 )
	Print_Text_On_Screen(screen,"Press num key 1: Basic Minimax",20,(0,255,0),SCREEN_VERTICAL/5 + 50)
	Print_Text_On_Screen(screen,"Press num key 2: Alpha Beta Pruned Minimax",20,(0,255,0),SCREEN_VERTICAL/5 + 100)
	Print_Text_On_Screen(screen,"Press num key 3: Depth Limited Minimax",20,(0,255,0),SCREEN_VERTICAL/5 + 150)
	Print_Text_On_Screen(screen,"Press num key 4: Alpha Beta Pruned Depth Limited Minimax",20,(0,255,0),SCREEN_VERTICAL/5 + 200)
	Print_Text_On_Screen(screen,"Press num key 5: Experimental Minimax",20,(0,255,0),SCREEN_VERTICAL/5 + 250)


def Game_TicTacToe(screen):

	running = True

	while running:

		screen.fill((255,0,0))
		Print_Text_On_Screen(screen,"Welcome to Tic Tac Toe",25,(255,255,255),SCREEN_VERTICAL/5 -80)
		Choose_Algorithm(screen)
		Print_Text_On_Screen(screen,"Press ESCAPE: To Exit",20,(0,0,0),SCREEN_VERTICAL/5 + 300)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
				elif event.key == K_1:
					Play_TicTacToe(screen,1)
				elif event.key == K_2:
					Play_TicTacToe(screen,2)
				elif event.key == K_3:
					Play_TicTacToe(screen,3)
				elif event.key == K_4:
					Play_TicTacToe(screen,4)
				elif event.key == K_5:
					Play_TicTacToe(screen,5)

		pygame.display.flip()

	return


def Game_OpenFieldTicTacToe(screen):

	running = True

	while running:

		screen.fill((255,0,0))
		Print_Text_On_Screen(screen,"Welcome to Open Field Tic Tac Toe",25,(255,255,255),SCREEN_VERTICAL/5 - 80)
		Choose_Algorithm(screen)
		Print_Text_On_Screen(screen,"Press ESCAPE: To Exit",20,(0,0,0),SCREEN_VERTICAL/5 + 300)
		Print_Text_On_Screen(screen,"Warning:First 4 algorithms require",20,(0,0,255),SCREEN_VERTICAL/5 + 350)
		Print_Text_On_Screen(screen," a lot of time with larger board size.",20,(0,0,255),SCREEN_VERTICAL/5 + 380)
		Print_Text_On_Screen(screen,"It is suggested use algorithm 5:",20,(0,0,255),SCREEN_VERTICAL/5 + 410)
		Print_Text_On_Screen(screen,"Experimental Minimax in such cases.",20,(0,0,255),SCREEN_VERTICAL/5 + 440)



		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
				elif event.key == K_1:
					Play_OpenFieldTicTacToe(screen,1)
				elif event.key == K_2:
					Play_OpenFieldTicTacToe(screen,2)
				elif event.key == K_3:
					Play_OpenFieldTicTacToe(screen,3)
				elif event.key == K_4:
					Play_OpenFieldTicTacToe(screen,4)
				elif event.key == K_5:
					Play_OpenFieldTicTacToe(screen,5)

		pygame.display.flip()

	return

def StartScreen():
	pygame.init()

	screen = pygame.display.set_mode([600,600])

	pygame.display.set_caption("Games")


	running = True
	while running:


		# Fill the background with white
		screen.fill((255, 255, 255))
		Print_Text_On_Screen(screen,"Strategy Games",25,(0,255,0),SCREEN_VERTICAL/5)
		Print_Text_On_Screen(screen,"Press Number Key 1: TicTacToe",25,(0,0,255),(SCREEN_VERTICAL/5) + 50)
		Print_Text_On_Screen(screen,"Press Number Key 2: Open Field Tic Tac Toe",25,(0,0,255),(SCREEN_VERTICAL/5)+ 100)
		Print_Text_On_Screen(screen,"Press ESCAPE Key: To exit",25,(255,0,0),(SCREEN_VERTICAL/5)+ 150)
		  

		# Did the user click the window close button?
		for event in pygame.event.get():
		    if event.type == pygame.QUIT:
		        running = False
		    elif event.type == KEYDOWN:
		    	if event.key == K_ESCAPE:
		    		running = False
		    	elif event.key == K_1:
		    		Game_TicTacToe(screen)
		    	elif event.key == K_2:
		    		Game_OpenFieldTicTacToe(screen)

		# Flip the display
		pygame.display.flip()

	# Done! Time to quit.
	pygame.quit()




StartScreen()


