"""
LIBRARIES IMPORTED
"""
import numpy as np
from random import choice
import time

"""
MISCILLANEOUS FUNCTIONS
"""

def cutoff_test(state, depth, depthLimit=6):
    if depth > depthLimit:
        return True
    else:
        return False

def eval_function(state,game,player):
        return game.utility(state,player)*100

def test_heu(state,game,player):

    sum=0
    for i in range(game.h):
        for j in range(game.v):
            if state.board[i][j]==player:
                move=i,j
                sum = max(game.k_in_row(state.board, move, player, (0, 1)) , game.k_in_row(state.board, move, player, (1, 0)), game.k_in_row(state.board, move, player, (1, -1)), game.k_in_row(state.board, move, player, (1, 1)))
                # print(sum)

    if player=='X':
        return (10**(sum-1)) + eval_function(state,game,player)
    else:
        return (-(10**(sum-1))) + eval_function(state,game,player)


"""
MINIMAX FUNCTIONS
"""


#basic minimax function
def minimax_decision(state, game):

    player = game.to_move(state)

    def max_value(state):

        if game.terminal_test(state):
            return game.utility(state, player)
        value = -np.inf
        for a in game.actions(state):
            value = max(value, min_value(game.result(state, a)))
        return value

    def min_value(state):

        if game.terminal_test(state):
            return game.utility(state, player)
        value = np.inf
        for a in game.actions(state):
            value = min(value, max_value(game.result(state, a)))
        return value

    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))



#minimax using depth limit search
def depth_limit_search(state, game,eval=eval_function,depthLimit=7):

    player = game.to_move(state)


    def max_value(state,depth):
        if cutoff_test(state,depth, depthLimit) or game.terminal_test(state):
            return eval(state,game,player)
        value = -np.inf
        for a in game.actions(state):
            value = max(value, min_value(game.result(state, a), depth+1))
        return value

    def min_value(state,depth):
        if cutoff_test(state, depth, depthLimit) or game.terminal_test(state):
            return eval(state,game,player)
        value = np.inf
        for a in game.actions(state):
            value = min(value, max_value(game.result(state, a), depth+1))
        return value

    return max(game.actions(state), key=lambda a: min_value(game.result(state, a), 1))



#minimax using alpha-beta pruning
def alpha_beta_search(state, game):

    player = game.to_move(state)

    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        value = -np.inf
        for a in game.actions(state):
            value = max(value, min_value(game.result(state, a), alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        value = np.inf
        for a in game.actions(state):
            value = min(value, max_value(game.result(state, a), alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        value = min_value(game.result(state, a), best_score, beta)
        if value > best_score:
            best_score = value
            best_action = a
    return best_action



#minimax using both depth-limit and alpha-beta pruning
def alpha_beta_depth_limit(state, game, eval=eval_function, depthLimit=6):


    player = game.to_move(state)


    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth, depthLimit) or game.terminal_test(state):
            return eval(state,game,player)

        value = -np.inf
        for a in game.actions(state):
            value = max(value, min_value(game.result(state, a), alpha, beta, depth + 1))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth, depthLimit) or game.terminal_test(state):
            return eval(state,game,player)

        value = np.inf
        for a in game.actions(state):
            value = min(value, max_value(game.result(state, a), alpha, beta, depth + 1))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value


    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        value = min_value(game.result(state, a), best_score, beta, 1)
        if value > best_score:
            best_score = value
            best_action = a
    return best_action



#same as alpha beta with depth limit but experimented heuristic value
def experimental_minimax(state,game):
    return alpha_beta_depth_limit(state,game,test_heu)



class State:
    def __init__(self,to_move, utility, board, moves):
        self.to_move=to_move
        self.utility=utility
        self.board=board
        self.moves=moves


class Game:


    def actions(self, state):
        return state.moves


    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move[0]][move[1]] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return State(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)



    def to_move(self, state):
        return state.to_move


    def utility(self, state, player):
        return state.utility if player == 'X' else -state.utility


    def terminal_test(self, state):
        return state.utility != 0 or len(state.moves) == 0



    def k_in_row(self, board, move, player, delta_x_y):
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while x>=0 and x<self.h and y>=0 and y<self.v and board[x][y] == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while x>=0 and x<self.h and y>=0 and y<self.v and board[x][y] == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n




    def check_match(self, board, move, player):
        if (self.k_in_row(board, move, player, (0, 1))>=self.k) or (self.k_in_row(board, move, player, (1, 0))>=self.k) or (self.k_in_row(board, move, player, (1, -1))>=self.k) or (self.k_in_row(board, move, player, (1, 1))>=self.k):
            return True
        else:
            return False



    def compute_utility(self, board, move, player):
        if self.check_match(board, move, player):
            return +1 if player == 'X' else -1
        else:
            return 0




    def display(self, state):
        board = state.board
        for x in range(0, self.h):
            for y in range(0, self.v):
                print(board[x][y], end=' ')
            print()

        print()
        print()




"""
TIC-TAC-TOE (3X3)
"""


class TicTacToe(Game):

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(0, h)
                 for y in range(0, v)]
        self.initial = State(to_move='X', utility=0, board=np.full((h,v),'-'), moves=moves)
