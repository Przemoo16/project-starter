FROM python:3.10

ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "${PYTHONPATH}:/backend/"

WORKDIR /backend

COPY ./backend/requirements.txt /backend/requirements.txt
RUN pip install --no-deps --no-cache-dir -r requirements.txt

COPY ./config/scripts/run_backend.sh /scripts/run_backend.sh
RUN chmod +x /scripts/run_backend.sh

COPY ./backend /backend

CMD /scripts/run_backend.sh
