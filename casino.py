import os
import time
import pandas
from bot import BotMaker
from login import StakeLogin
from creds import Credentials
from user_parser import UserParser
from utils import CasinoUtils

class StakeCasino:
    def __init__(self, cred_file:str):
        self.__creds = Credentials(cred_file)
        self.__creds.fetch()

        self.username = self.__creds.get_username()
        self.password = self.__creds.get_password()
        self.util = CasinoUtils()
        self.homepage = "https://stake.games/casino/bets"
        self.bot = None
        self.parser = None

    def goto_home(self):
        self.bot.move(self.homepage)

    def start_bot(self):
        self.bot = BotMaker()
        self.parser = UserParser(self.bot)

    def login(self):
        login = StakeLogin(self.bot, self.username, self.password)
        login.goto_login_page()
        login.login()

    def goto_user_profile(self, username:str):
        user_info_link = f"https://stake.games/casino/bets?name={username}&modal=user"
        self.bot.move(user_info_link)
        time.sleep(2)

    def get_users(self):
        self.parser.update_source()
        users = self.parser.get_user_list()
        return users

    def get_reg_date(self):
        self.parser.update_source()
        return self.parser.get_join_date()

    def get_hour_diff(self, timestamp):
        return self.util.time_diff_in_hours(timestamp)

    def shutdown(self):
        self.bot.shutdown()


class Main:
    def __init__(self):
        self.cred_file = 'credentials.json'
        self.casino = StakeCasino(self.cred_file)
        self.others = {'Users':[], 'Join Hour':[], 'Join Datetime':[]}
        self.under24 = {'Users':[], 'Join Hour':[], 'Join Datetime':[]}
        self.OTHERS_FILE = 'others.csv'
        self.UNDER24_FILE = 'under24.csv'

    def __print_logo(self):
        logo = """
            ------------------------
           |        CASINO BOT      |
            ------------------------
            \n\n
        """
        print(logo)

    def __login(self):
        print("[+] Starting Casino bot...")
        self.casino.start_bot()
        print("[+] Successfully Started Casino bot!")
        print("[+] Logging into StakeCasino...")
        self.casino.login()
        print("[+] Successfully logged into Casino!")
        print("[+] Sleeping for 10 secs")
        time.sleep(10)

    def __get_users(self, BUFFER_SIZE=100):
        users = []
        print("[+] Getting users: ", end="", flush=True)
        while (len(users) < BUFFER_SIZE):
            time.sleep(2)
            users += self.casino.get_users()
            users = list(set(users))
            print("|", end="", flush=True)
        return users

    def __append_data(self, user, diff, joined):
        if diff <= 24:
            self.under24['Users'].append(user)
            self.under24['Join Hour'].append(diff)
            self.under24['Join Datetime'].append(joined)
        else:
            self.others['Users'].append(user)
            self.others['Join Hour'].append(diff)
            self.others['Join Datetime'].append(joined)

    def __export_data(self):
        others_df = pandas.DataFrame(self.others)
        under24_df = pandas.DataFrame(self.under24)

        if os.path.exists(self.OTHERS_FILE):
            others_df = others_df.append(
                pandas.read_csv(self.OTHERS_FILE), 
                ignore_index=True
            )

        if os.path.exists(self.UNDER24_FILE):
            under24_df = under24_df.append(
                pandas.read_csv(self.UNDER24_FILE),
                ignore_index=True
            )
        
        others_df.to_csv(self.OTHERS_FILE, index=False)
        under24_df.to_csv(self.UNDER24_FILE, index=False)
        print(f"[+] Exported data of other users in {self.OTHERS_FILE}")
        print(f"[+] Exported data of under24 users in {self.UNDER24_FILE}")

    def start(self):
        self.__print_logo()
        self.__login()
        self.casino.parser.attach_utility(self.casino.util)

        start_time = time.time()
        while True:
            users = self.__get_users(BUFFER_SIZE=100)

            print("\n\n")
            counter = 1
            INTERVAL = 10

            for user in users:

                if counter % INTERVAL == 0:
                    print("\n[*] Sleeping for 2 minutes\n")
                    time.sleep(60*2)

                self.casino.goto_user_profile(user)

                reg_tstamp = self.casino.get_reg_date()
                while (reg_tstamp == None):
                    reg_tstamp = self.casino.get_reg_date()

                hours_diff = self.casino.util.time_diff_in_hours(reg_tstamp)
                print(f"{user} joined {hours_diff} hours ago on {reg_tstamp}")
                self.__append_data(user, hours_diff, reg_tstamp)
                
                counter += 1

            if (self.casino.util.time_diff_in_mins(start_time) >= 30):
                self.__export_data()
                start_time = time.time()

            self.casino.goto_home()


if __name__ == "__main__":
    main = Main()
    main.start()
