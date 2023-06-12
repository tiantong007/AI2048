from copy import deepcopy
vecIndex = range(4)
directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
class Grid:
    def __init__(self, size=4):
        self.size = size
        self.map = [[0] * self.size for i in range(self.size)]

    def clone(self):
        return deepcopy(self)

    def insertTile(self, pos, value):
        self.map[pos[0]][pos[1]] = value
    # 获取格子上的值
    def setCellValue(self, pos, value):
        self.map[pos[0]][pos[1]] = value

    def getAvailableCells(self):
        cells = [(x, y) for x in range(self.size) for y in range(self.size) if self.map[x][y] == 0]
        return cells

    def getMaxTile(self):
        return max(max(row) for row in self.map)

    def canInsert(self, pos):
        return self.getCellValue(pos) == 0

    def move(self, dir):
        dir = int(dir)
        if dir == 0:
            return self.moveUD(False)
        if dir == 1:
            return self.moveUD(True)
        if dir == 2:
            return self.moveLR(False)
        if dir == 3:
            return self.moveLR(True)

    def moveUD(self, down):
        r = range(self.size - 1, -1, -1) if down else range(self.size)
        moved = False
        for j in range(self.size):
            cells = [self.map[i][j] for i in r if self.map[i][j] != 0]
            self.merge(cells)
            for i, value in zip(r, cells + [0] * (self.size - len(cells))):
                if self.map[i][j] != value:
                    moved = True
                self.map[i][j] = value
        return moved

    def moveLR(self, right):
        r = range(self.size - 1, -1, -1) if right else range(self.size)
        moved = False
        for i in range(self.size):
            cells = [self.map[i][j] for j in r if self.map[i][j] != 0]
            self.merge(cells)
            for j, value in zip(r, cells + [0] * (self.size - len(cells))):
                if self.map[i][j] != value:
                    moved = True
                self.map[i][j] = value
        return moved

    def merge(self, cells):
        i = 0
        while i < len(cells) - 1:
            if cells[i] == cells[i + 1]:
                cells[i] *= 2
                del cells[i + 1]
            i += 1

    def canMove(self, dirs=vecIndex):
        for x in range(self.size):
            for y in range(self.size):
                if self.map[x][y] == 0:
                    return True
                for i in dirs:
                    move = directionVectors[i]
                    adjCellValue = self.getCellValue((x + move[0], y + move[1]))
                    if adjCellValue == self.map[x][y] or adjCellValue == 0:
                        return True
        return False

    def getAvailableMoves(self, dirs=vecIndex):
        availableMoves = []
        for x in dirs:
            gridCopy = self.clone()
            if gridCopy.move(x):
                availableMoves.append(x)
        return availableMoves
    # 检测是否越界
    def crossBound(self, pos):
        return pos[0] < 0 or pos[0] >= self.size or pos[1] < 0 or pos[1] >= self.size

    def getCellValue(self, pos):
        return self.map[pos[0]][pos[1]] if not self.crossBound(pos) else None