FROM python:3.12.1-alpine3.18

WORKDIR /app

COPY ./backend/ /app

RUN ls -a
RUN echo ls

RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["python","manage.py", "runserver", "0.0.0.0:8000"]
