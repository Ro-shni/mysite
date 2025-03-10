"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from home import views
#from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
#from .views import filter_projects


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('home',views.index,name='home'),
    #path('home', views.index, name='index'),
    #path('about', views.about, name='about'),
    path('login', views.login, name='login'),
    path('contact', views.contact, name='contact'),
    path('signup', views.signup, name='signup'),
    path('logout/', views.logoutpage, name='logout'),
    path('student1/',views.student1,name='student1'),
    path('student1/detail/<int:pk>/',views.studentdetail,name='studentdetail'),
    path('certi',views.certi, name='certi'),
    path('display',views.display, name='display'),
    path('profile',views.profile, name='profile'),
    path('favicon.ico', views.favicon, name='favicon'),
    path('certi/delete/<int:pk>/', views.certidel, name='certidel'),
    path('certi/update/<int:pk>/', views.certiupdate, name='certiupdate'),
    path('orders',views.orders, name='orders'),
    path('home/delete/<int:pk>/', views.ordersdel, name='ordersdel'),
    path('home/update/<int:pk>/', views.ordersupdate, name='ordersupdate'),
    path('student_index',views.student_index, name='student_index'),
    path('view_students',views.view_students, name='view_students'),
    path('certi_detail/<int:pk>/', views.certi_detail, name='certi_detail'),
    path('certi_list',views.certi_list, name='certi_list'),
    path('view_students_by_branch_section/<str:branch>/<str:section>/', views.view_students_by_branch_section, name='view_students_by_branch_section'),
    path('projects/', views.project_list, name='project_list'),  # Display project list
    path('filter_projects/', views.filter_projects, name='filter_projects'),
    #path('projects/', views.filtered_project_list, name='filtered_project_list'),
    path('projects/create/', views.create_project, name='create_project'),  # Create new project
    path('projects/edit/<int:pk>/', views.edit_project, name='edit_project'),  # Edit existing project
    path('projects/delete/<int:pk>/', views.delete_project, name='delete_project'),  # Delete a project
    path('register_for_event/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('unregister_for_event/<int:event_id>/', views.unregister_for_event, name='unregister_for_event'),
    path('event/<int:event_id>/', views.event_details, name='event_details'),
    path('create_team/', views.create_team, name='create_team'),
    path('add_student_to_team/<int:team_id>/', views.add_student_to_team, name='add_student_to_team'),
    path('create_progress_report/<int:student_id>/', views.create_progress_report, name='create_progress_report'),
    path('team_detail/<int:team_id>/', views.team_detail, name='team_detail'),
    #path('student_progress/<int:student_id>/', views.student_progress, name='student_progress'),
    path('search_student_progress/', views.search_student_progress, name='search_student_progress'),
    path('add_mentor/', views.add_mentor, name='add_mentor'),
    path('mentor_list/', views.mentor_list, name='mentor_list'),
    path('team_list/', views.team_list, name='team_list'),
    path('mentor_operations/', views.mentor_operations, name='mentor_operations'),
    path('operations_dashboard/', views.operations_dashboard, name='operations_dashboard'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)