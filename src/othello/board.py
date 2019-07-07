class Board(object):
    def __init__(self):
        self.empty = '.'
        self._board = [self.empty for _ in range(64)]  # 规格：8*8
        self._board[3*8+4], self._board[4*8+3] = 'X', 'X'
        self._board[3*8+3], self._board[4*8+4] = 'O', 'O'

    # 打印棋盘
    def print_b(self):
        board = self._board
        print(' ', ' '.join(list('ABCDEFGH')))
        for i in range(8):
            Tmp = []
            for j in range(8):
                Tmp.append(board[i*8+j])
            print(str(i + 1), ' '.join(Tmp))

    # 棋局终止
    def teminate(self, board):
        list1 = list(self.get_legal_actions(board,'X'))
        list2 = list(self.get_legal_actions(board,'O'))
        return [False, True][len(list1) == 0 and len(list2) == 0]

    # 判断赢家
    def get_winner(self):
        s1, s2 = 0, 0
        for i in range(8):
            for j in range(8):
                if self._board[i*8+j] == 'X':
                    s1 += 1
                if self._board[i*8+j] == 'O':
                    s2 += 1
        if s1 > s2:
            return 0  # 黑胜
        elif s1 < s2:
            return 1  # 白胜
        elif s1 == s2:
            return 2  # 平局

    # 落子
    def _move(self, board, action, color):
        x, y = action
        board[x*8+y] = color

        return self._flip(board, action, color)

    # 翻子（返回list）
    def _flip(self, board, action, color):
        flipped_pos = []
        for line in self._get_lines(action):
            for i, p in enumerate(line):
                if board[p[0]*8+p[1]] == self.empty:
                    break
                elif board[p[0]*8+p[1]] == color:
                    flipped_pos.extend(line[:i])
                    break

        for p in flipped_pos:
            board[p[0]*8+p[1]] = color

        return flipped_pos

    # 撤销
    def _unmove(self,board, action, flipped_pos, color):
        board[action[0]*8+action[1]] = self.empty

        uncolor = ['X', 'O'][color == 'X']
        for p in flipped_pos:
            board[p[0]*8+p[1]] = uncolor

    # 生成8个方向的下标数组，方便后续操作
    def _get_lines(self, action):
        board_coord = [(i, j) for i in range(8) for j in range(8)]  # 棋盘坐标

        r, c = action
        ix = r * 8 + c
        left = board_coord[r * 8:ix]  # 要反转
        right = board_coord[ix + 1:(r + 1) * 8]
        top = board_coord[c:ix:8]  # 要反转
        bottom = board_coord[ix + 8:8 * 8:8]

        if r <= c:
            lefttop = board_coord[c - r:ix:9]  # 要反转
            rightbottom = board_coord[ix + 9:(7 - (c - r)) * 8 + 7 + 1:9]
        else:
            lefttop = board_coord[(r - c) * 8:ix:9]  # 要反转
            rightbottom = board_coord[ix + 9:7 * 8 + (7 - (c - r)) + 1:9]

        if r + c <= 7:
            leftbottom = board_coord[ix + 7:(r + c) * 8:7]
            righttop = board_coord[r + c:ix:7]  # 要反转
        else:
            leftbottom = board_coord[ix + 7:7 * 8 + (r + c) - 7 + 1:7]
            righttop = board_coord[((r + c) - 7) * 8 + 7:ix:7]  # 要反转

        # 有四个要反转，方便判断
        left.reverse()
        top.reverse()
        lefttop.reverse()
        righttop.reverse()
        lines = [left, leftbottom, top, lefttop, righttop, bottom, rightbottom, right]
        return lines

    # 检测，位置是否有子可翻
    def _can_fliped(self,board, action, color, dxy):
        line = self._get_lines(action)
        for i, p in enumerate(line[dxy]):
            if board[p[0]*8+p[1]] == color:
                return True
        return False

    # 合法走法
    def get_legal_actions(self, board, color):
        uncolor = ['X', 'O'][color == 'X']
        uncolor_near_points = []  # 反色邻近的空位
        dxy = [(0, 1), (-1, 1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, -1), (0, -1)]
        for i in range(8):
            for j in range(8):
                if board[i*8+j] == uncolor:
                    for k in range(8):
                        x, y = i + dxy[k][0], j + dxy[k][1]
                        if 0 <= x <= 7 and 0 <= y <= 7 and board[x*8+y] == self.empty and (
                        x, y) not in uncolor_near_points and self._can_fliped(board, (x,y), color, k):
                            uncolor_near_points.append((x, y))
                            yield(x, y)