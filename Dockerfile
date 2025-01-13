FROM python:3.11.6
WORKDIR /app
ADD Server.py .
ADD util.py .
ADD lang_en.py .
ENTRYPOINT ["python3", "Server.py"]
