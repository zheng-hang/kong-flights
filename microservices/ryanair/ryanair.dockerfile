FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ryanair.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt -r ryanair.reqs.txt
COPY ./ryanair_codes.json .
COPY ./ryanairflights.py .
CMD [ "python", "./ryanairflights.py" ]