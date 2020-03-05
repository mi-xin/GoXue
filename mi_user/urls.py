"""GoXue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path
from . import views

app_name = 'mi_user'
urlpatterns = [
    path('login/', views.mi_login, name='login'),
    path('register/', views.mi_register, name='register'),
    path('logout/', views.mi_logout, name='logout'),
    path('information/', views.user_information, name='user_information'),
    path('information/update/',views.update_information,name='update_information'),
    path('information/updatepassword/',views.update_password,name='updatepassword')
    # path('classUpload/<int:class_id>/', views.user_class_upload_id, name='user_class_upload_id'),
    # path('class/damin',views.class_admin,name='class_admin'),
    # path('class/', views.user_class, name='user_class'),
]
