import django_redis
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.views import View


# Create your views here.


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # 获取数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        # 从数据库中验证数据
        user = authenticate(username=username, password=password)
        print(str(user))
        if user is not None:
            print("longining")
            # A backend authenticated the credentials
            login(request, user)
            redis=django_redis.get_redis_connection("is_login")
            redis.set(user.username,"true",30*60)
            request.session.set_expiry(30*60)
            request.session["is_login"] = True
            request.session["username"] = user.username
            response = redirect('http://127.0.0.1:8000/index/%s'%user.username)
            response.set_cookie("username", user.username, 30*60)
            return response
        else:
            # No backend authenticated the credentials
            login_mas="you password or username is wrong!"
            response=render(request, "login.html")
            response.set_cookie("login_mas",login_mas)
            return response
