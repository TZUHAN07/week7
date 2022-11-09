
from flask import Flask, request, render_template, session, redirect, url_for, make_response,jsonify
# 載入Flask,Request 物件, render_template 函式,session,redirect函式
import mysql.connector


# 建立Application 物件，可以設定靜態檔案的路徑處理
app = Flask(__name__, static_folder="static", static_url_path="/")
# 靜態檔案的資料價名稱 , 靜態檔案對應的網址路徑
app.secret_key = "any string but secret"  # 設定sessin的密鑰
# 連接 MySQL 資料庫
try:
    mydb = mysql.connector.connect(
        host="localhost",    # 主機名稱
        user="root",         # 帳號
        password="j610114*",  # 密碼
        database='website'   # 資料庫名稱
    )
except mysql.connector.Error as err:
        print(err)

@app.route("/", methods=['GET'])
def firstpage():  # 用來回應網站首頁函式
    return render_template("firstpage.html")

@app.route("/api/member", methods=['GET'])  # 建立/api對應的處理函式
def member_api():
    
    username=request.args["username"]
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT id, name, username FROM member WHERE username = %s ", (username,))
    member= mycursor.fetchone()
    if member:
        choose_username ={"id":member[0],"name":member[1],"username":member[2]}
        print(choose_username)
        return jsonify({"data":choose_username})
    else:
        #mycursor.close()
        #mydb.close()
        return jsonify({"data":None})      

               
# 啟動網站伺服器，可透過post參數指定埠號
app.run(port=3000, debug=True)
