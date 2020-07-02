"""api_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'projects/',views.Projects.as_view()),  # 使用as_view()方法把类视图注册为视图
    re_path(r'project/', views.Project.as_view()),  # 使用as_view()方法把类视图注册为视图
    re_path(r"^project1/(?P<pk>[\d]+).?$", views.Project1.as_view()),
    re_path(r'cases/?',views.TestCases.as_view()),
    re_path(r'run/?',views.ExcuteCase.as_view()),
]
