FROM python:3.7-slim
WORKDIR /app
COPY ./backend ./
COPY requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["gunicorn", "foodgram_api.wsgi:application", "--bind", "0:8000"]
