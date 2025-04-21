import pymysql
from dbutils import pooled_db
from flask import Flask, request, g
import lang_en as lang
from util import check_user_credentials, generate_hash, check_input_data


app = Flask(__name__)


app.pool = pooled_db.PooledDB(
        creator=pymysql,
        database="users",
        host="database",
        port=3306,
        user="batman",
        password="root",
        maxconnections=4,
        blocking=True
    )


@app.before_request
def setup_conn():
    g.conn = app.pool.connection()


@app.teardown_request
def close_conn(exception):
    if hasattr(g, "cursor"):
        g.cursor.close()
    if hasattr(g, "conn"):
        g.conn.close()


@app.route('/sign_up', methods=['POST'])
def sign_up():
    """
    this is a decorator function which firstly checks if user's
    input structure is valid. then checks if user's data exists in
    database or not. then tries to insert entered data into database.

    :return: returns 400 status code and a message if data is invalid.
    otherwise a 200 status code and a different message will be returned
    :rtype: string, http status code
    """
    data = request.get_json()
    username = list(data)[0]
    if check_input_data(data, username) is True:
        password = generate_hash(data, username)
        with g.conn.cursor() as cursor:
            if check_user_credentials(username, password, cursor) is False:
                cursor.execute('insert into information (username, password) values (%s, %s)', (username, password))
                g.conn.commit()
                return lang.Signup_success, 200
            else:
                return lang.Username_unavailable, 400
    return lang.User_Data_Input_Invalid, 400


@app.route('/login', methods=['POST'])
def login():
    """
    this is a decorator function which firstly checks if user's
    input structure is valid. then checks if user's data exists in
    database or not.

    :return: returns 400 status code and a message if data already exists
    in database. otherwise a 200 status code and a different message will
    be returned.
    :rtype: string, http status code
    """
    data = request.get_json()
    username = list(data)[0]
    password = generate_hash(data, username)
    if check_input_data(data, username) is True:
        with g.conn.cursor() as cursor:
            if check_user_credentials(username, password, cursor) is True:
                return lang.Login_success, 200
            else:
                return lang.User_Data_Input_Invalid, 400
    return lang.User_Data_Input_Invalid, 400


@app.route('/forgotten_password', methods=['POST'])
def forgotten_password():
    """
    this is a decorator function which firstly checks if user's
    input structure is valid. then checks if user's data exists in
    database or not. then tries to update password in database.

    :return: returns 400 status code and a message if data is invalid
    otherwise a 200 status code and a different message will be returned
    :rtype: string, http status code
    """
    data = request.get_json()
    username = list(data)[0]
    if check_input_data(data, username) is True:
        password = generate_hash(data, username)
        with g.conn.cursor() as cursor:
            if check_user_credentials(username, password, cursor) is True:
                cursor.execute('update information set password = %s where username = %s', (password, username))
                g.conn.commit()
                return lang.Update_password, 200
    return lang.User_Data_Input_Invalid, 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7070)
