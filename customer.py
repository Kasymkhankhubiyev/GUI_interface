import random


class Customer:
    def __init__(self, login=None, uid=None):
        #  надо реализовать рандомное создание ip
        if uid is None:
            self.uid = str(round(random.random() * 255)) + '.' + str(round(random.random() * 255)) + '.' + \
                     str(round(random.random() * 255)) + '.' + str(round(random.random() * 255))
        else:
            self.uid = uid
        self.user_login = login

    def return_uid(self):
        return self.uid

    def return_login(self):
        return self.user_login
