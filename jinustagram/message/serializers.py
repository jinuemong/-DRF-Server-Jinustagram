from dataclasses import field
from .models import Message,MessageRoom ,MessageUser
from rest_framework import serializers

class MessageSeralizer(serializers.ModelSerializer):
    class Meta:
        managed =True
        model = Message
        db_table = 'Messages'
        fields = "__all__"

class MessageUserSeralizer(serializers.ModelSerializer):
    class Meta:
        managed =True
        model = MessageUser
        db_table = 'MessageUsers'
        fields = "__all__"

class MessageRoomSeralizer(serializers.ModelSerializer):
    MessageUserPost = MessageUserSeralizer(many=True,read_only=True)
    messagePost = MessageSeralizer(many=True,read_only=True)
    class Meta:
        managed =True
        model = MessageRoom
        db_table = 'MessageRooms'
        fields = ['messageRoomId','MessageUserPost','messagePost']
        
