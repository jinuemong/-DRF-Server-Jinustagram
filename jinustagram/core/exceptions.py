
from rest_framework.views import exception_handler
#DRF setting으로 단순하게 오류 디렉토리를 반환
#유효성 검사를 실패하게 만든 모든 필드가 non_field_errors로 들어온다
#비밀번호가 다를 경우 같은 특정 error를 반환하게 하기 위해서는
# key를 error로 변경 해주어야 한다.

def core_exception_handler(exc, context):
    #DRF에서 제공하는 exception handler를 response로 먼저 받음
    response = exception_handler(exc,context)
    
    #처리할 에러를 핸들러에 넣어줌 
    handlers = {
        'ValidationError': _handle_generic_error
    }
    
    #들어온 exception type 식별
    exception_class = exc.__class__.__name__
    
    # 만약 에러가 직접 지정한 handler에서
    #처리할 수 있다면 취할 행동 ->_handle_generic_error실행
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    
    #아니라면 drf의 exception_handler 직접 반환
    return response

#ValidationError를 키 값으로 받아오면 실행되는 함수
#'errors' key값에 response.data를 담아 반환
def _handle_generic_error(exc, context, response):
    response.data = {
        'errors':response.data
        # 키 : 벨류 형식으로 리턴 
    }
    return response