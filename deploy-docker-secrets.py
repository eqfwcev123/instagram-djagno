#!/usr/bin/env python
import argparse
import os
import subprocess
from pathlib import Path

# 1.Host 에서 이미지 build
# 2.EC2애서 이미지 pull, run
# 3.Host --> EC2 --> Container 로 sercrets.json 전달
# 4.Container에서 runserver


parser = argparse.ArgumentParser()
parser.add_argument("cmd", type=str, nargs=argparse.REMAINDER)
args = parser.parse_args()

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    # 백그라운드로 실행하는 옵션 추가: 다른 터미널에서 프로세스를 돌리고 있다고 생각하면 된다.
    ('-d', ''),
    ('-p', '80:80'),
    ('--name', 'instagram'),
]

USER = 'ubuntu'
HOST = '15.164.228.223'
TARGET = f'{USER}@{HOST}'
HOME = str(Path.home())
IDENTITY_FILE = os.path.join(HOME, '.ssh', 'wpsNkp.pem')
SOURCE = os.path.join(HOME, 'projects', 'wps12th', 'instagram')
SECRETS_FILE = os.path.join(SOURCE, 'secrets.json')
DOCKER_IMAGE_TAG = "eqfwcev123/docker-wps12"


# commands
def run(cmd, ignore_error=False):
    process = subprocess.run(cmd, shell=True)
    if not ignore_error:
        process.check_returncode()
        # 성공하면 자식 프로세스한테 0을 반환하면 실패면 1
        # returncode: subprocess 를 돌리면 결과가 돌아오는데
        # main 프로세스 실행중 subprocess


def ssh_run(cmd, ignore_error=False):
    run(f"ssh -o StrictHostKeyChecking=no -i {IDENTITY_FILE} {TARGET} -C {cmd}", ignore_error=ignore_error)


# 1. 호스트에서 도커 이미지 build, push
def local_build_push():
    run(f'poetry export -f requirements.txt > requirements.txt')
    run(f'docker build -t {DOCKER_IMAGE_TAG} .')
    run(f'docker push {DOCKER_IMAGE_TAG}')


# 서버 초기설정
def server_init():
    ssh_run(f'sudo apt update')
    ssh_run(f'sudo DEBIAN_FRONTED=noninteractive apt -y dist-upgrade -y')
    ssh_run(f'sudo apt -y install docker.io')


# 2. 실행중인 컨테이너 종료, pull, run
def server_pull_run():
    ssh_run(f'sudo docker stop instagram', ignore_error=True)
    ssh_run(f'sudo docker pull {DOCKER_IMAGE_TAG}')
    ssh_run('sudo docker run {options} {tag} /bin/bash'.format(
        options=' '.join([
            f'{key} {value}' for key, value in DOCKER_OPTIONS
        ]),
        tag=DOCKER_IMAGE_TAG,
    ))


# 3.Host --> EC2 --> Container 로 sercrets.json 전달
def copy_secrets():
    run(f'scp -i {IDENTITY_FILE} {SECRETS_FILE} {TARGET}:/tmp', ignore_error=True)
    ssh_run(f'sudo docker cp /tmp/secrets.json instagram:/srv/instagram')


# 4.Container에서 runserver
def server_cmd():
    # 실행중인 nginx 종료
    ssh_run(f'sudo docker exec instagram /usr/sbin/nginx -s stop', ignore_error=True)
    ssh_run(f'sudo docker exec instagram python manage.py collectstatic --noinput')
    ssh_run(f'sudo docker exec -it -d instagram '
            f'supervisord -c /srv/instagram/.config/supervisord.conf -n')


# __name__ 은 자기 모듈의 이름을 가리킨다.
if __name__ == '__main__':
    try:
        local_build_push()
        server_init()
        server_pull_run()
        copy_secrets()
        server_cmd()
    except subprocess.CalledProcessError as e:
        print('deploy-docker-secrets-error')
        print(' cmd: ', e.cmd)
        print(' return code: ', e.returncode)
        print(' output: ', e.output)
        print(' stdout: ', e.stdout)
        print(' stderr: ', e.stderr)

# 1. 로컬
# - 도커이미지 build
# - 도커이미지 push
# EC2에서 우분투 초기설정 및 도커 설치
# - apt update
# - apt upgrade
# - apt install docker.io

# 2. EC2에서 실행중인 컨테이너 종료, pull, run
# - docker
# - pull
# - run

# 3. 로컬의 secrets.json --> EC2 --> Container
# scp 로 로컬 -> EC2
# docker cp로 EC2 -> Container

# 4. EC2에서 실행중인 Container 내부에 runserver 명령을 전달
# - docker exec <컨테이너 이름> <명령어>
