from os import system

class chararray:
    def __init__(self,tuple,state=None):
        self.height = tuple[0]
        self.width = tuple[1]
        if state is None:
            self.lst = []
            for i in range(self.height):
                row = []
                for j in range(self.width):
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
    def __init__(self, board_height=6, board_width=7, board_state=None):
        if board_state is None:
            self.board_matrix = chararray((board_height,board_width))
            self.board_matrix.refresh()

        else:
            self.board_matrix = board_state

        self.board_width = board_width
        self.board_height = board_height

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

    #tries to update board with given column and player obj, returns tuple:
    #tuple contains (if the chosen column updated the board, and the status of the game after the update{cont, draw, win})
    def update_board(self, column, current_player):
    
        column -= 1
        #dropping piece down...
        for i in range(self.board_height):
            position = self.board_height - 1 - i
            #if at lowest point, add respective marker
            if self.board_matrix[position][column] == '_':
                if current_player == 1:
                    self.board_matrix[position][column] = '#'
                if current_player == -1:
                    self.board_matrix[position][column] = 'O'

                #win condition in connect4comp
                win = win_condition(position, column, self, current_player)
                draw = '_' not in self.board_matrix[0]
                
                if win:
                    return 'win'
                elif draw:
                    return 'draw'

                return 'continue'

        raise Exception
    
    def refresh_board(self):
        self.board_matrix = chararray((self.board_height,self.board_width))
        self.board_matrix.refresh()

    #returns true if new board, false if there have been moves made
    def __bool__(self):
        return self.board_matrix[self.board_height-1] == ['_' for i in range(self.board_width)]

#evaluates non-won positions. This can and should be extended
def board_evaluation(board,player):
    return 0

class Node:
    def __init__(self,data=None,parent = None,
                    children=None, depth=0, evaluation = None, 
                    move_to_parent=1, node_id = None, move_container = None):
        self.data = data
        self.parent = parent
        self.move_to_parent = move_to_parent
        self.depth = depth
        self.evaluation = evaluation
        if node_id is None:
            self.node_id = str(self.move_to_parent)+'-'+str(self.depth)
        else:
            self.node_id = node_id

        if children is None:
            self.children = []
        else:
            self.children = children
        self.move_container = move_container
    
class Tree():
    def __init__(self,root_node_obj=None):
        #if no node is given, it is the node with empty board
        if root_node_obj is None:
            self.root_node = Node(data=Board())
        #else it is a node that must have a board specified as its data attribute
        else:
            self.root_node = root_node_obj

    def __repr__(self):

        def print_node(node):
            if node is None:
                return ''
            else:
                #conditional for troubleshooting
                if node.depth <= 2:
                    print(node.data)
                    print(f'Depth:{node.depth} Eval:{node.evaluation} MoveToParent:{node.move_to_parent} MoveContainer:{node.move_container}')
                for child in node.children:
                    print_node(child)
                return ''
        
        return print_node(self.root_node)


    #max depth int >= 1
    def make_tree(self,max_depth,turn,root_node=None):
        #if first time
        if root_node is None:
            root_node = self.root_node

        for column in range(root_node.data.board_width):
            #if chosen column is legal
            if root_node.data.board_matrix[0][column] == '_':
                #copy the board
                new_board = Board(board_state=root_node.data.board_matrix.copyboard())
                update = new_board.update_board(column+1,turn)
                #make these boards roots of subtrees
                new_node = Node(data=new_board,move_to_parent=column+1, depth=root_node.depth+1)
                root_node.children.append(new_node)
                
                #if this move wins, evaluate the board
                if update == 'win' :
                    #new_node.move_container = new_node.move_to_parent
                    new_node.evaluation = float('inf') * turn 

                elif update == 'draw':
                    #new_node.move_container = new_node.move_to_parent
                    new_node.evaluation = 0

                #if at the bottom of the tree, evaluate the board
                elif new_node.depth == max_depth:
                    #new_node.move_container = new_node.move_to_parent
                    new_node.evaluation = board_evaluation(new_node.data.board_matrix, turn)

                else:
                    self.make_tree(max_depth, root_node = new_node, turn = turn * -1)

    #score gametree
    def score_tree(self,turn,root_node=None):
        if root_node.evaluation is not None:
            return root_node.evaluation

        else:
            minimum_score = float('inf')
            for child in root_node.children:
                root_node.evaluation = -1 * turn * self.score_tree(turn = turn * -1, root_node = child) 
                if root_node.evaluation <= minimum_score:
                    minimum_score = root_node.evaluation
                    #move container holds the best move among all of the nodes children
                    root_node.move_container = child.move_to_parent
            root_node.evaluation = minimum_score * turn * -1
            return root_node.evaluation


def computers_choice(board,current_player,depth):
    #make game tree
    test_tree=Tree(Node(data=Board(board_state = board.board_matrix)))
    test_tree.make_tree(max_depth=depth,turn=current_player)
    #evaluate evaluate tree
    test_tree.score_tree(turn = -1, root_node = test_tree.root_node)
    return test_tree.root_node.move_container

def print_divider():
    print('=======================')
    print('       Connect-4       ')
    print('=======================')

#takes type input_type, set of accepted responses, and a error message return_string if right type but non-considered value, func always accepts quit, Quit, q, Q
def player_input(input_type, accepted, return_string):
    given = input()
    while True:
        try:
            if str(given) in ('Quit','quit','q','Q'):
                print('Game Quit!')
                print_divider()
                break

            if input_type(given) in accepted:
                given = input_type(given)
                return given
            
            else:
                given = input_type(given)
                print(return_string)
                given = input()
        except:
            if input_type == int:
                print('Not an integer! Please try again.')
                given = input()

            if input_type == str:
                print('Not an string! Please try again.')
                given = input()

class Player:
    def __init__(self,id, score = 0):
        self.id = id
        self.score = score
        if self.id == 1:
            self.alias = 1
        if self.id == -1:
            self.alias = 2

class Game:
    #takes board obj as game_board and a number of players
    def __init__(self,num_players = 1, game_board = None):
        self.num_players = num_players
        if game_board is None:
            self.game_board = Board()
        else:
            self.game_board= game_board


        self.game_over = False
        self.player1 = Player(1)
        self.player2 = Player(-1)
        self.current_player = self.player1
        self.accepted_columns = {i+1 for i in range(self.game_board.board_width)}
        self.difficulty_level = 5 #default medium

    def start(self):
        print_divider()
        print('Enter \'Quit\' at anytime to exit the game.')
        print('=======================')

        print('How many players? ( 1 / 2 )')
        self.num_players = player_input(int, (1,2), 'Please enter how many players ( 1 / 2 )')

        if self.num_players == 1:
            print('How difficult? ( Easy / Medium / Hard )')
            difficulty = player_input(str, ('easy','Easy','medium','med','Med','Medium','hard','Hard'), 'Please enter difficulty ( Easy / Medium / Hard )')

            #difficulty_level is the depth of the game tree, 4, 6, and 8 levels
            if difficulty in ('easy','Easy'):
                self.difficulty_level = 4
            elif difficulty in ('medium','Medium','med','Med'):
                self.difficulty_level = 5
            elif difficulty in ('hard','Hard'):
                self.difficulty_level = 6

            system('clear') #clears terminal screen on mac
            print_divider()

        if self.num_players == 2:
            system('clear') #clears terminal screen on mac
            print_divider()

        #gameloop
        while not self.game_over:
            if self.game_board:
                print(self.game_board)

            #if player...
            if self.current_player.id == 1:
                print('Player {}: Enter integer column 1 - {}'.format(self.current_player.alias, self.game_board.board_width))
                chosen_column = player_input(int, self.accepted_columns, 'Player {}: Please enter integer column 1 - {}'.format(self.current_player, self.game_board.board_width))
                #if quit is chosen here
                if chosen_column is None:
                    break

            #if computer...
            elif self.current_player.id == -1:
                if self.num_players == 1:
                    print('Computer\'s Turn.')
                    #insert more interesting function HERE
                    chosen_column = computers_choice(board = self.game_board, current_player=-1, depth = self.difficulty_level)
                
                if self.num_players == 2:
                    print('Player {}: Enter integer column 1 - {}'.format(self.current_player.alias, self.game_board.board_width))
                    chosen_column = player_input(int, self.accepted_columns, 'Player {}: Please enter integer column 1 - {}'.format(self.current_player, self.game_board.board_width))
                    #if quit is chosen here
                    if chosen_column is None:
                        break

            system('clear') #clears terminal screen on mac
            print_divider()

            #player's turn
            #takes column entry, loops if not in board or column filled
            while True:
                try:
                    update = self.game_board.update_board(chosen_column,self.current_player.id)
                    print(self.game_board)

                    if update == 'continue':
                        #change turn
                        if self.current_player.id == 1:
                            self.current_player = self.player2
                        elif self.current_player.id == -1:
                            self.current_player = self.player1
                        break
                
                    if update == 'win':
                        self.game_over = True
                        print('Player {} wins!'.format(self.current_player.alias))
                        if self.current_player.id == 1:
                            self.player1.score += 1
                        if self.current_player.id == -1:
                            self.player2.score += 1
                        
                    if update == 'draw':
                        self.game_over = True
                        print('Draw!')
                        self.player1.score += 0.5
                        self.player2.score += 0.5

                    print('Score: Player 1: {} Player 2: {}'.format(self.player1.score, self.player2.score))
                    print('Play again? ( Yes / No )')
                    again = player_input(str, ('yes','Yes','No','no'), 'Please enter \'Yes\' or \'No\'.')

                    if again in set(('Yes','yes')):
                        #reset board, player, and game_over
                        self.game_board.refresh_board()
                        #change start turn
                        if self.current_player.id == 1:
                            self.current_player = self.player2
                        elif self.current_player.id == -1:
                            self.current_player = self.player1
                        self.game_over = False
                        system('clear') #clears terminal screen on mac
                        print_divider()
                        break

                    if again in set(('No','no')):
                        self.player1.score = 0
                        self.player2.score = 0
                        print('Thank you for playing!')
                        break     

                except:
                    print(self.game_board)
                    print('Column Full! Try another.')
                    chosen_column = player_input(int, self.accepted_columns, 'Player {}: Please enter integer column 1 - {}'.format(self.current_player, self.game_board.board_width))
                    
                    system('clear')
                    print_divider()

                    if chosen_column is None:
                        self.game_over = True
                        break   

if __name__ == '__main__':
    game = Game()
    game.start()
