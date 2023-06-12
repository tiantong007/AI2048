import tkinter as tk
import db_sql
from tkinter import messagebox
username=''
def login():
    def login_verify():
        global username
        username = username_verify.get()
        if not username:
            messagebox.showinfo("错误", "请输入昵称！")
            return
        result = db_sql.selectuser(username)
        if result or result==0:
            messagebox.showinfo("登录成功", "欢迎您来到2048,您的最高分数为：{}".format(result))
        else:
            db_sql.insert_user(username)
            messagebox.showinfo("登录成功", "欢迎您来到2048,快创造属于你的记录吧！")
        root.destroy()
    root = tk.Tk()
    root.geometry("520x300")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width - 520) / 2)
    y = int((screen_height - 300) / 2)
    root.geometry("+{}+{}".format(x, y))
    root.title("登陆界面")
    tk.Label(text="欢迎来到2048游戏", font=("方正粗黑宋简体", 20)).place(x=140, y=70)
    tk.Label(text="前方何人，报上名来：", font=("方正粗黑宋简体", 15)).place(x=120, y=130)
    username_verify = tk.StringVar()
    username_login_entry = tk.Entry(root, textvariable=username_verify, width=30, font=("方正粗黑宋简体", 15))
    username_login_entry.place(x=120, y=170)
    tk.Button(text="进入游戏", width="10", font=("方正粗黑宋简体", 15), command=login_verify).place(x=200, y=230)
    root.mainloop()
if __name__ == '__main__':
    login()
