import random, string


def generate_random_code(size=8):
    """
    Generate random code with length size

    generates random characters with length matching the given
    input parameter, size. if no size is specified, the random
    code length is set as 8.

    :param size:
    :return:
    """

    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.punctuation) for _ in range(size))

