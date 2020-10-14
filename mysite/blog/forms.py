from django import forms # フォームのインポート

# モデルを追加した場合、メソッドの追加だけでなくファイル先頭のインポートも忘れずに
from .models import Post, Comment

# 引数forms.ModelFromとは、HTMLからサーバーにPOSTリクエストを送信したもの（request.POST）
class PostForm(forms.ModelForm):

    class Meta:
        # 登録するテーブル名
        model = Post
        # titleとtextタグと思われる
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
