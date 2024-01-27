FROM python:3.12.1-alpine3.18

WORKDIR /app

COPY . /app

RUN ls -al

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "-u", "backend/manage.py", "runserver", "0.0.0.0:8000"]