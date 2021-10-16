import hashlib
import os
import re

from django.contrib.auth import authenticate, login
from django.views import View
from django_redis import get_redis_connection

from EJAT.my_libs.verifications import get_verification
from django import http
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
# from .models import Article
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import MyUser,UserData
from forget.models import UserMD5


# Create your views here.


@csrf_exempt
def usernameChecked(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        count = MyUser.objects.filter(username=username).count()
        return HttpResponse(count)
    else:
        return render(request, "404.html")


@csrf_exempt
def emailChecked(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        count = MyUser.objects.filter(email=email).count()
        return HttpResponse(count)
    else:
        return render(request, "404.html")


@csrf_exempt
def emailverificationChecked(request):
    if request.method == 'POST':
        email = request.POST.get('emailverification_email')
        redis_conn = get_redis_connection("verification")
        print(redis_conn.keys("*"))
        redis_conn.delete(email)
        verification = get_verification()
        masage = '''
            <h2>your verification</h2>
            <br>
            <p>This is to make sure that the mailbox you entered is a valid mailbox, which belongs to your private information. We apply this to services such as password retrieval, password modification, and user logout.</p>
            <br>
            <p> This is your verification code, the verification code will expire within 5 minutes, please fill in in time:</p>
            <h1>         %s</h1>
        ''' % verification

        redis_conn.set(email, verification, 300)
        print(redis_conn.keys("*"))
        send_mail("verification", message="", from_email="ejatjonamar@outlook.com", recipient_list=[email],
                  fail_silently=False, html_message=masage
                  )

        return HttpResponse(1)
    else:
        return render(request, "404.html")


class Register(View):
    def get(self, request):
        verification_error = request.session.pop("verification_error", "")
        return render(request, 'register.html', context={"verification_error": verification_error})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        verification = request.POST.get("emailverification")
        redis_conn = get_redis_connection("verification")
        verification_cont = redis_conn.get(email)
        # 验证信息
        if not re.match(r"[\w]+(\.[\w]+)*@[\w]+(\.[\w])+", email):
            request.session["verification_error"] = "please check whether the email address is correct !"
            return redirect("register")
        if not re.match(r"\w{1,32}$", username):
            request.session["verification_error"] = "please check whether the username is correct !"
            return redirect("register")

        if not re.match(r"^\w{6,32}$", password):
            request.session["verification_error"] = "please check whether the password is correct !"
            return redirect("register")

        if not re.match(r"^\w{1,32}$", first_name):
            request.session["verification_error"] = "please check whether the first name is correct !"
            return redirect("register")

        if not re.match(r"^\w{1,32}$", last_name):
            request.session["verification_error"] = "please check whether the last name is correct !"
            return redirect("register")
        if str(verification_cont) == verification:
            try:
                count = MyUser.objects.filter(Q(username=username) | Q(email=email)).count()
                if count == 0:
                    user = MyUser.objects.create_user(username=username, email=email, password=password,
                                                      first_name=first_name,
                                                      last_name=last_name)
                    user.save()
                    m = hashlib.md5()
                    dic={"username":user.username,"password":user.password,"email":user.email}
                    m.update(repr(dic).encode(encoding='utf-8'))
                    md5 = m.hexdigest()
                    user_md5 = UserMD5.objects.create(user_name=username, email=email, user_md5=md5,user=user)
                    user_md5.save()
                    user_data=UserData.objects.create(user=user)
                    user_data.save()
                    # 登录
                    response=redirect('http://127.0.0.1:8000/login/')
                    mas="Registered successfully, please log in!"
                    response.set_cookie("login_mas",mas)
                    return response
                else:
                    return HttpResponseForbidden(
                        '''
                        Duplicate email or username!
                        It seems that you have already registered. Go back to the login page to log in or retrieve your password.
                        '''
                    )
            except Exception as e:
                print(e)
                try:
                    MyUser.objects.get(Q(username=username) & Q(email=email)).delete()
                    UserMD5.objects.get(email=email).delete()
                    return HttpResponseForbidden(
                        '''
                            There was an error in registration!
                            Please contact the administrator or log in again.
                            '''
                    )
                except Exception as e:
                    print(e)
                    return HttpResponseForbidden(
                        '''
                        An exception occurs, please contact the administrator or register again.
                        The reason for this exception: data import was successful, registration failed.
                        An exception occurred when the system tried to delete the imported data.
                        '''
                    )
        else:
            request.session["verification_error"] = "Your verification code is wrong ?"
            return redirect("register")

