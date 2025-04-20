FROM python:3.11.6
ENV DNS_SERVER=185.51.200.2
ENV DNS_SERVER=178.22.122.100
#RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
#Important: if any changes occur in one of dockerfile lines, next lines after that line won't run from cache.
RUN pip install -r requirements.txt --default-timeout=1000
COPY Server.py .
COPY lang_en.py .
COPY util.py .
ENTRYPOINT ["python3", "-u", "Server.py"]
