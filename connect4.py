from connect4comp import computers_choice, Board
from os import system

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
