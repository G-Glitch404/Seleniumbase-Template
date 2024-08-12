import random
import string
import os

password = lambda: ''.join(
    random.choices(
        string.ascii_letters + string.digits + "@#$%&!",
        k=random.randint(8, 16),
    )
)


def path(file_path: str) -> str:
    """ converts a relative path to an absolute path """
    seperator = '\\' if 'nt' in os.name.lower() else '/'
    return os.path.join(
        seperator.join(
            os.path.realpath(
                os.path.join(
                    os.getcwd(),
                    os.path.dirname(__file__)
                )
            ).split(seperator)[:-1]),  # remove the current folder from path
        file_path
    )


def get_filename(file_path: str) -> str:
    """ returns the filename from a file path """
    if "/" in file_path:
        return file_path.split("/")[-1]
    elif "\\" in file_path:
        return file_path.split("\\")[-1]

    return file_path


def username() -> str:
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
