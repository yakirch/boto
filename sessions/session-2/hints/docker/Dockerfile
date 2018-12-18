FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install flask
RUN mkdir -p /var/www/flask/
ADD webapp.py /var/www/flask/webapp.py
CMD ["/var/www/flask/webapp.py"]
