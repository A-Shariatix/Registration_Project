import bcrypt


def check_user_credentials(username, password, cursor):
"""this function checks if user's information including
username and password exists in database.

:param username: stores json data's key in a list
:type username: list

:param password: stores json data's value in a hashed format
:type password: bytes

:param cursor: stores the connected cursor to database
:type cursor: 

:param user_exist: stores the number of infected rows
:type user_exist: int

:return: True if both expected username and password
exist in database. otherwise False.
:rtype: bool
"""
    user_exist = cursor.execute(f'select username, password '
                                f'from information where username = "{username}"'
                                f' and password = "{password}"')
    if user_exist == 1:
        return True
    else:
        return False


def check_input_data(info, username):
"""this function checks validation of user's input.

:param info: 
"""
    if len(username) > 0 and len(info[username]) > 0:
        return True
    return False


"""this function hashes the given key of the given dictionary
and returns it as hashed password"""


def generate_hash(data, user):
    salt = b'$2b$12$NmjU6/raMmtCvJMHgx6ht.'
    password = bcrypt.hashpw(data[user].encode("utf-8"), salt)
    return password
