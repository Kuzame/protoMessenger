# Copyright - Adrian Harminto
import socket
from thread import *
from functions import *
from time import sleep

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 4000 # Arbitrary non-privileged port
clientList=[]
clientUser=[]
userList={}
path=os.path.join(sys.path[0], "data.json")
userList=updateContent(path)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

'''
Main Menu:
1. Logout
2. Change Password
3. Broadcast to all
4. Messaging Service
    1. Send Message
        1. View Online Users
            0. Cancel
            1. 2. 3. etc...
                [Enter message]
        2. View Friends
            0. Cancel
            1. 2. 3. etc...
                [Enter message]
        3. Cancel
    2. View Unread Messages
    3. View Read Messages
    4. Cancel
5. Add as Friend
    1. View Online Users
        0. Cancel
        1. 2. etc [Enter which online user]
    2. Add Users by username (ID)
        0. Cancel
        [Enter username]
    3. Cancel
6. View Pending Friend Requests
7. View Online Users
8. View Friends' Status/Wall Timeline
    0. Cancel
    1. 2. 3. etc...
        1. View Status
        2. View Wall/Status History
        3. Cancel
9. My Status/Wall Timeline
    1. Post Status
        [Enter message]
    2. View My Status
    3. View My Wall Timeline
    4. Cancel
'''
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    global userList
    notLogin=True
    user=''
    fname=''
    lname=''
    pwd=''
    #Sending message to connected client
    conn.send('Welcome to the server. Please login\n') #send only takes string
    while(notLogin):
        conn.send('Username: ')
        user=conn.recv(1024)
        conn.send('Password: ')
        pwd=conn.recv(1024)
        try:

            if(pwd==userList['users'][user]["password"]):
                fname=getfname(user, userList)
                lname=getlname(user, userList)
                conn.send("Welcome back "+fname+' '+lname+"!\nYou have "+totalUnreadMsg(user, userList)+ " unreaded message(s) & "+totalFriendRequest(user, userList)+" friend request(s)\n")
                clientUser.append(user)
                notLogin=False
            else:
                conn.send("Invalid pass\n")
        except:
            conn.send("Invalid username\n")


    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #Receiving from client
        conn.send(menu())
        data = conn.recv(1024)
        if not data:
            break
        reply = data
        userList=updateContent(path)
        #if data[0:2]=="!q":
        if data=="1": # Logout
            print(fname+' '+lname+' has logged out.')
            conn.send("Logging out\n")
            conn.close()
            clientList.remove(conn)
            clientUser.remove(user)
            print('Remaining connected client(s): {}'.format(len(clientList)))
            break
        elif data=="2": # Change password
            conn.send("Changing password\nEnter new password: ")
            pwd=conn.recv(1024)
            userList['users'][user]["password"]=pwd
            conn.send(saveJSON(userList))

        elif data=="3": # Public chat
            conn.send('Enter message to public chat (broadcast): ')
            temp=conn.recv(1024)
            for a in range(len(clientList)):
                clientList[a].sendall('(Public chat) '+fname+' '+lname+": "+temp)
            temp=''
        elif data=="4": # Messaging Service
            while True:
                conn.send(msgPrint())
                data = conn.recv(1024)
                if data=='1': #Send Message
                    while True:
                        conn.send(sendMsgPrint())
                        data = conn.recv(1024)
                        if data=='1': #View online users
                            while True:
                                conn.send(onlineList(clientUser, userList))
                                data = conn.recv(1024)
                                if data=='0': # Cancel
                                    break
                                else:
                                    conn.send("Enter the message: ")
                                    msg = conn.recv(1024)
                                    conn.send(sendOnlineMessage(data, msg, user, clientUser, userList, clientList))
                                    conn.send(saveJSON(userList))
                                    data=-1
                                    break
                        elif data=='2': #View friend lists
                            while True:
                                conn.send(friendList(user, clientUser, userList))
                                data = conn.recv(1024)
                                if data=='0': # Cancel
                                    break
                                else:
                                    conn.send("Enter the message: ")
                                    msg = conn.recv(1024)
                                    conn.send(sendFriendMessage(data, msg, user, userList, clientUser, clientList))
                                    conn.send(saveJSON(userList))
                                    data=-1
                                    break
                        else: #Cancel sending message
                            break
                        if data==-1: #Redirect to main menu (from successful operations)
                            break
                elif data=='2': #View Unread Message
                    conn.send(viewUnreadMsg(user, userList))
                    conn.send(saveJSON(userList))
                    break
                elif data=='3': #View Read Message
                    conn.send(viewReadMsg(user, userList))
                    break
                else: #Back to main menu
                    break
                if data==-1: #Redirect to main menu (from successful operations)
                    break
        elif data=="5": #Add as Friend
            while True:
                conn.send(addFriendPrint())
                data = conn.recv(1024)
                if data=='1': #Add from online user
                    conn.send(onlineList(clientUser, userList))
                    conn.send("Select user to add: ")
                    which = conn.recv(1024)
                    if which!='0':
                        conn.send(sendFriendRequest(clientUser[int(which)-1], user, userList, clientUser, clientList))
                        conn.send(saveJSON(userList))
                        data=-1
                if data=='2': #Add by using existing username
                    conn.send("Select username to add: ")
                    friendUsername = conn.recv(1024)
                    conn.send(sendFriendRequest(friendUsername, user, userList, clientUser, clientList))
                    conn.send(saveJSON(userList))
                    data=-1
                    break
                else:
                    break
                if data==-1:
                    break
        elif data=="6": #View/Accept Friend request
            if totalFriendRequest(user, userList)=='0':
                conn.send("You have no friend request!\n")
            else:
                conn.send(friendRequestList(user, clientUser, userList))
                which = conn.recv(1024)
                if which!='0':
                    conn.send(acceptFriendRequest(which, user, userList, clientUser, clientList))
                    conn.send(saveJSON(userList))
        elif data=="7": #View online users
            conn.send(onlineList(clientUser, userList))
        elif data=="8": #View friends' Status/Wall Timeline
            if totalFriends(user, userList)=='0':
                conn.send("You have no friends!\n")
            else:
                while True:
                    conn.send(friendList(user, clientUser, userList))
                    data = conn.recv(1024)
                    friendUsername=getFriend(data, user, userList)
                    if data=='0':
                        break
                    else:
                        conn.send(statusOptionsPrint(data, user, userList))
                        selection= conn.recv(1024)
                        if selection=='1':
                            conn.send(viewStatus(friendUsername, userList))
                            data=-1
                        elif selection=='2':
                            conn.send(viewWall(friendUsername, userList))
                            data=-1
                    if data==-1:
                        break
        elif data=="9": #My Status/Wall Timeline
            conn.send(myStatusPrint())
            data = conn.recv(1024)
            if data=='1': #Post Status
                conn.send("What's on your mind? (Post): ")
                data = conn.recv(1024)
                conn.send(postStatus(data, user, userList))
                conn.send(saveJSON(userList))
            elif data=='2': # View My Status
                conn.send(viewStatus(user, userList))
            elif data=='3': # View My Wall Timeline
                conn.send(viewWall(user, userList))
            data=-1
        else:
            pass

    #came out of loop
    conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    clientList.append(conn)
    print 'List of connected client(s): ' + str(len(clientList))
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
