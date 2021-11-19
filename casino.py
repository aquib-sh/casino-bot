import time
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


if __name__ == "__main__":
    cred_file = 'credentials.json'

    casino = StakeCasino(cred_file)

    print("[+] Starting Casino bot...")
    casino.start_bot()
    print("[+] Successfully Started Casino bot!")

    print("[+] Logging into StakeCasino...")
    casino.login()
    print("[+] Successfully logged into Casino!")
    print("[+] Sleeping for 10 secs")
    time.sleep(10)

    casino.parser.attach_utility(casino.util)

    while True:
        time.sleep(2)
        print("[+] Getting users...")
        users = casino.get_users()
        print(f"Got {len(users)} users")

        for user in users:
            print(f"Checking for user: {user}")
            casino.goto_user_profile(user)

            reg_tstamp = casino.get_reg_date()
            while (reg_tstamp == None):
                reg_tstamp = casino.get_reg_date()

            hours_diff = casino.util.time_diff_in_hours(reg_tstamp)
            print(f"{user} joined {hours_diff} hours ago on {reg_tstamp}")

        if len(users) > 0:
            break
        else:
            casino.goto_home()

    casino.shutdown()
