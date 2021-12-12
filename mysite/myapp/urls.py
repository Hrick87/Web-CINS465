from django.urls import path
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index),
    path('useful/', views.delete_random),
    path('login/', auth_views.LoginView.as_view()),
    path('register/', views.register_view),
    path('logout/', views.logout_view),
    #path('suggestion/', views.suggestion_view),
    path('profile/<str:username>/comment/<int:stat_id>/', views.comment_view),
    path('profile_status/', views.profile_status_view),
    path('profile/<str:username>/', views.profile_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
