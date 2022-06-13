FROM python:3.10

ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "${PYTHONPATH}:/backend/"

RUN pip install --upgrade pip

WORKDIR /backend

COPY ./backend/requirements.txt /backend/requirements.txt
RUN pip install --no-deps --no-cache-dir -r requirements.txt

COPY ./config/scripts/wait-for-it.sh /var/scripts/wait-for-it.sh
COPY ./config/backend/gunicorn.conf.py /var/scripts/gunicorn.conf.py
COPY ./config/backend/run.sh /var/scripts/run.sh
RUN chmod +x /var/scripts/wait-for-it.sh /var/scripts/gunicorn.conf.py /var/scripts/run.sh

COPY ./backend /backend

CMD /var/scripts/run.sh
