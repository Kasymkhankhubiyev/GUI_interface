import random


class Customer:
    def __init__(self, login=None, uid=None):
        #  надо реализовать рандомное создание ip
        self.uid = uid
        self.user_login = login

    def return_uid(self):
        return self.uid

    def return_login(self):
        return self.user_login
