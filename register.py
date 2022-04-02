import sqlite3
import hashingFunction
import protocols

def get_username():
    username = input("Write your username\r\n")
    return username

def get_password():
    password = input("Write your password\r\n")
    return password


# username = get_username()
# password = get_password()

username = "danial"
password = "751250"

Create_User = 'INSERT INTO User(username, password) VALUES (?,?)'
Get_Users = 'SELECT * FROM User WHERE username = ?'

def check_users(user):
    with sqlite3.connect('database.sqlite3') as connection:
        users = connection.cursor()
        users.execute(Get_Users,(user,))
        return users.fetchall()

#print(check_users(username))

def register_validation(username, password):
    if len(check_users(username)) == 0:
        if len(password) > 5:
            print("Your account is registered !!!\r\n" +
                  f"Welcome {username}")
            return ("registered")
        else:
            print("Your password should be at lease 6 character")
            return ("passLimited")
    else:
        print("This username is already in use\r\n"
              "You have choise new username or login and Try again")
        return ("duplicate")

def register(username,password):
    with sqlite3.connect('database.sqlite3') as connection:
        connection.execute(Create_User, tuple((username, password)))
        connection.commit()

register_validation(username,password)




