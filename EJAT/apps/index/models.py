from django.contrib.auth.validators import UnicodeUsernameValidator
from tinymce.models import HTMLField
from django.db import models
from register.models import MyUser


# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=120, db_index=True)

    class Meta:
        index_together = ["name"]


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    index = models.IntegerField(default=999)

    class Meta:
        index_together = ["name"]


class Article_htmlField(models.Model):
    article_html = HTMLField()

class Article_excerpt(models.Model):
    article_excerpt=models.TextField(blank=False, null=False, db_index=True)



class Article(models.Model):
    id = models.AutoField(primary_key=True)

    # author_user_id = models.IntegerField()
    author_user = models.ForeignKey(MyUser, db_index=True, on_delete=models.CASCADE)
    Show_picture = models.URLField()
    # author_name = models.CharField(max_length=150)
    title = models.CharField(max_length=200, db_index=True)
    excerpt = models.OneToOneField(Article_excerpt,on_delete=models.CASCADE)
    # excerpt=models.CharField(max_length=383,db_index=True)
    tag = models.ManyToManyField(Tag, blank=True)
    category = models.ManyToManyField(Category, blank=True, db_index=True)
    is_reprint = models.BooleanField()
    # reprint = models.ForeignKey(Reprint, on_delete=models.DO_NOTHING, blank=True, null=True)
    # references = models.ForeignKey(References, on_delete=models.DO_NOTHING, blank=True, null=True)
    article = models.OneToOneField(Article_htmlField, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True, db_index=True)
    Likes_num = models.PositiveIntegerField(default=0)
    Forwarded = models.PositiveIntegerField(default=0)
    reply_num = models.PositiveIntegerField(default=0)
    # reply = models.ForeignKey(Reply, on_delete=models.DO_NOTHING, blank=True, null=True)
    views_num = models.PositiveIntegerField(default=0)
    collect_num = models.PositiveIntegerField(default=0)

    # , "tag", "category""id",, "author_name"  , "excerpt"
    class Meta:
        index_together = ["author_user", "title", "creation_time",
                          "Likes_num", "Forwarded"]
        ordering = ['id']


class UserArticleData(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    class Meta:
        index_together = ["id", "article", "user"]
        ordering = ['id']


class Views(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        index_together = ["id", "user", "article", "creation_time", "modified_time"]
        ordering = ['id']


class Likes(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = ["id", "user", "article", "creation_time"]
        ordering = ['id']


class Collect(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = ["id", "user", "article", "creation_time"]
        ordering = ['id']


class Reprint(models.Model):
    reprint_id = models.AutoField(primary_key=True)
    reprint_mas = models.CharField(max_length=120)
    reprint_link = models.URLField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        index_together = ["reprint_id", "article"]
        ordering = ['reprint_id']


class References(models.Model):
    references_id = models.AutoField(primary_key=True)
    references_name = models.CharField(max_length=120)
    references_link = models.URLField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        index_together = ["references_id", "article"]
        ordering = ['references_id']


class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    # from_user_id = models.IntegerField(verbose_name="from_user_id")
    # to_user_id = models.IntegerField(verbose_name="to_user_id")
    to_reply_id = models.IntegerField(verbose_name="to_reply_id")
    from_user = models.ForeignKey(MyUser, models.CASCADE, related_name="reply_from_user")
    to_user = models.ForeignKey(MyUser, models.CASCADE, related_name="reply_to_user")
    reply = HTMLField(verbose_name="reply")
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    creation_time = models.DateTimeField('creation_time', auto_now_add=True, blank=False, null=False)

    # "from_user_id","reply_id","to_user_id" ,
    class Meta:
        index_together = ["to_reply_id", "article", "creation_time",
                          "from_user", "to_user"]
        ordering = ['reply_id']
