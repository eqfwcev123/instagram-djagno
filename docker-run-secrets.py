#!/usr/bin/env python
# 시크릿이 들어간 도커 컨테이너 실행(로컬)
import argparse
import subprocess

# argparser 사용방법
# 1. argparser 객체 생성하기 ----> parser = argparser.ArgumentParser()
# 2. argument 추가하기 ----> parser.add_argument()

# ArgumentParser 객체 생성
parser = argparse.ArgumentParser()

# 각 cli 인자가 어떻게 파싱될지 지정
parser.add_argument(
    "cmd",
    type=str,  # 사용자가 입력한 CLI(기본으로 문자열)을 타입 케스팅 해준다.
    nargs=argparse.REMAINDER  # arguments 의 개수. 총 몇개의 argument 를 사용자가 지정할지 말해준다.
)

# add_argument 로 지정한 내용을 적용
args = parser.parse_args()

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-d', ''),
    ('-p', '8001:80'),  # 컨테이너 내부의 80번과 연결
    ('--name', 'instagram'),
]

DOCKER_IMAGE_TAG = 'eqfwcev123/docker-wps12'

# poetry export로 docker build시 사용할 requirements.txt 작성
subprocess.run(f'poetry export -f requirements.txt > requirements.txt', shell=True)

# 도커 컴퓨터 생성(Secrets.json 이 없는 이미지를 build)
subprocess.run(f'docker build -t {DOCKER_IMAGE_TAG} -f Dockerfile .', shell=True)
# 기존에 실행중인 name=instagram인 컨테이너 실행 중지
subprocess.run(f'docker stop instagram', shell=True)

# secrets.json이 없는 상태로 docker run으로 bash를 실행 -> background로 들어감
# 이전에 설치한 도커 컴퓨터 실행
subprocess.run('docker run {options} {tag} /bin/bash'.format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ]),
    tag=DOCKER_IMAGE_TAG,
), shell=True)

# 실행중인 도커 컴퓨터에 secrets.json을 전송. 경로는 instagram 이미지 내부의 /srv/instagram 디렉토리
subprocess.run('docker cp secrets.json instagram:/srv/instagram', shell=True)

# collectstatic 을 subproces.run 을 이용해서 자동 실행 시키기
subprocess.run('docker exec -it instagram ./manage.py collectstatic', shell=True)

# 실행중인 name=instagram 인 컨테이너에서 argparse로 입력받은 cmd또는 bash를 실행(foreground 모드)
subprocess.run('docker exec -it instagram {cmd}'.format(
    cmd=' '.join(args.cmd) if args.cmd else 'supervisord -c ../.config/supervisord.conf -n'
), shell=True)
