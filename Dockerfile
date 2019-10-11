FROM python:3

COPY . /opt/SocialFish
RUN apt-get update
RUN apt-get install python3 python3-pip python3-dev -y
WORKDIR /opt/SocialFish
RUN pip3 install -r requirements.txt
EXPOSE 5000
RUN chmod +x /opt/SocialFish/SocialFish.py
ENTRYPOINT ["/opt/SocialFish/SocialFish.py","user","senha"]
