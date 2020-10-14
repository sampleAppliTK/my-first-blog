from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404

# 更新するモデル、フォームが増えたらインポートを忘れずに
from .models import Post, Comment
from .forms import PostForm, CommentForm

"""
login_requiredは、Djangoのデコレーターの一つ
デコレーターの使い方は、@login_requiredをdefの一つ上の行に追加する（メソッドの装飾）
ユーザーがログイン中なら、メソッドを実行
そうでないならurls.pyにPageNotFoundエラーを返す
"""
from django.contrib.auth.decorators import login_required



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

@login_required
def post_draft_list(request):
    # published_date__isnull=True 公開日が空の記事を記事作成日の昇順で取得
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_detail(request, pk):
    # pk＝主キー
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# 記事の新規投稿
@login_required
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
            # post.published_date = timezone.now()　# 公開日を設定しないと下書きとなる

            post.save()
            # 登録した記事のページに遷移する（viewsクラスのpost_detailメソッドを実行）
            return redirect('post_detail', pk=post.pk)
    else:
        # フォームの入力項目に不足がある場合、不正な入力項目を示す
        form = PostForm()
    # 入力した項目はそのままで編集画面に戻る
    return render(request, 'blog/post_edit.html', {'form': form})

# 記事の編集
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # 公開日を設定しないと下書きとして投稿する
            # 理由は、公開する記事（post_list）は公開日が今日の日付以前の記事を表示するため
            # 公開日が無い記事はpost_listでは表示できない
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# 下書きを公開へ
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

# 記事の削除
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)

    isPublish = post.published_date
    post.delete()

    if isPublish is None:
        # 削除した記事に公開日が無い場合、下書き一覧へ
        return redirect('post_draft_list')
    else:
        # 削除した記事に公開日がある場合、公開記事一覧へ
        return redirect('post_list')

# コメント登録
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

# コメント編集
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

# コメント削除
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
