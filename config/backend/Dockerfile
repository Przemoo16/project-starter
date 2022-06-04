FROM python:3.10

ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "${PYTHONPATH}:/backend/"

RUN pip install --upgrade pip

WORKDIR /backend

COPY ./backend/requirements.txt /backend/requirements.txt
RUN pip install --no-deps --no-cache-dir -r requirements.txt

COPY ./config/scripts/wait-for-it.sh /scripts/wait-for-it.sh
COPY ./config/backend/gunicorn.conf.py /scripts/gunicorn.conf.py
COPY ./config/backend/run.sh /scripts/run.sh
RUN chmod +x /scripts/wait-for-it.sh /scripts/gunicorn.conf.py /scripts/run.sh

COPY ./backend /backend

CMD /scripts/run.sh
