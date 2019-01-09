FROM python:3

LABEL Author=greenmind.sec@gmail.com

RUN apt-get update -y &&\
    apt-get install -y  python3-pip \ 
                        php7.0 \
                        unzip &&\
    rm -rf /var/lib/{apt,dpkg,cache,log}

WORKDIR /root

COPY . .

RUN wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip &&\
    unzip ngrok-stable-linux-amd64.zip -d /root/base/Server/ &&\
    rm -rf ngrok-stable-linux-amd64.zip &&\
    pip3 install -r /root/requirements.txt &&\
    chmod +x /root/SocialFish.py &&\
    ln -s /root/SocialFish.py /bin/SocialFish

ENTRYPOINT ["/root/SocialFish/SocialFish.py"]
