FROM python:3.9.1-buster

ENV MYSQL_HOST=mysql
ENV MYSQL_PORT=3306

RUN mkdir -p /home/Cictio

WORKDIR /home/Cictio

COPY . .

RUN pip3 install pymysql
RUN pip3 install cryptography
RUN pip3 install sqlalchemy

RUN chmod +x ./wait-for-it.sh ./entrypoint.sh

RUN useradd -ms /bin/bash algo_trading_user
USER algo_trading_user

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python3", "main/main.py"]
