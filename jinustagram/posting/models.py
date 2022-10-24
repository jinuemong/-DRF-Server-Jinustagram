from enum import auto
from django.db import models
from user.models import Profile
from django.utils import timezone
# Create your models here.

#게시물
class poster(models.Model):
    posterId = models.BigAutoField(primary_key=True,help_text="Poster ID")
    username = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='posterPost',db_column='username',to_field='username_id')
    uploadTime = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    def __str__(self):
        return str(self.posterId)

#댓글
class Comment(models.Model):
    commentId = models.BigAutoField(primary_key=True,help_text="Comment ID")
    posterId = models.ForeignKey(poster,on_delete=models.CASCADE,related_name='commentPost',db_column='posterId',to_field='posterId')
    writer = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='commentPost',db_column='writer',to_field='username_id')
    writerImage = models.ImageField(default='default.png',upload_to="%Y/%m/%d")
    uploadTime = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    
#게시물 이미지
class Image(models.Model):
    imageId = models.BigAutoField(primary_key=True,help_text="Poster Image ID")
    posterId = models.ForeignKey(poster,on_delete=models.CASCADE,related_name='imagePost',db_column='posterId',to_field='posterId')
    Oneimage = models.ImageField(default='default.png',upload_to="%Y/%m/%d")
    
#좋아요
class Like(models.Model):
    likeId = models.BigAutoField(primary_key=True,help_text="Like ID")
    posterId = models.ForeignKey(poster,on_delete=models.CASCADE,related_name='likePost',db_column='posterId',to_field='posterId')
    liker = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='likePost',db_column='liker',to_field='username_id')
    likerImage = models.ImageField(default='default.png',upload_to="%Y/%m/%d")
    uploadTime = models.DateTimeField(auto_now_add=True)
        
#스토리   
class Story(models.Model):
    storyId = models.BigAutoField(primary_key=True, help_text="Story ID")
    username = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='storyPost',db_column='username',to_field='username_id')
    storyImage = models.ImageField(default='default.png',upload_to="%Y/%m/%d")
    uploadTime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.storyId)

#스토리 시청자
class StoryViewer(models.Model):
    storyId = models.ForeignKey(Story,on_delete=models.CASCADE,db_column='story_id',
                                related_name='storyViewerPost',to_field='storyId')
    viewer = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='storyViewerPost',to_field='username_id')
    viewerImage = models.ImageField(default='default.png',upload_to="%Y/%m/%d")
    
    