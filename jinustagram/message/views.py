from os import stat
from pyexpat.errors import messages
from urllib import response
from django.shortcuts import render
from .models import Message, MessageRoom ,MessageUser
from .serializers import MessageRoomSeralizer, MessageSeralizer, MessageUserSeralizer
from user.serializers import MiniProfileSeralizer
from user.models import Profile
from rest_framework import viewsets , filters
from rest_framework.views import APIView
from rest_framework import status ,filters 
from rest_framework.response import Response

class MessageRoomViewSet(viewsets.ModelViewSet):
    
    queryset = MessageRoom.objects.all()
    serializer_class = MessageRoomSeralizer
    
    
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSeralizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=writer__username__username']
    
    
class MessageUserViewSet(viewsets.ModelViewSet):
    queryset = MessageUser.objects.all()
    serializer_class = MessageUserSeralizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=messageRoomId__messageRoomId']
    
#해당 유저들의 메시지 룸이 존재하는 지 확인 하여 id값 or 값없음 (-1) or 에러값 반환
class FindMessageRoom(APIView):
    
    def post(self,request):
        data = request.data
        user1 = data["username"]
        user2 = data["targetUserName"]
        
        user1RoomIdList = MessageUser.objects.filter(username=user1).values('messageRoomId')
        user2RoomIdList = MessageUser.objects.filter(username=user2).values('messageRoomId')
        
        user1RoomIdList = [user1RoomIdList[i]['messageRoomId'] for i in range(0,len(user1RoomIdList)) ] #쿼리셋 to 리스트
        user2RoomIdList = [user2RoomIdList[i]['messageRoomId'] for i in range(0,len(user2RoomIdList)) ] #쿼리셋 to 리스트
        intersection = list(set(user1RoomIdList) & set(user2RoomIdList))
        #같은 id 룸이 있다면 id룸 존재 
        if len(intersection)>0:
            return Response(intersection[0],status=status.HTTP_200_OK) 
        elif len(intersection)==0:
            return Response(-1,status=status.HTTP_200_OK) 
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class MessageRoomProfile(APIView):
    
    def post(self,request):
        user = request.data["username"]
        messageRoomProfileList = []
        targetList = MessageUser.objects.filter(username=user).values()
        
        #채팅 방을 하나씩 불러옴 
        for target in targetList:
            profile = Profile.objects.get(username=target['targetUser_id'])
            serializer_profile  =MiniProfileSeralizer(profile)
            profile = serializer_profile.data
            #마지막 메시지 받아옴 
            last_message = Message.objects.filter(messageRoomId=target['messageRoomId_id']).last()
            #오브젝트 데이터를 serializer에 넣어줌 
            serializer_message  = MessageSeralizer(last_message)
            message = serializer_message.data
            if last_message: #메시지 존재
                appList = {"messageRoomId":target['messageRoomId_id'],"username":profile['username'],"userImage":profile['userImage']
                           ,"lastMessage":message['body'],"lastMessageTime":message['uploadTime'], "lastMessageId":message['messageId'],
                           "storyCount":profile['storyCount'],"storyPost":profile['storyPost']}
                messageRoomProfileList.append(appList)
            else:
                appList = {"messageRoomId":target['messageRoomId_id'],"username":profile['username'],
                           "userImage":profile['userImage'],"lastMessage":"","lastMessageTime":"","lastMessageId":-1,
                           "storyCount":profile['storyCount'],"storyPost":profile['storyPost']} 
                messageRoomProfileList.append(appList)
                
                
        return Response(messageRoomProfileList,status=status.HTTP_200_OK)