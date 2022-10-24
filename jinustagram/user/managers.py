
#BaseUserManager : user를 생성할 때 사용하는 헬퍼 클래스
# create_user : user 생성
# create _superuser :관리자 생성, create_user를 거쳐 
# is_supseruser , is_staff 부분을 True로 변경

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None,**extra_fields):
    
        if username is None:
            raise TypeError("Users must have a username.") 
        if email is None:
            raise TypeError('Users must have an email address.')
        if password is None:
            raise TypeError('Users must have a password.')
        
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            **extra_fields
        )
        
        # django 에서 제공하는 pw 함수
        user.set_password(password)
        user.save()
        
        return user
        
        
    #admin user = superuser 제작
        
    def create_superuser(self, username, email, password, **extra_fields):
            
        if password is None:
            raise TypeError("Superuser must have a password.")
            
        # 우선 create_user 함수로 사용자 저장
        user = self.create_user(username,email,password,**extra_fields)
        
        #관리자로 지정하기
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user