from flask import Flask, render_template, url_for,request,redirect
from flask_mysqldb import MySQL
from sqlalchemy import text

app = Flask(__name__)
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_DB']='wedapp'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template('Login.html')

# @app.route("/register",methods=['GET','POST'])
# def register():
#     return render_template('Register.html')


@app.route("/wellcom",methods=['GET', 'POST'])
def wellcom():
    return "<h1>Hello world</h1>"

@app.route("/main",methods=['GET', 'POST'])
def main():
    if request.method == "POST":
        if request.form.get('register') == 'register':
            return redirect(url_for('register')) #เปิดหน้า register
        elif request.form.get('login') == 'login':
            username = request.form.get('username')
            password = request.form.get('password')
            print(username,password)
            if check_login(username,password): #ส่งไปเช็ครหัสผ่าน
                return Home() #เรียกใช้ root /main
            else:
                return "<h>รหัสไม่ถูกต้อง</h>"

        elif request.form.get('cancel') == 'cancel':
            return redirect(url_for('login'))
        elif request.form.get('submit') == 'submit':
            name = request.form.get('name')
            username = request.form.get('username')
            password = request.form.get('password')
            Cpassword = request.form.get('Cpassword')
            # return redirect(url_for('submit',name=name,username=username,password=password))
            return submit(name,username,password)



#-------------------------- เก็บข้อมูลลง Data base --------------------------------
# @app.route("/submit/<string:name>/<string:username>/<string:password>",methods=['GET', 'POST'])
def submit(name,username,password):
    print(name,username,password)
    if check_register(name,username):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO member (name,username,password) VAlUES (%s,%s,%s)",(name,username,password))
        mysql.connection.commit()
        return "<h1>ผ่านน</h1>"
    else:
        return "<h1>ไม่ผ่านน</h1>"
#-------------------------- เก็บข้อมูลลง Data base --------------------------------




#--------------------------- เช็คการสมัคร --------------------------------------
def check_register(name,username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT name,username FROM member")
    data = cur.fetchall()
    for j in range(0,len(data)):
        if name == data[j]['name'] or username == data[j]['username'] :
            item = False
            break
        else:
            item = True
    print(item)
    return item
#--------------------------- เช็คการสมัคร --------------------------------------




#-------------------- เช็ครหัสผ่าน ------------------------------------#
def check_login(username,password): 
    cur = mysql.connection.cursor()
    cur.execute("SELECT username,password FROM member WHERE username=%s",[username])
    data = cur.fetchall()
    print(data)
    print(type(data))
    print(username,password)
    # print(type(data[0]['name']))
    # print(type(name))
    # print(name)
    if data != (): #  ---> () ค่าว่างใน Tuples
        if username == data[0]['username'] and password == data[0]['password']:
            return True
        else:
            return False
    else:
        return False
#-------------------- เช็ครหัสผ่าน ------------------------------------#



@app.route("/login",methods=['GET', 'POST'])
def login():
    return render_template("Login.html")

@app.route("/register",methods=['GET', 'POST'])
def register():
    return render_template("Register.html")

@app.route("/home",methods=['GET', 'POST'])
def Home():
    return render_template("/Home.html")





if __name__ == "__main__":
    app.debug =True
    app.run(host="localhost",port=8000)