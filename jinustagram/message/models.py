from email.mime import image
from django.db import models
from user.models import Profile
from django.utils import timezone
# Create your models here.

#메시지 룸 (아이디로 구별, 사용자 식별 ) 
class MessageRoom(models.Model):
    messageRoomId = models.BigAutoField(primary_key=True,help_text="Message Room ID")

#구체적 메시지 
class Message(models.Model):
    messageId = models.BigAutoField(primary_key=True,help_text="Meesage ID")
    messageRoomId = models.ForeignKey(MessageRoom,on_delete=models.CASCADE,related_name='messagePost',db_column='messageRoomId',to_field='messageRoomId')
    writer = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='messagePost',db_column='writer',to_field='username_id')
    uploadTime = models.DateTimeField(auto_now_add=True)
    body = models.TextField(null=True)
    messageImage = models.ImageField(null=True,upload_to="%Y/%m/%d")

class MessageUser(models.Model):
    messageRoomId = models.ForeignKey(MessageRoom,on_delete=models.CASCADE,related_name='MessageUserPost',db_column='messageRoomId',to_field='messageRoomId')
    username =  models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='MessageUserPost',db_column='username',to_field='username_id')
    isActive = models.BooleanField(null=False,default=False) #해당 유저에게 채팅방이 활성화 상태인지  - 서로 비활성화 상태면 룸 삭제 
    lastMessageId =  models.IntegerField(default=True) #삭제 이후 메시지 역활  - 채팅방을 나갈 경우 이 이후의 메시지만 공개 
    lastReadMessageId = models.IntegerField(default=True) # 마지막으로 읽은 메시지 역할 - 채팅방을 안 읽은 경우 여기부터 로딩
    targetUser =  models.ForeignKey(Profile,on_delete=models.CASCADE,to_field='username_id')
