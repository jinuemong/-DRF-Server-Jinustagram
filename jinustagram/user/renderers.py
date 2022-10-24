import json

from rest_framework.renderers import JSONRenderer
#응답(Response)이 올 때 이 데이터들의 출처를 
# 쉽게 알 수 있도록 묶어주는 작업

class UserJsonRenderer(JSONRenderer):
    charset= 'utf-8'
    
    def render(self,data,media_type=None, renderer_context=None):
        #view에서 error를 던지면 내부 data에 errors에 담기게 됨
        errors = data.get('errors',None) #에러를 받아옴
        
        #토큰은 byte 형태, 직렬화 불가능 하기때문에 rendering 전에
        #decode 해야함 - 해독
        #따라서 데이터의 토큰을 우선 받아온 후
        token = data.get('token',None)
        
        #에러가 있다면 data를 user key에 넣지 않고 반환
        if errors is not None:
            return super(UserJsonRenderer, self).render(data)
        
        #데이터를 유저 키에 넣는 과정
        #token 이 바이트 일 경우
        if token is not None and isinstance(token,bytes):
            data['token'] = token.decode('utf-8') 
        
        return json.dumps({
            'user': data
        })
        #바이트 -> utf-8로 변환 후 다시 token에 추가
        #이후에 뷰에 적용 해야함