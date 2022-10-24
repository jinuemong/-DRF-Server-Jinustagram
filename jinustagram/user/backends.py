#drf에서 jwt 인증을 지원하기 위한 파일

import jwt

from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User

class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'
    
    def authenticate(self, request):
        #어떠한 여부에도 상관 없이 모든 요청에서 호출
        # 두 종류의 value 값을 반환
        # 1. None : header 에 토큰을 포함하지 않는 경우  - 인증실패
        # 2. (user,token) : 인증 성공
        # 이외의 경우는 에러 발생 의미 - 반환값 없음 
        # AuthenticationFailed 에러 처리 -> drf에서 처리해줌
        
        #auth_header는 header 이름(token), 인증 해야하는 jwt를 가져야 함
        #postman에서 token이 여기서 header 이름
        #토큰값 앞에 token이 없는 경우 None 반환
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        #prefix.lower() -> 바깥에서 받아온 token 값
        #두가지 값이 필요한데 
        if not auth_header:
            return None
        if len(auth_header)==1:
            return None
        elif len(auth_header) > 2:
            return None
        
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')
        #token xlsdjfsldjflsdfjlsd -> split()으로 받아옴
        
        if prefix.lower() != auth_header_prefix:
            return None
        
        #위 과정들을 통과하면 접근 허용 함수 실행
        return self._authenticate_credentials(request, token)
    
    def _authenticate_credentials(self, request, token):
        try:
             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        #error 발생 처리 시 -> None 이거나 토큰 발견 이외의 에러
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)
        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        
        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)
        
        return (user,token)