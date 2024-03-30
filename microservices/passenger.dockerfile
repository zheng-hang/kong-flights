FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt passenger.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt passenger.reqs.txt
COPY ./passenger.py .
CMD [ "python", "./passenger.py" ]