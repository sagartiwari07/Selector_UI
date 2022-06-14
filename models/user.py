from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, res: dict = None):
        if res is not None:
            self.email = res['email']
            self.password = res['password']
