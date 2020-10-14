from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Stock

# 更新するモデル、フォームが増えたらインポートを忘れずに
from .forms import StockForm
from .web_yahoo_stockcode import WebYahooStockCode

# Create your views here.
def stock_list(request):

    # 空のstockテーブルの入力フォームを生成 base.htmlで使用するform
    form = StockForm()

    # modelsの中でテーブル設計とは別物のWebYahooStockCodeを呼び出すような設計が有りなのか不明なので
    # 一覧画面で出す株価に紐づく詳細データは、viewsクラスで取得するように設計
    # WebYahooStockCodeのインスタンス一つ渡して、htmlでループ毎にインスタンスを再利用するのも良さそう
    # htmlに引き渡し用のクラスを作成しても良さそう

    # 最終的には、株価コード順にしたい。今は作成日付の昇順
    stock_detail_list = __getStockDetailList(request)
    return render(request, 'stock/post_list.html', {'stock_detail_list': stock_detail_list}, {'form': form})

def stock_find(request):

    if request.method == "POST":
        web = WebYahooStockCode(request.POST["code"])

    return render(request, 'stock/find_result.html', {'web': web})

def stock_reg(request):
    # フォーム送信時、request.POST にデータが追加されている
    # post_edit.html  タグform method="POST" class="post-form"

    if request.method == "POST":
        # フォームにタイトルと記事を送信した時
        form = StockForm(request.POST)

        if form.is_valid():
            # フォームの値が正しい時
            post = form.save(commit=False)
            # ログインユーザーは、サンプルのブログで作成済みのため、今回は未ログインでも使用できる機能にする
            post.author = request.user
            post.save()

    #params = {'message': 'メンバーの一覧', 'data': data}
    #return render(request, 'user/list.html', params)

    else:
        # フォームの入力項目に不足がある場合、不正な入力項目を示す
        form = StockForm()

    # 登録、エラーどちらでもトップに戻る

    # 登録処理後、stockテーブルの一覧を取得する
    stock_detail_list = __getStockDetailList(request)
    return render(request, 'stock/post_list.html', {'stock_detail_list': stock_detail_list}, {'form': form})

# 記事の削除
def stock_remove(request, code):
    stock = get_object_or_404(Stock.objects.filter(author=request.user, code=code))
    stock.delete()
    form = StockForm()
    stock_detail_list = __getStockDetailList(request)
    return render(request, 'stock/post_list.html', {'stock_detail_list': stock_detail_list}, {'form': form})


# 一覧画面の株価コードに紐づく詳細データ取得
def __getStockDetailList(stocks):
    list = []
    for stock in stocks:
        list.append(WebYahooStockCode(str(stock.code)))

    return list

# 一覧画面の株価コードに紐づく詳細データ取得
def __getStockDetailList(request):
    list = []

    if request.user.is_authenticated:
        # ログイン中ならDBからデータを取得する
        stocks = Stock.objects.filter(author=request.user, created_date__lte=timezone.now()).order_by('created_date')

        for stock in stocks:
            list.append(WebYahooStockCode(str(stock.code)))

    return list
