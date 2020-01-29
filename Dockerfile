FROM    python:3.7-slim

RUN     apt -y update && apt -y dist-upgrade

# requirements를 /tmp에 복사 후, pip install 실행
# requirements.txt 가 바뀌기 전까지 이부분은 계속 캐싱 한다
COPY    ./requirements.txt /tmp/
RUN     pip install -r /tmp/requirements.txt

# 소스코드 복사후 runserver
COPY . /srv/instagram
WORKDIR /srv/instagram/app
CMD     python manage.py runserver 0:8000



