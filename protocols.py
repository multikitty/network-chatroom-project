# Set Protocols in here


# Register a client
def client_register(user_name, password):
    return (f"Make -Option <user:{user_name}> -Option <password:{password}>")

# Accepted user to register
def accepted_client_register(id):
    return (f"User Accepted -Option <id:{id}>")

# Not Accepted (Rejected) user to register
def rejected_client_register(str):
    return(f"User Not Accepted -Option <reason:{str}")

# Login a client
def client_login(user_name, password):
    return (f"Connect -Option <user:{user_name} -Option <pass:{password}")

# Connected a user and logged in
def client_logged_in(id,sid):
    return (f"Connected -Option <id:{id} -Option <SID:{sid}")

# ERROR (can't) to login
def error_login(str):
    return (f"ERROR -Option <reason:{str}")

# Join client to group
def join_client_to_room(user_name, Group_name):
    return (f"Group -Option <user:{user_name} -Option <gname:{Group_name}")

# Added a client to a group
def added_client_to_group(user_name):
    return (f"<{user_name}> join the chat room.")

# Welcome client to join group
def welcome_client_to_groupO(user_name):
    return(f"Hi <{user_name}>, welcome to the chat room.")

# Request for get online clients
def request_get_online_clients(user_name):
    return (f"Users -Option <user:{user_name}>")

# Answer to request of get online clients
def get_online_clients(req):
    user_names = ""
    for client in req:
        user_names = user_names + str(client) + "|"
    user_names = user_names[0:len(user_names) - 1]
    return (f"USERS_LIST: \r\n{user_names}\r\n")

# Send general message from a client in group
def send_geeneral_client_message(GAPNAME , msg):
    return (f"GM -Option <to:{GAPNAME} -Option <message_len:{len((msg))}> -Option <message_body:{msg}")

# Send general message from a server in group
def send_geeneral_server_message(username, GAPNAME, msg):
    return (f"GM -Option <from:{username}> -Option <to:{GAPNAME}> -Option <message_len:{len(msg)}> -Option <message_body:{msg}>")

# Send private message from client
def send_private_client_message(user_name, msg):
    return (f"PM -Option <message_len:{len(msg)}> -Option <to:{user_name}> -Option <message_body:”{msg}”>")

# Send private message from server
def send_private_server_message(source_user, destination_user, msg):
    return (f"PM -Option <from:{source_user}> -Option <to:{destination_user}> -Option <message_len:{len(msg)}> -Option <message_body:”{msg}”>")

# Request for leave a group or chat from client
def client_leave(name):
    return (f"End -Option <id:{name}")

# Declaration of leave a client
def declaration_leave_client(user_name):
    return (f"{user_name} left the chat room.")

# Split => Make -Option <user:{user_name}> -Option <passwrod:{password}>
def split_client_register(message):
    msg = message.replace(" ", "")
    msg = msg.replace("-Option", "")
    msg = msg.replace("Make", "")
    msg = msg.replace("<", "")
    msg = msg.replace(">", "")
    msg = msg.replace("user:", "")
    msg = msg.replace("password:", "--")
    return msg;

