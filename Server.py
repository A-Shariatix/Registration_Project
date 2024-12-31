from flask import Flask, request
import pymysql
import lang_en as lang
from util import check_user_credentials, generate_hash, check_input_data


app = Flask(__name__)


""" sign_up code: first gets data in json format from user,
 including username and password; then checks if both username 
 and password do exist. after that, it hashes the password and
 checks if the hashed password and the username exist in database.
 if it doesn't exist, the query will be executed."""


@app.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.get_json()
    username = list(data)[0]
    if check_input_data(data, username) is True:
        password = generate_hash(data, username)
        if check_user_credentials(username, password, cursor) is False:
            cursor.execute(f'insert into information (username, password) values ("{username}", "{password}")')
            conn.commit()
            return lang.Signup_success, 204
        else:
            return lang.Username_unavailable, 400
    return lang.User_Data_Input_Invalid, 400


""" login code: first gets data in json format from user,
 including username and password; then checks if both username 
 and password do exist. after that, it hashes the password and
 checks if the hashed password and the username exist in database.
 if it exists, the query will be executed."""


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = list(data)[0]
    password = generate_hash(data, username)
    if check_input_data(data, username) is True:
        if check_user_credentials(username, password, cursor) is True:
            return lang.Login_success, 204
        else:
            return lang.User_Data_Input_Invalid, 400
    return lang.User_Data_Input_Invalid, 400


""" forgotten_password code: first gets data in json format from user,
 including username and password; then checks if both username 
 and password do exist. after that, it hashes the password and
 checks if the hashed password and the username exist in database.
 if it exists, the query will be executed."""


@app.route('/forgotten_password', methods=['POST'])
def forgotten_password():
    data = request.get_json()
    username = list(data)[0]
    if check_input_data(data, username) is True:
        password = generate_hash(data, username)
        if check_user_credentials(username, password, cursor) is True:
            cursor.execute(f'update information set password = "{password}" where username = "{username}"')
            conn.commit()
            return lang.Update_password, 204
    return lang.User_Data_Input_Invalid, 400


if __name__ == '__main__':
    conn = pymysql.connect(
        host='localhost',
        password='root',
        database='users',
        port=3306,
        user='root'
    )
    cursor = conn.cursor()
    app.run()
