# 도커 이미지를 생성하는 파일
# 도커 이미지 내부에 있어야 하는 것들: python, pip 환경들, 소스코드
# 현재 도커파일의 경로는 EC2 서버의 instagram 프로젝트 내부이다
FROM    python:3.7-slim

RUN     apt -y update && apt -y dist-upgrade && apt -y autoremove
RUN     apt-get install vim -y
RUN     apt -y install nginx

# The /tmp directory in linux is whre temporary files and directories
# are created by applications. /tmp directory is cleaned up only at the time
# of system startup and reboot
COPY    ./requirements.txt /tmp/

# production.txt 파일에 보면 -r ./base.txt 이 있는데 -r ./base.txt 를 다운한다는 뜻이다.
RUN     pip install -r /tmp/requirements.txt

# 소스코드 복사후 runserver
COPY    . /srv/instagram
WORKDIR /srv/instagram/app


RUN     cp /srv/instagram/.config/instagram.nginx /etc/nginx/sites-enabled/
