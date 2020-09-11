from django.shortcuts import render
from django.utils import timezone
"""
models の前にあるドットは カレントディレクトリ 、もしくは カレントアプリケーション のことです。
views.pyと models.pyは、同じディレクトリに置いてあります。
だから、こんな風に.とファイル名だけを使って、簡単に記述することが出来るのです。
（ファイル名の拡張子.pyは必要ないです）
そして、モデルの名前を指定してインポートします(この場合のモデルは Postですね)。
"""
from .models import Post # mysite\blog\models.py を Postという名前でインポート

# Create your views here.

# blog/urls.pyから呼び出される
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    # blog\templates\blog\post_list.html を読み込む
    return render(request, 'blog/post_list.html', {'posts': posts})
