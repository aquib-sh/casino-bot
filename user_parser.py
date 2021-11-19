from bs4 import BeautifulSoup

class UserParser:
    def __init__(self, bot):
        self.bot = bot
        self.source = self.bot.page_source()
        self.soup = BeautifulSoup(self.source, "lxml")
        self.util = None

    def attach_utility(self, util):
        self.util = util

    def update_source(self):
        self.source = self.bot.page_source()
        self.soup = BeautifulSoup(self.source, "lxml")

    def get_user_list(self) -> list:
        tbody = self.soup.find('tbody', {'data-bets-loading':'false'})
        table_rows = tbody.find_all('tr')
        users = []

        for row in table_rows:
            user = row.find_all('td')[1].text.strip()
            if (user != 'Hidden'):
                users.append(user)

        return users

    def get_join_date(self):
        for s in self.soup.find_all('span'):
            if 'Joined on' in s.text:
                date_o_join = s.find('span').text
                join_tstamp = self.util.to_datetime(date_o_join)
                return join_tstamp


                




