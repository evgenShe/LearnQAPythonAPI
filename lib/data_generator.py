import random
import string
from datetime import datetime


class DataGenerator:
    def prepare_good_email(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")

        return f"{base_part}{random_part}@{domain}"

    def prepare_bad_email(self):
        base_part = "test"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")

        return f"{base_part}{random_part}{domain}"

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))

        return rand_string


data_generator = DataGenerator()
