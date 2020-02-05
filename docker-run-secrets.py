#!/usr/bin/env python
# 시크릿이 들어간 도커 컨테이너 실행(로컬)
import subprocess

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

# 실행중인 도커 컴퓨터에 secrets.json을 전송
subprocess.run('docker cp secrets.json instagram:/srv/instagram', shell=True)

# 다시 /bin/bash를 실행 시켜준다
subprocess.run('docker exec -it instagram /bin/bash', shell=True)

# 그다음에 gunicorn으로 연결을 해준다.
