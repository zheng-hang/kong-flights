FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
RUN python -m pip install --no-cache-dir -r amqp.reqs.txt
COPY ./bookings.py ./amqp_connection.py ./
CMD [ "python", "./bookings.py" ]