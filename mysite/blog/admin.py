from django.contrib import admin

# admin.site.registerに追加だけでなく、ファイル先頭のインポート
from .models import Post, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
