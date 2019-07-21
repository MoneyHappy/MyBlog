from django.contrib import admin
from .models import Blog, BlogType

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blogType', 'author', 'get_read_num', 'createTime', 'updateTime')

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'typeName')
    ordering = ('id',)

admin.site.site_header = '欢哥后台管理登陆'
admin.site.site_title = '欢哥博客后台管理'