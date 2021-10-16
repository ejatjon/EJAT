from django.contrib import admin

# Register your models here.
from index.models import Article, Tag, Category, UserArticleData, Views, Likes, Collect, Reprint, References, \
    Reply


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'Show_picture', 'author_user', 'creation_time','Likes_num','Forwarded','article','reply_num','views_num','collect_num','excerpt')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-creation_time',)
    #后台数据列表排序方式
    list_display_links = ('id', 'title','article')
    # 设置哪些字段可以点击进入编辑界面

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-name',)
    #后台数据列表排序方式
    list_display_links = ('name',)
    # 设置哪些字段可以点击进入编辑界面
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','index')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-name',)
    #后台数据列表排序方式
    list_display_links = ('name', 'index')
    # 设置哪些字段可以点击进入编辑界面
@admin.register(UserArticleData)
class UserArticleDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-id',)
    #后台数据列表排序方式
    list_display_links = ('id', 'user',)
    # 设置哪些字段可以点击进入编辑界面

@admin.register(Views)
class ViewsAdmin(admin.ModelAdmin):
    list_display = ('id',  'user', 'creation_time','modified_time')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-creation_time',)
    #后台数据列表排序方式
    list_display_links = ('id', 'user')
    # 设置哪些字段可以点击进入编辑界面
@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ('id', 'creation_time','user')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-creation_time',)
    #后台数据列表排序方式
    list_display_links = ('id', 'user',)
    # 设置哪些字段可以点击进入编辑界面
@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ('id', 'creation_time', 'user')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-creation_time',)
    # 后台数据列表排序方式
    list_display_links = ('id', 'user',)
    # 设置哪些字段可以点击进入编辑界面
@admin.register(Reprint)
class ReprintAdmin(admin.ModelAdmin):
    list_display = ('reprint_id','reprint_mas','reprint_link',)
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-reprint_id',)
    #后台数据列表排序方式
    list_display_links = ('reprint_id','reprint_mas','reprint_link',)
    # 设置哪些字段可以点击进入编辑界面
@admin.register(References)
class ReferencesAdmin(admin.ModelAdmin):
    list_display = ('references_id','references_name','references_link',)
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-references_id',)
    #后台数据列表排序方式
    list_display_links = ('references_id','references_name','references_link')
    # 设置哪些字段可以点击进入编辑界面
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('reply_id','to_reply_id','from_user','to_user','reply','creation_time')
    # 文章列表里显示想要显示的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('-creation_time',)
    #后台数据列表排序方式
    list_display_links = ('reply_id','to_reply_id','from_user','to_user','reply')
    # 设置哪些字段可以点击进入编辑界面