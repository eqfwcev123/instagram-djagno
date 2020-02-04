#!/usr/bin/env python
import subprocess

import boto3

DOCKER_IMAGE_TAG = 'eqfwcev123/docker-wps12'
session = boto3.session.Session(profile_name='wps-secrets-manager')
credentials = session.get_credentials()
print(' ====== credentials 는 ====== ', credentials)
print(' ====== credentials 는 ====== ', credentials.__dict__)
# ====== credentials 내부 ======
# {
#   'access_key': '*****',
#   'secret_key': '*****',
#   'token': None,
#   'method': 'shared-credentials-file'
#   }
access_key = credentials.access_key
secret_key = credentials.secret_key

# subprocess.run() 은 Shell 커맨드를 실행 시킨다.

# 외부 shell 에서 실행하는 결과를 받아오기
# "aws configure get aws_access_key_id --profile wps-secrets-manager" 의 결과를 access_key에 저장
access_key = subprocess.run(
    'aws configure get aws_access_key_id --profile wps-secrets-manager',
    stdout=subprocess.PIPE,
    shell=True
).stdout.decode('utf-8').strip()

secret_key = subprocess.run(
    'aws configure get aws_secret_access_key --profile wps-secrets-manager',
    stdout=subprocess.PIPE,
    shell=True
).stdout.decode('utf-8').strip()
print(access_key)
print(secret_key)

DOCKER_OPTIONS = [('--rm', ''),
                  ('-it', ''),
                  ('-p', '8001:8000'),
                  ('--name', 'instagram'),
                  ('--env', f'AWS_SECRETS_MANAGER_ACCESS_KEY_ID={access_key}'),  # --env : 환경변수 설정
                  ('--env', f'AWS_SECRETS_MANAGER_SECRET_ACCESS_KEY={secret_key}')
                  ]

# ==== 기존의 컨테이너 실행 중지 ====
# docker stop instagram
subprocess.run('docker stop instagram', shell=True)

# ===== 컨테이너 실행 ====
# docker run
# --rm -it -p 8001:8000
# --name instagram
# --env AWS_SECRETS_MANAGER_ACCESS_KEY_ID='...',
# --env AWS_SECRETS_MANAGER_SECRET_ACCESS_KEY='...'
subprocess.run('docker run {options} eqfwcev123/docker-wps12'.format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ])
), shell=True)
subprocess.run(f'docker cp secrets.json instagram:/srv/instagram')
subprocess.run('docker exec -it instagram /bin/bash'.format(
    options=' '.join([
        f'{key} {value}' for key, value in DOCKER_OPTIONS
    ]),
    tag=DOCKER_IMAGE_TAG
), shell=True)

# 위에 있는 코드들은 다음과 같다
# docker run --rm -it -p 8001:8000 --name instagram \
# --env AWS_SECRETS_MANAGER_ACCESS_KEY_ID=$(aws configure get aws_access_key_id --profile wps-secrets-manager)\
# --env AWS_SECRETS_MANAGER_SECRET_ACCESS_KEY_=$(aws configure get aws_secret_access_key --profile wps-secrets-manager)
