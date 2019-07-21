from django.contrib import admin
from .models import ReadNum,ReadDate


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object', 'content_type', 'object_id')

@admin.register(ReadDate)
class ReadDateAdmin(admin.ModelAdmin):
    list_display = ('read_date', 'read_num', 'content_object', 'content_type', 'object_id')
