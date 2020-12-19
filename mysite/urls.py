"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
#from trips.views import hello_world, home, index, sign_up, sign_in, log_out
from trips.views import hello_world, home, login, signup, mainweb, logout, base, manager, managerlogin, managerpsedit, modify, delete, managerpost, managerlogout, result, post, search
from django.conf.urls import include, url
from trips import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login, name='Login'),
    path('signup/', signup, name='Signup'),
    path('mainweb/', mainweb, name='Mainweb'),
    path('logout/', logout, name='Logout'),
    path('base/', base, name='base'),
    path('home/', home, name='Home'),
    path('post/', post, name='Post'),
    path('search/', search, name='Search'),
    path('result/', result, name='Result'),
    path('manager/login', managerlogin, name='Managerlogin'),
    path('manager/logout', managerlogout, name='Managerlogout'),
    path('manager/password', manager, name='ManagerPassword'),
    path('manager/post', managerpost, name='ManagerPost'),
    path('manager/delete', delete, name='Delete'),

    path('manager/edit', managerpsedit, name='Edit'),
    path('manager/modify', modify),
    url(r'hello/$', hello_world, name="Hello"),
    #url(r'hello/$', hello_world),


]

'''
    url(r'^hello/$', hello_world),
    url(r'^home/$', home),
    path('', index),
    path('register/', sign_up, name='Register'),
    path('login/', sign_in, name='Login'),
    path('logout/', log_out, name='Logout')
    #path('register', views.sign_up, name='Register'),

    url(r'login/$', login),
    url(r'signup/$', signup, name='Signup'),
    url(r'mainweb/$', mainweb),
    url(r'logout/$', logout),
    '''
