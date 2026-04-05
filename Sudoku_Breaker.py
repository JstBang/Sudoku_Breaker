import requests #可自動從網站中匯入cookies
import datetime #取得時間
from tabulate import tabulate #美化顯示版面
import streamlit as st

#api url rules
#daily mission url:"https://sudoku.com/api/dc/yyyy-mm-dd"
#optional difficulty mission url: "https://sudoku.com/api/v2/classic/{difficulty}/app_start"

#取得難易度或每日挑戰網址
def geturl():
    if dif in difficulties:
        url = f"https://sudoku.com/api/v2/classic/{dif}/app_start"
    elif dif == "today":
        date = datetime.date.today()
        url = f"https://sudoku.com/api/dc/{date}"
    else:
        return False
    return url

#爬取題目跟解答(以供對答案)
def getmission():
    headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    rs = requests.session()
    response = requests.get(url, headers=headers)
    doc = response.json()
    return [doc.get("mission"), doc.get("solution")]

#將題目從一行轉為二維陣列
def organize(mission):
    board = []
    for i in range(9):
        board.append([])
        for j in range(9):
            t = mission[i*9+j]
            board[i].append(t)
    return board

#取得最近(從左上角至右下角)的空格欄位(x,y)，若無空格判定為完成(傳回False)
def empty_cell_exist():
    for i in range(9):
        for j in range(9):
            if board[i][j] == '0':
                return [i, j]
    return False

#檢查填入數字是否合法(列行區)
def valid_number_check(num, x, y):
    #horizontal
    for i in range(9):
        if board[y][i] == num:
            return False
    
    #column
    for i in range(9):
        if board[i][x] == num:
            return False
        
    #block
    for i in range((y//3)*3, (y//3)*3+3):
        for j in range((x//3)*3, (x//3)*3+3):
            if board[i][j] == num:
                return False
    
    return True

#由1填至9測試，若皆不合法則改為0並遞迴至上一層
def solver():
    cell_exist = empty_cell_exist()
    if not cell_exist:
        return True
    x, y = cell_exist[1], cell_exist[0]
    for i in range(1,10):
        if valid_number_check(str(i), x, y):
            board[y][x] = str(i)
            if solver():
                return True
            else:
                board[y][x] = '0'
    return False

#印出版面
def show(board):
    print(tabulate(board, tablefmt="fancy_grid"))

difficulties = ["easy", "medium", "hard", "expert", "master", "extreme"]

dif = input("請輸入難度(本日為today): ").lower()
url = geturl()
if not url:
    print("難度輸入錯誤")
else:
    mission, solution= map(str, getmission())
    board = organize(mission)

    if solver():
        show(board)
    else:
        print("no solution available")
    show(organize(solution))
