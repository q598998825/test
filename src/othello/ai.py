import random

'''
作者：hhh5460
时间：2017年7月1日
'''


class AI(object):
    '''
    三个水平等级：初级（beginner）、中级（intermediate）、高级（advanced）
    '''

    def __init__(self, level_ix=0):
        # 玩家等级
        self.level = ['beginner', 'intermediate', 'advanced'][level_ix]
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
                if board[i][j] == color:
                    score += self.board_weights[i][j]
                elif board[i][j] == uncolor:
                    score -= self.board_weights[i][j]
        return score

    # AI的大脑
    def brain(self, board, opponent, depth):
        if self.level == 'beginer':  # 初级水平
            _, action = self.randomchoice(board)
        elif self.level == 'intermediate':  # 中级水平
            _, action = self.minimax(board, opponent, depth)
        elif self.level == 'advanced':  # 高级水平
            _, action = self.minimax_alpha_beta(board, opponent, depth)
        assert action is not None, 'action is None'
        return action

    # 随机选（从合法走法列表中随机选）
    def randomchoice(self, board):
        color = self.color
        action_list = list(board.get_legal_actions(color))
        return None, random.choice(action_list)

    # 极大极小算法，限制深度
    def minimax(self, board, opfor, depth=4):  # 其中 opfor 是假想敌、陪练
        '''参考：https://github.com/k-time/ai-minimax-agent/blob/master/ksx2101.py'''
        color = self.color

        if depth == 0:
            return self.evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            return self.evaluate(board, color), None

        best_score = -100000
        best_action = None

        for action in action_list:
            flipped_pos = self.move(board, action)  # 落子
            score, _ = opfor.minimax(board, self, depth - 1)  # 深度优先，轮到陪练
            self.unmove(board, action, flipped_pos)  # 回溯

            score = -score
            if score > best_score:
                best_score = score
                best_action = action

        return best_score, best_action

    # 极大极小算法，带alpha-beta剪枝
    def minimax_alpha_beta(self, board, opfor, depth=8, my_best=-float('inf'), opp_best=float('inf')):
        '''参考：https://github.com/k-time/ai-minimax-agent/blob/master/ksx2101.py'''
        color = self.color

        if depth == 0:
            return self.evaluate(board, color), None

        action_list = list(board.get_legal_actions(color))
        if not action_list:
            return self.evaluate(board, color), None

        best_score = my_best
        best_action = None

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

        return best_score, best_action