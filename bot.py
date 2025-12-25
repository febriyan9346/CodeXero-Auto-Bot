import requests
import json
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_checksum_address
from datetime import datetime
import pytz
from colorama import Fore, Style, init
import time
import os
import random

os.system('clear' if os.name == 'posix' else 'cls')

import warnings
warnings.filterwarnings('ignore')

import sys
if not sys.warnoptions:
    import os
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)

class CodexeroBot:
    def __init__(self):
        self.base_url = "https://backend.codexero.xyz/api"
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.codexero.xyz",
            "referer": "https://www.codexero.xyz/",
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }
        self.token = None
        self.wallet_address = None
        self.proxies = []
        self.use_proxy = False
        # Daftar task yang akan diklaim
        self.tasks = [
            {"id": "daily-visit-app", "name": "Daily Visit App"},
            {"id": "visit-codexero", "name": "Visit Codexero"}
        ]
    
    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN}CODEXERO AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def random_delay(self):
        delay = random.randint(1, 10)
        self.log(f"Delay {delay} seconds...", "INFO")
        time.sleep(delay)
    
    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)
    
    def load_proxies(self, filename="proxies.txt"):
        try:
            if not os.path.exists(filename):
                self.log(f"File {filename} not found.", "WARNING")
                return []
            
            with open(filename, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
            
            if proxies:
                self.log(f"Successfully loaded {len(proxies)} proxies.", "SUCCESS")
            return proxies
        except Exception as e:
            self.log(f"Error reading proxy: {str(e)}", "ERROR")
            return []

    def get_proxy_dict(self, proxy_string):
        if not proxy_string:
            return None
        return {
            "http": proxy_string,
            "https": proxy_string
        }

    def create_signature(self, private_key, wallet_address):
        try:
            timestamp = int(datetime.now().timestamp() * 1000)
            
            if not private_key.startswith('0x'):
                private_key = '0x' + private_key
            
            account = Account.from_key(private_key)
            
            if account.address.lower() != wallet_address.lower():
                self.log(f"Wallet mismatch! Private key: {account.address}, Expected: {wallet_address}", "ERROR")
                return None
            
            checksum_address = to_checksum_address(wallet_address)
            message = "Sign in to Cluster Points Program\n\nWallet: {}\nTimestamp: {}".format(checksum_address, timestamp)
            
            encoded_message = encode_defunct(text=message)
            signed_message = account.sign_message(encoded_message)
            
            signature = signed_message.signature.hex()
            if not signature.startswith('0x'):
                signature = '0x' + signature
            
            return {
                "message": message,
                "signature": signature,
                "timestamp": timestamp
            }
        except Exception as e:
            self.log(f"Error creating signature: {str(e)}", "ERROR")
            return None
    
    def check_points(self, proxy=None):
        try:
            if not self.token or not self.wallet_address:
                return

            url = f"{self.base_url}/user/{self.wallet_address}"
            headers = self.headers.copy()
            headers["authorization"] = f"Bearer {self.token}"

            response = requests.get(url, headers=headers, proxies=proxy, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                totals = data.get('totals', {})
                total_points = totals.get('totalPointsEarned', 0)
                today_earnings = totals.get('todayEarnings', 0)
                
                time_str = self.get_wib_time()
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Total Points: {total_points:,} | Today: +{today_earnings:,}{Style.RESET_ALL}")
                return True
            else:
                self.log(f"Failed to check points: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Error checking points: {str(e)}", "ERROR")
            return False

    def login(self, private_key, proxy=None):
        try:
            if not private_key.startswith('0x'):
                private_key = '0x' + private_key
            
            account = Account.from_key(private_key)
            wallet_address = account.address
            self.wallet_address = wallet_address
            
            proxy_msg = "No Proxy"
            if proxy:
                try:
                    if '@' in proxy['http']:
                        proxy_msg = proxy['http'].split('@')[1]
                    else:
                        proxy_msg = proxy['http'].split('//')[1]
                except:
                    proxy_msg = "Proxy Active"

            self.log(f"Proxy: {proxy_msg}", "INFO")
            
            self.log(f"{wallet_address[:6]}...{wallet_address[-4:]}", "INFO")
            
            self.random_delay()
            
            sig_data = self.create_signature(private_key, wallet_address)
            if not sig_data:
                return False
            
            payload = {
                "walletAddress": wallet_address,
                "message": sig_data["message"],
                "signature": sig_data["signature"]
            }
            
            response = requests.post(
                f"{self.base_url}/auth/login",
                headers=self.headers,
                json=payload,
                proxies=proxy,
                timeout=30
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'token' in data:
                        self.token = data['token']
                    elif 'access_token' in data:
                        self.token = data['access_token']
                    
                    time_str = self.get_wib_time()
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Login successful!{Style.RESET_ALL}")
                    return True
                except:
                    time_str = self.get_wib_time()
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Login successful!{Style.RESET_ALL}")
                    return True
            else:
                self.log(f"Login failed: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Error during login: {str(e)}", "ERROR")
            return False
    
    def redeem_task(self, task_id, task_name, proxy=None):
        try:
            if not self.token:
                self.log("Token not available", "ERROR")
                return False
            
            headers = self.headers.copy()
            headers["authorization"] = f"Bearer {self.token}"
            
            payload = {
                "walletAddress": self.wallet_address,
                "taskId": task_id
            }
            
            self.log(f"Processing Task: {task_name}", "INFO")
            
            self.random_delay()
            
            response = requests.post(
                f"{self.base_url}/task/redeem",
                headers=headers,
                json=payload,
                proxies=proxy,
                timeout=30
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    pts = data.get('points', 0)
                    times_redeemed = data.get('timesRedeemed', 0)
                    message = data.get('message', '')
                    
                    time_str = self.get_wib_time()
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] {task_name} - Earned +{pts} Points! (Total Redeems: {times_redeemed}){Style.RESET_ALL}")
                    return True
                except:
                    time_str = self.get_wib_time()
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] {task_name} - Claim Success!{Style.RESET_ALL}")
                    return True
            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    message = error_data.get('message', 'Unknown error')
                    if 'already' in message.lower() or 'claimed' in message.lower():
                        self.log(f"{task_name} - Already claimed", "WARNING")
                    else:
                        self.log(f"{task_name} - Redeem failed: {message}", "ERROR")
                except:
                    self.log(f"{task_name} - Redeem failed: {response.text}", "ERROR")
                return False
            else:
                self.log(f"{task_name} - Redeem failed: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Error redeeming task {task_name}: {str(e)}", "ERROR")
            return False
    
    def process_all_tasks(self, proxy=None):
        """Process semua task yang ada di daftar"""
        success_count = 0
        
        for task in self.tasks:
            if self.redeem_task(task["id"], task["name"], proxy):
                success_count += 1
            time.sleep(1)  # Delay antar task
        
        return success_count
    
    def read_accounts(self, filename="accounts.txt"):
        try:
            with open(filename, 'r') as f:
                accounts = [line.strip() for line in f if line.strip()]
            return accounts
        except FileNotFoundError:
            self.log(f"File {filename} not found!", "ERROR")
            return []
        except Exception as e:
            self.log(f"Error reading file: {str(e)}", "ERROR")
            return []
    
    def process_account(self, private_key, proxy_dict):
        if self.login(private_key, proxy_dict):
            # Process semua task
            task_success = self.process_all_tasks(proxy_dict)
            self.log(f"Completed {task_success}/{len(self.tasks)} tasks", "INFO")
            
            self.random_delay()
            self.check_points(proxy_dict)
            return True
        return False
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)
    
    def run(self):
        self.print_banner()
        
        choice = self.show_menu()
        
        if choice == '1':
            self.use_proxy = True
            self.proxies = self.load_proxies()
            if not self.proxies:
                self.log("No proxies loaded. Continuing without proxy...", "WARNING")
                self.use_proxy = False
        else:
            self.use_proxy = False
            self.log("Running without proxy", "INFO")
        
        accounts = self.read_accounts()
        if not accounts:
            self.log("No accounts in accounts.txt", "WARNING")
            return

        self.log(f"Loaded {len(accounts)} accounts successfully", "INFO")
        self.log(f"Tasks to claim: {len(self.tasks)}", "INFO")
        for task in self.tasks:
            self.log(f"  - {task['name']} ({task['id']})", "INFO")
        
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle = 1
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            success_count = 0
            
            for i, private_key in enumerate(accounts):
                proxy_dict = None
                if self.use_proxy and self.proxies:
                    proxy_url = self.proxies[i % len(self.proxies)]
                    proxy_dict = self.get_proxy_dict(proxy_url)

                self.log(f"Account #{i+1}/{len(accounts)}", "INFO")
                
                if self.process_account(private_key, proxy_dict):
                    success_count += 1
                
                if i < len(accounts) - 1:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(2)
            
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{len(accounts)}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            
            wait_time = 24 * 60 * 60
            self.countdown(wait_time)

if __name__ == "__main__":
    bot = CodexeroBot()
    bot.run()
