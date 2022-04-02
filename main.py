import register
import client

def get_command():
    print("What do you want ? \r\n" +
      "1. Register\r\n" +
      "2. Login \r\n")
    command = input("Select an option:\r\n")

    if command == '1':
        print("Register Mode")

    elif command == '2':
        print("Login Mode")

    else:
        print("Wrong command, try again !!!")
        get_command()


