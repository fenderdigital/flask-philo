import bcrypt


def run(print_salt=True, app=None):
    salt = bcrypt.gensalt(8)
    if print_salt:
        print(salt)
    return salt
