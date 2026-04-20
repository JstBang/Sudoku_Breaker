import requests #可自動從網站中匯入cookies
import datetime #取得時間
import streamlit as st #UI設計
from tabulate import tabulate #美化版面
import time #計算耗費時間

#region 爬蟲

#api url rules
#daily mission url:"https://sudoku.com/api/dc/yyyy-mm-dd"
#optional difficulty mission url: "https://sudoku.com/api/v2/classic/{difficulty}/app_start"

#取得難易度或每日挑戰網址
def geturl():
    #檢測輸入的難度是否在預設裡面(difficuties那個list)或是今天的，否則傳回False
    if dif == "Today":
        date = datetime.date.today() #取得今天格式化後的日期(Ex:2026-04-06)
        url = f"https://sudoku.com/api/dc/{date}"
    elif dif == "Master":
        url = f"https://sudoku.com/api/v2/classic/evil/app_start"
    else:
        url = f"https://sudoku.com/api/v2/classic/{dif.lower()}/app_start"
    return url

#爬取題目跟解答(以供對答案)
def getmission():
    headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.get(url, headers=headers)
    doc = response.json()
    return doc.get("mission")

#將題目從一行轉為二維陣列
def organize(mission):
    board = []
    for i in range(9):
        board.append([])
        for j in range(9):
            t = mission[i*9+j]
            board[i].append(t)
    return board

#endregion

#region 演算法

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
    #找空格
    cell_exist = empty_cell_exist()
    if not cell_exist:
        return True
    x, y = cell_exist[1], cell_exist[0]

    #將找到的空格填入1~9
    for i in range(1,10):
        #測試該格是否合法
        if valid_number_check(str(i), x, y):
            board[y][x] = str(i)
            #如果合法就下一層
            if solver():
                #這裡是如果都填滿了，empty_cell_valid()會傳回True，而這個solver()也傳回True到main裡面呼叫他的地方
                return True
            else:
                #1~9都失敗後，將上一層改回0並回朔
                board[y][x] = '0'
    return False

#endregion

#region UI

def get_time():
    return time.time()

#印出版面
def show(board, original):
    if not original:
        st.code(tabulate(board, tablefmt="fancy_grid"), language="text")
    else:
        b = tabulate(board, tablefmt="fancy_grid").replace('0', ' ')
        st.code(b, language="text")

st.title("Sudoku Breaker Online")
tab1, tab2 = st.tabs(["從Sudoku.com抓取題目", "自行輸入題目"])

with tab1:
    dif = st.selectbox("請選擇難度或每日挑戰", ["Select", "Easy", "Medium", "Hard", "Expert", "Master", "Extreme", "Today"])
    if st.button("從網站抓取") and dif != "Select":
        url = geturl()
        mission = getmission()
        board = organize(mission)
        col1, col2= st.columns(2)
        with col1:
            st.write("The original mission:")
            show(board, True)
            start_time = get_time()
        if solver():
            with col2:
                st.write("The generated Solution:")
                show(board, False)
                end_time = get_time()
                st.write(f"耗時: {round(end_time - start_time, 5)}秒")
        else:
            with col2:
                st.write("No solution available")

with tab2:
    board = [list("0"*9) for i in range(0, 81, 9)]
    for i in range(9):
        cols = st.columns(9)
        for j in range(9):
            with cols[j]:
                ans = st.text_input(label=f"{i}{j}", value='', max_chars=1, label_visibility="collapsed")
                if ans == '' or ans == ' ':
                    ans = '0'
                board[i][j] = ans
    #board = organize("290045801080026300040890006008003007432000000010000600005070000000002008100530004")
    col1, col2= st.columns(2)
    if st.button("生成"):
        numbers = ['0','1','2','3','4','5','6','7','8','9']
        isNumber = True
        for i in range(9):
            for j in range(9):
                if board[i][j] not in numbers:
                    isNumber = False
                    st.write(f"({j+1},{i+1}) 填入無效字元")
        if isNumber:
            with col1:
                st.write("The original mission:")
                show(board, True)
                start_time = get_time()
            if solver():
                with col2:
                    end_time = get_time()
                    st.write("The generated Solution:")
                    show(board, True)
                    st.write(f"耗時: {round(end_time - start_time, 5)}秒")
            else:
                with col2:
                    st.write("No solution available")

#endregion