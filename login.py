import time
import random

class StakeLogin:
    """Login into the stakes website

    Parameters
    ----------
    bot: BotMaker
        The active bot session which will be used to login

    username: str
        Username to be used for login

    password: str
        Password to be used for login
    """
    def __init__(self, bot, username:str, password:str):
        self.bot = bot
        self.username = username
        self.password = password
        self.homepage = "https://stake.games/?tab=login&modal=auth"
        self.xpaths = {
                "username" : '//input[@name="emailOrName"]',
                "password" : '//input[@name="password"]',
                "login_btn" : '//button[@type="submit"]'
                }

    def goto_login_page(self):
        self.bot.move(self.homepage)

    def __send_keys_for_human(self, elem, _key:str):
        """Uses send_key function with random pauses in between."""
        elem.clear()
        for k in _key:
            time.sleep(random.random())
            elem.send_keys(k)

    def login(self):
        username_elem = self.bot.get_element(self.xpaths['username'])
        self.__send_keys_for_human(username_elem, self.username)
       
        password_elem = self.bot.get_element(self.xpaths['password'])
        self.__send_keys_for_human(password_elem, self.password)

        self.bot.get_element(self.xpaths['login_btn']).click()





