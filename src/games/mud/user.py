import uuid


class User:
    def __init__(self):
        self.host_id = uuid.uuid1()
        self.hostname = "DAVIDPOOTER"
        self.username = None
        self.password = None

    def getty(self):
        self.username = input("username:\t")
        self.password = input("password:\t")
