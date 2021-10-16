import random
import time

import django_redis
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from index.models import Article


class Categore(View):
    def get(self,request):
        category_name=request.GET.get('category_name','网络攻击')
        page_num=request.GET.get('page',1)
        lists=Article.objects.filter(category__name=category_name)
        print(lists)
        new_article=[]
        time1=time.time()
        redis_conn = django_redis.get_redis_connection("index_page_cache")
        datas = redis_conn.get("headlines")
        if not (datas == None or datas == "" or datas == " "):
            try:
                datas = eval(datas)
                head = random.sample(datas, 8)
                for i in head:
                    artcle = Article.objects.get(id=i["id"])
                    new_article.append(artcle)
            except Exception as e:
                print("headlines", e)
        else:
            try:
                datas = Article.objects.order_by("-id", "-Likes_num")[:100]
                head = random.sample(list(datas), 8)
                for i in head:
                    new_article.append(i)
            except Exception as e:
                print("headlines", e)
        paginator = Paginator(lists, 8)  # 对查询到的数据对象list进行分页，设置超过5条数据就分页
        print("time:",time1-time.time())
        try:
            lists = paginator.page(page_num)  # 获取当前页码的记录
        except PageNotAnInteger:
            lists = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            lists = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        return render(request, 'category.html', locals())
    def post(self,request):
        return HttpResponse("use get")
