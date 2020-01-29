#!/usr/bin/env sh
IDENTITY_FILE="$HOME/.ssh/wpsNkp.pem"
USER="ubuntu"
HOST="13.209.65.54"
TARGET=${USER}@${HOST}
ORIGIN_SOURCE="$HOME/projects/wps12th/instagram"
DEST_SOURCE="/srv/"
SSH_CMD="ssh -i ${IDENTITY_FILE} ${TARGET}"
REPO_NAME="eqfwcev123/docker-wps12"
TAG_NAME="inst"
REPO_TAG=${REPO_NAME}:${TAG_NAME}

echo "== Docker 배포 =="

# 서버 초기설정
echo "apt update & upgrade & autoremove"
${SSH_CMD} -C 'sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y && apt -y autoremove'
echo "apt install python3-pip"
${SSH_CMD} -C 'sudo apt -y install python3-pip'

# 서버에 docker 설치
echo "install docker"
sudo apt-get install docker-ce docker-ce-cli containerd.io

# pip freeze
echo "pip freeze"
"$HOME"/.pyenv/versions/3.7.5/envs/wps-instagram/bin/pip freeze >"$HOME"/projects/fastcampus/12th/instagram/requirements.txt

# 서버에서 docker 실행
echo "run docker"
sudo docker run --rm -it -p 80:8000 ${REPO_TAG}



echo "== Docker 배포 완료 =="
