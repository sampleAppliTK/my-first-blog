from django.urls import path
from . import views # blog/views.pyをインポートする　ここではviews.py は、blogフォルダの中にしかないのでこれでOK


urlpatterns = [
    # ローカルだとhttp://127.0.0.1:8000/
    # PythonAnywhereだとhttp://sampleapplitk.pythonanywhere.com/
    #　上記のリクエストが来たとき、views.post_listメソッドを実行する
    # post_list が行先であることをDjangoが伝える
    path('', views.post_list, name='post_list'),
]
