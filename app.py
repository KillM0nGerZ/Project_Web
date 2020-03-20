from flask import Flask, render_template, redirect, request, url_for, session
from flask_mysqldb import MySQL, MySQLdb
from sqlalchemy import text
import bcrypt

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
        cur.execute("SELECT * FROM member WHERE username=%s",[username])
        user = cur.fetchall()
        print(user[0]['password'])
        if user != ():
            if password == user[0]['password']:
                session['mem_id'] = user[0]['mem_id']
                session['name'] = user[0]['name']
                session['username'] = user[0]['username']
                return redirect(url_for("index"))
        else:
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

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO member (name,username,password) VALUES (%s,%s,%s)",(name,username,password))  # INSERT Database
        print(cur)
        mysql.connection.commit() 
        # session['name'] = name            # save to session
        # session['username'] = username    # save to session  

        return redirect(url_for("Login"))

# -------- Stop register ---------- #



# -------- Start Logout ---------- #
@app.route('/loguot')
def loguot():
    session.clear()  
    return redirect(url_for("index"))
# -------- Stop Logout ---------- #



@app.route('/Runner')
def Runner():
    return render_template("Runner.html")



# -------------- show status --------------
@app.route('/runner',methods=["GET", "POST"])
def runner():
    session['date'] = request.form['date']
    session['distance'] = request.form['distance']
    session['Num_time'] = request.form['Num_time']
    session['pace'] = request.form['pace'] 


    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO runner (mem_id,distance,Num_time,pace,date) VALUES (%s,%s,%s,%s,%s)",(session['mem_id'],session['distance'],session['Num_time'],session['pace'],session['date']))  # INSERT Database
    print(cur)
    mysql.connection.commit()

    return redirect(url_for("Runner"))
# -------------- show status --------------



@app.route('/Ranking')
def Ranking():
    return render_template("Ranking.html")




if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug =True
    app.run(host="localhost",port=800)