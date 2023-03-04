FROM docker.io/python:3.9.16-alpine3.17

RUN sed -i "s/v3.17/edge/g" /etc/apk/repositories
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk upgrade -U
RUN apk add --no-cache py3-psutil py3-requests py3-nmap py3-qrcode py3-flask py3-colorama py3-flask-login py3-secretstorage py3-jupyter-packaging
RUN apk add --no-cache gcc ethtool nmap bash

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv --python 3
RUN pipenv install requests
RUN pipenv install PyLaTeX
RUN pipenv install python3-nmap
RUN pipenv install qrcode
RUN pipenv install Flask
RUN pipenv install colorama
RUN pipenv install Flask_Login
RUN pipenv install nmap
#RUN pipenv install python-secrets

COPY . .

CMD [ "pipenv", "run", "python", "SocialFish.py" ]
#pipenv run python SocialFish.py