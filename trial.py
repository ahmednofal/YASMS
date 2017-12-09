class User(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password
        alice = User('Alice A. Adams', 'secret')



def jobj(o):
        return o.__dict__
