FROM python:3

MAINTAINER greenmind.sec@gmail.com

RUN apt-get update -y

RUN apt-get install python3-pip -y

RUN apt-get install php7.0 -y

RUN apt-get install unzip -y

WORKDIR /root

RUN git clone https://github.com/UndeadSec/SocialFish.git

WORKDIR /root/SocialFish/base/Server/

RUN wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip

RUN unzip ngrok-stable-linux-amd64.zip

RUN rm -rf ngrok-stable-linux-amd64.zip

WORKDIR /root/SocialFish

RUN pip3 install -r requirements.txt

RUN chmod +x SocialFish.py

RUN ln -s /root/SocialFish/SocialFish.py /bin/SocialFish


ENTRYPOINT ["/root/SocialFish/SocialFish.py"]

#CMD ["--help"]