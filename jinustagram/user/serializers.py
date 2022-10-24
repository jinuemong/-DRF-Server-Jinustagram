from operator import mod
from .models import Profile , User , follower , following ,searchLog
from rest_framework import serializers
from posting.serializers import posterSeralizer , storySeralizer , storyViewerSeralizer
from posting.serializers import likeSeralizer ,commentSeralizer 
#로그인 기능을 위한 import
from django.contrib.auth import authenticate
from django.utils import timezone

#serializer를 통해 사용자 등록을 위한 
# 요청(request)과 응답(response)을 직렬화(serialize)
class RegistrationSerializer(serializers.ModelSerializer):
    #pw는 serializing 할 때는 포함되지 않도록 하기 위함
    password = serializers.CharField(
        max_length = 128,
        min_length = 8,
        write_only = True
    )
    token = serializers.CharField(max_length = 255,read_only=True)
    
    class Meta:
        model = User
        fields  =[
            'email',
            'username',
            'password',
            'token'
            ]
    def create(self,validated_data):
        username = validated_data['username']
        if username =='superuser':
            print("슈퍼 유저가 생성 되었습니다.",username)
            return User.objects.create_superuser(**validated_data)
        else:
            print("슈퍼 유저가 생성 실패",username)
            return User.objects.create_user(**validated_data)


#사용자 로그인을 위한 serializers
#사용자로부터 제공받은 email과 password를 확인하고, 
# 그에 맞는 응답을 보내주는 기능
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    def validate(self, data): #유효성 확인
        username = data.get('username',None)
        password = data.get('password',None)
        if username is None:
            raise serializers.ValidationError(
                'An username address is required to log in.'
            )
        
        if password  is None:
            raise serializers.ValidationError(
                'An password is required to log in.'
            )
        
        user = authenticate(username=username, password=password)
        #username과 pw를 받아 데이터베이스의 username과 pw 매칭 
        #해당 데이터가 없을 시 None 반환 + 오류 메시지 
        
        
        if user is None:
            raise serializers.ValidationError(
                'An user with this username and pw was not found'
            )
            
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated'
            )
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        token = user.token
        return{
            'username':user.username,
            'token':token,
            'last_login': user.last_login
        }

#사용자 정보를 확인, 업데이트용 Serializer
class UserSerializer(serializers.ModelSerializer):
    #패스워드 쓰기 옵션만 활성화 - 읽기 절대 불가능 
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'token'
        ]
        
        #토큰은 입력받을 필요가 없으므로
        #유저 따로 read_only_fields 속성을 줌
        read_only_fields = ('token', )
        
    #사용자 업데이트 할 때마다 실행
    def update(self, instance, validated_data):
        password = validated_data.pop('password',None)
        #password는 setattr로 처리할 수 없음
        #장고에서 자체적으로 함수를 제공하기 때문에 따로 처리
        #pop으로 password 우선 제거 
        #보안성 강화를 위함
        
        #view에서 넘어온 데이터들 -password 제외
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
            
        #만약 password를 수정한 부분이 있다면
        #패스워드를 새롭게 설정
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        #인스턴스 자체에 저장될 뿐 db에 직접 저장되진
        #않음 view에서 seralizer.save() 호출 시 저장 
        return instance
    
class followingSeralizer(serializers.ModelSerializer):
    # username = serializers.StringRelatedField(many = True,read_only=True)
    class Meta:
        managed = True
        model = following    
        fields = [ 'username','toUser']
        
class followerSeralizer(serializers.ModelSerializer):
    # username = serializers.StringRelatedField(many = True,read_only=True)
    class Meta:
        managed = True
        model = follower    
        fields = [ 'fromUser','username']
        
class searchLogSeralizer(serializers.ModelSerializer):
    class Meta:
        managed=True
        model = searchLog
        fields= ['id','username','log']
        
class ProfileSeralizer(serializers.ModelSerializer):
    #유저 네임과 관련된 필드 -게시물
    posterPost = posterSeralizer(many = True,read_only=True)
    likePost= likeSeralizer(many = True,read_only=True)
    commentPost =commentSeralizer(many = True,read_only=True)
    
    # 유저 네임과 관련된 필드 - 스토리
    storyPost = storySeralizer(many = True,read_only=True)
    storyViewerPost = storyViewerSeralizer(many = True,read_only=True)
    
    #시그널을 위한 필드 - user생성시 자동 생성
    #username = serializers.StringRelatedField(read_only=True)
    
    followerPost = followerSeralizer(many= True,read_only=True)
    followingPost = followingSeralizer(many= True,read_only=True)
    
    #갯수 카운터를 위한 필드
    posterCount = serializers.ReadOnlyField( source='posterPost.count')
    storyCount = serializers.ReadOnlyField(source = 'storyPost.count')
    followingCount = serializers.ReadOnlyField( source='followingPost.count')
    followerCount = serializers.ReadOnlyField( source='followerPost.count')
    class Meta:
        managed = True
        model = Profile
        fields = ['id','username','customName','userImage','userComment',
                  'posterCount','followingCount','followerCount',
                  'posterPost','storyCount','likePost', 'commentPost',
                  'storyPost','storyViewerPost',
                  'followerPost', 'followingPost']
 
    ##*** 중요 유저 아이디로 유저 이름 받는 방법######
    # username_username = serializers.SerializerMethodField('get_username_username')
    # def get_username_username(self,obj):
    #     return obj.username.username
    ##############################################

# 개별적으로 선언도 가능 
# class ProfileAvatarSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Profile
#         fields = ("avatar", )


    
      
#프로필 추출  
class MiniProfileSeralizer(serializers.ModelSerializer):
    # 유저 네임과 관련된 필드 - 스토리 (미니 프로필 클릭 시 바로 스토리로 이동하기 위함 )
    storyCount = serializers.ReadOnlyField(source = 'storyPost.count')
    storyPost = storySeralizer(many = True,read_only=True)
    class Meta:
        model = Profile
        fields = ['username','userImage','customName','storyCount'
                  ,'storyPost']
