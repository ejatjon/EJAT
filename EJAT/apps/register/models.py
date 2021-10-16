from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class MyUser(AbstractUser):
    mobile_phone = models.CharField(verbose_name='mobile_phone', max_length=11, blank=True)

    class Meta:
        # 联合索引
        index_together = ["username", "email", "date_joined", "mobile_phone", "id", "last_login",
                          "first_name"]


class Images(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="user_data/moments/%Y/%m/%d")

    class Meta:
        index_together = ["id"]


class Moments(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    images = models.ManyToManyField(Images, blank=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    class Meta:
        index_together = ["id", "user"]


class Fans(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(MyUser, verbose_name="from_user", on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey(MyUser, verbose_name="to_user", on_delete=models.CASCADE, related_name="to_user")
    on_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = ["id", "from_user", "to_user", "on_time"]


class UserData(models.Model):
    sex = (("Male", "male"), ("female", "female"), ("unknown", "unknown"))
    lv = (("lv1", "lv1"), ("lv2", "lv2"), ("lv3", "lv3"), ("lv4", "lv4"), ("lv5", "lv5"), ("lv6", "lv6"))
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    images = models.ManyToManyField(Images, blank=True)
    introduce = models.TextField(blank=True)
    birthday = models.DateTimeField(blank=True, null=True)
    user_image = models.ImageField(upload_to='user_data/user_head_portrait/%Y/%m/%d',
                                     default="user_data/user_head_portrait/default.jpg")
    user_background_image=models.ImageField(upload_to='user_data/user_background_images/%Y/%m/%d',
                                     default="user_data/user_background_images/default.jpg")
    Country = models.CharField(max_length=120, blank=True)
    nationality = models.CharField(max_length=120, blank=True)
    mother_tongue = models.CharField(max_length=120, blank=True)
    language_learned_list = models.CharField(max_length=350, blank=True)
    company = models.CharField(max_length=220, blank=True)
    religion = models.CharField(max_length=220, blank=True)
    education = models.CharField(max_length=120, blank=True)
    gender = models.CharField(max_length=120, choices=sex, default="unknown")
    grade = models.CharField(max_length=120, choices=lv, default="lv1")
    points_earned = models.IntegerField(default=0)
    class Meta:
        index_together = ["nationality", "mother_tongue", "religion", "education",
                        "points_earned"]



class tinify_user_head_image_no_compression(models.Model):
    image=models.ImageField(null=False,blank=False)
    create_time=models.DateTimeField(auto_now_add=True)

class tinify_user_images_no_compression(models.Model):
    image=models.ImageField(null=False,blank=False)
    create_time=models.DateTimeField(auto_now_add=True)


