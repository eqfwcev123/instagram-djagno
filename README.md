1. 
2.  
3.  
4.  
5. EC2에 docker 설치
6. Ec2에서 docker run 명령어 실행 
   `docker run --rm -it -p 80:8000 <저장소명>`

docker 설치 및 run 명령어 실행하는 부분을 `deploy-docker.sh` 안에 적절히 작성하기



### API 문서



#### 인증

##### BasicAuth

---

HTTP의 BasicAuthentication 을 이용

HTTP Header의 `Authorization` 키에 `Basic <Value>` 값을 넣어 전송

`<value>` 에 들어가는 값은 **`username:password`** 문자열을 Base64로 인코딩한 값

ex):

`Authorization: Basic 값`

#### TokenAuth

---

[DRF라이브러리](https://www.django-rest-framework.org/api-guide/authentication/)에서 제공하는 토큰 인증 방식

HTTP Header의 `Authorization` 키에 `Token<value>` 값을 넣어 전송

`<value>` 에 들어가는 



#### posts

---

