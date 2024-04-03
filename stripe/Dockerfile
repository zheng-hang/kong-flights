FROM python:latest
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY server.py .
# EXPOSE 5000
ENV PYTHONUNBUFFERED 1
CMD ["python", "server.py"] 
