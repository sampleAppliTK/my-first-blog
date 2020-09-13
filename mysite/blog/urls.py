from django.urls import path
from . import views # blog/views.pyをインポートする　ここではviews.py は、blogフォルダの中にしかないのでこれでOK



# viewsクラスのメソッドは、views.pyで定義している
urlpatterns = [
    # ローカルだとhttp://127.0.0.1:8000/
    # PythonAnywhereだとhttp://sampleapplitk.pythonanywhere.com/
    #　上記のリクエストが来たとき、views.post_listメソッドを実行する
    # post_list が行先であることをDjangoが伝える
    path('', views.post_list, name='post_list'),

    # http://127.0.0.1:8000/post/1/　タイトルをクリックしたときのリンクを生成
    # post_detail.html を読み込む。上記URLの場合　変数pkに 1 入れてから　post_detailメソッドを実行する
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]
