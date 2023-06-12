import pymysql

# 打开数据库连接，参数1：主机名或IP；参数2：用户名；参数3：密码；参数4：数据库名
db = pymysql.connect(host='127.0.0.1', user='root', password='123456', database='2048')
cursor = db.cursor()
# 查询最高排名
def usertop(username):
    cursor.execute("SELECT COUNT(*)+1 AS score_rank FROM score WHERE max_score > (SELECT max_score FROM score WHERE name = %s);",[username])
    result = cursor.fetchone()
    return result[0]
# 查询最高分
def selecttop():
    # 使用execute()方法执行SQL查询
    cursor.execute("SELECT * FROM score ORDER BY max_score DESC LIMIT 10")
    # 使用fetchone()方法获取单条数据
    result = cursor.fetchall()
    return result
def selectdata():
    # 使用execute()方法执行SQL查询
    cursor.execute("SELECT max(max_score) from score")
    # 使用fetchone()方法获取单条数据
    data = cursor.fetchone()
    return data[0]
# 查询用户
def selectuser(username):
    select_sql = "select max_score from score WHERE name=%s"
    cursor.execute(select_sql, [username])
    data = cursor.fetchone()
    if data:
        return data[0]
# 添加一条最高分数据
# def insertdata(max_score):
#     if max_score>history_score:
#         insert_score_sql = "insert into score (max_score) values ({0})".format(max_score)
#         # 执行语句
#         cursor.execute(insert_score_sql)
#         # 提交数据
#         db.commit()
# 更新一条个人最高分数据
def insertdata2(name,max_score):
    your_history_score = selectuser(name)
    if max_score > your_history_score:
        # insert_score_sql = "INSERT INTO score (name,max_score) VALUES (%s,{})".format(max_score)
        update_score_sql = "UPDATE score SET max_score={} WHERE name=%s".format(max_score)
        # 执行语句
        cursor.execute(update_score_sql, [name])
        # 提交数据
        db.commit()
# 添加一条用户数据
def insert_user(username):
    insert_score_sql = "insert into score (name,max_score) values (%s,0)"
    # 执行语句
    cursor.execute(insert_score_sql, [username])
    # 提交数据
    db.commit()
# 获取历史最高分数
history_score=selectdata()
# 获取最高分
max_score = selectdata()