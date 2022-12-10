FROM python:3.7-slim
WORKDIR /app
COPY ./backend ./backend
COPY requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir
ENTRYPOINT ["tail", "-f", "/dev/null"]
