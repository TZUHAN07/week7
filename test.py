
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


@app.route("/member")  # 建立/member對應的處理函式
def sucessful():
    # check if the users exist or not
    if not session.get("name"):
        return redirect("/")
    else:
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(
            "SELECT member.name,message.content FROM member INNER JOIN message ON member.id =message. member_id")
        message = mycursor.fetchall()
        total = len(message)

        for data in range(total):
            each_name = message[data][0]
            each_message = message[data][1]
            data += data

        #mycursor.close()
        #mydb.close()
        return render_template("member.html", name=session["name"], each_name=each_name, each_message=each_message)


@app.route("/api/member", methods=["GET","PATCH"])  # 建立/api對應的處理函式
def member_api():
    if request.method == "GET":
        if session.get("username"):
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
                mydb.close()
                return jsonify({"data":None})    
        else:
            return jsonify({"data":None})

    if request.method == "PATCH":
        name = request.get_json()
        print(name)
        username=session["username"]
        if session.get("username"):
            mycursor = mydb.cursor(buffered=True)
            mycursor.execute("UPDATE member SET name= %s WHERE username= %s", (name["name"],username))
            mydb.commit()  # 提交至數據庫執行
            
            session.name =name["name"]
            mycursor.close()
            response=make_response(jsonify(name),200)
            print(response)
            return jsonify(ok=True) 
        else:
            return jsonify(error=True)

               

@app.route("/error")  # 建立/error對應的處理函式
def geterror():
    message = request.args["message"]
    return render_template("error.html", message=message)


@app.route("/signup", methods=["POST"])  # 建立註冊頁對應的處理函式
def signup():
    message = ''
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT * FROM member WHERE username = %s ", (username,))
    account = mycursor.fetchone()
    if account:
        message = "帳號已經被註冊"
        return redirect(url_for("geterror", message=message))
    else:
        insert_data = (
            "INSERT INTO member (name, username,password) VALUES (%s,%s,%s)")
        val = (name, username, password)
        mycursor.execute(insert_data, val)  # 執行sql語句
        mydb.commit()  # 提交至數據庫執行
        mycursor.close()
        mydb.close()
        return render_template("firstpage.html")


@app.route("/signin", methods=["POST"])
def signin():  # 用來進⾏驗證的函式
    username = request.form["username"]
    password = request.form["password"]
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT * FROM member WHERE username = %s AND password= %s", (username, password))
    account = mycursor.fetchone()
    if account:
        session["id"] = account[0]
        session["name"] = account[1]
        session["username"] = account[2]
        session["password"] = account[3]
        return redirect(url_for("sucessful"))

    else:
        mycursor.close()
        mydb.close()
        return redirect(url_for("geterror", message="帳號、或密碼輸入錯誤"))


@app.route("/signout", methods=["GET"])
def signout():  # 用來進⾏登出的函式
    session.pop("id", None)
    session.pop("name", None)
    session.pop("username", None)
    session.pop("password", None)
    # session.clear()
    return redirect(url_for("firstpage"))


@app.route("/message", methods=["post"])
def message():
    content = request.form["message"]
    id = session["id"]  # 存放在 cookie 的 id
    insert_data = (
        "INSERT INTO message(member_id, content) VALUES (%s, %s)")
    val = (id, content)
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(insert_data, val)
    mydb.commit()
    mycursor.close()
    mydb.close()
    return redirect(url_for("sucessful"))


# 啟動網站伺服器，可透過post參數指定埠號
app.run(port=3000, debug=True)
