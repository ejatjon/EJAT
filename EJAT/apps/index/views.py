import datetime
import json
import random
import numpy as np
import time
from collections import Counter

import django_redis
from django.core import serializers
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from register.models import MyUser, UserData,Fans
from index.models import References, Reprint, Article, Tag, Category, UserArticleData, Reply, Article_htmlField,Article_excerpt

# Create your views here.
# from EJAT.apps.index.tasks import CourseTask


import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events

# print('django-apscheduler')


# def job2(name):
#     # 具体要执行的代码
#     print('{} 任务运行成功！{}'.format(name, time.strftime("%Y-%m-%d %H:%M:%S")))


# 实例化调度器

scheduler = BackgroundScheduler()
# 调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")
#
#
# 添加任务1
# 每隔5s执行这个任务
@register_job(scheduler, "cron", second=30, id='index_page_cache9')
def index_page_cache():
    print("开始了")
    try:
        t1=time.time()
        data=Article.objects.order_by("-creation_time","-Likes_num")[:100]
        headlines = []
        for i in data:
            try:
                article=model_to_dict(i)
                data={"id":article["id"]}
                headlines.append(data)
            except Exception as e:
                print(e)
        t2=time.time()
        hot_tags =Counter(list(Tag.objects.values_list("name", flat=True))).most_common(1000) # flat可以返回一个列表，不然默认返回一个元组
        t3=time.time()
        hot_articles = []
        data=Article.objects.all().order_by("-views_num", "-creation_time")[0:1001]
        for i in data:
            try:
                article=model_to_dict(i)
                data = {"id": article["id"]}
                hot_articles.append(data)
            except Exception as e:
                print(e)
        t4=time.time()
        anoder_news = []
        data=Article.objects.order_by("-Likes_num", "-reply_num", "-collect_num", "-views_num")[0:1000]
        for i in data:
            try:
                article=model_to_dict(i)
                data = {"id": article["id"]}
                anoder_news.append(data)
            except Exception as e:
                print(e)
        t5=time.time()
        bast_of_the_week = []
        data=Article.objects.order_by("-creation_time", "-Likes_num", "-collect_num", "Forwarded")[0:1000]
        for i in data:
            try:
                article = model_to_dict(i)
                data = {"id": article["id"]}
                bast_of_the_week.append(data)
            except Exception as e:
                print(e)
        t6=time.time()
        recommend=[]
        data=Article.objects.order_by("-Likes_num", "-collect_num", "Forwarded")[0:1000]
        for i in data:
            try:
                article = model_to_dict(i)
                data = {"id": article["id"]}
                recommend.append(data)
            except Exception as e:
                print(e)
        bast_authors=[]
        author_list=Article.objects.order_by("-Likes_num").values("author_user").distinct()
        try:
            if len(author_list)==1:
                user=MyUser.objects.get(id=author_list[0]["author_user"])
                userdata=model_to_dict(UserData.objects.get(user=user))
                userdata={"id":userdata["id"],"user":userdata["user"]}
                bast_authors.append(userdata)
            elif len(author_list)>=1:
                for i in author_list:
                    user = MyUser.objects.get(id=i["author_user"])
                    userdata = model_to_dict(UserData.objects.get(user=user))
                    userdata = {"id": userdata["id"], "user": userdata["user"]}
                    bast_authors.append(userdata)
            else:
                print("index_page_cache Exception ")
        except Exception as e:
            print(e)
        t7=time.time()
        redis_conn=django_redis.get_redis_connection("index_page_cache")
        redis_conn.delete("headlines")
        redis_conn.set("headlines",str(headlines),120)
        redis_conn.delete("hot_tags")
        redis_conn.set("hot_tags", str(hot_tags), 120)
        redis_conn.delete("hot_articles")
        redis_conn.set("hot_articles",str(hot_articles),120)
        redis_conn.delete("anoder_news")
        redis_conn.set("anoder_news",str(anoder_news),120)
        redis_conn.delete("bast_of_the_week")
        redis_conn.set("bast_of_the_week", str(bast_of_the_week), 120)
        redis_conn.delete("bast_authors")
        redis_conn.set("bast_authors", str(bast_authors), 120)
        redis_conn.delete("recommend")
        redis_conn.set("recommend", str(recommend), 120)

        t8=time.time()
        print(t8-t7)
        return 'ok'
    except Exception as e:
        print("错误是这个：",e)
# #
# #     # headlines = []#头条文章标题
# #     # latest = []#头条文章
# #     # sta1 = time.time()
# #     # a = Article.objects.order_by("-id")[:1000]
# #     # # # 2. 根据 点赞数 进行排序
# #     # a = sorted(a, key=lambda item: item.Likes_num)[0:100]
# #     # head = random.sample(list(a), 5)
# #     # sta2 = time.time()
# #     # print("1.%s" % (sta2 - sta1))
# #     # for i in head:
# #     #     headlines.append(i)
# #     # sta3 = time.time()
# #     # print("2.%s" % (sta3 - sta2))
# #     # print(headlines)
# #     # for i in random.sample(a, 4):
# #     #     latest.append(i)
# #     # sta4 = time.time()
# #     # print("3.%s" % (sta4 - sta3))
# #     # hot_tags = []
# #     # t = Tag.objects.values_list("name", flat=True)  # flat可以返回一个列表，不然默认返回一个元组
# #     # print(t)
# #     # tt = Counter(t).most_common(100)  # 进行排序 返回前100位
# #     # for i in random.sample(tt, 10):
# #     #     hot_tags.append(i)
# #     # sta5 = time.time()
# #     # print(hot_tags)
# #     # print("4.%s" % (sta5 - sta4))
# #     # hot_nwes = []
# #     # #
# #     # n = list(Article.objects.all().order_by("-views_num", "-creation_time")[0:1001])
# #     # print(n)
# #     # # print([i.title for i in n])
# #     # sta6 = time.time()
# #     # print("5.%s" % (sta6 - sta5))
# #     # # n=Counter()
# #     # hot_nwes=random.sample(n, 100)
# #     # sta7 = time.time()
# #     # print("6.%s" % (sta7 - sta6))
# #
# #
# # # scheduler.add_job(job2, "interval", seconds=2, args=['王飞'], id="job7")
# #
# #
# # 监控任务
# # register_events(scheduler)
# a = scheduler.get_jobs()
# print(a)
# # 调度器开始运行
scheduler.start()

#


@csrf_exempt
def insertData(request):
#     # text=Tag.objects.filter(name__contains="武漢")
#     # # datas=text.first().article_set.all()
#     # # print(datas)
#     # print([i.name for i in text])
#     # ok=0
#     # for i in [i for i in text]:
#     #     try:
#     #         i.delete()
#     #         print(i.name)
#     #         ok+=1
#     #         print(ok)
#     #     except Exception as e:
#     #         print(e)
#     # text = Tag.objects.filter(name__contains="武漢")
#     # print([i.name for i in text])
#     # print(len(text))
#     # headlines = []
#     # latest = []
#     # sta1 = time.time()
#     # redis_conn=django_redis.get_redis_connection("index_page_cache")
#     # datas=redis_conn.get("headlines")
#     # if not(datas==None or datas=="" or datas==" "):
#     #     try:
#     #         datas=eval(datas)
#     #         head = random.sample(datas, 5)
#     #         sta2 = time.time()
#     #         print("1.%s" % (sta2 - sta1))
#     #         for i in head:
#     #             artcle=Article.objects.get(id=i["id"])
#     #             headlines.append(artcle)
#     #         sta3 = time.time()
#     #         print("2.%s" % (sta3 - sta2))
#     #         for i in random.sample(datas, 4):
#     #             artcle=Article.objects.get(id=i["id"])
#     #             latest.append(artcle)
#     #         sta4 = time.time()
#     #         print("3.%s" % (sta4 - sta3))
#     #     except Exception as e:
#     #         sta4 = time.time()
#     #         print("headlines",e)
#     # else:
#     #     try:
#     #         datas = Article.objects.order_by("-id","_Likes_num")[:100]
#     #         # # 2. 根据 pub_date 进行排序
#     #         head = random.sample(list(datas), 5)
#     #         sta2 = time.time()
#     #         print("1.%s" % (sta2 - sta1))
#     #         for i in head:
#     #             headlines.append(i)
#     #         sta3 = time.time()
#     #         print("2.%s" % (sta3 - sta2))
#     #         # print(headlines)
#     #         for i in random.sample(datas, 4):
#     #             latest.append(i)
#     #         sta4 = time.time()
#     #         print("3.%s" % (sta4 - sta3))
#     #     except Exception as e:
#     #         sta4 = time.time()
#     #         print("headlines",e)
#     # hot_tags = []
#     # datas=redis_conn.get("hot_tags")
#     # if not (datas==None or datas=="" or datas==" "):
#     #     try:
#     #         datas=eval(datas)
#     #         hot_tags=random.sample(datas, 10)
#     #         sta5 = time.time()
#     #         print("4.%s" % (sta5 - sta4))
#     #     except Exception as e:
#     #         sta5 = time.time()
#     #         print("hot_tags",e)
#     # else:
#     #     try:
#     #         datas = Tag.objects.values_list("name", flat=True)
#     #         # print(list(t))
#     #         datas = Counter(list(datas)).most_common(100)
#     #         # print("$$$$$$$$$$",datas)
#     #         for i in random.sample(datas, 10):
#     #             hot_tags.append(i[0])
#     #         sta5 = time.time()
#     #         print(hot_tags)
#     #         print("4.%s" % (sta5 - sta4))
#     #     except Exception as e:
#     #         sta5 = time.time()
#     #         print("hot_tags else",e)
#     # hot_nwes = []
#     # datas=redis_conn.get("hot_articles")
#     # if not (datas==None or datas=="" or datas==" "):
#     #     try:
#     #         datas=eval(datas)
#     #         for i in random.sample(datas, 100):
#     #             artcle=Article.objects.get(id=i["id"])
#     #             hot_nwes.append(artcle)
#     #         sta6 = time.time()
#     #         print("5.%s" % (sta6 - sta5))
#     #     except Exception as e:
#     #         sta6 = time.time()
#     #         print("hot_news",e)
#     # else:
#     #     try:
#     #         datas = Article.objects.all().order_by("-creation_time", "-views_num")[0:1001]
#     #         # print("HOT_NEWS",[i.title for i in datas])
#     #         sta6 = time.time()
#     #         print("5.%s" % (sta6 - sta5))
#     #         # n=Counter()
#     #         for i in random.sample(list(datas), 100):
#     #             hot_nwes.append(i)
#     #         sta7 = time.time()
#     #         print("6.%s" % (sta7 - sta6))
#     #     except Exception as e:
#     #         sta6 = time.time()
#     #         print("hot_news",e)
#     # anoder_news = []
#     # datas=redis_conn.get("anoder_news")
#     # if not (datas==None or datas=="" or datas==" "):
#     #     try:
#     #         datas=eval(datas)
#     #         news = np.random.choice(datas,size=6)
#     #         for i in news:
#     #             artcle = Article.objects.get(id=i["id"])
#     #             anoder_news.append(artcle)
#     #         sta7=time.time()
#     #         print("anoder:%s"%(sta7-sta6))
#     #     except Exception as e:
#     #         sta7=time.time()
#     #         print("anoder_news",e)
#     # else:
#     #     try:
#     #
#     #         datas = Article.objects.order_by("-Likes_num", "-reply_num", "-collect_num", "-views_num")[0:1000]
#     #         anoder_news = random.sample(list(datas), 6)
#     #         sta7=time.time()
#     #
#     #     except Exception as e:
#     #         sta7=time.time()
#     #
#     #         print("anoder_news else",e)
#     # bast_of_the_week = []
#     # datas=redis_conn.get("bast_of_the_week")
#     # if not (datas==None or datas=="" or datas==" "):
#     #     try:
#     #         datas=eval(datas)
#     #         bests=random.sample(datas, 4)
#     #         for i in bests:
#     #             artcle=Article.objects.get(id=i["id"])
#     #             bast_of_the_week.append(artcle)
#     #         sta8=time.time()
#     #         print(sta8-sta7)
#     #     except Exception as e:
#     #         sta8=time.time()
#     #
#     #         print("bw",e)
#     # else:
#     #     try:
#     #         datas = Article.objects.order_by("-creation_time", "-Likes_num", "-collect_num", "Forwarded")[0:1000]
#     #         for i in random.sample(datas, 4):
#     #             bast_of_the_week.append(i)
#     #         # print("@@@@@@@@@@@@@@@@@@@@",bast_of_the_week)
#     #         sta8=time.time()
#     #
#     #
#     #     except Exception as e:
#     #         sta8=time.time()
#     #
#     #         print("bw else",e)
#     # bast_author = []
#     # datas = redis_conn.get("bast_authors")
#     # if not (datas==None or datas=="" or datas==" "):
#     #     try:
#     #         datas=eval(datas)
#     #         if len(list(datas)) == 1:
#     #             author= MyUser.objects.get(id=datas[0]["user"])
#     #             author_data = UserData.objects.get(user=author)
#     #             datas={"author":author,"author_data":author_data}
#     #             bast_author.append(datas)
#     #         else:
#     #             datas=random.sample(datas, 1)
#     #             author=MyUser.objects.get(id=datas[0]["id"])
#     #             author_data = UserData.objects.get(user=author)
#     #             datas = {"author": author, "author_data": author_data}
#     #             bast_author.append(datas)
#     #         sta9 = time.time()
#     #         print(sta9 - sta8)
#     #     except Exception as e:
#     #         sta9 = time.time()
#     #
#     #         print("author",e)
#     # else:
#     #     sta9 = time.time()
#     #
#     #     datas = Article.objects.order_by("-Likes_num").values("author_user").distinct()
#     #     try:
#     #         if len(datas) == 1:
#     #             author = MyUser.objects.get(id=datas[0]["author_user"])
#     #             author_data = UserData.objects.get(user=author)
#     #             datas = {"author": author, "author_data": author_data}
#     #             bast_author.append(datas)
#     #         elif len(datas) >= 1:
#     #             for i in datas:
#     #                 author = MyUser.objects.get(id=i["author_user"])
#     #                 author_data = UserData.objects.get(user=author)
#     #                 datas = {"author": author, "author_data": author_data}
#     #                 bast_author.append(datas)
#     #         else:
#     #             print("index_page_cache Exception ")
#     #     except Exception as e:
#     #         print("author else",e)
#     # popular = []
#     # datas=redis_conn.get("bast_of_the_week")
#     # if not (datas==None or datas=="" or datas==" "):
#     #     try:
#     #         po=random.sample(eval(datas), 6)
#     #         for i in po:
#     #             artcle = Article.objects.get(id=i["id"])
#     #             popular.append(artcle)
#     #         sta10=time.time()
#     #         print(sta10-sta9)
#     #     except Exception as e:
#     #         sta10=time.time()
#     #         print("popular",e)
#     # else:
#     #     sta10 = time.time()
#     #     try:
#     #         datas = Article.objects.order_by("-creation_time", "-Likes_num", "-collect_num", "Forwarded")[0:1000]
#     #         for i in random.sample(list(datas), 6):
#     #             popular.append(i)
#     #     except Exception as e:
#     #         print("popular else",e)
#     #
#     # tui = []
#     # datas=redis_conn.get("recommend")
#     # if not (datas==None or datas=="" or datas==" "):
#     #     try:
#     #         tu=random.sample(eval(datas), 4)
#     #         for i in tu:
#     #             artcle = Article.objects.get(id=i["id"])
#     #             tui.append(artcle)
#     #         print("tui:%s"%(time.time()-sta10))
#     #     except Exception as e:
#     #         print("tui",e)
#     # else:
#     #     try:
#     #         datas = [
#     #             [model_to_dict(i) for i in Article.objects.order_by("-Likes_num", "-collect_num", "Forwarded")[0:1000]]]
#     #         for i in random.sample(datas, 4):
#     #             tui.append(i)
#     #         sta5=time.time()
#     #         print("%s"%(sta5-sta4))
#     #     except Exception as e:
#     #         print("tui else",e)
#     # context = {
#     #     "headlines": headlines,
#     #     "latest": latest,
#     #     "hot_tags": hot_tags,
#     #     "hot_nwes": hot_nwes,
#     #     "anoder_news": anoder_news,
#     #     "bast_of_the_week": bast_of_the_week,
#     #     "bast_author": bast_author,
#     #     "popular": popular,
#     #     "tui": tui
#     # }
#     # print(context)
#     # print(time.time()-sta1)
#
#     # 添加文章的用户数据

    with open(r"D:\网上下载的软件\EJAT\EJAT\my_libs\new_Hacker_News_artical_list", "r", encoding="utf-8") as f:
        lists = eval(f.read())
    # Reprint.objects.all().delete()
    # References.objects.all().delete()
    # Article.objects.all().delete()
    # Tag.objects.all().delete()
    # Category.objects.all().delete()
    for list in lists:
        # print(list)
        user=MyUser.objects.get(username="ejatjon")
        # user_id=user.id
        # print(user_id)
        author_name=list[2][0]
        # print(author_name)
        title=list[1][0]
        # print(title)
        """
        对内容进行截取可以提高数据库性能
        """
        # excerpt=str(list[7][0]).split("。",1)[0]
        # if int(len(excerpt)) > 383:
        #     print("so loog")
        #     excerpt=excerpt[0:383]
        # print(excerpt)
        """
        但是我想把内容全部都加进去
        """
        excerpt = Article_excerpt.objects.create(article_excerpt=str(list[-2][0]))
        excerpt.save()
        tags=list[3][0]
        # print(tags)
        categorys=list[8][0]
        # print(categorys)
        is_reprint=True
        references=list[4]
        article=list[5]
        article=Article_htmlField.objects.create(article_html=article)
        article.save()
        Show_picture=list[6][0]
        print(Show_picture)

        # author_name=author_name,
        # article_object=Article.objects.create(author_user_id=user_id,author_name=author_name,title=title,excerpt=excerpt,is_reprint=is_reprint,article=article)
        article_object=Article.objects.create(author_user=user,Show_picture=Show_picture,title=title,excerpt=excerpt,is_reprint=is_reprint,article=article)

        for tag in tags:
            # print(str(tag))
            datas=Tag.objects.create(name=str(tag))
            datas.save()
            article_object.tag.add(datas)
        for c in categorys:
            # print(str(c))
            category=Category.objects.create(name=str(c))
            category.save()
            article_object.category.add(category)
        try:
            re=References.objects.create(references_name=str(references[1][0]),references_link=str(references[0][0]),article=article_object)
        except Exception as e:
            print(e)
            re=References.objects.create(references_name="Hacker News",references_link=list[0],article=article_object)

        r=Reprint.objects.create(reprint_mas="Hacker News",reprint_link=list[0],article=article_object)
        re.save()
        r.save()
        article_object.save()
        user_article_data=UserArticleData.objects.create(article=article_object,user=user)
        user_article_data.save()


    print(lists[0])


    #
    # with open("EJAT/my_libs/new_pansci_artical_list01.txt", "r", encoding="utf-8") as f:
    #     lists = eval(f.read())
    # with open("C:\\Users\\ejatjon\Desktop\\artical_data", "r", encoding="utf-8") as f:
    #     dicts = eval(f.read())
    # num=0
    # error=0
    # for list in lists:
    #     url = list[0]
    #     title = dicts[url]['title']
    #     Show_picture = dicts[url]["image"]
    #     print(Show_picture)
    #     # print(title)
    #     user = MyUser.objects.get(username="ejatjon")
    #     # user_id = user.id
    #     author_name = list[1][0]
    #     # print(author_name)
    #     """
    #     对内容进行截取可以提高数据库性能
    #     """
    #     # excerpt = str(list[-3])
    #     # if int(len(excerpt)) > 383:
    #     #     print("so loog")
    #     #     excerpt=excerpt[0:383]
    #     # # print(excerpt)
    #     """
    #     但是我想把内容全部都加进去
    #     """
    #     excerpt = Article_excerpt.objects.create(article_excerpt=str(list[-5]))
    #     excerpt.save()
    #     tags = list[-1]
    #     # print(tags)
    #     # print(list[-2])
    #     is_reprint = True
    #     references = list[2]
    #     try:
    #         article=Article_htmlField.objects.create(article_html=list[3])
    #     except Exception:
    #         error+=1
    #         print(error)
    #         continue
    #     article.save()
    #     excerpt.save()
    #     try:
    #         # article_object = Article.objects.create(author_user_id=user_id, author_name=author_name, title=title,
    #         #                                         excerpt=excerpt, is_reprint=is_reprint, article=article)
    #         #                                         , author_name=author_name
    #         article_object = Article.objects.create(author_user=user, Show_picture=Show_picture, title=title,
    #                                                 excerpt=excerpt, is_reprint=is_reprint, article=article)
    #         for tag in tags:
    #             # print(str(tag[0]))
    #             try:
    #                 datas = Tag.objects.create(name=str(tag[0]))
    #                 datas.save()
    #                 article_object.tag.add(datas)
    #             except Exception as e:
    #                 print("error"+str(e))
    #
    #         category = Category.objects.create(name=str(list[-2]))
    #         category.save()
    #         article_object.category.add(category)
    #         try:
    #             for r in references:
    #                 # print(str(r))
    #                 ref = References.objects.create(references_name=str(r[0][0]),
    #                                                references_link=str(r[1][0]), article=article_object)
    #                 ref.save()
    #
    #
    #
    #         except Exception as e:
    #             print("******************************************************************************************")
    #             print(e)
    #             print("********************************************************************************************")
    #             try:
    #                 for r in references:
    #                     print(str(r))
    #                     ref = References.objects.create(references_name=str(references[0][0]),
    #                                                    references_link=str(url), article=article_object)
    #                     ref.save()
    #             except Exception as e:
    #                 print("#######################################################################################")
    #                 print(e)
    #                 print("###########################################################################################")
    #                 ref = References.objects.create(references_name="Pansci asia", references_link=list[0],
    #                                                article=article_object)
    #                 ref.save()
    #         r = Reprint.objects.create(reprint_mas="Pansci asia", reprint_link=list[0], article=article_object)
    #         r.save()
    #         article_object.save()
    #         user_article_data = UserArticleData.objects.create(article=article_object, user=user)
    #         user_article_data.save()
    #         print('fuck:'+str(num))
    #     except Exception as e:
    #         print(e)
    #         num+=1
    return HttpResponse("ok")
#

class Index(View):
    def get(self, request, user_name=None):
        if user_name==None:
            response = redirect('http://127.0.0.1:8000/')
            return response
        redis = django_redis.get_redis_connection("is_login")
        is_login = redis.get(user_name)
        # print(is_login)
        if is_login == "true":
            headlines = []
            latest = []
            sta1 = time.time()
            redis_conn = django_redis.get_redis_connection("index_page_cache")
            datas = redis_conn.get("headlines")
            if not (datas == None or datas == "" or datas == " "):
                try:
                    datas = eval(datas)
                    head = random.sample(datas, 10)
                    sta2 = time.time()
                    print("1.%s" % (sta2 - sta1))
                    for i in head:
                        artcle = Article.objects.get(id=i["id"])
                        headlines.append(artcle)
                    sta3 = time.time()
                    print("2.%s" % (sta3 - sta2))
                    for i in random.sample(datas, 4):
                        artcle = Article.objects.get(id=i["id"])
                        latest.append(artcle)
                    sta4 = time.time()
                    print("3.%s" % (sta4 - sta3))
                except Exception as e:
                    sta4 = time.time()
                    print("headlines", e)
            else:
                try:
                    datas = Article.objects.order_by("-id", "-Likes_num")[:100]
                    # # 2. 根据 pub_date 进行排序
                    head = random.sample(list(datas), 10)
                    sta2 = time.time()
                    # print("1.%s" % (sta2 - sta1))
                    for i in head:
                        headlines.append(i)
                    sta3 = time.time()
                    # print("2.%s" % (sta3 - sta2))
                    # print(headlines)
                    for i in random.sample(list(datas), 4):
                        latest.append(i)
                    sta4 = time.time()
                    # print("3.%s" % (sta4 - sta3))
                except Exception as e:
                    sta4 = time.time()
                    print("headlines", e)
            hot_tags = []
            datas = redis_conn.get("hot_tags")
            if not (datas == None or datas == "" or datas == " "):
                try:
                    datas = eval(datas)
                    hot_tags = random.sample(datas, 10)
                    sta5 = time.time()
                    # print("4.%s" % (sta5 - sta4))
                except Exception as e:
                    sta5 = time.time()
                    print("hot_tags", e)
            else:
                try:
                    datas = Tag.objects.values_list("name", flat=True)
                    # print(list(t))
                    datas = Counter(list(datas)).most_common(100)
                    # print("$$$$$$$$$$",datas)
                    for i in random.sample(datas, 10):
                        hot_tags.append(i[0])
                    sta5 = time.time()
                    print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJj")
                    print(hot_tags)
                    print("4.%s" % (sta5 - sta4))
                except Exception as e:
                    sta5 = time.time()
                    print("hot_tags else", e)
            hot_nwes = []
            datas = redis_conn.get("hot_articles")
            if not (datas == None or datas == "" or datas == " "):
                try:
                    datas = eval(datas)
                    news=np.random.choice(datas, size=10)
                    for i in news:
                        aa=time.time()
                        artcle = Article.objects.get(id=i["id"])
                        hot_nwes.append(artcle)
                        print("aaa",time.time()-aa)
                    sta6 = time.time()
                    print("5.%s" % (sta6 - sta5))
                except Exception as e:
                    sta6 = time.time()
                    print("hot_news", e)
            else:
                try:
                    datas = Article.objects.all().order_by("-creation_time", "-views_num")[0:1001]
                    sta6 = time.time()
                    print("5.%s" % (sta6 - sta5))
                    for i in random.sample(list(datas), 100):
                        hot_nwes.append(i)
                    sta7 = time.time()
                    print("6.%s" % (sta7 - sta6))
                except Exception as e:
                    sta6 = time.time()
                    print("hot_news", e)
            anoder_news = []
            datas = redis_conn.get("anoder_news")
            if not (datas == None or datas == "" or datas == " "):
                try:
                    datas = eval(datas)

                    news = np.random.choice(datas, size=4)
                    for i in news:
                        artcle = Article.objects.get(id=i["id"])
                        anoder_news.append(artcle)
                    sta7 = time.time()
                    print("anoder:%s" % (sta7 - sta6))
                except Exception as e:
                    sta7 = time.time()
                    print("anoder_news", e)
            else:
                try:
                    datas = Article.objects.order_by("-Likes_num", "-reply_num", "-collect_num", "-views_num")[0:1000]
                    anoder_news = random.sample(list(datas), 4)
                    sta7 = time.time()
                except Exception as e:
                    sta7 = time.time()
                    print("anoder_news else", e)
            bast_of_the_week = []
            datas = redis_conn.get("bast_of_the_week")
            if not (datas == None or datas == "" or datas == " "):
                print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQqq")
                try:
                    datas = eval(datas)
                    bests = random.sample(datas, 6)
                    for i in bests:
                        artcle = Article.objects.get(id=i["id"])
                        bast_of_the_week.append(artcle)
                    sta8 = time.time()
                    print(sta8 - sta7)
                except Exception as e:
                    sta8 = time.time()
                    print("bw", e)
            else:
                try:
                    datas = Article.objects.order_by("-creation_time", "-Likes_num", "-collect_num", "Forwarded")[
                            0:1000]
                    bast_of_the_week=random.sample(list(datas), 6)
                    sta8 = time.time()
                except Exception as e:
                    sta8 = time.time()
                    print("bw else", e)
            bast_author = []
            datas = redis_conn.get("bast_authors")
            if not (datas == None or datas == "" or datas == " "):
                try:
                    datas = eval(datas)
                    if len(list(datas)) == 1:
                        author = MyUser.objects.get(id=datas[0]["user"])
                        author_data = UserData.objects.get(user=author)
                        Focus = str(Fans.objects.filter(to_user=author).count())
                        Posts = str(UserArticleData.objects.filter(user=author).count())
                        datas = {"author": author, "author_data": author_data, "Posts": Posts, "Focus": Focus}
                        print("wwwwwwwwwwwwwww",datas,"rrrrrrrrrrrrrrrrrrrrrr")

                        bast_author.append(datas)
                    else:
                        datas = random.sample(datas, 1)
                        author = MyUser.objects.get(id=datas[0]["id"])
                        author_data = UserData.objects.get(user=author)
                        Focus = str(Fans.objects.filter(to_user=author).count())
                        Posts = str(UserArticleData.objects.filter(user=author).count())
                        datas = {"author": author, "author_data": author_data,"Posts":Posts,"Focus":Focus}
                        print("wwwwwwwwwwwwwww",datas,"rrrrrrrrrrrrrrrrrrrrrr")
                        bast_author.append(datas)
                    sta9 = time.time()
                    print(sta9 - sta8)
                except Exception as e:
                    sta9 = time.time()
                    print("author", e)
            else:
                sta9 = time.time()
                datas = Article.objects.order_by("-Likes_num").values("author_user").distinct()
                try:
                    if len(datas) == 1:
                        author = MyUser.objects.get(id=datas[0]["author_user"])
                        author_data = UserData.objects.get(user=author)
                        Focus = str(Fans.objects.filter(to_user=author).count())
                        Posts = str(UserArticleData.objects.filter(user=author).count())
                        datas = {"author": author, "author_data": author_data, "Posts": Posts, "Focus": Focus}
                        print("wwwwwwwwwwwwwww",datas,"rrrrrrrrrrrrrrrrrrrrrr")
                        bast_author.append(datas)
                    elif len(datas) >= 1:
                        i=random.sample(list(datas),1)[0]
                        author = MyUser.objects.get(id=i["author_user"])
                        author_data = UserData.objects.get(user=author)
                        Focus = str(Fans.objects.filter(to_user=author).count())
                        Posts = str(UserArticleData.objects.filter(user=author).count())
                        datas = {"author": author, "author_data": author_data, "Posts": Posts, "Focus": Focus}
                        bast_author.append(datas)
                    else:
                        print("index_page_cache Exception ")
                except Exception as e:
                    print("author else", e)
            popular = []
            datas = redis_conn.get("bast_of_the_week")
            if not (datas == None or datas == "" or datas == " "):
                try:
                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa")
                    po = random.sample(eval(datas), 6)
                    for i in po:
                        artcle = Article.objects.get(id=i["id"])
                        popular.append(artcle)
                    sta10 = time.time()
                    print(sta10 - sta9)
                except Exception as e:
                    sta10 = time.time()
                    print("popular", e)
            else:
                sta10 = time.time()
                try:
                    print("ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
                    datas = Article.objects.order_by("-creation_time", "-Likes_num", "-collect_num", "Forwarded")[
                            0:1000]
                    popular=random.sample(list(datas), 6)
                except Exception as e:
                    print("popular else", e)
            tui = []
            datas = redis_conn.get("recommend")
            if not (datas == None or datas == "" or datas == " "):
                try:
                    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
                    tu = random.sample(eval(datas), 4)
                    for i in tu:
                        artcle = Article.objects.get(id=i["id"])
                        reply=Reply.objects.filter(article=artcle)
                        datas={"artcle":artcle,"reply":reply}
                        tui.append(datas)
                    print("tui:%s" % (time.time() - sta10))
                    print(tui)
                except Exception as e:
                    print("tui", e)
            else:
                try:
                    print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
                    datas = Article.objects.order_by("-Likes_num", "-collect_num", "Forwarded")[0:1000]
                    datas=random.sample(list(datas), 4)
                    for i in datas:
                        reply=Reply.objects.filter(article=i)
                        datas={"artcle":i,"reply":reply}
                        tui.append(datas)
                    sta5 = time.time()
                    print("%s" % (sta5 - sta4))
                except Exception as e:
                    print("tui else", e)
            context = {
                "headlines": headlines,
                "latest": latest,
                "hot_tags": hot_tags,
                "hot_nwes": hot_nwes,
                "anoder_news": anoder_news,
                "bast_of_the_week": bast_of_the_week,
                "bast_author": bast_author,
                "popular": popular,
                "tui": tui
            }
            print(time.time() - sta1)


            return render(request, "index.html", context=context)
        else:
            response = redirect('http://127.0.0.1:8000/login/')
            mas = "Login timed out, please log in again."
            response.set_cookie("login_mas", mas)
            return response

    def post(self, request, user_name):
        pass
