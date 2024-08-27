import time
import random
import string
import os

wait = lambda x=1: time.sleep(rand_range(x))
password = lambda: ''.join(
    random.choices(
        string.ascii_letters + string.digits + "@#$%&!",
        k=random.randint(8, 16),
    )
)  # generate a random password (8-16 characters long)


def path(file_path: str, secondary_path: str = None) -> str:
    """ converts a relative path to an absolute path """
    seperator = '\\' if 'nt' in os.name.lower() else '/'
    file = os.path.join(
        seperator.join(
            os.path.realpath(
                os.path.join(
                    os.getcwd(),
                    os.path.dirname(__file__)
                )
            ).split(seperator)[:-1]),  # remove the current folder from path
        file_path
    )
    return file if secondary_path is None else os.path.join(file, secondary_path)


def get_filename(file_path: str) -> str:
    """ returns the filename from a file path """
    if "/" in file_path:
        return file_path.split("/")[-1]
    elif "\\" in file_path:
        return file_path.split("\\")[-1]

    return file_path


def username() -> str:
    """ generate a random username (lowercase, 20 characters max) """
    chance = lambda: random.choice(
        random.sample(range(20), k=10)
    ) % 2 == 0

    user: str = ''
    names: list[str] = list(string.digits + string.ascii_letters)
    random.shuffle(names)
    for word in random.choices(names, k=15):
        if chance(): user += word[1]
        if chance():
            user += ''.join(
                random.choices(
                    string.digits, k=random.randint(1, 3)
                )
            )

    return user.lower()[:20]


def rand_range(num: int | float) -> float:
    """
    choose a random float between num - 1 and num + 1 intentionally made for time.sleep() to never stop in a pattern

    :param num: int or float
    :type num: int or float

    :rtype: float
    :return: a random float in the rango of num
    """
    return float(
        str(random.choice(
            [
                round(random.uniform(num - 1, num + 1), 2)
                for _ in range(100)
            ]
        )).replace("-", "")
    )
