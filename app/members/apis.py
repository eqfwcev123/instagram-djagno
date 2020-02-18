from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializers import UserSerializer


class AuthTokenAPIView(APIView):
    # post 를 사용하는 이유는 사용자의 아이디 비번을 전송해서 토큰을 생성해야 하기 때문이다.
    # 이럴때는 GET 보다 POST 사용
    def post(self, request):
        username = request.data['username']  # 사용자가 계정으로 로그인.(string)
        # checker = json.dumps(username)
        # print('유저네임이 json 데이터인지 확인하기',checker)
        password = request.data['password']  # 사용자가 계정으로 로그인.(string)
        user = authenticate(username=username, password=password)  # 유효한 사용자인지 검사
        print(type(user))
        if user:
            token, _ = Token.objects.get_or_create(user=user)  # 유효할 경우 사용자에게 토큰 제공
        else:
            raise AuthenticationFailed()  # 존재하지 않은 유저일 경우 인증 실패 오류를 반환

        # user 데이터를 serialize 해줘야 하는 이유:
        # response 로 token 과 사용자의 데이터를 보내줘야 한다.
        # user 는 User모델의 인스턴스이다. 인스턴스를 JSON 데이터로 보내주기 위해서는 serialize 를 해줘야 한다
        # JSON데이터로 보내줘야 하기 때문에 is_valid()를 해줄 필요가 없다
        serializer = UserSerializer(user)

        data = {
            'token': token.key,
            'user': serializer.data
        }

        return Response(data)
        # serializer = UserSerializer(data=request.data)
        # if serializer.is_valid():
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 지금 UserSerializer()가 에러가 나는 이유:
    # UserSerializer()를 이용하면 create 혹은 update()를 주어진 인수를
    # 통해 자동으로 호출해주는데, 위에서는 이미 존재하는 user를 또 생성 할려고 하기 때문에
    # 에러가 나는 것이다.

    # ModelSerializer는 자동으로 create() update() 를 호출해줌

    """
    클라이언트
    usernmae/password
    is_valid 는 deeserialize 할때 사용
    serialize 는 인스턴스를 --> 데이터(JSON)로 변환. Instance 자체는 이미 valid 하기 때문에 is_valid 를 안해줘도 된다.


    deserializer 는 외부데이터(JSON) -->(is_valid 검증) --> 파이썬 데이터 --> 인스턴스로 변환
    """
