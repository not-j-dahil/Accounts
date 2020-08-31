import sqlite3 #for database
import hashlib #for hashing
import datetime #for pepper
import random

conn = sqlite3.connect("TestDB.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS accounts (username TEXT, password TEXT, salt TEXT)")
conn.commit()

#SALT
def makeSalt():
    '''creates salt for hashing passwords'''
    chars = "!£$%&.1234567890"
    ranNum = random.randint(5,10)
    salt = ""
    for i in range(ranNum):
        ranChar = chars[random.randint(1, len(chars)-1)]
        salt = salt + ranChar
    return salt

def makePepper():
    '''creates pepper for hashing passwords'''
    currentDT = datetime.datetime.now()
    hour = currentDT.hour
    minute = currentDT.minute
    second = currentDT.second
    return str(hour+minute+second)

def userRegister():
    '''Function to ask the user to register'''
    same = True
    username = input("Enter username: ")
    while same:
        password = input("Enter password: ")
        conpassword = input("Enter password again: ")
        if(password == conpassword):
            register(username, password)
            same = False
        else:
            print("Mismatched passwords")
    
def register(username, password):
    '''Function to register a user'''
    salt = makeSalt()
    pepper = makePepper()
    hashpass = hashlib.md5(password.encode()).hexdigest()
    seasonedpass = hashlib.md5((hashpass+salt+pepper).encode()).hexdigest()
    cursor.execute("INSERT INTO accounts VALUES (?, ?, ?)",(username, seasonedpass, salt))
    data = cursor.execute("SELECT * FROM accounts").fetchall()
    print("\n", data, "\n")
    conn.commit()

def userLogin():
    '''Function to ask the user to Login'''
    username = input("Enter username: ")
    password = input("Enter password: ")
    userFound = login(username, password)

def login(user, password):
    '''Function to login a user, returns true if found'''
    data = cursor.execute("SELECT * FROM accounts WHERE username = ?", (user,)).fetchone()
    print(data)
    if data == None:
        print("User not found\n")
    else:
        hashpass = hashlib.md5(password.encode()).hexdigest()
        storedPass = data[1]
        salt = data[2]
        print(type(salt))
        for i in range(23+59+59):
            #i = pepper
            seasonedpass = hashlib.md5((hashpass+salt+str(i)).encode()).hexdigest()
            if seasonedpass == storedPass:
                return True
        return False # user not found

def main():
    print("hello world\n")

    while True:
        userInput = input("What do you want to do? \n1. Register \n2. Login \n3. Show table \n4. Drop Table \n5. Exit \n\n:").lower()
        if userInput in ["Exit","5"]:
            print("Bye bye :]")
            break
        elif userInput in ["register", "1"]:
            userRegister()
        elif userInput in ["login", "2"]:
            userLogin()
        elif userInput in ["show table", "3"]:
            if(cursor.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='accounts'").fetchone()[0] == 1):
                print(" = This is the Table =\n",cursor.execute("SELECT * FROM accounts").fetchall(), "\n")
            else:
                print("No tables found")
        elif userInput in ["drop table", "4"]:
            cursor.execute("DROP TABLE accounts")
            conn.commit


if __name__ == "__main__":
    main()
