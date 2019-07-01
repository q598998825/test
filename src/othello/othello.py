from board import Board
from player import HumanPlayer, AIPlayer

'''
作者：hhh5460
时间：2017年7月1日
'''


# 游戏
class Game(object):
    def __init__(self):
        self.board = Board()
        self.current_player = None

    # 生成两个玩家
    def make_two_players(self):
        ps = input("Please select two player's type:\n\t0.Human\n\t1.AI\nSuch as:0 0\n:")
        p1, p2 = [int(p) for p in ps.split(' ')]
        if p1 == 1 or p2 == 1:  # 至少有一个AI玩家
            level_ix = int(
                input("Please select the level of AI player.\n\t0: beginner\n\t1: intermediate\n\t2: advanced\n:"))
            if p1 == 0:
                player1 = HumanPlayer('X')
                player2 = AIPlayer('O', level_ix)
            elif p2 == 0:
                player1 = AIPlayer('X', level_ix)
                player2 = HumanPlayer('O')
            else:
                player1 = AIPlayer('X', level_ix)
                player2 = AIPlayer('O', level_ix)
        else:
            player1, player2 = HumanPlayer('X'), HumanPlayer('O')  # 先手执X，后手执O

        return player1, player2

    # 切换玩家（游戏过程中）
    def switch_player(self, player1, player2):
        if self.current_player is None:
            return player1
        else:
            return [player1, player2][self.current_player == player1]

    # 打印赢家
    def print_winner(self, winner):  # winner in [0,1,2]
        print(['Winner is player1', 'Winner is player2', 'Draw'][winner])

    # 运行游戏
    def run(self):
        # 生成两个玩家
        player1, player2 = self.make_two_players()

        # 游戏开始
        print('\nGame start!\n')
        self.board.print_b()  # 显示棋盘
        while True:
            self.current_player = self.switch_player(player1, player2)  # 切换当前玩家

            action = self.current_player.think(self.board)  # 当前玩家对棋盘进行思考后，得到招法

            if action is not None:
                self.current_player.move(self.board, action)  # 当前玩家执行招法，改变棋盘

            self.board.print_b()  # 显示当前棋盘

            if self.board.teminate():  # 根据当前棋盘，判断棋局是否终止
                winner = self.board.get_winner()  # 得到赢家 0,1,2
                break

        self.print_winner(winner)
        print('Game over!')

        self.board.print_history()

def test():
    Game().run()