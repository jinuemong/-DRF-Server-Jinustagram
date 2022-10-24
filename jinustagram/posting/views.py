from .models import poster , Comment ,Image ,Like
from .models import Story, StoryViewer , Profile
from user.views import myfollowingProfileView
from user.serializers import MiniProfileSeralizer
from .serializers import posterSeralizer , commentSeralizer
from .serializers import imageSeralizer, likeSeralizer
from .serializers import storySeralizer, storyViewerSeralizer
from rest_framework import viewsets ,serializers ,filters 
from rest_framework.views import APIView
from rest_framework.response import Response
import random
from rest_framework import status ,filters 
class PosterViewSet(viewsets.ModelViewSet):
    
    queryset = poster.objects.all()
    serializer_class = posterSeralizer
    filter_backends= [filters.SearchFilter]
    search_fields  = ['=username__username__username']
    #foreinkeyfield_foreinkeyfield__name

        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = commentSeralizer
    filter_backends= [filters.SearchFilter]
    search_fields  = ['=writer__username__username']

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = imageSeralizer
    filter_backends= [filters.SearchFilter]
    search_fields  = ['=posterId__posterId']

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = likeSeralizer
    filter_backends= [filters.SearchFilter]
    
        #쿼리셋 초기화!!!!!!!!!!!!!!!!
    def get_queryset(self):
        liker = self.request.query_params.get('liker')
        posterId = self.request.query_params.get('posterId')
        if liker and posterId:
            queryset =self.queryset.filter(liker__username__username  = liker) \
            & self.queryset.filter(posterId__posterId  = posterId)     
            return queryset
        else:
            return self.queryset    

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = storySeralizer
    filter_backends= [filters.SearchFilter]
    search_fields  = ['=username__username__username']

    
class StoryViewerViewSet(viewsets.ModelViewSet):
    queryset = StoryViewer.objects.all()
    serializer_class = storyViewerSeralizer
    filter_backends= [filters.SearchFilter] 
    
        #쿼리셋 초기화!!!!!!!!!!!!!!!!
    def get_queryset(self):
        viewer = self.request.query_params.get('viewer')
        storyId = self.request.query_params.get('storyId')
        if viewer and storyId:
            queryset =self.queryset.filter(viewer__username__username  = viewer) \
            & self.queryset.filter(storyId__storyId  = storyId)     
            return queryset
        else:
            return self.queryset
    
    
class RandomPosterViewSet(APIView):
    #두가지 경우:  팔로잉 하고있는 유저 or 추천 유저
    def post(self,request):
        posterList = []
        profileList = []
        type = request.data['type']
        user = request.data['username']
        username = Profile.objects.get(username=user) #자신 
        put_list = myfollowingProfileView.put_list_fg(self,username) #내팔로잉 리스트
        excludeList = set([put_list[i].toUser for i in range(0,len(put_list)) ] ) #쿼리셋 to set
        excludeList.add(username) #내 팔로잉 리스트 + 자신
        #type1 : 팔로잉 중 - 시간 순서, 댓글 좋아요 x 
        if type=="1":
            profileList = [MiniProfileSeralizer(put).data for put in excludeList]
    
        #type2 : 팔로잉 x - 랜덤
        else:
            Profile_list = Profile.objects.all() #전체 리스트 집합 
            Profile_list = [Profile_list[i] for i in range(0,len(Profile_list)) ] #쿼리셋 to 리스트
            #전체 리스트에서 내 팔로잉 리스트 , 내 아이디를 제외 시킴 
            profileList = [i for i in Profile_list if i not in excludeList]
            rand_int =len(profileList) if len(profileList)<=10 else 10
            rand_list = random.sample(profileList,rand_int)
            profileList = [MiniProfileSeralizer(put).data for put in rand_list] #하나씩 넣어서 리스트 완성
        
        #유저 한명씩 탐색 
        for profile in profileList:
            poster_List = poster.objects.filter(username=profile['username']).values()
            poster_List = [poster_List[i] for i in range(0,len(poster_List))] #쿼리셋 to 리스트
            #해당 유저의 포스터 탐색  
            count=0
            for onePoster in poster_List:
                #해당 id에 내가 쓴 댓글이 있는경우 , 내가 좋아요 한 경우가 아니라면 추가 
                isComment = Comment.objects.filter(posterId=onePoster['posterId'])& Comment.objects.filter(writer=user)
                isLike =    Like.objects.filter(posterId=onePoster['posterId'])& Like.objects.filter(liker=user) 
                if not(isComment or isLike):
                    posterList.append({"miniProfiles":profile,"poster":onePoster}) 
                    count+=1
                    if (count>3): #인당 3개까지만 추가 
                        break
            #최대 30개 까지만 반환
            if len(posterList)>30:
                break       
        return  Response(sorted(posterList,key=lambda onePoster:onePoster["poster"]['posterId']),status=status.HTTP_200_OK)

