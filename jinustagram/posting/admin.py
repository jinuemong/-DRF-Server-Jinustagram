from django.contrib import admin
from . import models
admin.site.register(models.poster)
admin.site.register(models.Image)
admin.site.register(models.Like)
admin.site.register(models.Comment)

admin.site.register(models.Story)
admin.site.register(models.StoryViewer)
# Register your models here.
