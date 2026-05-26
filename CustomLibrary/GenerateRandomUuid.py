import random
import uuid

def generate_random_number_uuid():
    random_number = random.randint(1000000000000, 9999999999999)
    random_uuid = uuid.uuid4()
    return f"{random_number}-{random_uuid}"
