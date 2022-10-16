FROM ubuntu:18.04

RUN apt update
RUN apt install python3.8 -y  
RUN apt install python3-pip -y
RUN apt-get install netcat -y

WORKDIR /home
COPY ./dev-requirments.txt req.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r req.txt

EXPOSE 8000

COPY ./src /app/src

COPY entrypoint.sh entrypoint.sh
COPY test.sh test.sh
CMD ["sh", "entrypoint.sh"]
