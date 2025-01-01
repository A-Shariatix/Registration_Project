import bcrypt


def check_user_credentials(username, password, cursor):
"""this function checks if user's information including
username and password exists in database.

:param username: stores json data's key in a list
:type username: list

:param password: stores json data's value in a hashed format
:type password: bytes

:param cursor: stores the connected cursor to database
:type cursor: Cursor

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


def check_input_data(data, username):
"""this function checks validation of user's input.

:param data: stores user's sent data in json format
:type data: json

:param username: stores data's key
:type username: string

:return: True if username and password are entered;
otherwise False.
:rtype: bool
"""
    if len(username) > 0 and len(data[username]) > 0:
        return True
    return False


def generate_hash(data, username):
"""this function hashes the given stringand returns
it as hashed password.

:param data: stores user's sent data in json format
:type data: json

:param username: stores info's key
:type username: string

:param salt: stores a pre ordered salt
:type salt: bytes

:param password: stores json data's value in a hashed format
:type password: bytes

:return: returns hashed password
:rtype: bytes
"""
    salt = b'$2b$12$NmjU6/raMmtCvJMHgx6ht.'
    password = bcrypt.hashpw(data[username].encode("utf-8"), salt)
    return password
