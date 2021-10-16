import hashlib
import re

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from forget.models import UserMD5

from register.models import MyUser


class Reset(View):
    def get(self, request, email=None):
        if email==None:
            return redirect("http://127.0.0.1:8000/forget/")
        user_md5_count = UserMD5.objects.filter(email=email).count()
        if user_md5_count == 1:
            try:
                redis_user_md5 = get_redis_connection("user_md5")

                md5 = redis_user_md5.get(email)
                if md5 is not None:

                    return render(request, "reset.html")
                else:
                    return HttpResponse(
                        '''
                        Before changing your password, you should perform email verification on the Forgot Password page.
                        '''
                    )
            except Exception as e:
                return HttpResponse(
                    '''
                    An exception occurs, please contact the administrator!
                    '''
                )

        elif user_md5_count >= 2:
            return HttpResponse(
                '''
                Your account has been registered multiple times! Please contact the administrator.
                '''
            )
        else:
            return render(request, "404.html")

    def post(self, request, email):
        redis_user_md5 = get_redis_connection("user_md5")
        print("1111111111111111111111111111111111111111111")
        md5 = redis_user_md5.get(email)
        print(md5)
        print("222222222222222222222222222222222222222222222222222")
        email = request.POST.get("email")
        new_password = request.POST.get("new_password")
        if not re.match(r"^\w{6,32}$", new_password):
            response = render(request, "reset.html", )
            reset_mas="Password format is wrong!"
            response.set_cookie("reset_mas", reset_mas)
            return response
        if md5 is not None:
            try:
                user_md5 = UserMD5.objects.get(Q(user_md5=md5) & Q(email=email))
                print(user_md5.email)
                print(user_md5.user_md5)
                user_old = MyUser.objects.get(Q(email=email))
                print(user_old.password)
                user_old.set_password(new_password)
                user_old.save()
                user_new = MyUser.objects.get(Q(email=email))
                dic = {"username": user_new.username, "password": user_new.password, "email": user_new.email}
                print(user_new.password)
                m = hashlib.md5()
                print(repr(dic))
                m.update(repr(dic).encode("utf_8"))
                user_md5.user_md5 = m.hexdigest()
                print(m.hexdigest())
                user_md5.save()
                login_mas = "Password reset complete!"
                response = redirect("http://127.0.0.1:8000/login/")
                response.set_cookie("login_mas", login_mas)
                return response
            except Exception as e:
                print(e)
                return HttpResponse(
                    """An exception occurred during the password modification process!
                    Solution: Go back to the
                    forgotten password page to verify the email and then perform this operation.
                    Reason analysis:
                    1. The email address you filled in the forget password page does not match the email address you
                    submitted now.
                    2. After you have changed your password, you directly change your password again
                    without performing email verification on the Forgot Password page. """
                )
        else:
            return HttpResponse(
                '''
                Before changing your password, you should perform email verification on the Forgot Password page.
                '''
            )



