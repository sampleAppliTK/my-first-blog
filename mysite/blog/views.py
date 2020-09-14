from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm

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

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# 記事の新規投稿
def post_new(request):
    # フォーム送信時、request.POST にデータが追加されている
    # post_edit.html  タグform method="POST" class="post-form"

    if request.method == "POST":
        # フォームにタイトルと記事を送信した時
        form = PostForm(request.POST)

        if form.is_valid():
            # フォームの値が正しい時
            post = form.save(commit=False)

            # author（投稿者）は必須
            post.author = request.user

            # 公開日
            post.published_date = timezone.now()

            post.save()
            # 登録した記事のページに遷移する（viewsクラスのpost_detailメソッドを実行）
            return redirect('post_detail', pk=post.pk)
    else:
        # フォームの入力項目に不足がある場合、不正な入力項目を示す
        form = PostForm()
    # 入力した項目はそのままで編集画面に戻る
    return render(request, 'blog/post_edit.html', {'form': form})

# 記事の編集
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
