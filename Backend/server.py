# third-party imports
import pymysql
from dbutils import pooled_db
from flask import Flask, request, g
import time

# local app imports
import lang_en as lang
from util import check_user_credentials, generate_hash, check_input_data
import exporter


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


@app.before_request
def start_timer():
    g.start_time = time.time()


@app.after_request
def end_timer(response):
    if hasattr(request, 'start_time'):
        duration = time.time() - g.start_time
        exporter.request_duration.labels(
            status=str(response.status_code), path=request.path, method=request.method
        ).observe(duration)
        exporter.requests_duration_distribution.labels(
            status=str(response.status_code), path=request.path, method=request.method
        ).observe(duration)
    return response


@app.before_request
def increase_active_request():
    exporter.active_requests.labels(
        path=request.path, method=request.method
    ).inc()


@app.after_request
def decrease_active_request(response):
    exporter.active_requests.labels(
        path=request.path, method=request.method
    ).dec()
    return response


@app.after_request
def request_counter(response):
    exporter.http_requests_total.labels(
        status=str(response.status_code), path=request.path, method=request.method
    ).inc()
    return response


@app.teardown_request
def close_conn(exception):
    if hasattr(g, "conn"):
        g.conn.close()
    if hasattr(g, "cursor"):
        g.conn.close()


@app.route('/metrics')
def metrics():
    return exporter.metrics()


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
