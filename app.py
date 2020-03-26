from flask import Flask, render_template, redirect, request, url_for, session,flash
from flask_mysqldb import MySQL, MySQLdb
from sqlalchemy import text
import bcrypt

import checkError as c


app = Flask(__name__)
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_DB']='wedapp'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql = MySQL(app)

# @app.route("/main",methods=['GET','POST'])
# def main():
#     print("เข้า main")
#     print(request.form.get('send'))
#     if request.form.get('send') == 'register':
#         print("เข้า register")
#         return redirect(url_for('register'))
#     elif request.form.get('send') == 'login':
#         print("เข้า login")
#         username = request.form['username']
#         password = request.form['password']
#         return redirect(url_for('/login'))
#         # return login(username,password)

# -------- Start index ----------- #
@app.route('/')
def index():
    return render_template("index.html")
# -------- Stop index ------------ #


# -------- Start OpenLogin ---------- #
@app.route("/Login",methods=['GET', 'POST'])
def Login():
    return render_template("Login.html")
# -------- Stop OpenLogin ---------- #



# -------- Start Login ---------- #
@app.route("/login",methods=['GET', 'POST'])
def login():
    print(request.method)
    if request.method == "POST":
        username =request.form['username']
        password =request.form['password']
        # username =request.form.get('username')
        # password =request.form.get('password')
        print(username,password)
        cur = mysql.connection.cursor()
        # cur.execute("SELECT * FROM member WHERE username=%s",[username])
        cur.execute("SELECT * FROM member ")
        user = cur.fetchall()
        if c.checkLogin(user,username,password):
            print(user[0]['password'])
            if user != ():
                for i in user:
                    if username == i['username']:
                        print(user[0])
                        session['mem_id'] = i['mem_id']
                        session['name'] = i['name']
                        session['username'] = i['username']
                        return redirect(url_for("index"))
            else:
                return redirect(url_for("Login"))
        else:
            flash("รหัสผ่านผิด")
            return redirect(url_for("Login"))

# -------- Stop Login ---------- #




# -------- Start register ---------- #
@app.route('/register',methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("Register.html")
    else:
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        # hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        Cpassword = request.form['Cpassword']


        if c.PasswordNUM(password,Cpassword):
            if c.chaeckPassword(password,Cpassword):
                cur = mysql.connection.cursor()
                cur.execute("SELECT * FROM member ")
                user = cur.fetchall()
                if c.checkRegister(user,username,password):
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO member (name,username,password) VALUES (%s,%s,%s)",(name,username,password))  # INSERT Database
                    print(cur)
                    mysql.connection.commit() 
                    # session['name'] = name            # save to session
                    # session['username'] = username    # save to session  

                    return redirect(url_for("Login"))
                else:
                    flash("Username นี้ไม่สามารถใช้งานได้")
                    return render_template("Register.html")
            else:
                flash("กรุณากรอก password ให้ถูกต้อง")
                return render_template("Register.html")
        else:
            flash("กรุณากรอก password เฉพาะตัวเลข")
            return render_template("Register.html")

# -------- Stop register ---------- #



# -------- Start Logout ---------- #
@app.route('/loguot')
def loguot():
    session.clear()  
    return redirect(url_for("index"))
# -------- Stop Logout ---------- #



@app.route('/Runner')
def Runner():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM runner WHERE mem_id = "+str(session['mem_id']))
        data = cur.fetchall()
        count = 0
        sum_distance = 0
        sum_pace = 0
        avg_distance = 0
        avg_pace = 0

        if data != (): # เช็คค่าว่างของ  User
            for i in data:
                count +=1
                sum_distance +=float(i['distance'])
                sum_pace += float(i['pace'])
            avg_distance = "%.2f" % (sum_distance/count)
            avg_pace = "%.2f" % (sum_pace/count)

        session['count'] = count
        session['sum_distance'] = sum_distance
        session['avg_distance'] = avg_distance
        session['avg_pace'] =  avg_pace


        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM ranking WHERE mem_id = "+str(session['mem_id']))
        checkdata = cur.fetchall()
        print(checkdata)
        if checkdata == ():
            cur.execute("INSERT INTO ranking (mem_id,distance,avg_distance,run_num,avg_pace) VALUES (%s,%s,%s,%s,%s)",(session['mem_id'],session['sum_distance'],session['avg_distance'],session['count'],session['avg_pace']))
            mysql.connection.commit()
        else:
            cur.execute("UPDATE ranking SET distance ="+str(session['sum_distance'])+",avg_distance ="+str(session['avg_distance'])+ ",run_num ="+str(session['count'])+",avg_pace ="+str(session['avg_pace'])+" WHERE mem_id ="+str(session['mem_id']))
            mysql.connection.commit()
        return render_template("Runner.html",row=data)
    except:
        return render_template("Runner.html")

    

# -------------- show status --------------
@app.route('/runner',methods=["GET", "POST"])
def runner():


    session['date'] = request.form['date']
    session['distance'] = request.form['distance']
    session['Num_time'] = request.form['Num_time']

    if c.checkRunner(session['date'] ,session['distance'],session['Num_time']):
        if c.checkDigit(session['distance'],session['Num_time']):
            session['pace'] = request.form['pace'] 
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO runner (mem_id,distance,Num_time,pace,date) VALUES (%s,%s,%s,%s,%s)",(session['mem_id'],session['distance'],session['Num_time'],session['pace'],session['date']))  # INSERT Database
            print(cur)
            mysql.connection.commit()

            return redirect(url_for("Runner"))
        else:
            print("ใส่ตัวเลข")
            flash("กรุณากรอกตัวเลข")
            return redirect(url_for("clear"))
    else:
        print("ไม่ผ่านนน")
        flash("กรุณากรอกข้อมูลให้ครบ")
        return redirect(url_for("Runner"))
# -------------- show status --------------







@app.route('/clear')
def clear():
    session['date'] = ""
    session['distance'] = ""
    session['Num_time'] = ""
    session['pace'] = ""
    return redirect(url_for("Runner"))





@app.route('/Ranking')
def Ranking():
    cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM ranking ORDER BY distance DESC")
    cur.execute("SELECT member.name,ranking.distance, ranking.avg_pace FROM ranking INNER JOIN member ON member.mem_id = ranking.mem_id ORDER BY distance DESC")
    data = cur.fetchall()
    num=0
    item=[]
    for i in data:
        num+=1
        i['num']=num
        item.append(i)
    item = tuple(item)
    return render_template("Ranking.html",row=data,num=item)




if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug =True
    app.run(host="localhost",port=800)