import string
import random

def generate_random_string():
    result = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(20)])
    return result