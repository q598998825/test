from ai import AI
from board import *
import time
'''
作者：hhh5460
时间：2017年7月1日
'''


# 玩家
class Player(object):
    def __init__(self, color):
        self.color = color

    # 思考
    def think(self, board):
        pass

    # 落子
    def move(self, board, action):
        flipped_pos = self._move(board,action, self.color)
        return flipped_pos

    # 悔子
    def unmove(self, board, action, flipped_pos):
        self._unmove(board,action, flipped_pos, self.color)


# 人类玩家
class HumanPlayer(Player):
    def __init__(self, color):
        super().__init__(color)

    def think(self, board):
        while True:
            action = input("Turn to '{}'. \nPlease input a point.(such as 'A1'): ".format(self.color))  # A1~H8
            r, c = action[1], action[0].upper()
            if r in '12345678' and c in 'ABCDEFGH':  # 合法性检查1
                x, y = '12345678'.index(r), 'ABCDEFGH'.index(c)
                if (x, y) in board.get_legal_actions(self.color):  # 合法性检查2
                    return x, y

max1 = 0.0
# 电脑玩家（多重继承）
class AIPlayer(Player, AI, Board):

    def __init__(self, color, level_ix=0):
        super().__init__(color)  # init Player
        super(Player, self).__init__(level_ix)  # init AI
        super(AI, self).__init__()

    def think(self, board):
        print("Turn to '{}'. \nPlease wait a moment. AI is thinking...".format(self.color))
        time1 = time.time()
        uncolor = ['X', 'O'][self.color == 'X']
        opfor = AIPlayer(uncolor)  # 假想敌，陪练
        action = self.brain(board, opfor, 5)
        time2 = time.time()
        timetmp=time2-time1
        print("action,", action)
        global  max1
        if(max1<timetmp):
            max1=timetmp
        print("思考消耗时间 :%f,最大消耗时间%f"%(timetmp,max1))
        return action