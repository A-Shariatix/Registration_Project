PY = python3

requirements:
	@pip install flask
	@pip install bcrypt
	@pip install pymysql
	@pip install cryptography

server:
	@${PY} Server.py

test:
	@${PY} util_test

