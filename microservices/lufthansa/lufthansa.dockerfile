FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt lufthansa.req.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt -r lufthansa.req.txt
COPY ./arrDep.json .
COPY ./lufthansa.py .
COPY ./.env .
CMD [ "python", "./lufthansa.py" ]