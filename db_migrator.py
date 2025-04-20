import time
import pymysql


if __name__ == '__main__':
    conn = pymysql.connect(
        host='database',
        password='root',
        database='users',
        port=3306,
        user='batman',
    )
    cursor = conn.cursor()
    cursor.execute('create database if not exists users;')
    conn.commit()
    cursor.execute('''create table if not exists information(
    username varchar(255),
    password varchar(255)
    );''')
    conn.commit()
