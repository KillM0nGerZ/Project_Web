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
def home():
    return render_template("Home.html")
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
                session['name'] = user[0]['name']
                session['username'] = user[0]['username']
                return redirect(url_for("home"))
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
    return redirect(url_for("home"))
# -------- Stop Logout ---------- #



@app.route('/Runner')
def Runner():
    return render_template("Runner.html")


@app.route('/Ranking')
def Ranking():
    return render_template("Ranking.html")


@app.route('/r',methods=["GET", "POST"])
def r():
    # print(request.method)
    # date = request.form.get('date')
    # distance = request.form.get('distance')
    # Num_time = request.form.get('Num_time')
    # pace = request.form.get('pace')
    # return 'Form submitted'
    return redirect(url_for('r'))


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug =True
    app.run(host="localhost",port=800)