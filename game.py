# v14:bug优化
import time
import pygame
import random
import db_sql
import color as co
import login
import AI
import Grid
global game_over
game_over =False
# 登录
login.login()
# 游戏窗口长宽
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480
# 游戏板大小 数量为BOARD_SIZE^2 游戏板列表 当前得分 获取最高分
BOARD_SIZE = 4
TILE_SIZE = 120
board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
score = 0
global your_max_score
your_max_score=db_sql.selectuser(login.username)
max_score = db_sql.selectdata()
result=db_sql.selecttop()
# 初始化 创建游戏窗口，字体
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2048')
font = pygame.font.SysFont('方正粗黑宋简体', 26)
# 游戏板+分数记录(撤回需求 判断前记录 判断后记录 分数记录)
board_record0 = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
board_record1 = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
board_record2 = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
record_score=0
grid = Grid.Grid()
# 按钮作用域区域设置
reset_button_rect = pygame.Rect(520, 120, 150, 50)
revoke_button_rect = pygame.Rect(520, 190, 150, 50)
random_button_rect = pygame.Rect(520, 260, 150, 50)
ai_button_rect = pygame.Rect(520, 400, 150, 50)
ts_button_rect = pygame.Rect(520, 330, 150, 50)

# 绘制游戏
def draw_board():
    # 绘制游戏板
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # 游戏块背景，通过逐个绘制游戏块实现
            pygame.draw.rect(screen,'#BBADA0', (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            # 绘制游戏块
            block = pygame.Surface((TILE_SIZE - 20, TILE_SIZE - 20))
            block.fill(co.get_color(board[i][j]))
            screen.blit(block, (j * TILE_SIZE + 10, i * TILE_SIZE + 10))
            # 如果数组数字不为空
            if board[i][j] != 0:
                # 绘制游戏块数字
                text = font.render(str(board[i][j]), True, '#ffffff')
                text_rect = text.get_rect(center=((j * TILE_SIZE + TILE_SIZE / 2), (i * TILE_SIZE + TILE_SIZE / 2)))
                screen.blit(text, text_rect)
# 绘制得分
def draw_score():
    text = font.render('当前分数:' + str(score), True, '#ffffff')
    text_rect = text.get_rect(topleft=(SCREEN_WIDTH - 230, 10))
    screen.blit(text, text_rect)
# 绘制个人最高得分
def draw_your_max_score():
    global your_max_score
    if your_max_score<score:
        your_max_score=score
    text = font.render('你的纪录:' + str(your_max_score), True, '#ffffff')
    text_rect = text.get_rect(topleft=(SCREEN_WIDTH - 230, 40))
    screen.blit(text, text_rect)
# 绘制最高得分
def draw_max_score():
    global max_score
    if max_score<score:
        max_score=score
    text = font.render('最高纪录:' + str(max_score), True, '#ffffff')
    text_rect = text.get_rect(topleft=(SCREEN_WIDTH - 230, 70))
    screen.blit(text, text_rect)
#绘制按钮方法
def draw_button(x, y, width, height, color, text, text_color):
    # 绘制按钮
    pygame.draw.rect(screen, color, (x, y, width, height))
    # 绘制文本
    font_button = pygame.font.SysFont('fangsong', 24)
    text_button = font_button.render(text, True, text_color)
    text_rect = text_button.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_button, text_rect)
# 绘制按钮
def draw_any():
    draw_button(520, 120, 150, 50, '#2196F3', '重新开始', '#ffffff')
    draw_button(520, 190, 150, 50, '#2196F3', '撤回一次', '#ffffff')
    draw_button(520, 260, 150, 50, '#2196F3', '随便玩玩', '#ffffff')
    draw_button(520, 330, 150, 50, '#2196F3', '提示一下', '#ffffff')
    draw_button(520, 400, 150, 50, '#2196F3', '请代练', '#ffffff')


# 移动功能
def move(direction):
    global board, score
    if direction == 'up':
        for j in range(BOARD_SIZE):
            for i in range(1, BOARD_SIZE):
                # 如果游戏板存在数字
                if board[i][j] != 0:
                    k = i
                    # 向上移动
                    while k > 0 and board[k - 1][j] == 0:
                        k -= 1
                    #   如果上面两个相同则合成，分数+=合成后的格子，消除旧方块
                    if k > 0 and board[k - 1][j] == board[i][j]:
                        board[k - 1][j] *= 2
                        score += board[k - 1][j]
                        board[i][j] = 0
                    # 将方块上移至可移动最上方，消除旧方块
                    elif k != i:
                        board[k][j] = board[i][j]
                        board[i][j] = 0
    elif direction == 'down':
        for j in range(BOARD_SIZE):
            # 从倒数第二行开始倒序遍历到第 0 行
            for i in range(BOARD_SIZE - 2, -1, -1):
                if board[i][j] != 0:
                    k = i
                    while k < BOARD_SIZE - 1 and board[k + 1][j] == 0:
                        k += 1
                    if k < BOARD_SIZE - 1 and board[k + 1][j] == board[i][j]:
                        board[k + 1][j] *= 2
                        score += board[k + 1][j]
                        board[i][j] = 0
                    elif k != i:
                        board[k][j] = board[i][j]
                        board[i][j] = 0
    elif direction == 'left':
        for i in range(BOARD_SIZE):
            for j in range(1, BOARD_SIZE):
                if board[i][j] != 0:
                    k = j
                    while k > 0 and board[i][k - 1] == 0:
                        k -= 1
                    if k > 0 and board[i][k - 1] == board[i][j]:
                        board[i][k - 1] *= 2
                        score += board[i][k - 1]
                        board[i][j] = 0
                    elif k != j:
                        board[i][k] = board[i][j]
                        board[i][j] = 0
    elif direction == 'right':
        for i in range(BOARD_SIZE):
            # 从倒数第二列开始倒序遍历到第 0 列
            for j in range(BOARD_SIZE - 2, -1, -1):
                if board[i][j] != 0:
                    k = j
                    while k < BOARD_SIZE - 1 and board[i][k + 1] == 0:
                        k += 1
                    if k < BOARD_SIZE - 1 and board[i][k + 1] == board[i][j]:
                        board[i][k + 1] *= 2
                        score += board[i][k + 1]
                        board[i][j] = 0
                    elif k != j:
                        board[i][k] = board[i][j]
                        board[i][j] = 0
# 生成新游戏块
def new_tile():
    # 空游戏块数组
    empty_tiles = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                empty_tiles.append((i, j))
    if empty_tiles:
        # 随机选择空数组中的元素，并通过随机浮点小于0.9的方法使新游戏块为2：4的概率为9：1
        i, j = random.choice(empty_tiles)
        board[i][j] = 2 if random.random() < 0.9 else 4
# 检查游戏是否结束
def is_game_over():
    #设置flag判断是否进入结算界面
    flag=1
    # 设置主循环判断的变量为全局变量
    global game_over
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # 存在空格
            if board[i][j] == 0:
                return False
            # 寻找可合成游戏板
            if i > 0 and board[i][j] == board[i - 1][j]:
                return False
            if j > 0 and board[i][j] == board[i][j - 1]:
                return False
            if i < BOARD_SIZE - 1 and board[i][j] == board[i + 1][j]:
                return False
            if j < BOARD_SIZE - 1 and board[i][j] == board[i][j + 1]:
                return False
    else:
        flag=0
    if flag==0:
        game_over = True
        db_sql.insertdata2(login.username, your_max_score)
        show_game_over()
    return True
#游戏结束弹窗
def show_game_over():
    # print("tc")
    global  board, score,result
    result = db_sql.selecttop()
    # 排行榜背景
    screen.fill('#7d7d73')
    draw_board()
    # 绘制标题
    font = pygame.freetype.SysFont('方正粗黑宋简体', 50)
    font.render_to(screen, (120, 160), 'Game Over', '#ff0000')
    font = pygame.freetype.SysFont('方正粗黑宋简体', 26)
    font.render_to(screen, (120, 210), '本次游戏分数：'+str(score)+'分', '#ff0000')
    font.render_to(screen, (120, 240), '最高排名：第'+str(db_sql.usertop(login.username))+'名', '#ff0000')
    # print(usertop())
    font.render_to(screen, (490, 20), '排行榜', (255, 255, 255))
    # 绘制排行榜数据
    y = 70
    for i, data in enumerate(result):
        name, score_d = data
        text = f'{i + 1}. {name} : {score_d}分'
        font.render_to(screen, (490, y), text, (255, 255, 255))
        y += 40
    # 绘制再来一局+退出游戏按钮
    draw_button(50, 280, 150, 50, '#ff0000', '再来一局', '#ffffff')
    draw_button(280, 280,150, 50, '#ff0000', '退出游戏', '#ffffff')
    global game_over
    game_over = False
    # 结束后清空游戏板
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    score = 0
    xh2=True
    while xh2:
        reset_button2_rect = pygame.Rect(50, 280, 150, 50)
        quit_button_rect = pygame.Rect(250, 280, 150, 50)
        # 处理事件
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                xh2=False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if reset_button2_rect.collidepoint(pos):
                    score = 0
                    new_tile()
                    new_tile()
                    draw_board()
                    draw_any()
                    pygame.display.flip()
                    game_over = False
                    xh2 = False
                elif quit_button_rect.collidepoint(pos):
                    game_over = True
                    xh2 = False
#记录当前游戏板
def record_board(x):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x[i][j]=board[i][j]
# 比较游戏版数据，用来判断是否成功移动
def are_boards_equal(board1, board2):
    # 逐个比较两个列表中的每个元素，如果有任何元素不同，则不相等
    for i in range(len(board1)):
        for j in range(len(board1[i])):
            if board1[i][j] != board2[i][j]:
                # 移动成功记录board_record0
                for i in range(BOARD_SIZE):
                    for j in range(BOARD_SIZE):
                        board_record0[i][j]=board_record1[i][j]
                return False
    # 移动失败记录board_record0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            board_record1[i][j] = board_record0[i][j]
    return True
# 统计游戏块数据非零个数
def is_new_board():
    count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != 0:
                count += 1
    if count == 2:
        return True
    else:
        return False
# 撤回功能
def revoke_board():
    global score,record_score
    font = pygame.font.SysFont('方正粗黑宋简体', 36)
    font2 = pygame.font.SysFont('方正粗黑宋简体', 12)
    # 起始状态判断
    if is_new_board() :
        text = font.render("要不你先动动？", True, '#ff0000')
        # 在pygame屏幕中间绘制文本
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(0.7)
    # 已撤回判断
    elif board==board_record1:
        text = font.render("别点了只能撤回一次", True, '#ff0000')
        text2 = font2.render("(除非你再动一下)", True, '#ff0000')
        # 在pygame屏幕上绘制文本
        screen.blit(text, (120, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        screen.blit(text2, (SCREEN_WIDTH // 2 + 60, SCREEN_HEIGHT // 2 + text.get_height() // 2))
        pygame.display.flip()
        time.sleep(0.7)
    # 撤回实现
    else:
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                board[i][j] = board_record1[i][j]
        # 分数恢复
        score=record_score
# 随机游戏功能
dict = {0: "up", 1: "down", 2: "left", 3: "right"}
def random_move():
    for i in range(5000):
        random_number = random.choices(range(4), weights=[0.1, 0.7, 0.1, 0.7])[0]
        # 游戏板记录1
        record_board(board_record1)
        move_order=dict[random_number]
        move(move_order)
        # 游戏板记录2
        record_board(board_record2)
        if (are_boards_equal(board_record1, board_record2)) == False:
            new_tile()
#ai模式
def ai_move():
    grid.map = board
    gridCopy = grid.clone()
    a = AI.getMove(gridCopy)
    del gridCopy
    if a==0 or a==1 or a==2 or a==3:
        best_move = dict[a]
    else:
        return 6
    return best_move
# 游戏主循环
def start():
    global game_over,score,board,record_score
    new_tile()
    new_tile()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                # 游戏板记录1
                record_board(board_record1)
                # 分数记录
                record_score=score
                if event.key == pygame.K_UP:
                    move('up')
                elif event.key == pygame.K_DOWN:
                    move('down')
                elif event.key == pygame.K_LEFT:
                    move('left')
                elif event.key == pygame.K_RIGHT:
                    move('right')
                # 游戏板记录2
                record_board(board_record2)
                # 检测是否成功移动
                if (are_boards_equal(board_record1,board_record2))==False:
                    new_tile()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 按钮响应
                mouse_pos = pygame.mouse.get_pos()
                if reset_button_rect.collidepoint(mouse_pos):
                    draw_button(520, 120, 150, 50, '#ff0000', '重新开始', '#ffffff')
                    pygame.display.flip()
                    time.sleep(0.1)
                    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
                    score = 0
                    new_tile()
                    new_tile()
                elif revoke_button_rect.collidepoint(mouse_pos):
                    draw_button(520, 190, 150, 50, '#ff0000', '撤回一次', '#ffffff')
                    pygame.display.flip()
                    time.sleep(0.1)
                    revoke_board()
                elif random_button_rect.collidepoint(mouse_pos):
                    draw_button(520, 260, 150, 50, '#ff0000', '随便玩玩', '#ffffff')
                    pygame.display.flip()
                    time.sleep(0.1)
                    random_move()
                elif ai_button_rect.collidepoint(mouse_pos):
                    draw_button(520, 400, 150, 50, '#ff0000', '请代练', '#ffffff')
                    pygame.display.flip()
                    time.sleep(0.1)
                    for i in range(5000):
                        best_move = ai_move()
                        if best_move==6:
                            break
                        move(best_move)
                        new_tile()
                        screen.fill('#7d7d73')
                        draw_board()
                        draw_score()
                        draw_your_max_score()
                        draw_max_score()
                        draw_any()
                        pygame.display.flip()
                elif ts_button_rect.collidepoint(mouse_pos):
                    draw_button(520, 330, 150, 50, '#ff0000', '提示一下', '#ffffff')
                    pygame.display.flip()
                    time.sleep(0.1)
                    best_move = ai_move()
                    move(best_move)
                    new_tile()
        screen.fill('#7d7d73')
        draw_board()
        draw_score()
        draw_your_max_score()
        draw_max_score()
        # 绘图
        draw_any()
        pygame.display.flip()
        # 游戏是否结束
        is_game_over()
start()
# 数据库操作
db_sql.db.close()
pygame.quit()
