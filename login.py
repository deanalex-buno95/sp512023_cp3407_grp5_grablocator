class Login:

    """
    create login database
    """
    def __init__(self, first_name, last_name, ages, id, password):
        self.firstname = first_name
        self.lastname = last_name
        self.ages = ages
        self.id = id
        self.password = password

    def email (self):
        return '{}.{}@gmail.com'.format(self.firstname, self.lastname)

    def fullname(self):
        return '{} {}'.format(self.firstname, self.lastname)

