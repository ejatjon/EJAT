import random
import time
from collections import Counter
import django_redis
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from forget.models import UserMD5
from register.models import MyUser,Fans, UserData
from index.models import Reply, Article, UserArticleData, Tag
# Create your views here.

class Public(View):
    def get(self, request):
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
                print("1.%s" % (sta2 - sta1))
                for i in head:
                    headlines.append(i)
                sta3 = time.time()
                print("2.%s" % (sta3 - sta2))
                # print(headlines)
                for i in random.sample(list(datas), 4):
                    latest.append(i)
                sta4 = time.time()
                print("3.%s" % (sta4 - sta3))
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
                print("4.%s" % (sta5 - sta4))
            except Exception as e:
                sta5 = time.time()
                print("hot_tags", e)
        else:
            try:
                datas = Tag.objects.values_list("name", flat=True)
                datas = Counter(list(datas)).most_common(100)
                for i in random.sample(datas, 10):
                    hot_tags.append(i[0])
                sta5 = time.time()
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
                for i in random.sample(datas, 100):
                    artcle = Article.objects.get(id=i["id"])
                    hot_nwes.append(artcle)
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
                    print(datas)
                    bast_author.append(datas)
                else:
                    print("index_page_cache Exception ")
            except Exception as e:
                print("author else", e)
        popular = []
        datas = redis_conn.get("bast_of_the_week")
        if not (datas == None or datas == "" or datas == " "):
            try:
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
                datas = Article.objects.order_by("-creation_time", "-Likes_num", "-collect_num", "Forwarded")[
                        0:1000]
                popular=random.sample(list(datas), 6)
            except Exception as e:
                print("popular else", e)
        tui = []
        datas = redis_conn.get("recommend")
        if not (datas == None or datas == "" or datas == " "):
            try:
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
        print(context)
        print(time.time() - sta1)
        return render(request, "index.html", context=context)

    def post(self, request):
        return HttpResponse("Please use the correct request method! (GET request)")
