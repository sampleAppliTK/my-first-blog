from django.shortcuts import render

# Create your views here.

# blog/urls.pyから呼び出される
def post_list(request):
    # blog\templates\blog\post_list.html を読み込む
    return render(request, 'blog/post_list.html', {})
