from asyncio.windows_events import NULL
from pickle import TRUE
from numpy import source
from user.models import Profile
from .models import poster, Comment, Image, Like
from .models import Story, StoryViewer
from rest_framework import serializers 
#tip : 이미지 필드 serializers에서 사용하기
#필드명 = serializers.ImageField(use_url=True)
        
class commentSeralizer(serializers.ModelSerializer):
    class Meta:
        managed=True 
        model = Comment
        db_table = 'Comments'
        fields = ['commentId','posterId','writer','writerImage','uploadTime','body']
    
    #다른 모델 접근을 위해서 create 직접 조작 
    def create(self,validated_data):
        posterId = validated_data.get("posterId")
        writer = validated_data.get("writer")
        body = validated_data.get("body")
        writerImage = writer.userImage

        viewer_create =  Comment.objects.create(posterId =posterId
                                                    ,writer=writer
                                                    ,writerImage=writerImage
                                                    ,body =body) 
        return viewer_create        
    
class imageSeralizer(serializers.ModelSerializer):
    class Meta:
        managed=True 
        model = Image
        db_table = 'Images'
        fields = "__all__"

class likeSeralizer(serializers.ModelSerializer):
    #forgin 키 = liker = profile을 가리침 
    # likerImage = serializers.ImageField(source='liker.userImage')

    class Meta:
        managed=True 
        model = Like
        db_table = 'Likes'
        fields = ['likeId','posterId','liker','likerImage','uploadTime']     
        
     #다른 모델 접근을 위해서 create 직접 조작 
    def create(self,validated_data):
        posterId = validated_data.get("posterId")
        liker = validated_data.get("liker")
        likerImage = liker.userImage

        viewer_create =  Like.objects.create(posterId =posterId
                                                    ,liker=liker
                                                    ,likerImage=likerImage) 
        return viewer_create        
    
       
class posterSeralizer(serializers.ModelSerializer):
    commentPost = commentSeralizer(many = True,read_only=True)
    imagePost = imageSeralizer(many = True,read_only=True)
    likePost = likeSeralizer(many=True,read_only=True)
    # tip : 해당 유저 이름을 찾아줌 
    # def validated_username(self, data):
    #     return data
    # ##################
    
    #갯수 카운터를 위한 필드
    commentCount = serializers.ReadOnlyField( source='commentPost.count')
    likeCount = serializers.ReadOnlyField( source='likePost.count')
    imageCount = serializers.ReadOnlyField( source='imagePost.count')
    
    class Meta:
        managed=True 
        model = poster
        db_table = 'posters'
        fields = ['posterId','username','body',
                  'commentPost','imagePost','likePost','uploadTime',
                  'commentCount','likeCount','imageCount']
                
    #한번에 이미지 데이터 여러개 받는 방법
    def create(self, validated_data):
        images_data = self.context['request'].FILES    
        
        poster_create =  poster.objects.create(**validated_data)
        for image_data in images_data.getlist('Oneimage'):
            Image.objects.create(posterId=poster_create,Oneimage=image_data)
        return poster_create
     
class storyViewerSeralizer(serializers.ModelSerializer):
    class Meta:
        managed=True 
        model = StoryViewer
        db_table = 'StoryViewers'
        fields = ['storyId','viewer','viewerImage']
    
    #다른 모델 접근을 위해서 create 직접 조작 
    def create(self,validated_data):
        storyId = validated_data.get("storyId")
        viewer = validated_data.get("viewer")
        viewerImage = viewer.userImage

        viewer_create =  StoryViewer.objects.create(storyId =storyId
                                                    ,viewerImage=viewerImage) 
        return viewer_create
        

       
class storySeralizer(serializers.ModelSerializer):
    storyViewerPost = storyViewerSeralizer(many=True,read_only=True)
    class Meta:
        managed=True 
        model = Story
        db_table = 'Storys'
        fields = ['storyId','username','storyImage','uploadTime','storyViewerPost']
