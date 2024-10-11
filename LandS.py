import blackjack
import sqlite3
import time
import re
Username = ''
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check(email):
    if(re.fullmatch(regex, email)):
        print("Valid Email")
        return
    else:
        print("Invalid Email")
        return 'email'

#defining the database
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

database = sqlite3.connect('DATABASES.db')
database.row_factory = dict_factory
#creating the database columns
database.execute('''CREATE TABLE if not exists USERS
  (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    Email TEXT NOT NULL,
    Username TEXT NOT NULL,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Age INTEGER NOT NULL,
    Password TEXT NOT NULL,
    Wallet INTEGER NOT NULL);''')

def SignUp(username,password,firstname,lastname,age,email):
    #checking for clashing usernames
    clash = database.execute(
        "SELECT ID FROM USERS Where Username =?",[username]).fetchall()
    if len(clash) !=  0:
        clash = 'clashing'
        return clash
    #verifying age is above 17
    verify = int(age)-18
    if verify <= -1:
        underage= 'underage' 
        return underage

    Hpassword = 0
    Wallet = 1000
    
    #checking valid email   
    Echeck = check(email)
    if Echeck == 'email':
        return 'email'

    for x in range(len(password)):
        Hpassword = Hpassword + ord(password[x])
    Hpassword = ((Hpassword * 5 + 4)*542)//3 % 23
    #adding all new details to the database
    database.execute('''INSERT  INTO USERS (Email,Username,FirstName,LastName,Age,Password,Wallet) VALUES(?,?,?,?,?,?,?)''',
        [email, username, firstname, lastname, age, Hpassword, Wallet])
    database.commit()

    time.sleep(2)
    return username


def LogIn(username, password):

    Hpassword = 0
    for x in range(len(password)):
        Hpassword = Hpassword + int(ord(password[x]))
    Hpassword = ((Hpassword * 5 + 4 )* 542)//3 % 23
    #checking to find the username and password in database
    ForP = database.execute(
        "SELECT Username,Password FROM USERS WHERE Username =? AND Password =?",
        [username, Hpassword]).fetchone()
    if ForP != None:
        if ForP['Username'] == username:
            if int(ForP['Password']) == Hpassword:
                return username
    username = 'wrong'
    return username
    

def Welcome():
    global Username
    choice = input("Do you want to log in (l) or sign up (s)")
    if choice.lower() == 'l':
        Username = LogIn()
    elif choice.lower() == 's':
        Username = SignUp()



def playing(Username, database):
   black = input("do you want to play blackjack")
   while black == "yes":
       blackjack.Play(Username, database)
       black = input("do you want to play again")

