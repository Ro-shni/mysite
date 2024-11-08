from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('home',views.index,name='home'),
    #path('about', views.about, name='about'),
    path('login', views.login, name='login'),
    path('contact', views.contact, name='contact'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logoutpage, name='logout'),
    path('student1',views.student1,name='student1'),
    path('certi',views.certi, name='certi'),
    path('orders', views.orders, name='orders'), 
]