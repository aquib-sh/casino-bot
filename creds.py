import json

class Credentials:

    def __init__(self, creds_json_file:str):
        self.creds_file = creds_json_file
        self.data = {}

    def fetch(self):
        with open(self.creds_file, 'r') as fp:
            self.data = json.load(fp)

    def get_password(self):
        if "password" not in self.data:
            raise Exception("You must call fetch() method before getting the credentials")
        else:
            return (self.data['password'])

    def get_username(self):
        if "username" not in self.data:
            raise Exception("You must call fetch() method before getting the credentials")
        else:
            return (self.data['username'])






