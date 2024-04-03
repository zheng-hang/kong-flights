FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./scraper.py .
COPY ./invokes.py .
# COPY ./scheduler.py .
CMD [ "python", "./scraper.py" ]
# CMD [ "python", "./scheduler.py" ]