#!/usr/bin/env sh
IDENTITY_FILE="$HOME/.ssh/wpsNkp.pem"
HOST="ubuntu@15.164.228.223"
ORIGIN_SOURCE="$HOME/projects/wps12th/instagram" # 여기의 origin source 는 hoste OS의 프로젝트 경로이다
DEST_SOURCE="/home/ubuntu/projects/"
SSH_CMD="ssh -i ${IDENTITY_FILE} ${HOST}"

#### 노트 ####
# ~ 와 $HOME 은 동일하다
# home/ubuntu 는 내컴퓨터의 ~ 와 동일하다
############



# 숙제
# 다시 실행되는 서버 만들기
#(가능하다면) HOST만 바꾸고 이 스크립트를 실행 하면 전체 서버가 세팅되고 runserver된 화면 볼수 있도록 하기


echo "====Runserver 배포===="
echo "apt update & upgrade & autoremove"
${SSH_CMD} -C 'sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y && apt -y autoremove'
echo "apt install python3-pip"
${SSH_CMD} -C 'sudo apt -y install python3-pip'


# pip freeze
echo "pip freeze"
"$HOME"/.pyenv/versions/3.7.5/envs/wps-instagram/bin/pip freeze > "$HOME"/projects/fastcampus/12th/instagram/requirements.txt



echo "기존 폴더 삭제"
#기존 폴더 삭제
${SSH_CMD} sudo rm -rf ${DEST_SOURCE}
# ssh -i ~/.ssh/wps12th.pem ubuntu@54.180.119.84 sudo rm -rf /home/ubuntu/projects/instagram

echo "로컬에 있는 파일 업로드"
# 로컬에 있는 파일 업로드
${SSH_CMD} mkdir -p ${DEST_SOURCE}
scp -q -i "${IDENTITY_FILE}" -r "${ORIGIN_SOURCE}" ${HOST}:${DEST_SOURCE}
# scp -i ~/.ssh/wps12th.pem -r ~/projects/wps12th/instagram ubuntu@54.180.119.84:/home/ubuntu/projects/

echo "pip3 requirements 설치"
${SSH_CMD} pip3 install -q -r /home/ubuntu/projects/instagram/requirements.txt

# 실행 중이던 screen 종료
# ssh -i ~/.ssh/wps12th.pem ubuntu@54.180.119.84 -C "screen -X -S runserver quit"
${SSH_CMD} -C "screen -X -S runserver quit"

# screen 실행
# ssh -i ~/.ssh/wps12th.pem ubuntu@54.180.119.84 -C "screen -S runserver -d -m"
${SSH_CMD} -C "screen -S runserver -d -m"

# 실행중인 세션 명령어 전달
# ssh -i ~/.ssh/wps12th.pem ubuntu@54.180.119.84 -C "screen -r runserver -X stuff $'sudo python3 /home/ubuntu/projects/instagram/app/manage.py runserver 0:80\n'"
${SSH_CMD} -C "screen -r runserver -X stuff $'sudo python3 /home/ubuntu/projects/instagram/app/manage.py runserver 0:80\n'"


echo "====배포완료===="
