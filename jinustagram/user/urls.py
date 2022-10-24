
from django.urls import path,include
from .views import RegistrationAPIView , LoginAPIView 
from .views import UserRetrieveUpdateAPIView,ProfileViewSet , followerViewSet, followingViewSet 
from .views import randomUserView ,myfollowingProfileView,myFollowerProfileView , serachLogViewSet
from .views import MiniProfileView ,transformLogView ,searchingLogProfileView ,UpdateProfileView
from rest_framework.routers import DefaultRouter
router_user = DefaultRouter()
router_user.register('profile',  ProfileViewSet)
router_user.register('follower', followerViewSet)
router_user.register('following',followingViewSet)
router_user.register('searchLog',serachLogViewSet)

urlpatterns = [
    path('register/',RegistrationAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('current/',UserRetrieveUpdateAPIView.as_view()),
    path('myfollower/',myFollowerProfileView.as_view()),
    path('myfollowing/',myfollowingProfileView.as_view()),
    path('randomuser/',randomUserView.as_view()),
    path('miniprofile/',MiniProfileView.as_view({'get':'list'})),
    path('transformLog/',transformLogView.as_view()),
    path('searchingProfile/',searchingLogProfileView.as_view()),
    path('update/profile/',UpdateProfileView.as_view()),
    path('',include(router_user.urls)),
]



# 이전 코드 

# from .views          import UserCreate
# from rest_framework import urls

# urlpatterns = [
#     path('signup/', UserCreate.as_view()),
#     path('auth/', include('rest_framework.urls'))
#     #로그인을 위해서는 rest_framework에서 제공하는 기능을 활용
#     #편의상추가
# ]
