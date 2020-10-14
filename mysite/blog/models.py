from django.conf import settings
from django.db import models
from django.utils import timezone

# テーブル Postの定義
class Post(models.Model):
    # ForeignKeyで管理ユーザーテーブルとテーブルPostを紐づける（この場合、管理ユーザーが親、Postテーブルが子）
    # on_delete=models.CASCADE →おそらく管理ユーザーが消えたら、消えたユーザーが投稿したブログ記事が連動して消える設定になっている
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    # ForeignKeyでblog.models.pyで定義したテーブルPostとテーブルCommentを紐づける（この場合、Postテーブルが親、Commentテーブルが子）
    # on_delete=models.CASCADE →おそらくコメント投稿先のブログ記事が消されたら連動して消える設定になっている
    # related_nameは逆参照するための定義、このサンプルだとpost_list.htmlで記事に紐づいたコメントの投稿数を取得するのに、post.comment.countを使用してるがこれを実現させる
    # １つのモデルから複数のモデルを参照するときは、必ずrelated_nameを定義すること（そうでないとエラーとなる）→related_nameを指定しない場合は、参照先のモデル名_setとなる。
    # 逆参照とは、子モデルに親モデルをLEFT　JOINしてるイメージ
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
