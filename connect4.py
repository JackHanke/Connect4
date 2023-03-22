from os import system
from sys import platform
from random import randint
from time import sleep

if platform == 'win32': clear_string = 'cls'
if platform in ('darwin', 'linux'): clear_string = 'clear'

class chararray:
    def __init__(self,tuple,state=None):
        self.height = tuple[0]
        self.width = tuple[1]
        if state is None:
            self.lst = []
            for _ in range(self.height):
                row = []
                for _ in range(self.width):
                    row.append('_')
                self.lst.append(row)
        else:
            self.lst = state


    def __getitem__(self,index):
        return self.lst[index]

    def refresh(self):
        for row in range(self.height):
            for column in range(self.width):
                self.lst[row][column] = '_'

    def __repr__(self):
        return self.lst.__repr__()

    def copyboard(self):
        return_lst = []

        for lst in self.lst:
            copied_list = lst.copy()
            return_lst.append(copied_list)

        return chararray((self.height,self.width),return_lst)

#win condition determines if the most recent placement won the game
#i is the y coord, read from top, j is the x coord, read from left
def win_condition(i,j,board, current_player):
    #test if the current cell is viable to look at
    def test(_i,_j):
        #if out of bounds
        if _i < 0 or _i >= board.board_height or _j < 0 or _j >= board.board_width:
            return False

        #if empty
        value = board.board_matrix[_i][_j]
        if value == '_':
            return False

        #if opposite marker
        if (value == '#' and current_player == -1) or (value == 'O' and current_player == 1):
            return False

        return True

    #possible suroundings
    surrounding = [(i-1,j-1),(i,j-1),(i+1,j-1),(i+1,j),(i+1,j+1),(i,j+1),(i-1,j+1)]
    #test viable locations
    to_check=[]
    for item in surrounding:
        if test(item[0],item[1]):
            to_check.append(item)

    #test viables for connect four
    for item in to_check:
        delta_i = i-item[0]
        delta_j = j-item[1]
        #if the opposite direction is also viable
        if (i+delta_i,j+delta_j) in to_check:
            if test(i+2*delta_i,j+2*delta_j) or test(i-2*delta_i,j-2*delta_j):
                #inside win!
                return True
        else:
            if test(i-2*delta_i,j-2*delta_j) and test(i-3*delta_i,j-3*delta_j):
                #ray win
                return True

    return False

class Board:
    def __init__(self, board_height=6, board_width=7, board_state=None, whosmove=1):
        if board_state is None:
            self.board_matrix = chararray((board_height,board_width))
            self.board_matrix.refresh()

        else:
            self.board_matrix = board_state

        self.board_width = board_width
        self.board_height = board_height
        self.whosmove = whosmove

    def __bool__(self): return self.board_matrix[self.board_height-1] == ['_' for i in range(self.board_width)]

    def __repr__(self):
        board_labels = '|'
        divider = '|'
        for i in range(self.board_width):
            board_labels += ' ' + str(i+1) + ' '
            divider += '---' 
        board_labels += '|'
        divider += '|'

        board_string = ''
        for index, row in enumerate(self.board_matrix):
            board_string += '|'
            for item in row:
                board_string += ' ' + item + ' '
            
            if index == self.board_height-1:
                board_string += '|'
            else:
                board_string += '| \n'

        return board_string + '\n' + divider + '\n' + board_labels + '\n' + divider

    def update(self, column):
        column -= 1
        #dropping piece down...
        for i in range(self.board_height):
            position = self.board_height - 1 - i
            if self.board_matrix[position][column] == '_':
                if self.whosmove == 1: self.board_matrix[position][column] = '#'
                if self.whosmove == -1: self.board_matrix[position][column] = 'O'
                
                win = win_condition(position, column, self, self.whosmove)
                self.whosmove *= -1
                if win: return 'win'
                elif '_' not in self.board_matrix[0]: return 'draw'
                
                return 'continue'

        raise Exception

    def best_move(self, max_depth, verbose=False):
        def board_evaluation(board): return 0

        class Node:
            def __init__(self,data, depth = 0,parent = None, children = None, move_from_parent=None):
                self.data = data #board state
                self.eval = None #board eval
                self.depth = depth
                self.parent = parent
                self.move_from_parent = move_from_parent # the move taken to arrive at the node from it's parent    
                if children is None: self.children = []
                else: self.children = children
            
        #game tree class
        class Tree():
            def __init__(self,root, whosmoveroot):
                self.root = root
                self.whosmoveroot = whosmoveroot

            def make(self,max_depth,verbose):
                def help(node,max_depth,verbose):
                    for column in range(node.data.board_width):
                        if node.data.board_matrix[0][column] == '_':
                            new_board = Board(board_state=node.data.board_matrix.copyboard(), whosmove=node.data.whosmove)
                            update = new_board.update(column+1)
                            new_node = Node(data=new_board,move_from_parent=column+1, depth=node.depth+1)
                            node.children.append(new_node)
                            
                            if update == 'win' : new_node.eval = float('inf') * self.whosmoveroot * (1 - 2*(node.depth % 2))
                            elif update == 'draw': new_node.eval = 0
                            #if at the bottom of the tree, evaluate the board
                            elif new_node.depth == max_depth: new_node.eval = board_evaluation(new_node.data.board_matrix)
                            else: help(new_node, max_depth, verbose)
                                
                help(self.root, max_depth, verbose)

            def score(self, verbose):
                def help(node, verbose):
                    if node.eval is not None: return node.eval

                    if self.whosmoveroot*(2*(node.depth % 2)-1) == 1:
                        minscore = float('inf')
                        for child in node.children:
                            node.eval = help(child,verbose)
                            if node.eval < minscore:
                                minscore = node.eval
                            if child.depth <= 2 and verbose: 
                                print(child.data)
                                print('eval:',child.eval, 'move from parent:', child.move_from_parent, 'depth:', child.depth)
                        node.eval = minscore
                        return minscore
                
                    else:
                        maxscore = -float('inf')
                        for child in node.children:
                            node.eval = help(child,verbose)
                            if node.eval > maxscore:
                                maxscore = node.eval
                            if child.depth <=2 and verbose: 
                                print(child.data)
                                print('eval:',child.eval, 'move from parent:', child.move_from_parent, 'depth:', child.depth)
                        node.eval = maxscore
                        return maxscore

                return help(self.root, verbose)

            def best(self):
                if self.whosmoveroot == 1:
                    best_moves = []
                    maxscore = -float('inf')
                    for child in self.root.children:
                        if child.eval > maxscore: 
                            maxscore = child.eval
                            best_moves = [child.move_from_parent]
                        elif child.eval == maxscore:
                            best_moves.append(child.move_from_parent)

                    return best_moves[randint(0, len(best_moves)-1)]
                
                elif self.whosmoveroot == -1:
                    minscore = float('inf')
                    best_moves = []
                    for child in self.root.children:
                        if child.eval < minscore: 
                            minscore = child.eval
                            best_moves = [child.move_from_parent]
                        elif child.eval == minscore:
                            best_moves.append(child.move_from_parent)

                    return best_moves[randint(0,len(best_moves)-1)]

        return_tree = Tree(root=Node(data=self), whosmoveroot = self.whosmove)
        
        return_tree.make(max_depth, verbose)
        return_tree.score(verbose)
        return_val = return_tree.best()
        return return_val


#takes type input_type, set of accepted responses, and a error message return_string if right type but non-considered value, func always accepts quit, Quit, q, Q
def player_input(input_type, accepted, return_string):
    given = input()
    while True:
        try:
            if str(given) in ('Quit','quit','q','Q'):
                print('Game Quit.')
                break
            if input_type(given) in accepted:
                given = input_type(given)
                return given     
            else:
                given = input_type(given)
                print(return_string)
                given = input()
        except:
            if input_type == int: print('Not an integer! Please try again.')
            if input_type == str: print('Not an string! Please try again.')
            given = input()

def player_text_input(forbidden_string_lst = None): # takes users text input and returns it as long as it is not in a list of forbidden strings
    if forbidden_string_lst is None: forbidden_string_lst = []
    given = input()
    while True:
        if str(given) in ('Quit','quit','q','Q'):
                print('Game Quit.')
                break
        if given in forbidden_string_lst:
            print('You can\'t use that name! Choose another.')
            given = input()
        if len(given) > 50:
            print('The entered name is too long. Try entering a name less than 50 characters.')
            given = input()
        if len(given) == 0:
            print('The entered name is too short. Try entering a name that is atleast 1 character long.')
            given = input()
        if len(given) > 0 and len(given) <= 50 and given not in ('Quit','quit','q','Q') and given not in forbidden_string_lst:
            return given

class Player:
    def __init__(self, name, alias, computer=False):
        self.name = name
        self.alias = alias
        self.computer = computer #boolean if whether or not the player is the computer

class Game:
    def __init__(self, player1, player2):
        self.board=Board()
        self.player1 = player1 
        self.player2 = player2
        self.current_player = self.player1
        self.moves = 0

    def start(self):    
        print(self.board)
        result = 'continue'

        while True: #gameloop
            if not self.current_player.computer:
                print('{}\'s turn'.format(self.current_player.name))
                while True:
                    chosen_position = player_input(int, (1,2,3,4,5,6,7), 'Please enter integer 1 - 7.')
                    if chosen_position is None: return [0,0] # if user quits out here, they do not want to play again.
                    else:
                        result = self.board.update(chosen_position)
                        if result != 'illegal': break
                        print('That position is filled. Choose another location.')
                        
            if self.current_player.computer: 
                print('Computer\'s turn')
                chosen_position = self.board.best_move(max_depth=6) #give the computer what turn it is
                result = self.board.update(chosen_position)

            system(clear_string)
            print(self.board)
            if result in ('win', 'draw'):
                system(clear_string)
                print(self.board)
                if result == 'win':
                    print('{} wins!\n'.format(self.current_player.name))
                elif result == 'draw':
                    print('It\'s a draw!\n')
                return_lst = [0,0]
                if result == 'win': return_lst[self.current_player.alias-1] = 1
                elif result == 'draw': return_lst = [0.5,0.5]
                return return_lst

            if self.current_player.alias == 1: self.current_player = self.player2
            elif self.current_player.alias == 2: self.current_player = self.player1

class Session:
    def __init__(self):
        self.rivalries_dict = {}

    def start(self):
        system(clear_string)
        print('-----Welcome to Connect 4-----\n')
        sleep(0.5)
        
        play_again=True
        while play_again:
            
            print('Enter player names. Enter \'Computer\' for either Player 1 or Player 2 to play the computer.\n')

            sleep(0.5)

            print('What would you like Player 1\'s name to be?')
            name_1 = player_text_input()
            if name_1 is None: return False # if user quits out here, they do not want to play again.
            elif name_1 == 'Computer': self.player1 = Player(name='Computer', alias=1, computer=True)
            else: self.player1 = Player(name=name_1, alias = 1)

            print('What would you like Player 2\'s name to be?')
            name_2 = player_text_input([self.player1.name])
            if name_2 is None: return False # if user quits out here, they do not want to play again.
            elif name_2 == 'Computer': self.player2 = Player(name='Computer', alias=2, computer=True)
            else: self.player2 = Player(name=name_2, alias = 2)

            try:
                self.rivalries_dict[(name_1.lower(), name_2.lower())][0]
                self.rivalries_dict[(name_2.lower(), name_1.lower())][0]
            except KeyError:
                self.rivalries_dict[(name_1.lower(), name_2.lower())] = [0,0]
                self.rivalries_dict[(name_2.lower(), name_1.lower())] = [0,0]
            system(clear_string)

            print('Enter \'Quit\' at anytime to exit the game.\n')
            system(clear_string)
            game_result = Game(player1 = self.player1, player2 = self.player2).start()

            self.rivalries_dict[(name_1.lower(), name_2.lower())][0] += game_result[0]
            self.rivalries_dict[(name_1.lower(), name_2.lower())][1] += game_result[1]

            name1score = self.rivalries_dict[(name_1.lower(), name_2.lower())][0] + self.rivalries_dict[(name_2.lower(), name_1.lower())][1]
            name2score = self.rivalries_dict[(name_2.lower(), name_1.lower())][0] + self.rivalries_dict[(name_1.lower(), name_2.lower())][1]
            if name1score == 1: s1 = ''
            else: s1 = 's'
            if name2score == 1: s2 = ''
            else: s2 = 's'
            if name1score + name2score != 0: print('The running total is {} point{} for {} and {} point{} for {}.\n'.format(name1score,s1,name_1,name2score,s2,name_2))

            print('Would you like to play again?')
            play_again = player_input(str, ('yes', 'Yes', 'y', 'no', 'No', 'n'), 'Please enter \'Yes\' or \'No\'')
            if play_again in ('no', 'No', 'n') or play_again is None: play_again = False
            if play_again in ('yes', 'Yes', 'y'): play_again = True

if __name__ == '__main__': Session().start()
