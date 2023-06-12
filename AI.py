from random import shuffle
import math
import time

# 设置新方块可能值及概率2：4=1:9，棋盘大小，
TILE_VALUES = [2, 4]
PROBABILITY_OF_ADDING_TWO = 0.9
GRID_SIZE = 4
MAX_DEPTH = 16
MAX_POWER = 18
WEIGHTS = [2.5 ** i for i in range(MAX_POWER)]
DIRECTIONS = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
WEIGHT_MATRIX = [
[1, 2, 3, 4],
[6, 6, 5, 5],
[7, 7, 8, 8],
[13, 11, 10, 9]]  # 矩阵权重，用于特征评估

# 启发式算法 特征-惩罚评估+估价函数
def heuristic(grid):
    return feature_score(grid) - penalty_score(grid) + estimate_score(grid)
# 求解函数 为了将方块合成 遍历当前情况下各方块的分数 使值为p的方块具权重p^k令p^k+1>2p^k所以WEIGHT中将K设置为2.5
def estimate_score(grid):
    weight_copy = WEIGHTS.copy()
    weight_copy[1:3] = [0, 0]
    ret = 0
    max_value = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # 计算出该数字在对应权重列表weight中的下标idx。注意这里加上一个很小的数0.0000001，是为了避免取对数时出现错误。
            cell_value = grid.getCellValue((i, j))
            idx = int(math.log2(cell_value + 0.0000001) + 0.5)
            idx = max(0, idx)
            # 更新最大数组下标
            if idx > max_value:
                max_value = idx
            # 加分
            ret += weight_copy[idx]
    # 当方块值大于1024 额外加分 大数字的下标是n，加分值为(2^n * n/6) * n/5。
    if idx >= 10:
        ret += (1 << idx) * idx / 6
        ret = ret * idx / 5
    return float(ret)

# 特征函数，用于评估当前状态下的棋盘分数。
def feature_score(grid):
    score = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            cell_value = grid.getCellValue((i, j))
            if cell_value > 4:
                score += WEIGHT_MATRIX[i][j] * cell_value
    return float(score)

# 惩罚函数，为了使值相近的方块在一起，相邻如果差距大就会得到一个大的惩罚。如果两值相等，会减少惩罚
def penalty_score(grid):
    # 计算惩罚评估的值
    score = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            coordinate = (i, j)
            cell_value = grid.getCellValue(coordinate)
            for direction in DIRECTIONS:
                neighbor_coordinate = (coordinate[0] + direction[0], coordinate[1] + direction[1])
                # 相邻格子越界时跳过  如果值相等，减少惩罚
                if grid.crossBound(neighbor_coordinate):
                    continue
                # 获取相邻格子的值
                neighbor_value = grid.getCellValue(neighbor_coordinate)
                # 如果值相等，减少惩罚
                if neighbor_value == cell_value:
                    score -= cell_value
                # 惩罚分数+=值的差值
                score += abs(cell_value - neighbor_value)
    return float(score)


# MiniMax算法
class Solver():
    def __init__(self, estimate_fun, max_depth=MAX_DEPTH, max_time=0.1):
        self.max_depth = max_depth  # 最大搜索深度
        self.estimate_fun = estimate_fun  # 估价函数
        self.start_time = time.perf_counter()  # 开始时间
        self.max_time = max_time  # 最大搜索时间

    def solve(self, grid):
        # 找到最佳的移动方向
        move = self.maximize(grid, self.max_depth)[0]
        if move is None:
            moves = grid.getAvailableMoves()
            shuffle(moves)
            return moves[0]
        return move
        # 判断是否达到终止条件，包括搜索深度、可移动方向和搜索时间
    def is_terminal(self, actions, depth):
        return depth == 0 or len(actions) == 0 or time.perf_counter() - self.start_time > self.max_time

    # 最小化电脑的期望得分
    def minimize(self, grid, depth):
        # 检测空格子
        cells = grid.getAvailableCells()
        if self.is_terminal(cells, depth):
            return self.estimate_fun(grid)
        utility = 0
        # 存在空格，
        for cell in cells:
            # 生成max子树
            child = grid.clone()
            child.setCellValue(cell, TILE_VALUES[0])
            u1 = self.maximize(child, depth - 1)[1]
            child.setCellValue(cell, TILE_VALUES[1])
            u2 = self.maximize(child, depth - 1)[1]
            utility += PROBABILITY_OF_ADDING_TWO * u1 + (1 - PROBABILITY_OF_ADDING_TWO) * u2
        return float(utility / len(cells))

    # 最大化自身得分期望值
    def maximize(self, grid, depth):
        # 获取可移动方向列表
        moves = grid.getAvailableMoves()
        if self.is_terminal(moves, depth):
            return (None, self.estimate_fun(grid))
        max_utility = -1
        best_move = None
        # 打乱移动方案列表，遍历移动方案，依次计算价值
        shuffle(moves)
        for move in moves:
            # 生成min子树
            child = grid.clone()
            if not child.move(move):
                continue
            utility = self.minimize(child, depth - 1)
            if utility > max_utility:
                max_utility = utility
                best_move = move
        # 返回移动方向和最大价值
        return (best_move, float(max_utility))

# 获取移动方向
def getMove(grid):
    if grid.canMove():
        # 将当前局面的分数传递给solver对象
        solver = Solver(heuristic)
        move = solver.solve(grid)
        if move is None:
            return None
        else:
            return move
    else:
        return None
