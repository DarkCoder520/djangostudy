"""django01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import HttpResponse,render


def tangyuan(request):
    with open("templates/tangyuan/tangyuan.html") as f:
        htmlstr = f.read()
    return HttpResponse(bytes(htmlstr,encoding='utf-8'))


def login(request):
    return render(request,template_name='login.html')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', login),
    url(r'^tangyuan/', tangyuan),
]
