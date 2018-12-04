# Copyright - Adrian Harminto
from datetime import datetime
import os, sys, json
border='\n---------------------------------\n'

def getTime():
    return str(datetime.now().strftime("%a, %b %d %I:%M%p"))
    #str(datetime.now().strftime("%m-%d-%Y_%I.%M%p")

#Printings
def menu():
	data= "Main Menu:"+border+"1. Logout\n2. Change Password\n3. Broadcast to all\n4. Messaging Service\n5. Add as Friend\n6. View Pending Friend Requests\n7. View Online Users\n8. View Friends\n9. My Status/Wall Timeline"+border
	return data

def msgPrint():
    data="Messaging service: "+border+"1. Send Message\n2. View Unread Messages\n3. View Read Messages\n4. Cancel"+border
    return data

def sendMsgPrint():
    data="Send message to: "+border+"1. View Online Users\n2. View Friends\n3. Cancel"+border
    return data

def init():
	return "Welcome! Select the following options to:\n1. Sign in\n2. Register\n3. Exit"

def addFriendPrint():
    return "Add a friend through: "+border+"1. View Online Users\n2. Add Users by ID\n3. Cancel"+border

def statusOptionsPrint(which, user, userList):
    friendUsername=getFriend(which, user, userList)
    friendName=getfname(friendUsername, userList)
    return "Status/Wall Timeline: "+border+"1. View "+friendName+"'s Status\n2. View "+friendName+"'s Wall Timeline\n3. Cancel"+border

def myStatusPrint():
    return "My Status/Wall Timeline:"+border+"1. Post Status\n2. View My Status\n3. View My Wall Timeline\n4. Cancel"+border

# Function getters (in String)
def totalUnreadMsg(user, userList):
    return str(len(userList["data"][user]["unreadMsg"]))

def totalFriendRequest(user, userList):
    return str(len(userList["data"][user]["friendRequests"]))

def totalFriends(user, userList):
    return str(len(userList["data"][user]["friends"]))

def getfname(user, userList):
    return userList["users"][user]["fname"]

def getlname(user, userList):
    return userList["users"][user]["lname"]

def getFriend(which, user, userList):
    return userList["data"][user]["friends"][int(which)-1]

def getStatus(user, userList):
    return userList["data"][user]["status"]

def getWall(user, userList):
    temp=''
    x=userList["data"][user]["wall"]
    for i in range(len(x)):
        temp+=x[i]+'\n'
    return temp

# Viewer: unread/read messages, friends' status/wall
def viewUnreadMsg(user, userList):
    x=userList["data"][user]["unreadMsg"]
    if len(x)==0:
        return "You have no unread message!\n"
    temp='Unread message(s): '+border
    for i in range(len(x)):
        sender=x[i]["from"]
        name=userList["users"][sender]["fname"]+' '+userList["users"][sender]["lname"]
        msg=x[i]["msg"]
        time=x[i]["time"]
        temp+='['+time+'] '+name+": "+msg+'\n'
        # Copy message from unread to read,
        userList["data"][user]["readMsg"].append(x[i])

    #  then delete it from unread
    #for i in range(len(x)):
    del(userList["data"][user]["unreadMsg"][:])
    temp+=border
    return temp


def viewReadMsg(user, userList):
    x=userList["data"][user]["readMsg"]
    if len(x)==0:
        return "You have no message! :(\n"
    temp='Read message(s): '+border
    for i in range(len(x)):
        sender=x[i]["from"]
        name=userList["users"][sender]["fname"]+' '+userList["users"][sender]["lname"]
        msg=x[i]["msg"]
        time=x[i]["time"]
        temp+='['+time+'] '+name+": "+msg+'\n'
    temp+=border
    return temp

def viewStatus(user, userList):
    name=getfname(user, userList)+' '+getlname(user, userList)
    return name+' recently posted: '+getStatus(user, userList)

def viewWall(user, userList):
    name=getfname(user, userList)+' '+getlname(user, userList)
    return name+' Timeline Wall: \n'+getWall(user, userList)

# Print List of online users/friends
def onlineList(clientUser, userList):
    temp='List of online users: '+border
    temp+="| 0. Cancel |\n"
    for a in range(len(clientUser)):
        #" username: "+clientUser[a]
        temp+="| "+str(a+1)+"."+" ("+userList["users"][clientUser[a]]["fname"]+" "+userList["users"][clientUser[a]]["lname"]+") |\n"
    temp+='---------------------------------\n'
    return temp

def friendList(user, clientUser, userList):
    temp='Your friend(s): '+border
    temp+="| 0. Cancel |\n"
    for a in range(len(userList["data"][user]["friends"])):
        temp+="| "+str(a+1)+". "+userList["users"][userList["data"][user]["friends"][a]]["fname"]+" "+userList["users"][userList["data"][user]["friends"][a]]["lname"]
        try:
            clientUser.index(userList["data"][user]["friends"][a])
            temp+=' [Online] |'
        except:
            temp+=' [Offline] |'
            pass

        temp+="\n"
    temp+='---------------------------------\n'
    return temp

def friendRequestList(user, clientUser, userList):
    temp='Your friend request(s): '+border
    temp+="| 0. Cancel |\n"
    x=userList["data"][user]["friendRequests"]
    for a in range(len(x)):
        temp+="| "+str(a+1)+". "+userList["users"][x[a]]["fname"]+" "+userList["users"][x[a]]["lname"]
        try:
            clientUser.index(x[a])
            temp+=' [Online] |'
        except:
            temp+=' [Offline] |'

        temp+="\n"
    temp+='---------------------------------\n'
    return temp

def acceptFriendRequest(which, user, userList, clientUser, clientList):
    x=userList["data"][user]
    friend=x["friendRequests"][int(which)-1]
    x["friends"].append(friend)
    userList["data"][friend]["friends"].append(user)
    x["friendRequests"].remove(x["friendRequests"][int(which)-1])
    try:
        index=clientUser.index(friend)
        #Give notification to the friend that it's accepted
        clientList[index].send(getfname(user, userList)+' '+getlname(user,userList)+' has accepted your friend request!')
    except:
        pass
    return "Friend accepted!"

# Sending friend request
def sendFriendRequest(friendUser, user, userList, clientUser, clientList):
    if friendUser==user:
        return "Cannot add yourself as friend!\n"
    try:
        userList["users"][friendUser]
    except:
        return "Such username doesn't exist!\n"
    try:
        userList["data"][friendUser]["friends"].index(user)
        return "Already friend with this user!\n"
    except:
        x=userList["data"][friendUser]["friendRequests"]
        for i in range(len(x)):
            if x[i]==user:
                return "Already sent a friend request!\n"
        x.append(user)
        try:
            index=clientUser.index(friendUser)
            #Give notification to the friend that it's accepted
            clientList[index].send(getfname(user, userList)+' '+getlname(user,userList)+' has sent you a friend request!')
        except:
            pass
        return "Friend request sent!\n"
    return ""

# Sending an "unread" message to recipient
def sendOnlineMessage(data, msg, user, clientUser, userList, clientList):
    try:
        userList["data"][clientUser[int(data)-1]]["unreadMsg"].append({"from":user,"msg":msg, "time":getTime()})
        return "Message Sent!\n"
    except:
        return "Something is wrong.."

# Post status
def postStatus(msg, user, userList):
    x=userList["data"][user]
    x["status"]=msg
    x["wall"].append(msg)
    return "Posted!\n"

def sendFriendMessage(data, msg, user, userList, clientUser, clientList):
    userList["data"][userList["data"][user]["friends"][int(data)-1]]["unreadMsg"].append({"from":user,"msg":msg, "time":getTime()})
    friendUser=getFriend(data, user, userList)
    try:
        index=clientUser.index(friendUser)
        #Give live notification for the message sent
        clientList[index].send(getfname(user, userList)+' '+getlname(user,userList)+' has sent you a message! Check unread message.\n')
    except:
        pass
    return "Message Sent!\n"

# Saving file into json
def saveJSON(userList):
    try:
        with open(os.path.join(sys.path[0], "data.json"), 'w') as outfile:
            json.dump(userList,outfile)
        return ""#"The data has been saved successfully!\n"
    except:
        return "Error: Failed to save to JSON file"
    return ""

# Reload the json (users share this 1 file)
def updateContent(path):
    try:
        return json.loads(open(path).read())
    except:
        print 'Error: json file not found'
        return 'Error: json file not found'
        #sys.exit()
