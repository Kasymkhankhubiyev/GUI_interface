import random


class Customer():
    def __init__(self, login, uid=None):
        #  надо реализовать рандомное создание ip
        if uid is None:
            self.uid = str(round(random.random() * 255)) + '.' + str(round(random.random() * 255)) + '.' + \
                     str(round(random.random() * 255)) + '.' + str(round(random.random() * 255))
        else:
            self.uid = uid
        self.user_login = login


    def return_uid(self):
        return self.uid

