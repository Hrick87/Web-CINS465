from django.db import models
from django.contrib.auth.models import User as auth_user

# Create your models here.
#class SuggestionModel(models.Model):
#    suggestion = models.CharField(max_length=240)
#    author = models.ForeignKey(auth_user, on_delete=models.CASCADE)
#    published_on = models.DateTimeField(auto_now_add=True)
#    image = models.ImageField(
#            max_length = 144,
#            upload_to = 'uploads/%Y/%m/%d/',
#            null=True
#        )
#    image_description = models.CharField(
#                max_length=240,
#                null=True
#            )
#    
#    def __str__(self):
#        return str(self.author.username) + " " + str(self.suggestion)

class ProfileModel(models.Model):
    profilepic = models.ImageField(
            max_length = 144,
            upload_to = 'uploads/%Y/%m/%d/',
            null=True,
            blank=True
        ) 
    bio = models.TextField(default="Please write a bio here")
    profile_status = models.CharField(max_length=240)
    author = models.ForeignKey(auth_user, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
            max_length = 144,
            upload_to = 'uploads/%Y/%m/%d/',
            null=True,
            blank=True
        ) 

    def __str__(self):
        return str(self.author.username) + " " + str(self.profile_status)
    
    def __unicode__(self):
        return (self.author.username)

class CommentModel(models.Model):
    comment = models.CharField(max_length=240, null=True)
    author = models.ForeignKey(auth_user, on_delete=models.CASCADE)
    profile_status = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.author.username) + " " + str(self.comment)

