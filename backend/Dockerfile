FROM python:3.7-slim
RUN pip install --upgrade pip
WORKDIR /app
COPY ../backend/requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
COPY ../infra/ .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
