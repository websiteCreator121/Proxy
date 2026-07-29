#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# proxyscraper.py - iSH iOS Proxy Tool
# runs on Alpine, no heavy deps

import urllib.request
import urllib.error
import json
import re
import time
import socket
import sys
import os
from datetime import datetime

# ===== ANIMATION UTILS =====
def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def spinner(text, duration=1.5):
    chars = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f'\r{chars[i % len(chars)]} {text}')
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write('\r✓ {:<30}\n'.format(text))
    sys.stdout.flush()

def animate_banner():
    banner = """
╔═══════════════════════════════════════╗
║   ██████╗ ██████╗  ██████╗ ██╗  ██╗   ║
║   ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝   ║
║   ██████╔╝██████╔╝██║   ██║ ╚███╔╝    ║
║   ██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗    ║
║   ██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ║
║   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ║
║          PROXY SCRAPER v2.0            ║
╚═══════════════════════════════════════╝
    """
    for line in banner.split('\n'):
        print('\033[36m' + line + '\033[0m')
        time.sleep(0.03)

def progress_bar(current, total, width=40):
    pct = current / total
    filled = int(width * pct)
    bar = '█' * filled + '░' * (width - filled)
    sys.stdout.write(f'\r[{bar}] {current}/{total} ({pct*100:.1f}%)')
    sys.stdout.flush()

# ===== PROXY SOURCES =====
SOURCES = [
    'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    'https://raw.githubusercontent.com/hemantapkh/Proxy-List/main/http.txt',
    'https://raw.githubusercontent.com/UserR3X/Proxy-List/main/http.txt',
    'https://raw.githubusercontent.com/UserR3X/Proxy-List/main/socks4.txt',
    'https://raw.githubusercontent.com/UserR3X/Proxy-List/main/socks5.txt',
    'https://raw.githubusercontent.com/RX4096/ProxyList/master/http.txt',
    'https://raw.githubusercontent.com/RX4096/ProxyList/master/socks4.txt',
    'https://raw.githubusercontent.com/RX4096/ProxyList/master/socks5.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/http.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/https.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/socks4.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/socks5.txt',
    'https://raw.githubusercontent.com/ALIILAPRO/Proxy-list/main/http.txt',
    'https://raw.githubusercontent.com/ALIILAPRO/Proxy-list/main/socks4.txt',
    'https://raw.githubusercontent.com/ALIILAPRO/Proxy-list/main/socks5.txt',
    'https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt',
    'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt',
]

# ===== SCRAPER =====
def fetch_proxies():
    proxies = []
    total = len(SOURCES)
    print('\n\033[33m[+] Scraping proxy sources...\033[0m\n')
    
    for i, url in enumerate(SOURCES):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read().decode('utf-8', errors='ignore')
                found = re.findall(r'(\d+\.\d+\.\d+\.\d+):(\d+)', data)
                for ip, port in found:
                    proxies.append(f'{ip}:{port}')
                progress_bar(i+1, total)
        except:
            progress_bar(i+1, total)
            continue
    
    proxies = list(dict.fromkeys(proxies))
    print(f'\n\n\033[32m[+] Found {len(proxies)} unique proxies\033[0m')
    return proxies

# ===== CHECKER =====
def check_proxy(proxy, timeout=5):
    try:
        parts = proxy.split(':')
        if len(parts) != 2:
            return False, 0
        ip, port = parts
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        start = time.time()
        result = sock.connect_ex((ip, int(port)))
        elapsed = (time.time() - start) * 1000
        sock.close()
        if result == 0:
            return True, elapsed
        return False, elapsed
    except:
        return False, 0

def check_all(proxies):
    if not proxies:
        print('\033[31m[-] No proxies to check.\033[0m')
        return [], []
    
    good = []
    mid = []
    total = len(proxies)
    print(f'\n\033[33m[+] Checking {total} proxies...\033[0m\n')
    
    for i, proxy in enumerate(proxies):
        ok, ms = check_proxy(proxy)
        if ok:
            if ms < 800:
                good.append((proxy, ms))
            else:
                mid.append((proxy, ms))
        progress_bar(i+1, total)
    
    print(f'\n\n\033[32m[+] Good: {len(good)} | Mid: {len(mid)} | Dead: {total - len(good) - len(mid)}\033[0m')
    return good, mid

# ===== OUTPUT =====
def save_proxies(good, mid, filename='proxies.txt'):
    with open(filename, 'w') as f:
        f.write('# ===== GOOD PROXIES =====\n')
        for p, ms in good:
            f.write(f'{p}  # {ms:.0f}ms\n')
        f.write('\n# ===== MID PROXIES =====\n')
        for p, ms in mid:
            f.write(f'{p}  # {ms:.0f}ms\n')
    print(f'\033[32m[+] Saved to {filename}\033[0m')

# ===== MENU =====
def menu():
    while True:
        clear()
        animate_banner()
        print('\n\033[36m┌──────────────────────────────────────┐\033[0m')
        print('\033[36m│\033[0m  \033[33m1.\033[0m Scrape Proxies (20+ sources)      \033[36m│\033[0m')
        print('\033[36m│\033[0m  \033[33m2.\033[0m Check All Proxies (good/mid)      \033[36m│\033[0m')
        print('\033[36m│\033[0m  \033[33m3.\033[0m Scrape + Check + Save             \033[36m│\033[0m')
        print('\033[36m│\033[0m  \033[33m4.\033[0m Load Proxies from file             \033[36m│\033[0m')
        print('\033[36m│\033[0m  \033[33m5.\033[0m Exit                            \033[36m│\033[0m')
        print('\033[36m└──────────────────────────────────────┘\033[0m')
        
        choice = input('\n\033[36m[>] Select: \033[0m').strip()
        
        if choice == '1':
            clear()
            proxies = fetch_proxies()
            if proxies:
                with open('scraped.txt', 'w') as f:
                    f.write('\n'.join(proxies))
                print(f'\033[32m[+] Saved scraped.txt ({len(proxies)} proxies)\033[0m')
            input('\n[Press Enter]')
        
        elif choice == '2':
            try:
                with open('scraped.txt', 'r') as f:
                    proxies = [l.strip() for l in f if l.strip() and not l.startswith('#')]
            except:
                proxies = []
                print('\033[31m[-] No scraped.txt found. Run option 1 first.\033[0m')
                input('\n[Press Enter]')
                continue
            if proxies:
                good, mid = check_all(proxies)
                save_proxies(good, mid)
            input('\n[Press Enter]')
        
        elif choice == '3':
            clear()
            proxies = fetch_proxies()
            if proxies:
                with open('scraped.txt', 'w') as f:
                    f.write('\n'.join(proxies))
                good, mid = check_all(proxies)
                save_proxies(good, mid)
            input('\n[Press Enter]')
        
        elif choice == '4':
            fname = input('\n[>] Filename: ').strip()
            try:
                with open(fname, 'r') as f:
                    proxies = [l.strip() for l in f if l.strip() and not l.startswith('#')]
                print(f'\033[32m[+] Loaded {len(proxies)} proxies\033[0m')
                good, mid = check_all(proxies)
                save_proxies(good, mid, f'checked_{fname}')
            except:
                print('\033[31m[-] File not found.\033[0m')
            input('\n[Press Enter]')
        
        elif choice == '5':
            print('\n\033[36m[+] Exiting... 6767\033[0m')
            time.sleep(0.5)
            break
        
        else:
            input('\033[31m[-] Invalid. Press Enter.\033[0m')

# ===== BOOT =====
if __name__ == '__main__':
    try:
        menu()
    except KeyboardInterrupt:
        print('\n\033[33m[!] Interrupted. 6767\033[0m')
