IDENTITY_FILE="$HOME/.ssh/wpsNkp.pem"
USER="ubuntu"
HOST="15.164.228.223"
TARGET=${USER}@${HOST}
ORIGIN_SOURCE="$HOME/projects/wps12th/instagram/"
DOCKER_REPO="eqfwcev123/docker-wps12"
SSH_CMD="ssh -i ${IDENTITY_FILE} ${TARGET}"

### 순서
### 도커설치 --> 도커 이미지 생성(docker build) ---> 도커 이미지 도커 허브에 올리기(docker push)
### ---> 실행중이던 도커 컨테이너 종료 (docker stop) ---> 도커 이미지 Pull 해오기(docker pull)
### ---> 마지막으로 Docker 실행

echo "== Docker 배포 =="

# 1.서버 초기설정
echo "서버 초기설정 apt update & upgrade & autoremove"
${SSH_CMD} -C 'sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y && apt -y autoremove'

echo "poetry export"
# 2. requirements.txt 전달
poerty "export -f requirements.txt > requirements.txt"


# 3. docker 설치
echo "apt install docker.io"
${SSH_CMD} -C 'sudo apt -y install docker.io'

# 4. docker build 이미지 생성
echo "docker build"
docker build -q -t ${DOCKER_REPO} -f Dockerfile "${ORIGIN_SOURCE}"

# 5. docker push 이미지 docker hub 에 올리기
echo "docker push"
docker push ${DOCKER_REPO}

# 6. 실행중인 docker container 중지
echo "docker stop"
${SSH_CMD} -C 'sudo docker stop instagram'

# 7. docker image를 docker hub 에서 가져오기
echo "docker pull"
${SSH_CMD} -C "sudo docker pull ${DOCKER_REPO}"

# 8. EC2 컴퓨터에 있는 .aws 파일 삭제
${SSH_CMD} -C "sudo rm -rf /home/ubuntu/.aws"

# 9. 로컬에있는 .aws 파일을 EC2 컴퓨터에 복사
scp -q -i "${IDENTITY_FILE}" -r "$HOME/.aws/" ${TARGET}:/home/ubuntu/


echo "screen settings"
# 10. EC2 에 있는 Screen 으로 실행중인 docker container 실행 중지
${SSH_CMD} -C 'screen -X -S docker quit'
# 11. EC2 에 docker 라는 screen 생성
${SSH_CMD} -C 'screen -S docker -d -m'


# 12. EC2 내부에 docker container(컴퓨터) 실행. (현재 .aws 파일은 컨테이너 내부에 없음).
# .aws파일을 이미지에 넣지 않는 이유는 다른 사람들이 docker hub에서
# .aws/credentials 파일을 볼 수 있기 때문이다.
# 실행중인 세션에서 bash 실행 (마지막에 적어줄 경우 Dockerfile의 CMD 대신 마지막 CMD 에 /bin/bash 가 실행된다.
# 이때 컨테이너가 실행중이다.
echo "docker RUN CONTAINER"
${SSH_CMD} -C "screen -r docker -X stuff 'sudo docker run --rm -it -p 80:8000 --name=instagram eqfwcev123/docker-wps12 /bin/bash\n'"


# 13. EC2 컴퓨터안에 있는 ~/.aws/credentials 파일을 instagram 컨테이너 내부에 넣기
# 도커 컨테이너에다가 ubuntu 호스트가 가지고 있는 .aws폴더를 복사해 줘야한다.
# docker cp [OPTIONS] HOST_FILE_PATH|- CONTAINER:DEST_PATH
# docker cp 는 호스트가 가지고있는 파일을 컨테이너에 복사를 해주는 것이다.
# 이렇게 하면 .aws 폴더를 이미지에 넣지 않아도 된다.
echo "docker copy .aws/credentials"
${SSH_CMD} -C "sudo docker cp ~/.aws/ instagram:root"

# 14. Dockerfile의 마지막 CMD 실행. (서버실행)
echo "docker manage.py runserver"
${SSH_CMD} -C "screen -r docker -X stuff 'python manage.py runserver 0:8000\n'"

echo "finish!"

echo "== Docker 배포 완료 =="
