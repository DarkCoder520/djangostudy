from django.shortcuts import render,redirect
from .models import UserInfo


# Create your views here.
def login(request):
    error_msg = ""
    if request.method == "POST":
        email = request.POST.get("email","")
        pwd = request.POST.get("pwd")
        if email =="tayetang@163.com" and pwd=="tangyuan":
            return redirect("/user_list/")
        else:
            error_msg="邮箱或密码不正确"
    return render(request,"login.html",{'error_msg':error_msg})


def user_list(request):
    allUsers = UserInfo.objects.all()
    return render(request,"user_list.html",{'allUsers':allUsers})


def add_user(request):
    if request.method == "POST":
        name = request.POST.get("username","")
        UserInfo.objects.create(name=name)
        return  redirect("/user_list")

    return render(request,"add_user.html")