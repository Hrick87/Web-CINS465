from django import forms
from django.forms import ModelForm
from django.core.validators import validate_unicode_slug
from . import models
from myapp.models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as auth_user

def must_be_caps(value):
    if not value.isupper():
        raise forms.ValidationError("Not all upper case")
    return value

def must_be_unique(value):
    user_objects = auth_user.objects.filter(email=value)
    if len(user_objects) > 0:
        raise forms.ValidationError("Email already exists")
    return value

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class StatusForm(forms.Form):
    status_field = forms.CharField(label ='Status', max_length=240,)
    image = forms.ImageField(label='Image File', required=False,)
    
    def save(self, request):
        status_instance = models.ProfileModel()
        status_instance.profile_status = self.cleaned_data["status_field"]
        status_instance.image = self.cleaned_data["image"]
        status_instance.author = request.user
        status_instance.save()
        return status_instance

#class SuggestionForm(forms.Form):
#    suggestion_field = forms.CharField(
#                label='Suggestion',
#                max_length=240,
#            )
#    image = forms.ImageField(
#                label="Image File",
#                required=False,
#            )
#    image_description = forms.CharField(
#                label="Image Description",
#                required=False,
#            )
#
#    def save(self, request):
#        suggestion_instance = models.SuggestionModel()
#        suggestion_instance.suggestion = self.cleaned_data["suggestion_field"]
#        suggestion_instance.image = self.cleaned_data["image"]
#        suggestion_instance.image_description = self.cleaned_data["image_description"]
#        suggestion_instance.author = request.user
#        suggestion_instance.save()
#        return suggestion_instance

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
            label="Email",
            required=True,
            validators=[must_be_unique]
            )

    class Meta:
        model = auth_user
        fields = (
                "username",
                "email",
                "password1",
                "password2",
                )

        def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data["email"]
            if commit:
                user.save()
                return user

class Comment_Form(forms.Form):
    comment_field = forms.CharField(
            label='Comment',
            max_length=240,
            # validators=[validate_unicode_slug, must_be_caps],
            )

    def save(self, request, stat_id):
        status_instance = models.ProfileModel.objects.get(id=stat_id)
        comment_instance = models.CommentModel()
        comment_instance.comment = self.cleaned_data["comment_field"]
        comment_instance.author = request.user
        comment_instance.profile_status = status_instance
        comment_instance.save()
        return comment_instance


