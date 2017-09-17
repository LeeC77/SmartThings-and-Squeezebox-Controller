## Bridge program between smart things and the raspberry PI
##
##                       |  RASPBERRY PI INTERNAL
##                       |
##   S                   |                       S
##   T                   |  B                    B 
##       ---- HTTP --->  |  R  ---- TELNET --->  
##   S                   |  I                    S
##   E                   |  D                    E
##   R                   |  G                    R
##   V   <--- JSON ----  |  E  <--- TELNET ----  V
##   E                   |                       E
##   R                   |                       R
##                       |
##
## the Json will be sent via a line of shell code and TELNET treated as raw
## packets as far as possible

import socket
import threading
import subprocess

myIP = ''

telnetPort = 9090 #these need numbers
telnetIP = '192.168.1.85'

httpPort = 39500
httpIP = '' #raspi ip

SmartHubIP = '192.168.1.119'

def sendJSON(message):
    ##complie and send a JSON msg by shell script
    subprocess.call('curl -H \"Content-Type: application/json\" -X POST -d \'{\"SBSResponse\":\"' + message + '\"}\' http://' + SmartHubIP + ':' + str(httpPort), shell = True)

    

def telnetHandler():
    ##recvs and deals with telnet msgs, will use sendJSON funct
    while True:       
        msg = telSocket.recv(1024)

##        with lock:
##            print('recved on telnet: ' + msg.decode().strip())
            
        sendJSON(msg.decode())


def httpHandler():
    ##recvs and deals with HTTP msgs, will use sendTEL funct
    while True:
 
        con, addr = httpSocket.accept()

        SmartHubIP = addr[0]
	SmartHubPort = addr[1]
        
        requ = con.recv(1024)
            
##        with lock:
##            print('recved on http: ' + requ.decode().strip())
##            print('resolved IP: ' + SmartHubIP + '\n resolved Port: ' + str(SmartHubPort))

        con.close()

        telSocket.send(requ)
        


lock = threading.Lock() #allows threads to print


httpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creates the socket for recveing HTTP msgs (server type)
httpSocket.bind((httpIP, httpPort))
httpSocket.listen(3)


telSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#creates the telnet socket (client type)
telSocket.connect((telnetIP, telnetPort))
        

telnetDaemon = threading.Thread(target = telnetHandler, args = ()) #creates threads
httpDaemon = threading.Thread(target = httpHandler, args = ())
telnetDaemon.isDaemon() #sets threads to daemons
httpDaemon.isDaemon()

telnetDaemon.start() #begins threads 
httpDaemon.start()


while True:
    pass

