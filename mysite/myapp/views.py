from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import random
from datetime import datetime, timezone

from . import models
from . import forms

# Create your views here.
def index(request):
#    if request.method == "POST":
#        form = forms.SuggestionForm(request.POST)
#        if form.is_valid() and request.user.is_authenticated:
#            form.save(request)
#            form = forms.SuggestionForm()
#    else:
#        form = forms.SuggestionForm()
#
#    context = {
#        "title": "MyBook",
#        "body":"Hello World",
#       "form": form
#    }
    return render(request,"index.html")

def profile_view(request, username):
    username = User.objects.get(username=username)
    if request.method == 'POST':
        form = forms.StatusForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            form.save(request)
            return redirect("/profile/%s/"%request.user.username)
    else:
        form = forms.StatusForm()

    context = { 'title': "Your Profile", 'form': form }

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
            temp_stat["image_desc"] = stat.image_description
        else:
            temp_stat["image"] = ""
            temp_stat["image_desc"] = ""
       
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

