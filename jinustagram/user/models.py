
import encodings
import jwt
from datetime import datetime, timedelta #토큰 생성 로직에 사용
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.fields import BooleanField
from .managers import UserManager
#migrate 안될때 :python manage.py migrate posting --run-syncdb

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True,db_column='username')
    email = models.EmailField(unique=True,null=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    
    USERNAME_FIELD = 'username' #로그인 id로 사용
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    # def natural_key(self):
    #     return str(self.username)
    # #이 부분에서 forgin 값을 리턴 해줌
    
    def get_full_name(self):
            return self.username

    def get_short_name(self):
        return self.username
    
    
    #토큰을 사용자가 보다 간단하게 확인하기 위한 user.token
    @property
    def token(self):
        return self._generate_jwt_token( )
    
    #토큰 발행
    def _generate_jwt_token(self):
        dt = datetime.now( ) + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
            }, settings.SECRET_KEY, algorithm='HS256')
        
        return token

class Profile(models.Model): #user의 username을 참조하므로 username_id필드를 가지게됨
    username = models.OneToOneField(User,on_delete=models.CASCADE,db_column='username',to_field='username')
    customName = models.CharField(max_length=50,db_column='customName',default="")
    userImage = models.ImageField(default='default.png',upload_to="%Y/%m/%d")
    userComment = models.TextField(null=True,default="")
    def __str__(self):
        return self.username.username
    
class follower(models.Model):
    username  = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='followerPost',to_field='username_id')
    fromUser = models.ForeignKey(Profile,on_delete=models.CASCADE,to_field='username_id',)
    
class following(models.Model):
    username  = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='followingPost',to_field='username_id')
    toUser = models.ForeignKey(Profile,on_delete=models.CASCADE,to_field='username_id')

class searchLog(models.Model):
    username = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='searchLogPost',to_field='username_id')
    log = models.CharField(max_length=50,db_column='log')