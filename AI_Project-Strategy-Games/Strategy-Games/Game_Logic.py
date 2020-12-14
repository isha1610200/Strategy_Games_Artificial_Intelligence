#!/usr/bin/env python
# coding: utf-8


# In[1]:


import math


# In[2]:


class GeneralGame:
    
    def __init__(self):
        self.initialState = None;
    
    def PLAYER_TURN_DETECTOR(self,state):
        raise NotImplementedError
        
    def ACTIONS(self,state):
        raise NotImplementedError
            
    def RESULT(self,state,action):
        raise NotImplementedError

    def TERMINAL_TEST(self,state):
        raise NotImplemetedError
        
    def UTILITY(self,state):
        raise NotImplemetedError
        
    def CUTOFF_TEST(self,state,depth):  #CUTOFF_TEST method : optimized a bit as compared to the traditional one(Avoid checking for (not terminal test) for depth==0 case here... ;And if it comes out to be a terminal state then handle it in heuristic evaluation ... ) ( Because--> In traditional algo. Terminal state(s) evaluated 2 times: Time waste:    if  depth == 0 and not terminal test: then Eval_heur(s) elif its a terminal state then return utility else return False)
        if depth == 0:
            return 1
        elif self.TERMINAL_TEST(state):
            return 2
        else:
            return 3
        
    def EVAL(self,state,cut_off_parameter):
        if cut_off_parameter == 2: #Problem --> depth == 0 might also be terminal state.--> Can we rectify that in heuristic eval. in some way?:: Yes,taken care of there
            return self.UTILITY(state)
        else: #means we got depth == 0 in cutoff test and it may not be a terminal state.  Well we are expecting it to be a quiescent state.
            return self.HEURISTIC_EVALUATION(state)  # may be wanna check if its quiescent state. If yes , evaluate heuristic.   If not do quiescence search as it is suggested in the book.
                  # Here , I'm implementing a simple version of Depth-limited , where I evaluate heuristic irrespective of quiescence.                     
   
    def HEURISTIC_EVALUATION(self,state):
        raise NotImplementedError


# In[3]:


# MAX places 'X' while MIN places 'O'

class TicTacToe(GeneralGame):
    
    def __init__(self):   # Earlier--> thought of taking dimension as user input here , but then Heuristic .. done for fixed 3*3n board 
        super().__init__()
        self.initialState = ([['-','-','-'],['-','-','-'],['-','-','-']],'MAX')  #We maintain gamestate as the board state and who has to move right now
        self.POSITIVE_UTILITY = 10000
        
    def PLAYER_TURN_DETECTOR(self,Gamestate):
        return Gamestate[1]
        
    def ACTIONS(self,Gamestate):
        state = Gamestate[0]
        action_list = list()
        row = -1
        col = -1
        piece = None
        if self.PLAYER_TURN_DETECTOR(Gamestate) == 'MIN':
            piece = 'O'
        else:
            piece = 'X'
        for lst in state:
            row+=1
            col = -1
            for place in lst:
                col+=1
                if place == '-':
                    # action_list.append("Can place piece at {}".format((state.index(lst),lst.index(place))) ---> definitely wrong...
                    action_list.append("Place {} at ({},{})".format(piece,row,col))
        return action_list
    
    
    def RESULT(self,Gamestate,action):
        state = Gamestate[0]
        index = action.find("(")
        row = int(action[index + 1])
        col = int(action[index + 3])
        piece = None
        next_player = None
        if self.PLAYER_TURN_DETECTOR(Gamestate) == 'MIN':
            piece = 'O'
            next_player = 'MAX'
        else:
            piece = 'X'  # OR the better way to find piece is extract it from the action
            next_player = 'MIN'
        new_state = []
        for lst in state:
            new_sub_lst = []
            for element in lst:
                new_sub_lst.append(element)
            new_state.append(new_sub_lst)
        new_state[row][col] = piece
        new_game_state = (new_state,next_player)
        return new_game_state
    
    def TERMINAL_TEST(self,Gamestate): # Game is for a sqaure board
       
        return self.__TerminalTest_Utility_Helper(Gamestate,'X') or self.__TerminalTest_Utility_Helper(Gamestate,'O') or len(self.ACTIONS(Gamestate))==0 
        
        
        
    def __TerminalTest_Utility_Helper(self,Gamestate,symbol):
        state = Gamestate[0]
        lst_terminal = []
        dimension = len(state)
        
        for i in range(dimension):   #To cover horizontal and vertical lines
            sub_lst_1 = []
            sub_lst_2 = []
            for j in range(dimension):
                sub_lst_1.append(state[i][j])
                sub_lst_2.append(state[j][i])
            lst_terminal.append(sub_lst_1)
            lst_terminal.append(sub_lst_2)
            
        sub_lst_1 = []       
        sub_lst_2 = []
        r = 0
        c = dimension-1
        for i in range(dimension):   # To cover both the diagonals
            sub_lst_1.append(state[i][i])
            sub_lst_2.append(state[r][c])
            r = r+1
            c = c-1
        lst_terminal.append(sub_lst_1)
        lst_terminal.append(sub_lst_2)
        
        sub_lst= []
        for i in range(dimension):
            sub_lst.append(symbol)
            
        if sub_lst in lst_terminal:
            return True
        else:
            return False
            
                
    def UTILITY(self,terminalGameState): # Only applicable to terminal states
        utility_val = 0
        if self.__TerminalTest_Utility_Helper(terminalGameState,'X') == True: # MAX wins
            utility_val = self.POSITIVE_UTILITY
        elif self.__TerminalTest_Utility_Helper(terminalGameState,'O') == True : # MIN wins
            utility_val = -self.POSITIVE_UTILITY
        else: # Draw situation
            utility_val = 0
        return utility_val
       
        
            
    def HEURISTIC_EVALUATION(self,Gamestate):
        board_state = Gamestate[0]
        Sum = 0
        
        for row in range(3): # For horizontals
            sub_lst = board_state[row]  # We get i th row.  ###Note: reference is copied. No worries, since not modifying anything
            heur = self.__Heuristic_Eval_Helper(sub_lst)
            if heur == self.POSITIVE_UTILITY or heur == -self.POSITIVE_UTILITY:
                return heur
            else:
                Sum = Sum + heur
                
        for col in range(3):  # For Verticals
            sub_lst = []
            for row in range(3):
                sub_lst.append(board_state[row][col])
            #Sum = Sum + self.__Heuristic_Eval_Helper(sub_lst)
            heur = self.__Heuristic_Eval_Helper(sub_lst)
            if heur == self.POSITIVE_UTILITY or heur == -self.POSITIVE_UTILITY:
                return heur
            else:
                Sum = Sum + heur
            
        sub_lst_1 = [] # For diagonals
        sub_lst_2 = []
        for i in range(3):
            sub_lst_1.append(board_state[i][i])
            sub_lst_2.append(board_state[i][2-i])
        
        
        heur1 = self.__Heuristic_Eval_Helper(sub_lst_1)
        if heur1 == self.POSITIVE_UTILITY or heur1 == -self.POSITIVE_UTILITY:
            return heur1
        else:
            Sum = Sum + heur1
        
        heur2 = self.__Heuristic_Eval_Helper(sub_lst_2)
        if heur2 == self.POSITIVE_UTILITY or heur2 == -self.POSITIVE_UTILITY:
            return heur2
        else:
            Sum = Sum + heur2
        
        #Sum = Sum + self.__Heuristic_Eval_Helper(sub_lst_1) + self.__Heuristic_Eval_Helper(sub_lst_2)
        
        return Sum
        
        
        
    def __Heuristic_Eval_Helper(self,sub_lst):
        
        LIST_T_X = [ ['X','X','X'] ]
        LIST_10 = [['X','X','-'] , ['X','-','X'] , ['-','X','X']]
        LIST_1 = [['X','-','-'] , ['-','X','-'] , ['-','-','X']]
        LIST_T_O = [['O','O','O']]
        LIST_N_10 = [['O','O','-'], ['-','O','O'] , ['O','-','O']]
        LIST_N_1 = [['O','-','-'] , ['-','O','-'], ['-','-','O']]
        
        if sub_lst in LIST_T_X:
            return self.POSITIVE_UTILITY
        elif sub_lst in LIST_10:
            return 10
        elif sub_lst in LIST_1:
            return 1
        elif sub_lst in LIST_T_O:
            return -self.POSITIVE_UTILITY
        elif sub_lst in LIST_N_10:
            return -10
        elif sub_lst in LIST_N_1:
            return -1
        else:
            return 0
        
        


# In[4]:


"""
ttt = TicTacToe()
print(ttt.ACTIONS(  ([['-','X','-'],['-','X','O'],['-','-','-']],'MAX')   ))

print(ttt.RESULT(  ([['-','X','-'],['-','X','O'],['-','-','-']],'MIN') ,"Place piece at (2,2)"))
print(ttt.TERMINAL_TEST( ([['O','X','O'],
                           ['O','X','O'],
                           ['X','O','X']],'MAX') ))
print(ttt.TERMINAL_TEST(   ([['-','X','-'],['-','X','O'],['-','-','-']],'MAX')    ))
print(ttt.TERMINAL_TEST(  ([['-','X','-'],['-','X','O'],['X','X','X']],'MIN')  ))
print(ttt.TERMINAL_TEST(  ([
                           ['X','-','O'],
                           ['O','X','X'],
                           ['O','X','X']
                            ],'MAX')   ))
print(  ttt.UTILITY(   ([
                        ['X','-','O'],
                        ['O','X','X'],
                        ['O','X','X']
                        ] , 'MAX')  ))
print(ttt.UTILITY  (  ([
                        ['O','-','O'],
                        ['O','X','X'],
                        ['O','X','X']
                        ],'MIN')   ))
print(ttt.UTILITY(      ([['O','X','O'],
                         ['O','X','O'],
                         ['X','O','X']],'MAX')   ))
print(ttt.ACTIONS  (   ([
                        ['O','-','O'],
                        ['O','X','X'],
                        ['O','X','X']],'MIN')   ))

print(ttt.HEURISTIC_EVALUATION(  ([
                        ['O','-','O'],
                        ['O','X','X'],
                        ['O','X','X']
                        ],'MIN') ))
print(ttt.HEURISTIC_EVALUATION(   ([['O','X','O'],
                                    ['O','X','O'],
                                    ['X','O','X']],'MAX')  ))
 """                                   
                                    


# In[5]:


# MAX places 'X' while MIN places 'O'

class OpenFieldTicTacToe(GeneralGame):
    
    def __init__(self,dimension,connecting_length):   # Can take user input here about the dimensions of the board and accordingly form the list. 
        super().__init__()
        initial_list = []
        for j in range(dimension):
            sub_lst = []
            for i in range(dimension):
                sub_lst.append('-')
            initial_list.append(sub_lst)
        self.initialState = (initial_list,'MAX')  #We maintain gamestate as the board state and who has to move right now
        self.dimension = dimension
        self.connecting_length = connecting_length
        self.POSITIVE_UTILITY = 10*self.connecting_length
        
    def PLAYER_TURN_DETECTOR(self,Gamestate):
        return Gamestate[1]
        
    def ACTIONS(self,Gamestate):
        state = Gamestate[0]
        action_list = list()
        row = -1
        col = -1
        piece = None
        if self.PLAYER_TURN_DETECTOR(Gamestate) == 'MIN':
            piece = 'O'
        else:
            piece = 'X'
        for lst in state:
            row+=1
            col = -1
            for place in lst:
                col+=1
                if place == '-':
                    # action_list.append("Can place piece at {}".format((state.index(lst),lst.index(place))) ---> definitely wrong...
                    action_list.append("Place {} at ({},{})".format(piece,row,col))
        return action_list
    
    
    def RESULT(self,Gamestate,action):
        state = Gamestate[0]
        index = action.find("(")
        row = int(action[index + 1])
        col = int(action[index + 3])
        piece = None
        next_player = None
        if self.PLAYER_TURN_DETECTOR(Gamestate) == 'MIN':
            piece = 'O'
            next_player = 'MAX'
        else:
            piece = 'X'  # OR the better way to find piece is extract is from the action
            next_player = 'MIN'
        new_state = []
        for lst in state:
            new_sub_lst = []
            for element in lst:
                new_sub_lst.append(element)
            new_state.append(new_sub_lst)
        new_state[row][col] = piece
        new_game_state = (new_state,next_player)
        return new_game_state
    
    def TERMINAL_TEST(self,Gamestate): # Game is for a sqaure board
       
        return self.__TerminalTest_Utility_Helper(Gamestate,'X') or self.__TerminalTest_Utility_Helper(Gamestate,'O') or len(self.ACTIONS(Gamestate))==0 
        
        
        
    
    def __TerminalTest_Utility_Helper(self,Gamestate,symbol):
        board_state = Gamestate[0]
        dimension = self.dimension
        connecting_length = self.connecting_length
        
        
        for row in range(dimension):  # TO cover horizontals
            for start in range(dimension - connecting_length + 1):
                #if board_state[row][start:start + connecting_length] == check_lst:
                #    return True
                flag = 1
                for col in range(connecting_length):
                    if board_state[row][col + start] != symbol:
                        flag = 0
                if flag == 1:
                    return True

        for col in range(dimension): # TO COVER VERTICALS
            for start in range(dimension - connecting_length + 1):
                # Check for a vertical
                flag = 1
                for row in range(connecting_length):
                    if board_state[start + row][col] != symbol:
                        flag = 0
                if flag == 1:
                    return True

        def CHECK_MAIN_DIAGONAL(row,col):  # From an individual place
            if row + connecting_length <= dimension and col + connecting_length <= dimension:
                r = row
                c = col
                for i in range(connecting_length):
                    if board_state[r][c] != symbol:
                        return False
                    r = r+1
                    c = c+1
                return True                
            else:
                return False



        def CHECK_OTHER_DIAGONAL(row,col): # From an individual place
            if row + connecting_length <= dimension and col - connecting_length + 1>= 0:
                r = row
                c = col
                for i in range(connecting_length):
                    if board_state[r][c] != symbol:
                        return False
                    r = r+1
                    c = c-1
                return True                
            else:
                return False



        for row in range(dimension):  # Checking diagonals from an individual place
            for col in range(dimension):
                if CHECK_MAIN_DIAGONAL(row,col) == True or CHECK_OTHER_DIAGONAL(row,col) == True:
                    return True

        return False  


            
                
    def UTILITY(self,terminalGameState): # Only applicable to terminal states
        utility_val = 0
        if self.__TerminalTest_Utility_Helper(terminalGameState,'X') == True: # MAX wins
            utility_val = 10*self.connecting_length
        elif self.__TerminalTest_Utility_Helper(terminalGameState,'O') == True : # MIN wins
            utility_val = -10*self.connecting_length
        else: # Draw situation
            utility_val = 0
        return utility_val
       
        
    def HEURISTIC_EVALUATION(self,Gamestate):
        board_state = Gamestate[0]
        Sum = 0
        
        dimension = self.dimension
        connecting_length = self.connecting_length

        sub_lst = []
        for row in range(dimension):  # TO cover horizontals
            for start in range(dimension - connecting_length + 1):
                sub_lst = board_state[row][start:start + connecting_length]
                heur = self.__Heuristic_Eval_Helper(sub_lst)
                if heur[1] == 'Terminal':
                    return heur[0]
                else:
                    Sum = Sum + heur[0]

        
        for col in range(dimension): # TO COVER VERTICALS
            for start in range(dimension - connecting_length + 1):
                sub_lst = []
                # Check for a vertical
                for row in range(connecting_length):
                    sub_lst.append(board_state[start + row][col])
                heur = self.__Heuristic_Eval_Helper(sub_lst)
                if heur[1] == 'Terminal':
                    return heur[0]
                else:
                    Sum = Sum + heur[0]

                        
               

        def Heuristic_CHECK_MAIN_DIAGONAL(row,col):  # From an individual place
            if row + connecting_length <= dimension and col + connecting_length <= dimension:
                r = row
                c = col
                sub_lst = []
                for i in range(connecting_length):
                    sub_lst.append(board_state[r][c])
                    r = r+1
                    c = c+1
                return self.__Heuristic_Eval_Helper(sub_lst)
            else:
                return (0,'**')



        def Heuristic_CHECK_OTHER_DIAGONAL(row,col): # From an individual place
            if row + connecting_length <= dimension and col - connecting_length + 1>= 0:
                r = row
                c = col
                sub_lst = []
                for i in range(connecting_length):
                    sub_lst.append(board_state[r][c])
                    r = r+1
                    c = c-1
                return self.__Heuristic_Eval_Helper(sub_lst)                
            else:
                return (0,'**')



        for row in range(dimension):  # Checking diagonals from an individual place
            for col in range(dimension):
                tup1 = Heuristic_CHECK_MAIN_DIAGONAL(row,col)
                tup2 = Heuristic_CHECK_OTHER_DIAGONAL(row,col)
                if tup1[1] == 'Terminal':
                    return tup1[0]
                if tup2[1] == 'Terminal':
                    return tup2[0]
                else:
                    Sum = Sum + tup1[0] + tup2[0]
                   
 
        return Sum


    def __Heuristic_Eval_Helper(self,sub_lst):
        dimension = self.dimension
        connecting_length = self.connecting_length
        
        count_X = 0
        count_O = 0
        
        for symbol in sub_lst:
            if symbol == 'X':
                count_X = count_X + 1
            elif symbol == 'O':
                count_O = count_O + 1
            else:
                pass
        
        if count_X == connecting_length:
            return (self.POSITIVE_UTILITY,'Terminal') # remember , it should match with utility method
        
        if count_O == connecting_length:
            return (-self.POSITIVE_UTILITY,'Terminal') # remeber , it should match with utility method
            
        if count_X > 0 and count_O == 0:
            return (2*count_X,'NonT')
        
        elif count_O > 0 and count_X == 0:
            return (-2*count_O,'NonT')
        
        else:
            return (0,'NonT')
        


# In[6]:




def MINIMAX_VALUE(GameObject,Gamestate):
    player = GameObject.PLAYER_TURN_DETECTOR(Gamestate)
    if GameObject.TERMINAL_TEST(Gamestate):
        return GameObject.UTILITY(Gamestate)
    elif player == 'MAX':
        value = -math.inf
        for action in GameObject.ACTIONS(Gamestate):
            value = max(value,MINIMAX_VALUE(GameObject, GameObject.RESULT(Gamestate,action)))
        return value
    else: # means MIN player
        value = math.inf
        for action in GameObject.ACTIONS(Gamestate):
            value = min(value,MINIMAX_VALUE(GameObject,GameObject.RESULT(Gamestate,action)))
        return value


# In[7]:



#import math
#print(type(math.inf))


# In[9]:


def COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNING(GameObject,Gamestate,alpha = -math.inf,beta = math.inf):
    player = GameObject.PLAYER_TURN_DETECTOR(Gamestate)
    if GameObject.TERMINAL_TEST(Gamestate):
        return GameObject.UTILITY(Gamestate)
    elif player == 'MAX':
        value = -math.inf
        for action in GameObject.ACTIONS(Gamestate):
            value = max(value,COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNING(GameObject, GameObject.RESULT(Gamestate,action),alpha,beta))
            if value>= beta:
                return value
            aplha = max(alpha,value)
        return value
    else: # means MIN player
        value = math.inf
        for action in GameObject.ACTIONS(Gamestate):
            value = min(value,COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNING(GameObject,GameObject.RESULT(Gamestate,action),alpha,beta))
            if value<= alpha:
                return value
            beta = min(beta,value)
        return value


# In[10]:


def COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNING_SLIDE(GameObject,Gamestate,alpha = -math.inf,beta = math.inf):
    player = GameObject.PLAYER_TURN_DETECTOR(Gamestate)
    if GameObject.TERMINAL_TEST(Gamestate):
        return GameObject.UTILITY(Gamestate)
    elif player == 'MAX':
        value = -math.inf
        for action in GameObject.ACTIONS(Gamestate):
            value = max(value,COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNING_SLIDE(GameObject, GameObject.RESULT(Gamestate,action),alpha,beta))
            if beta <= alpha:
                return value
            aplha = max(alpha,value)
        return value
    else: # means MIN player
        value = math.inf
        for action in GameObject.ACTIONS(Gamestate):
            value = min(value,COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNING_SLIDE(GameObject,GameObject.RESULT(Gamestate,action),alpha,beta))
            if beta<= alpha:
                return value
            beta = min(beta,value)
        return value


# In[11]:




def COMPUTE_MINIMAX_VALUE_DEPTH_LIMITED(GameObject,Gamestate,depth):
    player = GameObject.PLAYER_TURN_DETECTOR(Gamestate)
    cut_off_test = GameObject.CUTOFF_TEST(Gamestate,depth)
    if cut_off_test == 1 or cut_off_test == 2:
        return GameObject.EVAL(Gamestate,cut_off_test)
    elif player == 'MAX':
        value = -math.inf
        for action in GameObject.ACTIONS(Gamestate):
            value = max(value,COMPUTE_MINIMAX_VALUE_DEPTH_LIMITED(GameObject, GameObject.RESULT(Gamestate,action),depth-1))
        return value
    else: # means MIN player
        value = math.inf
        for action in GameObject.ACTIONS(Gamestate):
            value = min(value,COMPUTE_MINIMAX_VALUE_DEPTH_LIMITED(GameObject,GameObject.RESULT(Gamestate,action),depth-1))
        return value


# In[12]:


def COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNED_DEPTH_LIMITED(GameObject,Gamestate,depth,alpha = -math.inf,beta = math.inf):
    player = GameObject.PLAYER_TURN_DETECTOR(Gamestate)
    cut_off_test = GameObject.CUTOFF_TEST(Gamestate,depth)
    if cut_off_test == 1 or cut_off_test == 2:
        return GameObject.EVAL(Gamestate,cut_off_test)
    elif player == 'MAX':
        value = -math.inf
        for action in GameObject.ACTIONS(Gamestate):
            value = max(value,COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNED_DEPTH_LIMITED(GameObject, GameObject.RESULT(Gamestate,action),depth-1,alpha,beta))
            if value>= beta:
                return value
            aplha = max(alpha,value)
        return value
    else: # means MIN player
        value = math.inf
        for action in GameObject.ACTIONS(Gamestate):
            value = min(value,COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNED_DEPTH_LIMITED(GameObject,GameObject.RESULT(Gamestate,action),depth-1,alpha,beta))
            if value<= alpha:
                return value
            beta = min(beta,value)
        return value


# In[13]:


from time import time

def Timeout(start_time,time_limit):
    current_time = time()
    seconds_elapsed = current_time - start_time
    #print(seconds_elapsed)
    if seconds_elapsed >= time_limit:
        return True
    else:
        return False




def COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNED_DEPTH_LIMITED_TRANSPOSITION_TABLE(GameObject,Gamestate,depth,Transposition_table, alpha = -math.inf,beta = math.inf):
    #print("\nHello")
    player = GameObject.PLAYER_TURN_DETECTOR(Gamestate)
    cut_off_test = GameObject.CUTOFF_TEST(Gamestate,depth)
    if cut_off_test == 1 or cut_off_test == 2:
        return GameObject.EVAL(Gamestate,cut_off_test)
    NewLst = []
    for lst in Gamestate[0]:
        NewLst.append(tuple(lst))
    tup = tuple(NewLst)

     # Lookup Transposition table and return val.

    if tup in Transposition_table.keys():
            return Transposition_table[tup]
    else: # Means not available in transposition table 
        if player == 'MAX':
            value = -math.inf
            for action in GameObject.ACTIONS(Gamestate):
                value = max(value,COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNED_DEPTH_LIMITED_TRANSPOSITION_TABLE(GameObject, GameObject.RESULT(Gamestate,action),depth-1,Transposition_table, alpha,beta))
                if value>= beta:
                    return value
                aplha = max(alpha,value)
         #Store in transposition table
            Transposition_table[tup] = value 
            return value

        else: # means MIN player
            value = math.inf
            for action in GameObject.ACTIONS(Gamestate):
                value = min(value,COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNED_DEPTH_LIMITED_TRANSPOSITION_TABLE(GameObject,GameObject.RESULT(Gamestate,action),depth-1, Transposition_table ,alpha,beta))
                if value<= alpha:
                    return value
                beta = min(beta,value)
            #Store in  Transposition table
            Transposition_table[tup] = value
            return value




def EXPERIMENTAL_MINIMAX(GameObject,Gamestate,time_limit = 0.2):
    #print("Hi")
    if len(Gamestate[0]) < 4:
        return COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNED_DEPTH_LIMITED(GameObject,Gamestate,3)
    else:
        depth =1
        Transposition_table = {}
        start_time = time()
        time_limit = 0.04 # in seconds
        if len(Gamestate[0]) >= 5:
            time_limit = 0.02 # in seconds
        elif len(Gamestate[0]) >= 8:
            time_limit = 0.002
        while not Timeout(start_time,time_limit):
           # print("In loop")
            minimax_val = COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNED_DEPTH_LIMITED_TRANSPOSITION_TABLE(GameObject,Gamestate,depth,Transposition_table)
            depth = depth + 1
        return minimax_val



# In[14]:


def PRINT_GAME_STATE(current_board_state):
    for lst in current_board_state:
        print(lst)


def MAX_MOVE(GameObject,Gamestate): # by HUMAN ---> called when the GameState has 'MAX'
    print('Game state is:')
    PRINT_GAME_STATE(Gamestate[0])
    print('\nIts your turn:')
    print(' Legal actions:')
    i = 0
    action_list = GameObject.ACTIONS(Gamestate)
    for action in action_list:
        print("{}). {}".format(i,action))
        i = i+1
    action_index = int(input("Enter action index:"))
    return action_list[action_index]
    
    


# In[15]:


def HELPER_FOR_MIN_PLAYER_MOVE(GameObject,Gamestate,choice):
    val = math.inf
    for action in GameObject.ACTIONS(Gamestate):
        childNode = GameObject.RESULT(Gamestate,action)
        if choice == 1:
            minimax_val_child_node = MINIMAX_VALUE(GameObject,childNode)
        elif choice == 2:
        #minimax_val_child_node = COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNING_SLIDE(GameObject,childNode)
            minimax_val_child_node = COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNING(GameObject,childNode)
        elif choice == 3:
            minimax_val_child_node = COMPUTE_MINIMAX_VALUE_DEPTH_LIMITED(GameObject,childNode,5)
        elif choice == 4:
            minimax_val_child_node = COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNED_DEPTH_LIMITED(GameObject,childNode,3)
        else:
            minimax_val_child_node = EXPERIMENTAL_MINIMAX(GameObject,childNode)
        if val > minimax_val_child_node:
            val = minimax_val_child_node
            favourable_action = action
    return favourable_action


# In[16]:


def NEXT_MOVE(GameObject,Gamestate,choice): # by AI --->called  when the GameState has 'MIN'
    print('\n\n\nGame state is:')
    PRINT_GAME_STATE(Gamestate[0])
    print('\nIts my turn:')
    favourable_action =  HELPER_FOR_MIN_PLAYER_MOVE(GameObject,Gamestate,choice) ## ---> Here at this place , can change algorithms like alpha -beta pruning etc
    print('I will do:{}'.format(favourable_action))
    return favourable_action        

def GENERIC_GAME_PLAYING_AGENT(GameObject,Gamestate,choice):
    return NEXT_MOVE(GameObject,Gamestate,choice)        

# In[17]:



def PlayGame(GameObject,choice):
    Gamestate = GameObject.initialState
    while(GameObject.TERMINAL_TEST(Gamestate) is False): 
        if GameObject.PLAYER_TURN_DETECTOR(Gamestate) == 'MAX':
            action_by_max = MAX_MOVE(GameObject,Gamestate)  # Move by Human  NOTE:Here Gamestate indeed has 'MAX'
            Gamestate = GameObject.RESULT(Gamestate,action_by_max)
            print("\n------------------------------------------------------------------------------------\n")
        else:
            s_time = time()
            action_by_min = GENERIC_GAME_PLAYING_AGENT(GameObject,Gamestate,choice)
            e_time = time()
            print("Time taken by Game playing agent in seconds for a move:", e_time - s_time , "\n")
            Gamestate = GameObject.RESULT(Gamestate,action_by_min)
            print("\n****************************************************************************************\n")
    utility_value = GameObject.UTILITY(Gamestate)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    print("The terminal GameState is:")
    PRINT_GAME_STATE(Gamestate[0])
    if(utility_value > 0):
        print("\nYou Win")
    elif(utility_value < 0):
        print("\nAI wins")
    else:
        print("\nDRAW")


# In[18]:


"""
GameObject = TicTacToe()
PlayGame(GameObject,4)
"""


# In[19]:


#GameObject = TicTacToe()
"""
Game state is:
['-', 'O', '-']
['-', '-', '-']
['X', '-', 'X']

Its my turn:
I will do:Place O at (0,0)

"""
"""
current_board_state = [ ['-','O','-'] , ['-','-','-'],['X','-','X']]
current_game_state = (current_board_state , 'MIN')

state_1 = ([ ['O','O','-'] , ['-','-','-'],['X','-','X']],'MAX' )
state_2 = ([ ['-','O','-'] , ['-','-','-'],['X','O','X']],'MAX')
state_3 = ([ ['O','O','O'] , ['-','-','-'],['X','-','X']],'MAX' )
print(COMPUTE_MINIMAX_VALUE_DEPTH_LIMITED(GameObject,state_1,100))
print(COMPUTE_MINIMAX_VALUE_DEPTH_LIMITED(GameObject,state_2,100))
print(MINIMAX_VALUE(GameObject,state_1))
print(MINIMAX_VALUE(GameObject,state_2))
print(GameObject.HEURISTIC_EVALUATION(state_2))
"""


# In[20]:


"""
GameObject = OpenFieldTicTacToe(4,3)    #TicTacToe is basically OpenFieldTicTacToe(3,3)  
PlayGame(GameObject,4)
"""


# In[ ]:


""" ---> Text For refernece
Game state is:
['X', 'O', '-', '-']
['X', '-', '-', '-']
['-', '-', '-', '-']
['-', '-', '-', '-']

Its my turn:
I will do:Place O at (0,2)
"""

"""
current_board_state = [
    ['X','O','-','-'],
    ['X','-','-','-'],
    ['-','-','-','-'],
    ['-','-','-','-']
]

current_game_state = (current_board_state,'MIN')

state_1 = ( 
    [
    ['X','O','O','-'],
    ['X','-','-','-'],
    ['-','-','-','-'],
    ['-','-','-','-']
] , 'MAX'
)

state_2 =  ( 
    [
    ['X','O','-','-'],
    ['X','-','-','-'],
    ['O','-','-','-'],
    ['-','-','-','-']
] , 'MAX'
)

v1 = COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNING_SLIDE(GameObject,state_1)
v2 = COMPUTE_MINIMAX_VALUE_ALPHA_BETA_PRUNING_SLIDE(GameObject,state_2)
print(v1)
print(v2)
"""


# In[ ]:


def USER_OPTIONS():
    game_number = int(input("Enter 1 to play Tic Tac Toe while 2 to play Open Field Tic Tac Toe:"))
    GameObject = None
    if game_number == 1:
        GameObject = TicTacToe()
    elif game_number == 2:
        n = int(input("\nEnter n for n*n board:"))
        l = int(input("Enter connecting length:"))
        GameObject = OpenFieldTicTacToe(n,l)
    else:
        pass
    print("\nChoose the algorithm you want:")
    print("\n1.Basic Minimax\n2.Minimax with Alpha Beta Pruning\n3.Minimax with depth limit\n4.Minimax with both depth limit and alpha beta pruning \n5.Experimental Minimax\n")
    choice = int(input("Enter your choice:"))
    PlayGame(GameObject,choice)
    
    
#USER_OPTIONS()


#References:
# https://github.com/Cledersonbc/tic-tac-toe-minimax/blob/master/py_version/minimax.py
# https://www3.ntu.edu.sg/home/ehchua/programming/java/JavaGame_TicTacToe_AI.html --->used this for heuristic
# https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-tic-tac-toe/
# https://github.com/nishchal91/4x4-Tic-Tac-Toe
# https://cs.nyu.edu/courses/fall98/V22.0480-003/hwk6.html