from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.views.generic import TemplateView, ListView
from django.db.models import Q

import random
from datetime import datetime, timezone

from . import models
from . import forms
from myapp.forms import UserProfileForm
from myapp.models import Profile

# Create your views here.

#HomePageView and Search ResultsView code from: https://learndjango.com/tutorials/django-search-tutorial

class HomePageView(TemplateView):
    template_name = 'home.html'

class SearchResultsView(ListView):
    model = Profile
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Profile.objects.filter(Q(user__username__icontains=query) | Q(location__icontains=query))
        return object_list

@login_required
def update_profile(request):
    userprofile_form = UserProfileForm(request.POST, request.FILES, instance = Profile.objects.get(user=request.user))
    if request.method == 'POST':
        if userprofile_form.is_valid():
            userprofile_form.save()     
            return redirect('/profile/%s/'%request.user.username)  

    return render(request, 'editprofile.html', context={'userprofile_form': userprofile_form})

def profile_info_view(request):
    profile_info_objects = models.Profile.objects.all()
    profile_info_list = {}
    profile_info_list["profile_info"] = []
    for info in profile_info_objects:
        temp_info = {}
        temp_info["profile_info"] = info.profile_info
        temp_info["user"] = info.user
        temp_info["bio"] = info.bio
        temp_info["location"] = info.location
        if info.image:
            info_stat["profilepic"] = info.profilepic.url
            info_stat["image_desc"] = info.image_description
        else:
            info_stat["profilepic"] = ""
            info_stat["image_desc"] = ""
        profile_info_list["profile_info"] += [temp_info]

    return JsonResponse(profile_info_list)


#@login_required
#@transaction.atomic
#def update_profile(request):
#    if request.method == 'POST':
#        user_form = UserForm(request.POST, instance=request.user)
#        profile_form = ProfileForm(request.POST, instance=request.user.profile)
#        if user_form.is_valid() and profile_form.is_valid():
#            user_form.save()
#            profile_form.save()
#            messages.success(request, _('Your profile was successfully updated!'))
#            return redirect('settings:profile')
#        else:
#            messages.error(request, _('Please correct the error below.'))
#    else:
#        user_form = UserForm(instance=request.user)
#        profile_form = ProfileForm(instance=request.user.profile)
#
#    context = {
#        'user_form': user_form,
#        'profile_form': profile_form
#    }
#
#    return render(request, 'profile.html', context=context)


def profile_view(request, username):
    username = User.objects.get(username=username)
    profile_list = Profile.objects.all()
    if request.method == 'POST':
        form = forms.StatusForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request)
            return redirect("/profile/%s/"%request.user.username)
    else:
        form = forms.StatusForm()

    context = { 'title': "Your Profile", 'form': form, 'profile_list': profile_list }

    return render(request, "profile.html", context=context)

@login_required
def comment_view(request, stat_id, username):    
    username = User.objects.get(username=username)
    if request.method == "POST":
        form = forms.Comment_Form(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request, stat_id)
            return redirect("/profile/%s/"%request.user.username)
    else:
        form = forms.Comment_Form()

    context = {
        "title": "Comment",
        "stat_id": stat_id,
       "form": form
    }
    return render(request,"comment.html", context=context)

#def suggestion_view(request):
#    if not request.user.is_authenticated:
#        return redirect("/login/")
#    if request.method == "POST":
#        form = forms.SuggestionForm(request.POST, request.FILES)
#        if form.is_valid() and request.user.is_authenticated:
#            form.save(request)
#            return redirect("/suggestion/")
#    else:
#        form = forms.SuggestionForm()
#
#    context = {
#        "title": "Suggestion",
#       "form": form
#    }
#    return render(request,"suggestion.html", context=context)

def delete_random(request):
    some_list = models.SuggestionModel.objects.all()
    some_int = random.randrange(len(some_list))
    some_instance = some_list[some_int]
    some_instance.delete()
    print(some_int)
    return redirect("/")

def logout_view(request):
    logout(request)
    return redirect("/login/")

def register_view(request):
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect("/login/")
    else:
        form = forms.RegistrationForm()

    context = {
        "title": "Registration Page",
         "form": form
    }
    return render(request,"registration/register.html", context=context)

def profile_status_view(request):
    profile_status_objects = models.ProfileModel.objects.all().order_by("-published_on")
    profile_status_list = {}
    profile_status_list["profile_status"] = []
    for stat in profile_status_objects:
        comment_objects = models.CommentModel.objects.filter(
            profile_status=stat
            )
        temp_stat = {}
        temp_stat["profile_status"] = stat.profile_status
        temp_stat["id"] = stat.id
        temp_stat["author"] = stat.author.username
        temp_stat["date"] = stat.published_on.strftime("%Y-%m-%d")
        if stat.image:
            temp_stat["image"] = stat.image.url
            #temp_stat["image_desc"] = stat.image_description
        else:
            temp_stat["image"] = ""
            #temp_stat["image_desc"] = ""
       
        temp_stat["comments"] = []
        for comm in comment_objects:
            temp_comm = {}
            temp_comm["comment"] = comm.comment
            temp_comm["id"] = comm.id
            temp_comm["author"] = comm.author.username
            time_diff = datetime.now(timezone.utc) - comm.published_on
            time_diff_s = time_diff.total_seconds()
            if time_diff_s < 60:
                temp_comm["date"] = "published " + str(int(time_diff_s)) + " seconds ago"
            else:
                time_diff_m = divmod(time_diff_s,60)[0]
                if time_diff_m < 60:
                    temp_comm["date"] = "published " + str(int(time_diff_m)) + " minutes ago"
                else:
                    time_diff_h = divmod(time_diff_m,60)[0]
                    if time_diff_h < 24:
                        temp_comm["date"] = "published " + str(int(time_diff_h)) + " hours ago"
                    else:
                        temp_comm["date"] = comm.published_on.strftime("%Y-%m-%d %H:%M:%S")
            temp_stat["comments"] += [temp_comm]
        profile_status_list["profile_status"] += [temp_stat]

    return JsonResponse(profile_status_list)

