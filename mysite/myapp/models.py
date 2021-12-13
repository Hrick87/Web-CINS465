from django.db import models
from django.contrib.auth.models import User as auth_user
from django.db.models.signals import post_save
from django.dispatch import receiver

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

#ProfileInfo and signal classes code sourced from:
#https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

class Profile(models.Model):
    user = models.OneToOneField(auth_user, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profilepic = models.ImageField(
            max_length = 144,
            upload_to = 'uploads/%Y/%m/%d/',
            null=True,
            blank=True
        )
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=auth_user)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=auth_user)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ProfileModel(models.Model):
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

