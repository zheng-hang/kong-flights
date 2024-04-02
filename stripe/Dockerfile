FROM python:latest
WORKDIR /usr/src/app
ADD . /usr/src/app
RUN pip install -r requirements.txt
# EXPOSE 5000
ENV PYTHONUNBUFFERED 1
CMD ["python", "server.py"] 
