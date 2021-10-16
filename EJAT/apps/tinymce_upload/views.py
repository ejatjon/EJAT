import hashlib
import os
from functools import partial

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from register.models import MyUser,UserData
from tinymce_upload.models import TinymceDocumentSummary

from EJAT.apps.contact.tasks import tinypng_condense
from EJAT.settings import dav as settings


def md5(data, block_size=65536):
    # 创建md5对象
    m = hashlib.md5()
    # 对django中的文件对象进行迭代
    for item in data.chunks():
        # 把迭代后的bytes加入到md5对象中
        m.update(item)
    str_md5 = m.hexdigest()
    return str_md5


@csrf_exempt
def upload_image(request):
    print(request.path)
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "错误的文件格式"})
        MD5 = md5(file_obj)
        print(MD5)
        image_database_entity=TinymceDocumentSummary.objects.filter(file_md5=MD5)
        count=image_database_entity.count()
        print(count)
        if count==0:
            upload_time = timezone.now()
            path = os.path.join(
                settings.MEDIA_ROOT,
                'tinymce',
                'images',
                str(upload_time.year),
                str(upload_time.month),
                str(upload_time.day)
            )
            # 如果没有这个路径则创建
            if not os.path.exists(path):
                os.makedirs(path)

            file_path = os.path.join(path, MD5+"."+file_name_suffix)

            file_url = f'{settings.MEDIA_URL}tinymce/images/{upload_time.year}/{upload_time.month}/{upload_time.day}/{MD5}.{file_name_suffix}'
            print(file_url,file_path)
            with open(file_path, 'wb+') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            TinymceDocumentSummary.objects.create(file_md5=MD5, file_url=file_url, file_path=file_path).save()
            tinypng_condense.delay(MD5)
            return JsonResponse({
                'message': '上传图片成功',
                'location': file_url
            })
        else:
            file_url=image_database_entity[0].file_url
            print("okokkokokokokokokokokok")
            return JsonResponse({
                'message': '上传图片成功',
                'location': file_url
            })
    return JsonResponse({'detail': "错误的请求"})

