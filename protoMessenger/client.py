# Copyright - Adrian Harminto
import socket,sys,os,getpass
from threading import Thread
from time import sleep

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

host = 'localhost'
port = 4000
connected=True
loggedIn=False
passwordPrompt=True

s.connect((host,port))

def keepListening ():
    global connected, loggedIn,passwordPrompt
    while(connected):
        d=s.recv(1024)
        if len(d)==0:
            connected=False
            break
        if not d:
            break

        if loggedIn==False:

            if d[:12]=='Welcome back':#'Login Successful':
                loggedIn=True
        elif passwordPrompt==False:
            if d[:34]=='Password has changed successfully!':
                passwordPrompt=True
        elif d[:17]==  'Changing password':
            passwordPrompt=False

        if len(d)==0:
            connected=False
            break
        if not d:
            break
        print(d)

def getPass():
    global loggedIn
    while(not loggedIn):
        s.send(raw_input(""))
        s.send(getpass.getpass(""))
        sleep(1)
#------------ MAIN -----------------
Thread(target=keepListening,args=[]).start()
getPass()
while(connected):

    try :
        if passwordPrompt==True:
            s.send(raw_input(""))
        else:
            s.send(getpass.getpass(""))
            passwordPrompt=True
        sleep(0.5)

    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
