__author__ = "stefanotuv"


from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import UserLoginView, UserLogoutView
from allauth.account.views import login, logout, LogoutView


urlpatterns = [

    path("login/",UserLoginView.as_view(template_name='users/login.html'),name='users_login'),
    # path("login/",UserLoginView.as_view(),name='users_login'),
    # path("login/",login,name='users_login'),
    # path('signup', UserLoginView.as_view(template_name='users/signup.html'), name='users_signup'),
    path('signup/', views.register, name='users_signup'),
    # # path('register', views.register, name='users_register'),
    # path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='users_logout'),  #replaced with the allauth version
    path('logout/',UserLogoutView.as_view(template_name='users/logout.html'),name='users_logout'), #replaces the authview version
    # path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='users_logout'),
    # replaces the authview version
    # replaces the authview version
    # path('psw-reset',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
    path('profile/',views.profile,name='users_profile'),

    #
    # path('psw-reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(
    #          template_name='users/password_reset_done.html'
    #      ),
    #      name='password_reset_done'),
    # path('psw-reset-confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='users/password_reset_confirm.html'
    #      ),
    #      name='password_reset_confirm'),
    # path('psw-reset-complete/',
    #      auth_views.PasswordResetCompleteView.as_view(
    #          template_name='users/password_reset_complete.html'
    #      ),
    #      name='password_reset_complete'),
]