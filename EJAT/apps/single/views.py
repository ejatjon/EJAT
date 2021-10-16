from django.shortcuts import render
from django.views import View
from index.models import Article, Reply, References, Reprint
from django.utils.translation import gettext as _


# Create your views here.



class Single(View):
    def get(self,request,article_id):
        article=Article.objects.get(id=article_id)
        reply=Reply.objects.filter(article=article)
        references=References.objects.filter(article=article)
        reprint=Reprint.objects.filter(article=article)
        from django.conf import settings
        from django.http import HttpResponse
        from django.utils import translation
        user_language = 'ug'
        translation.activate(user_language)
        response = render(request, "single.html", locals())
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)

        _("hello world")
        # with open(r"D:\网上下载的软件\text\text_set.txt","r",encoding="utf-8") as f:
        #     a=eval(f.read())
        #     for i in a:
        #         with open("text.py","a",encoding="utf-8") as t:
        #             t.write('_(r"{}")\n'.format(i))

        return response

    def post(self,request):
        pass

