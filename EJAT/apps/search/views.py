import datetime
import time

import pytz
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from EJAT.settings.dav import TIME_ZONE
from register.models import MyUser, UserData,Fans
from index.models import References, Reprint, Article, Tag, Category, UserArticleData,Reply

# Create your views here.

time_zone=TIME_ZONE

def search(request):
    path = request.path
    action_url = path + "all" + "/"
    filter_dict = {"all": "All", "latest": "Latest", "most_viewed": "Most viewed", "most_likes": "Most likes",
                   "most_Favorites": "Most Favorites"}
    data_dict = {"anytime": "Anytime", "within_a_week": "Within a week", "within_a_month": "Within a month",
                 "within_three_months": "Within three months", "within_a_year": "Within a year"}
    checkbox_dict = {"match_the_title": {"title": "Match the title", "is_selected": False},
                     "category_match": {"title": "Category match", "is_selected": False},
                     "match_tags": {"title": "Match tags", "is_selected": False},
                     "match_content": {"title": "Match content", "is_selected": False},
                     "match_author": {"title": "Match author", "is_selected": False},
                     "synonym_matching": ["Synonym matching", 0]}
    language_select_dict = {"english": "English", "chinese": "汉语", "source_language": "Source language",
                            "uyghur": "ئۇيغۇر"}

    articles = []
    try:
        paginator = Paginator(articles, 5)
    except Exception:
        paginator = Paginator(articles, 5)
    try:
        articles = paginator.page(1)  # 获取当前页码的记录
    except PageNotAnInteger:
        articles = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    print("q in None!")
    return render(request, "search.html", locals())


class Search(View):
    def get(self, request, filter):
        try:
            time2=time.time()
            print(filter)
            filter_name = filter
            page_num = request.GET.get('page', 1)
            filter_dict = {"all": "All", "latest": "Latest", "most_viewed": "Most viewed", "most_likes": "Most likes", "most_Favorites": "Most Favorites"}
            data_dict = {"anytime": "Anytime", "within_a_week": "Within a week", "within_a_month": "Within a month",
                         "within_three_months": "Within three months", "within_a_year": "Within a year"}
            checkbox_dict = {"match_the_title": {"title":"Match the title","is_selected":True}, "category_match": {"title":"Category match","is_selected":False},
                             "match_tags": {"title":"Match tags","is_selected":False}, "match_content": {"title":"Match content","is_selected":False}, "match_author": {"title":"Match author","is_selected":False},
                             "synonym_matching": {"title":"Synonym matching","is_selected":False}}
            language_select_dict = {"english": {"title":"English","is_selected":False}, "chinese": {"title":"汉语","is_selected":False}, "source_language": {"title":"Source language","is_selected":False},
                                    "uyghur": {"title":"ئۇيغۇر","is_selected":False}}
            all_limits=[5,10,20,50,100]
            if filter_name == "":
                data_selected=""
                path = "http://127.0.0.1:8000/search/"
                action_url = path + "all" + "/"
                filter_name = "all"
                form_datas_url = "?"
                parameters = dict(request.GET)
                for x, y in parameters.items():
                    form_datas_url = form_datas_url + x + "=" + y[0] + "&"
                if not "limit" in parameters:
                    limit = 5
                else:
                    limit = parameters["limit"][0]
                if not "data" in parameters:
                    data = "anytime"
                    now = datetime.datetime.now(tz=pytz.timezone(time_zone))
                    print(now)
                    datatime_Q = Q(creation_time__lte=now)
                    data_selected=data
                else:
                    now = datetime.datetime.now(tz=pytz.timezone(time_zone))
                    data = parameters["data"][0]
                    if data == "anytime":
                        datatime_Q = Q(creation_time__lte=now)
                        data_selected=data
                    elif data == "within_a_week":
                        start = now - datetime.timedelta(hours=(24 * 6) + 23, minutes=59, seconds=59)
                        print(start)
                        datatime_Q = Q(creation_time__gte=start)
                        data_selected = data
                    elif data == "within_a_month":
                        start = now - datetime.timedelta(hours=(24 * 30) + 10, minutes=59, seconds=59)
                        print(start)
                        datatime_Q = Q(creation_time__gte=start)
                        data_selected = data
                    elif data == "within_three_months":
                        start = now - datetime.timedelta(hours=(24 * 30) * 3 + 32, minutes=59, seconds=59)
                        print(start)
                        datatime_Q = Q(creation_time__gte=start)
                        data_selected = data
                    elif data == "within_a_year":
                        start = now - datetime.timedelta(hours=(24 * 30) * 11 + (24 * 29) + 120, minutes=59, seconds=59)
                        print(start)
                        datatime_Q = Q(creation_time__gte=start)
                        data_selected = data
                    else:
                        datatime_Q = Q(creation_time__lte=now)
                        data_selected = "anytime"
                if not "language" in parameters:
                    language = "source_language"
                else:
                    language = parameters["language"][0]
                if not "q" in parameters:
                    articles = []
                    try:
                        paginator = Paginator(articles, int(limit))
                    except Exception:
                        paginator = Paginator(articles, 5)
                    try:
                        articles = paginator.page(page_num)  # 获取当前页码的记录
                    except PageNotAnInteger:
                        articles = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
                    except EmptyPage:
                        articles = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
                    print("q in None!")
                    return render(request, "search.html", locals())
                else:
                    keywords = parameters["q"][0]
                    try:
                        keywords_set = set(keywords)
                        keywords_set.remove(" ")
                        if len(keywords_set) == 0:
                            articles = []
                            try:
                                limit=int(limit)
                                paginator = Paginator(articles, limit)
                                if limit not in all_limits:
                                    all_limits.append(limit)
                            except Exception:
                                paginator = Paginator(articles, 5)
                            try:
                                articles = paginator.page(page_num)  # 获取当前页码的记录
                            except PageNotAnInteger:
                                articles = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
                            except EmptyPage:
                                articles = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
                            print("q in None!")
                            return render(request, "search.html", locals())
                    except Exception:
                        pass

                if "match_the_title" in parameters:
                    if "category_match" in parameters:
                        if "match_tags" in parameters:
                            if "match_content" in parameters:
                                if "match_author" in parameters:
                                    # if "synonym_matching" in parameters:
                                    articles = Article.objects.filter(
                                        Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(
                                            tag__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                                    checkbox_dict["match_the_title"]["is_selected"]=True
                                    checkbox_dict["category_match"]["is_selected"] = True
                                    checkbox_dict["match_tags"]["is_selected"] = True
                                    checkbox_dict["match_content"]["is_selected"] = True
                                    checkbox_dict["match_author"]["is_selected"] = True
                                # elif "synonym_matching" in parameters:
                                else:
                                    articles = Article.objects.filter(
                                        Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(
                                            tag__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                                    checkbox_dict["match_the_title"]["is_selected"] = True
                                    checkbox_dict["category_match"]["is_selected"] = True
                                    checkbox_dict["match_tags"]["is_selected"] = True
                                    checkbox_dict["match_content"]["is_selected"] = True
                            elif "match_author" in parameters:
                                # if "synonym_matching" in parameters:
                                articles = Article.objects.filter(
                                    Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(
                                        tag__name__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                                checkbox_dict["match_the_title"]["is_selected"] = True
                                checkbox_dict["category_match"]["is_selected"] = True
                                checkbox_dict["match_tags"]["is_selected"] = True
                                checkbox_dict["match_author"]["is_selected"] = True
                            # elif "synonym_matching" in parameters:
                            else:
                                articles = Article.objects.filter(
                                    Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(tag__name__icontains=keywords) & datatime_Q)
                                checkbox_dict["match_the_title"]["is_selected"] = True
                                checkbox_dict["category_match"]["is_selected"] = True
                                checkbox_dict["match_tags"]["is_selected"] = True
                        elif "match_content" in parameters:
                            if "match_author" in parameters:
                                # if "synonym_matching" in parameters:
                                articles = Article.objects.filter(
                                    Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(
                                        excerpt__article_excerpt__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                                checkbox_dict["match_the_title"]["is_selected"] = True
                                checkbox_dict["category_match"]["is_selected"] = True
                                checkbox_dict["match_content"]["is_selected"] = True
                                checkbox_dict["match_author"]["is_selected"] = True
                            # elif "synonym_matching" in parameters:
                            else:
                                articles = Article.objects.filter(
                                    Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                                checkbox_dict["match_the_title"]["is_selected"] = True
                                checkbox_dict["category_match"]["is_selected"] = True
                                checkbox_dict["match_content"]["is_selected"] = True
                        elif "match_author" in parameters:
                            # if "synonym_matching" in parameters:
                            articles = Article.objects.filter(
                                Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_the_title"]["is_selected"] = True
                            checkbox_dict["category_match"]["is_selected"] = True
                            checkbox_dict["match_author"]["is_selected"] = True
                        # elif "synonym_matching" in parameters:
                        else:
                            articles = Article.objects.filter(Q(title__icontains=keywords) | Q(category__name__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_the_title"]["is_selected"] = True
                            checkbox_dict["category_match"]["is_selected"] = True
                    elif "match_tags" in parameters:
                        if "match_content" in parameters:
                            if "match_author" in parameters:
                                # if "synonym_matching" in parameters:
                                articles = Article.objects.filter(
                                    Q(title__icontains=keywords) | Q(tag__name__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                                checkbox_dict["match_the_title"]["is_selected"] = True
                                checkbox_dict["match_tags"]["is_selected"] = True
                                checkbox_dict["match_author"]["is_selected"] = True
                            # elif "synonym_matching" in parameters:
                            else:
                                articles = Article.objects.filter(
                                    Q(title__icontains=keywords) | Q(tag__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                                checkbox_dict["match_the_title"]["is_selected"] = True
                                checkbox_dict["match_tags"]["is_selected"] = True
                                checkbox_dict["match_content"]["is_selected"] = True
                        elif "match_author" in parameters:
                            # if "synonym_matching" in parameters:
                            articles = Article.objects.filter(
                                Q(title__icontains=keywords) | Q(tag__name__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_the_title"]["is_selected"] = True
                            checkbox_dict["match_tags"]["is_selected"] = True
                            checkbox_dict["match_author"]["is_selected"] = True
                        # elif "synonym_matching" in parameters:
                        else:
                            articles = Article.objects.filter(Q(title__icontains=keywords) | Q(tag__name__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_the_title"]["is_selected"] = True
                            checkbox_dict["match_tags"]["is_selected"] = True
                    elif "match_content" in parameters:
                        if "match_author" in parameters:
                            # if "synonym_matching" in parameters:
                            articles = Article.objects.filter(Q(title__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_the_title"]["is_selected"] = True
                            checkbox_dict["match_content"]["is_selected"] = True
                            checkbox_dict["match_author"]["is_selected"] = True
                        # elif "synonym_matching" in parameters:
                        else:
                            articles = Article.objects.filter(Q(title__icontains=keywords) | Q(excerpt__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_the_title"]["is_selected"] = True
                            checkbox_dict["match_content"]["is_selected"] = True
                    elif "match_author" in parameters:
                        # if "synonym_matching" in parameters:
                        articles = Article.objects.filter(Q(title__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                        checkbox_dict["match_the_title"]["is_selected"] = True
                        checkbox_dict["match_author"]["is_selected"] = True
                    # elif "synonym_matching" in parameters:
                    #     articles = Article.objects.filter(Q(title__icontains=keywords) | Q())
                    else:
                        articles=Article.objects.filter(Q(title__icontains=keywords) & datatime_Q)
                        checkbox_dict["match_the_title"]["is_selected"] = True
                elif "category_match" in parameters:
                    if "match_tags" in parameters:
                        if "match_content" in parameters:
                            if "match_author" in parameters:
                                # if "synonym_matching" in parameters:
                                articles = Article.objects.filter(
                                    Q(category__name__icontains=keywords) | Q(tag__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) | Q(author_user_username__icontains=keywords) & datatime_Q)
                                checkbox_dict["category_match"]["is_selected"] = True
                                checkbox_dict["match_tags"]["is_selected"] = True
                                checkbox_dict["match_content"]["is_selected"] = True
                                checkbox_dict["match_author"]["is_selected"] = True
                            # elif "synonym_matching" in parameters:
                            else:
                                articles = Article.objects.filter(Q(category__name__icontains=keywords) | Q(tag__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                                checkbox_dict["category_match"]["is_selected"] = True
                                checkbox_dict["match_tags"]["is_selected"] = True
                                checkbox_dict["match_content"]["is_selected"] = True
                        elif "match_author" in parameters:
                            # if "synonym_matching" in parameters:
                            articles = Article.objects.filter(Q(category__name__icontains=keywords) | Q(author_user_username__icontains=keywords) & datatime_Q)
                            checkbox_dict["category_match"]["is_selected"] = True
                            checkbox_dict["match_author"]["is_selected"] = True
                        # elif "synonym_matching" in parameters:
                        else:
                            articles = Article.objects.filter(Q(category__name__icontains=keywords) | Q(tag__name__icontains=keywords) & datatime_Q)
                            checkbox_dict["category_match"]["is_selected"] = True
                            checkbox_dict["match_tags"]["is_selected"] = True
                    elif "match_content" in parameters:
                        if "match_author" in parameters:
                            # if "synonym_matching" in parameters:
                            articles = Article.objects.filter(
                                Q(category__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                            checkbox_dict["category_match"]["is_selected"] = True
                            checkbox_dict["match_content"]["is_selected"] = True
                            checkbox_dict["match_author"]["is_selected"] = True
                        # elif "synonym_matching" in parameters:
                        else:
                            articles = Article.objects.filter(Q(category__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                            checkbox_dict["category_match"]["is_selected"] = True
                            checkbox_dict["match_content"]["is_selected"] = True
                    elif "match_author" in parameters:
                        # if "synonym_matching" in parameters:
                        articles = Article.objects.filter(Q(category__name__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                        checkbox_dict["category_match"]["is_selected"] = True
                        checkbox_dict["match_author"]["is_selected"] = True
                    # elif "synonym_matching" in parameters:
                    else:
                        articles = Article.objects.filter(Q(category__name__icontains=keywords) & datatime_Q)
                        checkbox_dict["category_match"]["is_selected"] = True
                elif "match_tags" in parameters:
                    if "match_content" in parameters:
                        if "match_author" in parameters:
                            # if "synonym_matching" in parameters:
                            articles = Article.objects.filter(
                                Q(tag__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_tags"]["is_selected"] = True
                            checkbox_dict["match_content"]["is_selected"] = True
                            checkbox_dict["match_author"]["is_selected"] = True
                        # elif "synonym_matching" in parameters:
                        else:
                            articles = Article.objects.filter(Q(tag__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_tags"]["is_selected"] = True
                            checkbox_dict["match_content"]["is_selected"] = True
                    elif "match_author" in parameters:
                        # if "synonym_matching" in parameters:
                        articles = Article.objects.filter(
                            Q(tag__name__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                        checkbox_dict["match_tags"]["is_selected"] = True
                        checkbox_dict["match_author"]["is_selected"] = True
                    # elif "synonym_matching" in parameters:
                    else:
                        articles = Article.objects.filter(Q(tag__name__icontains=keywords) & datatime_Q)
                        checkbox_dict["match_tags"]["is_selected"] = True
                elif "match_content" in parameters:
                    if "match_author" in parameters:
                        # if "synonym_matching" in parameters:
                        articles = Article.objects.filter(Q(excerpt__article_excerpt__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                        checkbox_dict["match_content"]["is_selected"] = True
                        checkbox_dict["match_author"]["is_selected"] = True
                    # elif "synonym_matching" in parameters:
                    else:
                        articles = Article.objects.filter(Q(excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                        checkbox_dict["match_content"]["is_selected"] = True
                elif "match_author" in parameters:
                    # if "synonym_matching" in parameters:
                    articles = Article.objects.filter(Q(author_user__username__icontains=keywords) & datatime_Q)
                    checkbox_dict["match_author"]["is_selected"] = True
                    # elif "synonym_matching" in parameters:
                else:
                    time1=time.time()
                    articles = Article.objects.filter(Q(title__icontains=keywords) & datatime_Q)
                    checkbox_dict["match_the_title"]["is_selected"] = True
                    print("title-->",time.time()-time1)
            else:
                data_selected = ""
                now = datetime.datetime.now(tz=pytz.timezone("Asia/Urumqi"))
                print(now)
                request.path = ""
                path = "http://127.0.0.1:8000/search/"
                action_url = path + filter_name + "/"
                form_datas_url = "?"
                parameters = dict(request.GET)
                for x, y in parameters.items():
                    form_datas_url = form_datas_url + x + "=" + y[0] + "&"
                if not "limit" in parameters:
                    limit=5
                else:
                    limit = parameters["limit"][0]
                if not "data" in parameters:
                    data = "anytime"
                    now = datetime.datetime.now(tz=pytz.timezone(time_zone))
                    print(now)
                    datatime_Q=Q(creation_time__lte=now)
                    data_selected = data
                else:
                    now = datetime.datetime.now(tz=pytz.timezone(time_zone))
                    data = parameters["data"][0]
                    if data=="anytime":
                        datatime_Q = Q(creation_time__lte=now)
                        data_selected = data
                    elif data=="within_a_week":
                        start = now - datetime.timedelta(hours=(24*6)+23, minutes=59, seconds=59)
                        print(start)
                        datatime_Q = Q(creation_time__gte=start)
                        data_selected = data
                    elif data=="within_a_month":
                        start = now - datetime.timedelta(hours=(24*30)+10, minutes=59, seconds=59)
                        print(start)
                        datatime_Q = Q(creation_time__gte=start)
                        data_selected = data
                    elif data=="within_three_months":
                        start = now - datetime.timedelta(hours=(24*30)*3+32, minutes=59, seconds=59)
                        print(start)
                        datatime_Q = Q(creation_time__gte=start)
                        data_selected = data
                    elif data=="within_a_year":
                        start = now - datetime.timedelta(hours=(24*30)*11+(24*29)+120, minutes=59, seconds=59)
                        print(start)
                        datatime_Q = Q(creation_time__gte=start)
                        data_selected = data
                    else:
                        datatime_Q = Q(creation_time__lte=now)
                        data_selected = "anytime"

                if not "language" in parameters:
                    language = "source_language"
                else:
                    language = parameters["language"][0]
                if not "q" in parameters:
                    articles=[]
                    try:
                        limit=int(limit)
                        paginator = Paginator(articles, limit)
                        if limit not in all_limits:
                            all_limits.append(limit)
                    except Exception:
                        paginator = Paginator(articles, 5)
                    try:
                        articles = paginator.page(page_num)  # 获取当前页码的记录
                    except PageNotAnInteger:
                        articles = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
                    except EmptyPage:
                        articles = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
                    print("q in None!")
                    return render(request, "search.html", locals())
                else:
                    keywords = parameters["q"][0]
                    try:
                        keywords_set=set(keywords)
                        keywords_set.remove(" ")
                        if len(keywords_set)==0:
                            articles = []
                            try:
                                limit=int(limit)
                                paginator = Paginator(articles, limit)
                                if limit not in all_limits:
                                    all_limits.append(limit)
                            except Exception:
                                paginator = Paginator(articles, 5)
                            try:
                                articles = paginator.page(page_num)  # 获取当前页码的记录
                            except PageNotAnInteger:
                                articles = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
                            except EmptyPage:
                                articles = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
                            print("q in None!")
                            return render(request, "search.html", locals())
                    except Exception:
                        pass
                if "match_the_title" in parameters:
                    if "category_match" in parameters:
                        if "match_tags" in parameters:
                            if "match_content" in parameters:
                                if "match_author" in parameters:
                                    # if "synonym_matching" in parameters:
                                    articles = Article.objects.filter(
                                        Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(
                                            tag__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) | Q(
                                            author_user__username__icontains=keywords) & datatime_Q)
                                    checkbox_dict["match_the_title"]["is_selected"] = True
                                    checkbox_dict["category_match"]["is_selected"] = True
                                    checkbox_dict["match_tags"]["is_selected"] = True
                                    checkbox_dict["match_content"]["is_selected"] = True
                                    checkbox_dict["match_author"]["is_selected"] = True
                                # elif "synonym_matching" in parameters:
                                else:
                                    articles = Article.objects.filter(
                                        Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(
                                            tag__name__icontains=keywords) | Q(
                                            excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                                    checkbox_dict["match_the_title"]["is_selected"] = True
                                    checkbox_dict["category_match"]["is_selected"] = True
                                    checkbox_dict["match_tags"]["is_selected"] = True
                                    checkbox_dict["match_content"]["is_selected"] = True
                            elif "match_author" in parameters:
                                # if "synonym_matching" in parameters:
                                articles = Article.objects.filter(
                                    Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(
                                        tag__name__icontains=keywords) | Q(
                                        author_user__username__icontains=keywords) & datatime_Q)
                                checkbox_dict["match_the_title"]["is_selected"] = True
                                checkbox_dict["category_match"]["is_selected"] = True
                                checkbox_dict["match_tags"]["is_selected"] = True
                                checkbox_dict["match_author"]["is_selected"] = True
                            # elif "synonym_matching" in parameters:
                            else:
                                articles = Article.objects.filter(
                                    Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(
                                        tag__name__icontains=keywords) & datatime_Q)
                                checkbox_dict["match_the_title"]["is_selected"] = True
                                checkbox_dict["category_match"]["is_selected"] = True
                                checkbox_dict["match_tags"]["is_selected"] = True
                        elif "match_content" in parameters:
                            if "match_author" in parameters:
                                # if "synonym_matching" in parameters:
                                articles = Article.objects.filter(
                                    Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(
                                        excerpt__article_excerpt__icontains=keywords) | Q(
                                        author_user__username__icontains=keywords) & datatime_Q)
                                checkbox_dict["match_the_title"]["is_selected"] = True
                                checkbox_dict["category_match"]["is_selected"] = True
                                checkbox_dict["match_content"]["is_selected"] = True
                                checkbox_dict["match_author"]["is_selected"] = True
                            # elif "synonym_matching" in parameters:
                            else:
                                articles = Article.objects.filter(
                                    Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(
                                        excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                                checkbox_dict["match_the_title"]["is_selected"] = True
                                checkbox_dict["category_match"]["is_selected"] = True
                                checkbox_dict["match_content"]["is_selected"] = True
                        elif "match_author" in parameters:
                            # if "synonym_matching" in parameters:
                            articles = Article.objects.filter(
                                Q(title__icontains=keywords) | Q(category__name__icontains=keywords) | Q(
                                    author_user__username__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_the_title"]["is_selected"] = True
                            checkbox_dict["category_match"]["is_selected"] = True
                            checkbox_dict["match_author"]["is_selected"] = True
                        # elif "synonym_matching" in parameters:
                        else:
                            articles = Article.objects.filter(
                                Q(title__icontains=keywords) | Q(category__name__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_the_title"]["is_selected"] = True
                            checkbox_dict["category_match"]["is_selected"] = True
                    elif "match_tags" in parameters:
                        if "match_content" in parameters:
                            if "match_author" in parameters:
                                # if "synonym_matching" in parameters:
                                articles = Article.objects.filter(
                                    Q(title__icontains=keywords) | Q(tag__name__icontains=keywords) | Q(
                                        author_user__username__icontains=keywords) & datatime_Q)
                                checkbox_dict["match_the_title"]["is_selected"] = True
                                checkbox_dict["match_tags"]["is_selected"] = True
                                checkbox_dict["match_author"]["is_selected"] = True
                            # elif "synonym_matching" in parameters:
                            else:
                                articles = Article.objects.filter(
                                    Q(title__icontains=keywords) | Q(tag__name__icontains=keywords) | Q(
                                        excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                                checkbox_dict["match_the_title"]["is_selected"] = True
                                checkbox_dict["match_tags"]["is_selected"] = True
                                checkbox_dict["match_content"]["is_selected"] = True
                        elif "match_author" in parameters:
                            # if "synonym_matching" in parameters:
                            articles = Article.objects.filter(
                                Q(title__icontains=keywords) | Q(tag__name__icontains=keywords) | Q(
                                    author_user__username__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_the_title"]["is_selected"] = True
                            checkbox_dict["match_tags"]["is_selected"] = True
                            checkbox_dict["match_author"]["is_selected"] = True
                        # elif "synonym_matching" in parameters:
                        else:
                            articles = Article.objects.filter(
                                Q(title__icontains=keywords) | Q(tag__name__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_the_title"]["is_selected"] = True
                            checkbox_dict["match_tags"]["is_selected"] = True
                    elif "match_content" in parameters:
                        if "match_author" in parameters:
                            # if "synonym_matching" in parameters:
                            articles = Article.objects.filter(
                                Q(title__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) | Q(
                                    author_user__username__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_the_title"]["is_selected"] = True
                            checkbox_dict["match_content"]["is_selected"] = True
                            checkbox_dict["match_author"]["is_selected"] = True
                        # elif "synonym_matching" in parameters:
                        else:
                            articles = Article.objects.filter(
                                Q(title__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_the_title"]["is_selected"] = True
                            checkbox_dict["match_content"]["is_selected"] = True
                    elif "match_author" in parameters:
                        # if "synonym_matching" in parameters:
                        articles = Article.objects.filter(
                            Q(title__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                        checkbox_dict["match_the_title"]["is_selected"] = True
                        checkbox_dict["match_author"]["is_selected"] = True
                    # elif "synonym_matching" in parameters:
                    #     articles = Article.objects.filter(Q(title__icontains=keywords) | Q())
                    else:
                        articles = Article.objects.filter(Q(title__icontains=keywords) & datatime_Q)
                        checkbox_dict["match_the_title"]["is_selected"] = True
                elif "category_match" in parameters:
                    if "match_tags" in parameters:
                        if "match_content" in parameters:
                            if "match_author" in parameters:
                                # if "synonym_matching" in parameters:
                                articles = Article.objects.filter(
                                    Q(category__name__icontains=keywords) | Q(tag__name__icontains=keywords) | Q(
                                        excerpt__article_excerpt__icontains=keywords) | Q(
                                        author_user_username__icontains=keywords) & datatime_Q)
                                checkbox_dict["category_match"]["is_selected"] = True
                                checkbox_dict["match_tags"]["is_selected"] = True
                                checkbox_dict["match_content"]["is_selected"] = True
                                checkbox_dict["match_author"]["is_selected"] = True
                            # elif "synonym_matching" in parameters:
                            else:
                                articles = Article.objects.filter(
                                    Q(category__name__icontains=keywords) | Q(tag__name__icontains=keywords) | Q(
                                        excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                                checkbox_dict["category_match"]["is_selected"] = True
                                checkbox_dict["match_tags"]["is_selected"] = True
                                checkbox_dict["match_content"]["is_selected"] = True
                        elif "match_author" in parameters:
                            # if "synonym_matching" in parameters:
                            articles = Article.objects.filter(Q(category__name__icontains=keywords) | Q(
                                author_user_username__icontains=keywords) & datatime_Q)
                            checkbox_dict["category_match"]["is_selected"] = True
                            checkbox_dict["match_author"]["is_selected"] = True
                        # elif "synonym_matching" in parameters:
                        else:
                            articles = Article.objects.filter(
                                Q(category__name__icontains=keywords) | Q(tag__name__icontains=keywords) & datatime_Q)
                            checkbox_dict["category_match"]["is_selected"] = True
                            checkbox_dict["match_tags"]["is_selected"] = True
                    elif "match_content" in parameters:
                        if "match_author" in parameters:
                            # if "synonym_matching" in parameters:
                            articles = Article.objects.filter(
                                Q(category__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) | Q(
                                    author_user__username__icontains=keywords) & datatime_Q)
                            checkbox_dict["category_match"]["is_selected"] = True
                            checkbox_dict["match_content"]["is_selected"] = True
                            checkbox_dict["match_author"]["is_selected"] = True
                        # elif "synonym_matching" in parameters:
                        else:
                            articles = Article.objects.filter(
                                Q(category__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                            checkbox_dict["category_match"]["is_selected"] = True
                            checkbox_dict["match_content"]["is_selected"] = True
                    elif "match_author" in parameters:
                        # if "synonym_matching" in parameters:
                        articles = Article.objects.filter(Q(category__name__icontains=keywords) | Q(
                            author_user__username__icontains=keywords) & datatime_Q)
                        checkbox_dict["category_match"]["is_selected"] = True
                        checkbox_dict["match_author"]["is_selected"] = True
                    # elif "synonym_matching" in parameters:
                    else:
                        articles = Article.objects.filter(Q(category__name__icontains=keywords) & datatime_Q)
                        checkbox_dict["category_match"]["is_selected"] = True
                elif "match_tags" in parameters:
                    if "match_content" in parameters:
                        if "match_author" in parameters:
                            # if "synonym_matching" in parameters:
                            articles = Article.objects.filter(
                                Q(tag__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) | Q(
                                    author_user__username__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_tags"]["is_selected"] = True
                            checkbox_dict["match_content"]["is_selected"] = True
                            checkbox_dict["match_author"]["is_selected"] = True
                        # elif "synonym_matching" in parameters:
                        else:
                            articles = Article.objects.filter(
                                Q(tag__name__icontains=keywords) | Q(excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                            checkbox_dict["match_tags"]["is_selected"] = True
                            checkbox_dict["match_content"]["is_selected"] = True
                    elif "match_author" in parameters:
                        # if "synonym_matching" in parameters:
                        articles = Article.objects.filter(
                            Q(tag__name__icontains=keywords) | Q(
                                author_user__username__icontains=keywords) & datatime_Q)
                        checkbox_dict["match_tags"]["is_selected"] = True
                        checkbox_dict["match_author"]["is_selected"] = True
                    # elif "synonym_matching" in parameters:
                    else:
                        articles = Article.objects.filter(Q(tag__name__icontains=keywords) & datatime_Q)
                        checkbox_dict["match_tags"]["is_selected"] = True
                elif "match_content" in parameters:
                    if "match_author" in parameters:
                        # if "synonym_matching" in parameters:
                        articles = Article.objects.filter(
                            Q(excerpt__article_excerpt__icontains=keywords) | Q(author_user__username__icontains=keywords) & datatime_Q)
                        checkbox_dict["match_content"]["is_selected"] = True
                        checkbox_dict["match_author"]["is_selected"] = True
                    # elif "synonym_matching" in parameters:
                    else:
                        articles = Article.objects.filter(Q(excerpt__article_excerpt__icontains=keywords) & datatime_Q)
                        checkbox_dict["match_content"]["is_selected"] = True
                elif "match_author" in parameters:
                    # if "synonym_matching" in parameters:
                    articles = Article.objects.filter(Q(author_user__username__icontains=keywords) & datatime_Q)
                    checkbox_dict["match_author"]["is_selected"] = True
                    # elif "synonym_matching" in parameters:
                else:
                    time1 = time.time()
                    articles = Article.objects.filter(Q(title__icontains=keywords) & datatime_Q)
                    checkbox_dict["match_the_title"]["is_selected"] = True
                    print("title-->", time.time() - time1)
            if filter_name=="latest":
                articles=articles.order_by("-creation_time").distinct()   #explain

            elif filter_name=="most_viewed":
                articles = articles.order_by("-views_num").distinct()
            elif filter_name=="most_likes":
                articles = articles.order_by("-Likes_num").distinct()
            elif filter_name=="most_Favorites":
                articles = articles.order_by("-Forwarded").distinct()
            else:
                articles = articles.order_by(F("views_num")/F("Likes_num")).distinct()
            time3 = time.time()
            # print(len(articles))
            # print(articles.count())
            # print(articles)
            print("time3-->", time.time() - time3)
            try:
                limit=int(limit)
                paginator = Paginator(articles, limit)
                if limit not in all_limits:
                    all_limits.append(limit)
            except Exception:
                limit=5
                paginator=Paginator(articles, 5)
            try:
                articles = paginator.page(page_num)  # 获取当前页码的记录
            except PageNotAnInteger:
                articles = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
            except EmptyPage:
                articles = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
            print(articles)
            print(articles.object_list)


            print("time3-->", time.time() - time3)
            print(time.time()-time2)

            return render(request, "search.html", locals())
        except Exception as e:
            print(e)
            return HttpResponse(
                '''
                The program terminates abnormally!
                Please check if there is a problem with the URL you entered!
                If this happens multiple times and you have not found the reason, then please contact the administrator.
                '''
            )

    def post(self, request):
        print("search pass")
        pass

