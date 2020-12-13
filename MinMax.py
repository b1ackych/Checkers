from checkers.board import Board
from checkers.board_initializer import BoardInitializer 
from checkers.board_searcher import BoardSearcher
from checkers.game import Game
from checkers.piece import Piece
import random
import copy
import time


def timeIsUp(current_time_used, param):
    return current_time_used >= param


# evaluates position statically
def evalPos(pos):
    bs = BoardSearcher()
    bs.build(pos.board)
    red = bs.get_pieces_by_player(1)
    black = bs.get_pieces_by_player(2)
    # simple piece count
    len_red = len(red)
    len_black = len(black)
    res = 3*(len_red - len_black)*(12 / (len_black+len_red))

    # accounting for kings
    for piece in red:
        if piece.king: 
            res += 2
        else:
            res += (1 + (piece.position - 1)//4)/4

    for piece in black:
        if piece.king:
            res -= 2
        else:
            res -= (8 - (piece.position - 1)//4)/4
    
    return res


# pos is an instance of game
def bestMove(pos, time_for_move):
    start = time.time()
    side = pos.whose_turn()
    moves = pos.get_possible_moves()
    length = len(moves)

    if length == 1:
        return moves[0]

    eval = (-1)**side*1000
    best_move = random.choice(moves)
    alpha = -1000
    beta = 1000
    print("pose whose turn", pos.whose_turn())
    for i in range(length):
        m = moves[i]
        game = copy.deepcopy(pos)
        game.move(m)

        if timeIsUp(time.time() - start, time_for_move):            
            return best_move
        
        time_left = time_for_move - (time.time() - start)
        new_eval = minmax(game, time_left / (length-i), alpha, beta)
        ##
        print(m, new_eval)
        ##
        if side == 1:
            if eval < new_eval:
                eval = new_eval
                best_move = m
        else:
            if eval > new_eval:
                eval = new_eval
                best_move = m
    ##
    print("chosen move:",best_move, eval)
    ##
    return best_move


# 
def minmax(pos, available_time, alpha, beta):
    start = time.time()
    side = pos.whose_turn()
    moves = pos.get_possible_moves()
    length = len(moves)

    copy_pos = copy.deepcopy(pos)
    copy_moves = copy_pos.get_possible_moves()
    if len(copy_moves) == 0:
        return -999
    copy_pos.move(random.choice(copy_moves))
    keep_turn = copy_pos.whose_turn() == pos.whose_turn()

    eval = (-1)**(side+1)*1000 if not keep_turn else (-1)**side*1000
    for i in range(length):
        m = moves[i]
        game = copy.deepcopy(pos)
        game.move(m)

        if timeIsUp(time.time() - start, available_time):
            return evalPos(game)
        time_left = available_time - (time.time() - start)

        new_eval = minmax(game, time_left / (length - i), alpha, beta)
        if not keep_turn:
            if side == 1:
                if eval > new_eval:
                    eval = new_eval
            else:
                if eval < new_eval:
                    eval = new_eval
        else:
            if side == 1:
                if eval < new_eval:
                    eval = new_eval
            else:
                if eval > new_eval:
                    eval = new_eval
        
        # alpha_beta pruning
        if side == 1:
            alpha = max(alpha, eval)
        else:
            beta = min(beta, eval)
        if beta < alpha:
            if side == 1: # это надо закомментировать чтоб альфа-бета не юзал
                break     # игрок что ходит первым
            elif side == 2: # это надо закомментировать чтоб альфа-бета не юзал
                break     # игрок что ходит вторым

    return eval

if __name__ == "__main__":
    GAME = Game()
    count = 1
    while not GAME.is_over():
        start_time = time.time()
        new_move = bestMove(GAME, 4)
        count += 1
        # break
        print("move took: ", time.time() - start_time)
        print(new_move)
        GAME.move(new_move)
