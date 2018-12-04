# protoMessenger
### CS164 Networks Final Project
- Interaction between 1 server and multiple clients
- Has the following functionality:
```
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
```

### How to run
- Need to be able to run python on the machine
- Execute the following command to run 1 server
```
python server.py
```
- Execute as many clients as desire with the following command
```
python client.py
```
- Login authentication (can be added through .json file)
```
User: adr, Pass: asdf
User: lara, Pass: qwer
User: jason, Pass: test
```
- Press Ctrl+C When done with the server

### Features to be added
- Prompt to Login/Register when client first connected to the server by default
- Develop Register function
