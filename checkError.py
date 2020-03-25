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


