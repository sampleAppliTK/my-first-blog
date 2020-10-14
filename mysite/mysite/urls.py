"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include #　これを入れないとpathの引数で使用してるincludeが動かない（https://qiita.com/s-katsumata/items/c38788b6c56c107560d2）
from django.contrib.auth import views # Djangoの認証機能ライブラリ　これをインポートしないとviews.LoginViewが動かない
from django.conf import settings # Django-Debug-Toolberを動作するために使用

urlpatterns = [
    path('admin/', admin.site.urls),
    # ローカルだとhttp://127.0.0.1:8000/
    # PythonAnywhereだとhttp://sampleapplitk.pythonanywhere.com/
    # に来たリクエストは全てblog.urlsへリダイレクトするようになる
    path('stock/', include('stock.urls')),

    path('', include('blog.urls')),

    # django.contrib.auth をインポートする事
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),

#    path('stock/accounts/login/', views.LoginView.as_view(template_name='post_list.html'), name='login'),
#    path('stock/accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        #path('stock/', include(debug_toolbar.urls)),
    ]
