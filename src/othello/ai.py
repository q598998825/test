import copy,time
from mypthread import *

'''
作者：hhh5460
时间：2017年7月1日
'''

class AImsg():
    def __init__(self,board, AI1, AI2, depth, my_best, opp_best,resultist, action):
        self.board = board
        self.AI1 = AI1
        self.AI2 = AI2
        self.depth = depth
        self.my_best = my_best
        self.opp_best = opp_best
        self.resultlist = resultist
        self.action = action
class AI(object):
    '''
    三个水平等级：初级（beginner）、中级（intermediate）、高级（advanced）
    '''

    def __init__(self, level_ix=0):
        # 玩家等级
        self.level = 'advanced'
        # 棋盘位置权重，参考：https://github.com/k-time/ai-minimax-agent/blob/master/ksx2101.py
        self.board_weights = [
            [120, -20, 20, 5, 5, 20, -20, 120],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [5, -5, 3, 3, 3, 3, -5, 5],
            [20, -5, 15, 3, 3, 15, -5, 20],
            [-20, -40, -5, -5, -5, -5, -40, -20],
            [120, -20, 20, 5, 5, 20, -20, 120]
        ]

    # 评估函数（仅根据棋盘位置权重）
    def evaluate(self, board, color):
        uncolor = ['X', 'O'][color == 'X']
        score = 0
        for i in range(8):
            for j in range(8):
                if board[i*8+j] == color:
                    score += self.board_weights[i][j]
                elif board[i*8+j] == uncolor:
                    score -= self.board_weights[i][j]
        return score

    # AI的大脑
    def brain(self, board, opponent, depth):
        if self.level == 'advanced':  # 高级水平
            _, action = self.minimax_alpha_beta(board, opponent, depth)

        if action is not None:
            return action
        return -1

    # 极大极小算法，带alpha-beta剪枝
    def minimax_alpha_beta(self, board, opfor, depth=8, my_best=-float('inf'), opp_best=float('inf')):
        '''参考：https://github.com/k-time/ai-minimax-agent/blob/master/ksx2101.py'''
        color = self.color

        if depth == 0:
            return self.evaluate(board, color), None

        action_list = list(self.get_legal_actions(board,color))
        if not action_list:
            return self.evaluate(board, color), None

        best_score = my_best
        best_action = None
        tmp = self.deal4pth(action_list, board, opfor, depth, my_best, opp_best) #多线程处理
        if(tmp is None):
            for action in action_list:
                flipped_pos = self.move(board, action)  # 落子
                score, _ = opfor.minimax_alpha_beta(board, self, depth - 1, -opp_best, -best_score)  # 深度优先，轮到陪练
                self.unmove(board, action, flipped_pos)  # 回溯

                score = -score
                if score > best_score:
                    best_score = score
                    best_action = action

                if best_score > opp_best:
                    break
        elif(tmp[1] is not None):
            best_score = tmp[0]
            best_action = tmp[1]

        return best_score, best_action

    def deal4pth(self, action_list, board, opfor, depth=8, my_best=-float('inf'), opp_best=float('inf')):
        if(len(action_list) > 4): #每隔一段深度才分线程处理
            return None
        best_score = my_best
        best_action = None
        pthlist = []
        #print(action_list)
        resultist = []
        i = 0
        for action in action_list:
            AI1 = copy.copy(self)
            board1 = copy.copy(board)
            AImsg1 = AImsg(board1,opfor,AI1,depth, my_best, opp_best,resultist, action)
            mypthread1 = mypthread(self.pthProc,AImsg1)
            mypthread1.start()

        while(len(action_list)!= len(resultist)):
            i=i+1
            time.sleep(0.3)

        for result in resultist:
            if result[0] > best_score:
                best_score = result[0]
                best_action = result[1]

        return [best_score, best_action]

    def pthProc(self,arg:AImsg):
        #print("pthProc start!!!")
        #调用minimax_alpha_beta算法
        flipped_pos = self.move(arg.board, arg.action)  # 落子
        score, _ = arg.AI1.minimax_alpha_beta(arg.board,arg.AI2,arg.depth -1,-arg.opp_best,-arg.my_best)
        self.unmove(arg.board, arg.action, flipped_pos)  # 回溯

        score = -score
        arg.resultlist.append([score,arg.action])
        #返回结果
        #print("pthProc end!!!")