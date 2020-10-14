from django.urls import path
from . import views # blog/views.pyをインポートする　ここではviews.py は、blogフォルダの中にしかないのでこれでOK



# viewsクラスのメソッドは、views.pyで定義している
urlpatterns = [
    # ローカルだとhttp://127.0.0.1:8000/
    # PythonAnywhereだとhttp://sampleapplitk.pythonanywhere.com/
    #　上記のリクエストが来たとき、views.post_listメソッドを実行する
    # post_list が行先であることをDjangoが伝える
    path('', views.stock_list, name='stock_list'),
    path('reg/', views.stock_reg, name='stock_reg'),
    path('find/', views.stock_find, name='stock_find'),
    path('remove/<int:code>/', views.stock_remove, name='stock_remove'),
]
