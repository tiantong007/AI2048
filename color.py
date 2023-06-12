#颜色表
def get_color(value):
    # 根据游戏块数字获取颜色
    colors = {
        0: '#CDC1B4',
        2: '#eee4da',
        4: '#ede0c8',
        8: '#f2b179',
        16: '#f59563',
        32: '#f67c5f',
        64: '#f65e3b',
        128: '#edcf72',
        256: '#edcc61',
        512: '#edc850',
        1024: '#edc53f',
        2048: '#edc22e',
    }
    return colors.get(value, '#000000')