import random
import string


def get_unique_short_id(len=6):
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=len)
    )
