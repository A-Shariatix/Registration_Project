PY = python3

requirements:
	@pip install flask
	@pip install bcrypt
	@pip install pymysql

server:
	@${PY} Server.py

test:
	@${PY} util_test

