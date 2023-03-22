import unittest
from connect4 import Board

class TestComputer(unittest.TestCase):
    def test(self):
        #winning board state properly evaluated as total loss
        # | _  _  _  _  _  _  _ | 
        # | _  _  _  _  _  _  O | 
        # | _  O  _  O  _  _  O | 
        # | _  #  _  #  #  _  # | 
        # | _  #  O  #  #  _  O | 
        # | O  #  #  #  O  _  O |
        # |---------------------|
        # | 1  2  3  4  5  6  7 |
        # |---------------------|
        test = Board()
        test.board_matrix[5][0] = 'O'
        test.board_matrix[5][1] = '#'
        test.board_matrix[4][1] = '#'
        test.board_matrix[3][1] = '#'
        test.board_matrix[2][1] = 'O'
        test.board_matrix[5][2] = '#'
        test.board_matrix[4][2] = 'O'
        test.board_matrix[5][3] = '#'
        test.board_matrix[4][3] = '#'
        test.board_matrix[3][3] = '#'
        test.board_matrix[2][3] = 'O'
        test.board_matrix[5][4] = 'O'
        test.board_matrix[4][4] = '#'
        test.board_matrix[3][4] = '#'
        test.board_matrix[5][6] = 'O'
        test.board_matrix[4][6] = 'O'
        test.board_matrix[3][6] = '#'
        test.board_matrix[2][6] = 'O'
        test.board_matrix[1][6] = 'O'
        test_given_depth = 2
        # print(test)
        self.assertEqual(test.best_move(test_given_depth), 3)

    def test1(self):
        #| _  _  _  _  _  _  _ | 
        #| _  _  _  _  _  _  _ | 
        #| _  _  _  _  _  _  _ | 
        #| _  _  _  _  _  _  _ | 
        #| #  _  _  _  _  _  _ | 
        #| #  #  #  _  O  O  O |
        #|---------------------|
        #| 1  2  3  4  5  6  7 |
        #|---------------------|
        test1 = Board()
        test1.board_matrix[5][0] = '#'
        test1.board_matrix[5][6] = 'O'
        test1.board_matrix[5][1] = '#'
        test1.board_matrix[5][5] = 'O'
        test1.board_matrix[5][2] = '#'
        test1.board_matrix[5][4] = 'O'
        test1.board_matrix[4][0] = '#'
        test1_given_depth = 2
        # print(test1)
        self.assertEqual(test1.best_move(test1_given_depth), 4)

    def test2(self):
        #| _  O  _  _  _  _  _ | 
        #| #  O  _  _  _  _  _ | 
        #| O  O  _  _  O  _  _ | 
        #| O  #  _  _  #  _  _ | 
        #| O  O  O  #  #  #  _ | 
        #| #  #  #  O  #  #  _ |
        #|---------------------|
        #| 1  2  3  4  5  6  7 |
        #|---------------------|
        test2 = Board()
        test2.board_matrix[5][0] = '#'
        test2.board_matrix[4][0] = 'O'
        test2.board_matrix[3][0] = 'O'
        test2.board_matrix[2][0] = 'O'
        test2.board_matrix[1][0] = '#'
        test2.board_matrix[5][1] = '#'
        test2.board_matrix[4][1] = 'O'
        test2.board_matrix[3][1] = '#'
        test2.board_matrix[2][1] = 'O'
        test2.board_matrix[1][1] = 'O'
        test2.board_matrix[0][1] = 'O'
        test2.board_matrix[5][2] = '#'
        test2.board_matrix[4][2] = 'O'
        test2.board_matrix[5][3] = 'O'
        test2.board_matrix[4][3] = '#'
        test2.board_matrix[5][4] = '#'
        test2.board_matrix[4][4] = '#'
        test2.board_matrix[3][4] = '#'
        test2.board_matrix[2][4] = 'O'
        test2.board_matrix[5][5] = '#'
        test2.board_matrix[4][5] = '#'
        test2_given_depth = 2
        # print(test2)
        self.assertNotIn(test2.best_move(test2_given_depth),(6,7))

    def test3(self):
        # | O  O  _  O  #  #  _ | 
        # | O  O  _  O  #  O  _ | 
        # | O  O  _  #  #  O  # | 
        # | #  #  _  #  O  #  O | 
        # | O  #  _  #  #  O  # | 
        # | #  #  #  O  O  #  O |
        # |---------------------|
        # | 1  2  3  4  5  6  7 |
        # |---------------------|

        test3 = Board()
        test3.board_matrix[5][0] = '#'
        test3.board_matrix[4][0] = 'O'
        test3.board_matrix[3][0] = '#'
        test3.board_matrix[2][0] = 'O'
        test3.board_matrix[1][0] = 'O'
        test3.board_matrix[0][0] = 'O'
        test3.board_matrix[5][1] = '#'
        test3.board_matrix[4][1] = '#'
        test3.board_matrix[3][1] = '#'
        test3.board_matrix[2][1] = 'O'
        test3.board_matrix[1][1] = 'O'
        test3.board_matrix[0][1] = 'O'
        test3.board_matrix[5][2] = '#'
        test3.board_matrix[5][3] = 'O'
        test3.board_matrix[4][3] = '#'
        test3.board_matrix[3][3] = '#'
        test3.board_matrix[2][3] = '#'
        test3.board_matrix[1][3] = 'O'
        test3.board_matrix[0][3] = 'O'
        test3.board_matrix[5][4] = 'O'
        test3.board_matrix[4][4] = '#'
        test3.board_matrix[3][4] = 'O'
        test3.board_matrix[2][4] = '#'
        test3.board_matrix[1][4] = '#'
        test3.board_matrix[0][4] = '#'
        test3.board_matrix[5][5] = '#'
        test3.board_matrix[4][5] = 'O'
        test3.board_matrix[3][5] = '#'
        test3.board_matrix[2][5] = 'O'
        test3.board_matrix[1][5] = 'O'
        test3.board_matrix[0][5] = '#'
        test3.board_matrix[5][6] = 'O'
        test3.board_matrix[4][6] = '#'
        test3.board_matrix[3][6] = 'O'
        test3.board_matrix[2][6] = '#'
        test3_given_depth = 4
        # print(test3)
        self.assertEqual(test3.best_move(test3_given_depth, verbose=True), 7)

    def test4(self):
        #| _  _  _  _  _  _  _ | 
        #| _  _  _  _  _  _  _ | 
        #| _  _  _  _  _  _  _ | 
        #| _  _  _  #  _  _  _ | 
        #| O  _  _  #  _  _  _ | 
        #| O  _  _  #  _  _  _ |
        #|---------------------|
        #| 1  2  3  4  5  6  7 |
        #|---------------------|
        test4 = Board()
        test4.board_matrix[5][0] = 'O'
        test4.board_matrix[4][0] = 'O'
        test4.board_matrix[5][3] = '#'
        test4.board_matrix[4][3] = '#'
        test4.board_matrix[3][3] = '#'
        test4_given_depth = 2
        # print(test4)
        self.assertEqual(test4.best_move(test4_given_depth), 4)

    def test5(self):
        # | _  _  _  _  _  _  _ | 
        # | _  _  _  _  _  _  _ | 
        # | #  _  _  _  _  _  _ | 
        # | O  _  _  O  _  _  _ | 
        # | O  _  #  #  #  _  _ | 
        # | O  _  #  #  O  _  _ |
        # |---------------------|
        # | 1  2  3  4  5  6  7 |
        # |---------------------|
        test5 = Board()
        test5.board_matrix[5][0] = 'O'
        test5.board_matrix[4][0] = 'O'
        test5.board_matrix[3][0] = 'O'
        test5.board_matrix[2][0] = '#'
        test5.board_matrix[5][2] = '#'
        test5.board_matrix[4][2] = '#'
        test5.board_matrix[5][3] = '#'
        test5.board_matrix[4][3] = '#'
        test5.board_matrix[3][3] = 'O'
        test5.board_matrix[5][4] = 'O'
        test5.board_matrix[4][4] = '#'
        test5_given_depth = 5
        #print(test5)
        
        self.assertNotIn(test5.best_move(test5_given_depth), (2,6))


if __name__ == '__main__': unittest.main()
