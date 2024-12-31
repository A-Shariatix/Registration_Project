import bcrypt


"""this function checks if user's information including
username and password exists in database"""


def check_user_credentials(username, password, cursor):
    user_exist = cursor.execute(f'select username, password '
                                f'from information where username = "{username}"'
                                f' and password = "{password}"')
    if user_exist == 1:
        return True
    else:
        return False


"""this function checks validation of user's input"""


def check_input_data(info, username):
    if len(username) > 0 and len(info[username]) > 0:
        return True
    return False


"""this function hashes the given key of the given dictionary
and returns it as hashed password"""


def generate_hash(data, user):
    salt = b'$2b$12$NmjU6/raMmtCvJMHgx6ht.'
    password = bcrypt.hashpw(data[user].encode("utf-8"), salt)
    return password
