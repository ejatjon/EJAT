from celery import shared_task
import tinify
from django.forms import model_to_dict
from tinymce_upload.models import TinymceDocumentSummary
from contact.models import TinifyResult,TinifyException
from EJAT.settings.dav import TINYPNG_KEY

@shared_task
def tinypng_condense(MD5):
    try:
        image_database_entity = TinymceDocumentSummary.objects.get(file_md5=MD5)
        print("=====================================================",model_to_dict(image_database_entity))
        image_path=image_database_entity.file_path
        print(image_path)
        tinify.key = TINYPNG_KEY
        source = tinify.from_file(image_path)
        source.to_file(image_path)
        print("ok!!!")
        TinifyResult.objects.create(path=image_path,masage="succeed").save()
        image_database_entity.delete()
        print("returned")
        return

    except Exception as e:
        TinifyResult.objects.create(path="Exception", masage=e).save()
        TinifyException.objects.create(path="Exception", Exception=e).save()
        print("returned")
        return
