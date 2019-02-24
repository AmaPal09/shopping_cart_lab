"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""

    # TODO: need to implement this
    def __init__(self, first_name, last_name, email, hashed_password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hashed_password = hashed_password


    def __repr__(self):
        return "<Customer: {}, {}, {}".format(self.first_name, 
                                              self.last_name, 
                                              self.email)


    def is_correct_password(self, password):
        return hash(password) == self.hashed_password


cust_dict = {}
def read_file_by_line(filename):
    with open(filename) as customer_file:
        for line in customer_file:
            line = line.strip()
            first_name, last_name, email, password = line.split('|')
            cust_dict[email] = Customer(first_name, 
                                        last_name, 
                                        email, 
                                        hash(password))





def get_by_email(email):
    return cust_dict.get(email, '')


read_file_by_line('customers.txt')