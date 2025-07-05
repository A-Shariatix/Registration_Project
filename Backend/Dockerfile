FROM python:3.11.6
WORKDIR /app
COPY requirements.txt .
#Important: if any changes occur in one of dockerfile lines, next lines after that line won't run from cache.
RUN pip install -r requirements.txt --default-timeout=1000
COPY Server.py .
COPY lang_en.py .
COPY util.py .
ENTRYPOINT ["python3", "-u", "Server.py"]
