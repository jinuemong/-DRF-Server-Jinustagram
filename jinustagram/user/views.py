
from .models import Profile , follower, following , searchLog 
from posting.models import Like,Comment, StoryViewer
from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer 
from .serializers import UserSerializer , ProfileSeralizer
from .serializers import followerSeralizer, followingSeralizer , searchLogSeralizer
from .serializers import MiniProfileSeralizer
from rest_framework.permissions import AllowAny , IsAuthenticated 
#IsAuthenticated : permission_classes 에 넣어줄 옵션
#인증된, 로그인된 사용자만 접근 가능한 옵션 - 업데이트 용
from rest_framework.generics import RetrieveUpdateAPIView , RetrieveDestroyAPIView
# 이미 create 기능을 만들었기 때문에 create를 제외한 retrieve,update 기능 사용
from rest_framework import status ,filters 
from .renderers import UserJsonRenderer 
#렌더 작업 전송
from rest_framework.decorators import api_view
import random

class RegistrationAPIView(APIView):
    
    permission_classes = (AllowAny,)
    #누가 view를 사용할 수있는지 권한
    #사용자 등록(회원가입)은 누구나 가능
    serializer_class  = RegistrationSerializer
    renderer_classes = (UserJsonRenderer,)  
     
    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    #클라이언트가 요청한 데이터를 받아와 직렬화, 유효성 확인,저장    
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    #이후 반환
    
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJsonRenderer,)
    serializer_class = LoginSerializer
    
    
    def post(self, request):
        #입력 값 서버로 전송
        user = request.data
        #유저 정보를 serializer에 보내줌
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView,RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    #인증된 사용자만 접근 가능
    renderer_classes = (UserJsonRenderer,)
    serializer_class = UserSerializer
    
    def get(self,request,*args, **kwargs):
        #get Method
        serializer = self.serializer_class(request.user)
        #저장하지 않고, 단순히 user 객체를 클라이언트에게 보내줌
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        #부분 업데이트가 가능하게 함
        serializer_data = request.data
        
        #instance, validated_data를 serializer에게 전달함
        #instance는 request.user , validated_data는 serializer_data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
            # partial=True : 부분 업데이트가 가능한 옵션
        )
        
        serializer.is_valid(raise_exception=True)
        #여기서 업데이트 된 정보를 db에 저장 
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        user.delete()
        return Response(data, status=status.HTTP_200_OK)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSeralizer
    filter_backends = [filters.SearchFilter]
    search_fields  = ['=username__username']
    #<참조하는 필드__참조 당하는 명>으로 해줘야 외래키 검색 가능

#프로필 수정 
# *******프로필 수정시 like , comment, storysviewer의 이미지 초기화 
class UpdateProfileView(APIView):
    def get_object(self,id):
        try:
            return Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(id,status=status.HTTP_400_BAD_REQUEST)
         
    def post(self,request):
        data = request.data
        profile = self.get_object(data['id'])
        #like , comment, storysviewer의 이미지 초기화
        serializer = ProfileSeralizer(profile,data=data)
        if serializer.is_valid():
            serializer.save()
            profile = self.get_object(data['id'])
            setImage=serializer.data['userImage']
            #중첩 uri 제거 후 다른 필드 업데이트 
            setImage=setImage.replace('/media','')
            Like.objects.filter(liker=data['username']).update(likerImage=setImage)
            Comment.objects.filter(writer=data['username']).update(writerImage=setImage)
            StoryViewer.objects.filter(viewer=data['username']).update(viewerImage=setImage)            
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        #커맨드 data['userComment']
        #별명 data['customName']
        #이름 data['username']
        #이미지 data['userImage']
        #아이디 data['id']

    
# 작은 프로필  - 최소한 정보만 포함
class MiniProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = MiniProfileSeralizer
    filter_backends = [filters.SearchFilter]
    search_fields  = ['=username__username','customName']

class followerViewSet(viewsets.ModelViewSet):
    queryset = follower.objects.all()
    serializer_class = followerSeralizer
    filter_backends = [filters.SearchFilter]
    
    #쿼리셋 초기화!!!!!!!!!!!!!!!!
    def get_queryset(self):
        username = self.request.query_params.get('username')  # type: ignore
        fromUser = self.request.query_params.get('fromUser')  # type: ignore
        if username and fromUser: 
            queryset =self.queryset.filter(username__username__username  = username) \
            & self.queryset.filter(fromUser__username__username  = fromUser)     
            return queryset
        else:
            return self.queryset
        
    #삭제 메서드 초기화
    def delete(self,request):
        data = request.data
        fromUser, username= data['fromUser'], data['username']
        obj = self.queryset.filter(fromUser=fromUser,username=username)
        obj[0].delete()
        return Response(data,status=status.HTTP_200_OK) 

class followingViewSet(viewsets.ModelViewSet):
    queryset = following.objects.all()
    serializer_class = followingSeralizer
    filter_backends = [filters.SearchFilter]

    #쿼리셋 초기화!!!!!!!!!!!!!!!!
    def get_queryset(self):
        username = self.request.query_params.get('username')  # type: ignore
        toUser = self.request.query_params.get('toUser')  # type: ignore
        if username and toUser:
            queryset =self.queryset.filter(username__username__username  = username) \
            & self.queryset.filter(toUser__username__username  = toUser)     
            return queryset
        else:
            return self.queryset
    
    #삭제 메서드 초기화
    def delete(self,request):
        data = request.data
        username , toUser= data['username'] , data['toUser']
        obj = self.queryset.filter(username=username,toUser=toUser)
        obj[0].delete()
        return Response(data,status=status.HTTP_200_OK) 

#검색 로그 기록
class serachLogViewSet(viewsets.ModelViewSet):
    queryset=  searchLog.objects.all().order_by('-id')
    serializer_class = searchLogSeralizer
    filter_backends = [filters.SearchFilter]
    search_fields  = ['=username__username__username'] 

    #삭제 메서드 초기화         
    def delete(self,request):
        data = request.data
        logId = data['id']
        obj = self.queryset.get(id=logId)
        obj.delete()
        return Response(data,status=status.HTTP_200_OK) 
    
#검색 결과로 프로필을 보여줌 
class searchingLogProfileView(APIView):
    def post(self,requset):
        data =requset.data
        data_list= Profile.objects.filter(
            username__username__icontains  = data['username']) | Profile.objects.filter(customName__icontains  = data['customName'])
        multiList ,count = [] , 0
        for data in data_list:
            if count==20: #프로필 20개까지만 불러옴
                break 
            serializer_data  =MiniProfileSeralizer(data)
            multiList.append(serializer_data.data)
            count+=1
        return Response(multiList,status=status.HTTP_200_OK) 

#사용자 로그를 변환해줌 : 프로필이 있다면 
class transformLogView(APIView):
    def post(self,request):
        data = request.data
        username = data['username']
        LogList = searchLog.objects.filter(username=username).values() #사용자의 로그 추적 
        LogList = [LogList[i] for i in range(0,len(LogList)) ] #쿼리셋 to 리스트
        multiList = []
        for log in LogList:
            user = log['log']
            #로그로 프로필이 존재하는지 확인
            isTrueUser = Profile.objects.filter(username = user).exists()
            isTrueCustom = Profile.objects.filter(customName = user).exists()
            if isTrueUser: #프로필있음
                profile = Profile.objects.get(username=user)
                serializer  =MiniProfileSeralizer(profile)
                profile_data = serializer.data
                profile_data['id'] = log['id'] #id값을 추가
                multiList.append(profile_data)
            elif isTrueCustom: #프로필 해당 커스텀 이름 있음
                profile = Profile.objects.get(customName=user)
                serializer  =MiniProfileSeralizer(profile)
                profile_data = serializer.data
                profile_data['id'] = log['id'] #id값을 추가
                multiList.append(profile_data)
            else: #프로필 없음
                multiList.append(log)
        multiList.reverse() #검색 로그 역순
        return Response(multiList,status=status.HTTP_200_OK)


#내 팔로워의 프로필 
class myFollowerProfileView(APIView):
    def put_list_fr(self,username):
        fromUser_list = follower.objects.filter(username=username)
        return fromUser_list
    
    #get함수 커스텀
    def post(self,request):
        username = request.data['username']
        put_list = self.put_list_fr(username) #내팔로워 리스트
        putList = [put_list[i].fromUser for i in range(0,len(put_list)) ] #쿼리셋 to 리스트
        followList = [MiniProfileSeralizer(put).data for put in putList ] #하나씩 넣어서 리스트 완성
        return Response(followList,status=status.HTTP_200_OK)
            

#내 팔로잉의 프로필
class myfollowingProfileView(APIView):
    
    def put_list_fg(self,username): #총 myfollowerList 반환
        toUser_list = following.objects.filter(username=username)
        return toUser_list
    
    def post(self,request):
        username =request.data['username']
        put_list = self.put_list_fg(username) #내팔로잉 리스트
        putList = [put_list[i].toUser for i in range(0,len(put_list)) ] #쿼리셋 to 리스트
        followingList = [MiniProfileSeralizer(put).data for put in putList ] #하나씩 넣어서 리스트 완성
        return Response(followingList, status=status.HTTP_200_OK)

#랜덤 유저 불러오기                
class randomUserView(APIView):
    
    def post(self,request):
        Profile_list = Profile.objects.all() #전체 리스트 집합 
        Profile_list = [Profile_list[i] for i in range(0,len(Profile_list)) ] #쿼리셋 to 리스트
    
        username = Profile.objects.get(username=request.data['username']) #자신 
        put_list = myfollowingProfileView.put_list_fg(self,username) # type: ignore #내팔로잉 리스트
        excludeList = set([put_list[i].toUser for i in range(0,len(put_list)) ] ) #쿼리셋 to set
        excludeList.add(username)

        #전체 리스트에서 내 팔로잉 리스트 , 내 아이디를 제외 시킴 
        profileList = [i for i in Profile_list if i not in excludeList]
                
        
        #최대 10명, 최소 n명의 유저 수 추출
        rand_int =len(profileList) if len(profileList)<=10 else 10
        rand_list = random.sample(profileList,rand_int)
        
        randList = [MiniProfileSeralizer(put).data for put in rand_list ] #하나씩 넣어서 리스트 완성
        #생성할 필요 없이 랜덤 데이터 전송
        return Response(randList, status=status.HTTP_200_OK)
    



