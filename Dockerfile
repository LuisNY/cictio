FROM python:3.9.1-buster

ENV MYSQL_HOST=cictio_mysql
ENV MYSQL_PORT=3306
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /home/cictio-server

WORKDIR /home/cictio-server

COPY . .

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update 
RUN apt-get install apache2 -y
RUN apt-get install apache2-utils -y
EXPOSE 8081


CMD ["apache2ctl", "-D", "FOREGROUND"]

RUN pip3 install pymysql
RUN pip3 install cryptography
RUN pip3 install sqlalchemy
RUN pip3 install python-dateutil

RUN chmod +x ./wait-for-it.sh ./entrypoint.sh

RUN useradd -ms /bin/bash cictio_user
USER cictio_user

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "main/main.py", "--host=0.0.0.0"]
