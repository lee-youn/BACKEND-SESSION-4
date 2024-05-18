"""
URL configuration for config project.

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
from django.urls import path
import poll.views

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path('poll/', poll.views.poll_list, name = 'poll_list'),
    path('poll/<int:id>/', poll.views.poll_detail, name = 'poll_detail'),
    path('poll/<int:id>/agree/', poll.views.poll_agree, name = 'poll_agree'),
    path('poll/<int:id>/disagree/', poll.views.poll_disagree, name = 'poll_disagree'),
]
