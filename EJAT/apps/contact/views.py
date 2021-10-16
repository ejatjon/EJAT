from django.http import HttpResponse
from django.shortcuts import render
from tinymce_upload.models import TinymceDocumentSummary

# Create your views here.
from django.views import View

from contact.models import TinifyException, TinifyResult,Contact




class Contacts(View):

    def get(self,request):
        TinymceDocumentSummary.objects.all().delete()
        TinifyResult.objects.all().delete()
        TinifyException.objects.all().delete()
        return render(request,"contact.html")

    def post(self,request):
        name=request.POST.get("name")
        email=request.POST.get("email")
        subject=request.POST.get("subject")
        message=request.POST.get("message")
        print(name,email,subject,message)
        return HttpResponse("ok")
