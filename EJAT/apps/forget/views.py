from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django_redis import get_redis_connection
from EJAT.my_libs.verifications import get_verification
from forget.models import UserMD5
from register.models import MyUser
# Create your views here.

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
        print(email)
        user_count = MyUser.objects.filter(email=email).count()
        print(user_count)
        if user_count == 1:
            redis_conn = get_redis_connection("forgot_verification")
            print(redis_conn.keys("*"))
            redis_conn.delete(email)
            verification = get_verification()
            masage = '''
                <h2>your verification</h2>
                <br>
                <p>We have received your request to modify your password. If it is not your own operation, please contact the administrator of this site.</p>
                <br>
                <p> This is your verification code, the verification code will expire within 5 minutes, please fill in in time:</p>
                <h1>         %s</h1>
                <h3>                EJAT Service Center.</h3>
            ''' % verification

            redis_conn.set(email, verification, 300)
            print(redis_conn.keys("*"))
            send_mail("verification", message="", from_email="ejatjonamar@outlook.com", recipient_list=[email],
                      fail_silently=False, html_message=masage
                      )

            return HttpResponse(1)
        elif user_count>=1:
            return HttpResponse(
                '''
                This mailbox has multiple users registered.This is not allowed, so you can't do this.
                Please contact the administrator to retrieve your password.
                This website only wants to know about this bug.
                '''
            )
        else:
            return HttpResponse(
                '''
                This operation cannot be performed if the email address you entered has not been registered yet!
                '''
            )
    else:
        return render(request, "404.html")


class ForgotPassword(View):
    def get(self, request):
        return render(request, "forgot.html")

    def post(self, request):
        email = request.POST.get("email")
        verification = request.POST.get("emailverification")
        try:
            redis_conn_forgot = get_redis_connection("forgot_verification")
            verification_cont = redis_conn_forgot.get(email)
            if str(verification_cont) == verification:
                try:
                    user_md5 = UserMD5.objects.get(email=email).user_md5
                    redis_conn_user_md5 = get_redis_connection("user_md5")
                    redis_conn_user_md5.set(email,user_md5,300)
                    return redirect("/reset/%s"%email)
                except Exception as e:
                    print(e)
                    return HttpResponse(
                        '''
                        It seems that your email is not registered, so you can't perform this operation!
                        If you are sure that you have already registered, please contact the administrator or try again.
                        '''
                    )
            else:
                return HttpResponse(
                    '''
                    The verification code you filled in is inaccurate or has expired!
                    The reasons for this result are:
                     1. You filled in the wrong email verification code.
                     2. The verification code you filled out has expired and was deleted by the system.
                     3. If you click the button to send the verification code multiple times,
                     the system only keeps the verification code sent last, and you did not receive the correct verification code.
                    '''
                )
        except Exception as e:
            return HttpResponse(
                '''
                Your email address does not exist in the database, so this operation cannot be performed!
                If you have already registered, please try again.
                If you can't solve it, please contact the administrator
                '''
            )
