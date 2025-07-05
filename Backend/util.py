import bcrypt


def check_user_credentials(username, password, cursor):
    """
    This function checks if user's information including
    username and password exist in database.

    :param username: First item of the generated list, which is made of received json data
    :type username: str

    :param password: The value of the only key in received json data, which gets hashed by generate_hash function
    :type password: bytes

    :param cursor: A database object that let us execute queries row by row
    :type cursor: MySQLCursor

    :return: True if matching credentials exist in database, otherwise false
    :rtype: bool
    """
    user_exist = cursor.execute('''select username, password
                                from information where username = %s
                                and password = %s''', (username, password))

    # fetcher = cursor.fetchone()
    # print(fetcher)
    # print(f'matching users found : {user_exist}')
    if user_exist == 1:
        return True
    elif user_exist == 0:
        return False


def check_input_data(user_data, username):
    """
    This function checks if client has entered username and password or not

    :param user_data: Json format data sent by client, including username and password
    :type user_data: dict

    :param username: First item of the generated list, which is made of received json data
    :type username: str

    :return: True if username and password exists in received json data, otherwise false
    :rtype: bool
    """
    if len(username) > 0 and len(user_data[username]) > 0:
        return True
    return False


def generate_hash(user_data, username):
    """
    This function generates a hashed password using salt, and it encodes using utf-8

    :param user_data: Json format data sent by client, including username and password
    :type user_data: dict

    :param username: First item of the generated list, which is made of received json data
    :type username: str

    :return: hashed password
    :rtype: bytes
    """
    salt = b'$2b$12$NmjU6/raMmtCvJMHgx6ht.'
    password = bcrypt.hashpw(user_data[username].encode("utf-8"), salt)
    return password
