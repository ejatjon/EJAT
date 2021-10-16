from django.db import models

# Create your models here.
class TinymceDocumentSummary(models.Model):
    file_path=models.FilePathField()
    file_url=models.URLField()
    file_md5=models.CharField(max_length=32,primary_key=True)