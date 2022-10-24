
from django.urls import path, include
from .views import PosterViewSet , CommentViewSet ,ImageViewSet
from .views import LikeViewSet, StoryViewSet, StoryViewerViewSet,RandomPosterViewSet
from rest_framework.routers import DefaultRouter


router_posting = DefaultRouter()
router_posting.register('poster',PosterViewSet)
router_posting.register('comment',CommentViewSet)
router_posting.register('images',ImageViewSet)
router_posting.register('likes',LikeViewSet)
router_posting.register('story',StoryViewSet)
router_posting.register('storyViewer',StoryViewerViewSet)

urlpatterns = [
    path('',include(router_posting.urls)),
    path('randomPoster/',RandomPosterViewSet.as_view()),
]
