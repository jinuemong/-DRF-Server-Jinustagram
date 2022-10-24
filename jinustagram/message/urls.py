
from django.urls import path, include
from .views import MessageRoomViewSet ,MessageViewSet, MessageUserViewSet
from .views import FindMessageRoom , MessageRoomProfile
from rest_framework.routers import DefaultRouter


router_posting = DefaultRouter()
router_posting.register('messageRoom',MessageRoomViewSet)
router_posting.register('message',MessageViewSet)
router_posting.register('messageUser',MessageUserViewSet)

urlpatterns = [
    path('findMessageRoom/',FindMessageRoom.as_view()),
    path('MessageRoomProfile/',MessageRoomProfile.as_view()),
    path('',include(router_posting.urls)),
]
