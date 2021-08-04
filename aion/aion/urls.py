"""aion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservations.urls')),
    path('analytics/', include('analytics.urls')),
]

from django.contrib.auth import views as auth_views
from reservations import views as core_views
from reservations.forms import LogInForm, PasswordResetFormAion, PasswordResetConfirmFormAion, PasswordChangeFormAion

from django.urls import include, re_path

urlpatterns += [
    
    # Authentication URLS
    path(
        'signin/', 
        auth_views.LoginView.as_view(
            redirect_authenticated_user=True, 
            template_name='registration/login.html', 
            authentication_form=LogInForm
        ), 
        name='signin'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Account Creation URLS
    path('signup/', core_views.signup, name='signup'),
    path(
        'signup/registration/account_activation_sent/', 
        core_views.account_activation_sent, 
        name='account_activation_sent'
    ),
    path(
        'activate/<uidb64>/<token>/', 
        core_views.activate, 
        name='activate'
    ),
    
    # Password Reset Views
    path(
        'password_reset/', 
        auth_views.PasswordResetView.as_view(
            form_class=PasswordResetFormAion
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(), 
        name='password_reset_done'
    ),
    path(
        'password_reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            form_class=PasswordResetConfirmFormAion
        ), 
        name='password_reset_confirm'),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            form_class=PasswordChangeFormAion
        ), 
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
    # Captcha URLs
    re_path(r'^captcha/', include('captcha.urls')),
]

