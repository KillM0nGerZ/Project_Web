def checkLogin(data,username,password):
    for i in data:
        if i['username'] == username:
            print("มีจ้าา")
            for j in data:
                if j['password']  == password:
                    return True
                else:
                    return False
    return False
    
def checkRegister(data,name,username):
    for i in data:
        if i['username'] == username:
            return False
        if i['name'] == name:
            return False
    return True

def chaeckPassword(password,Cpassword):
    return password == Cpassword



def checkRunner(date,distance,Num_time):
    if date == "" or distance == "" or Num_time == "" :
        return False
    else:
        return True

def checkDigit(distance,Num_time):
    try:
        float(distance)
        float(Num_time)
        return True
    except:
        return False

def PasswordNUM(password,Cpassword):
    try:
        float(password)
        float(Cpassword)
        return True
    except:
        return False
def checkNUM(distance):
    if int(distance) < 0:
        return False
    else:
        return True

def checkTime(Num_time):
    if int(Num_time) < 0:
        return False
    else:
        return True