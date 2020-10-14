from bs4 import BeautifulSoup
from urllib import request
# コマンドラインからの実行した時は、インポートされない（相対インポートが出来ないっぽい。attempted relative import with no known parent package）
# つまりmodelsを組み込む設計自体が良くない
from .models import Stock
import importlib

# decimalクラスで定義してるDecimalメソッドのみをインポート
# もしfromが無い場合だと、このクラスで使用してるDecimalをdecimal.Decimalと書き換えないとダメ
from decimal import Decimal

# reクラスをインポート（reで定義してるメソッドを全て使える）
import re

class WebYahooStockCode:
    def __init__(self,code):
        self.__code = code
        self.PER = 4
        self.PBR = 5
        self.NONE_STR = "---"
        url = 'https://info.finance.yahoo.co.jp/search/?query=' + self.__code
        response = request.urlopen(url)
        self.soup = BeautifulSoup(response, "html.parser")
        if self.soup.find("span",{"class":"sign"}) is None:
            self.__existsCode = True
            self.__company_name = self.soup.find("th",{"class":"symbol"}).text
            self.__industry_name = self.soup.find("dd",{"class":"category yjSb"}).text
            self.soup_list = self.soup.find_all("div",{"class":"lineFi yjMS clearfix"})
            self._getPer()
            self._getPbr()
        else:
            self.__existsCode = False

    def _getPer(self):
        self.__per_decimal, self.__per_text = self.__strCost(self.__soupExtraction(self.PER), "20.00")

    def _getPbr(self):
        self.__pbr_decimal, self.__pbr_text = self.__strCost(self.__soupExtraction(self.PBR), "1.00")

    def __soupExtraction(self, type):
        result = re.search('[+-]?([0-9]+(\.[0-9]*)?|\.[0-9]+)([eE][+-]?[0-9]+)?', self.soup_list[type].find("strong").text)

        if result is not None:
            return result[0]
        else:
            return self.NONE_STR

    # 複数の返り値確認用のメソッド
    # 普通に組むなら割安割高の判定は、プロパティ取得メソッドに実装すれば良いだけ
    def __strCost(self, magnification, comparison_decimal):
        if magnification != self.NONE_STR:
            if Decimal(magnification) < Decimal(comparison_decimal):
                return magnification + "倍", "割安"
            else:
                return magnification + "倍", "割高"

        else:
            return self.NONE_STR + "倍", "不明"

    # プロパティを定義
    @property
    def company_name(self):
        return self.__company_name

    @property
    def industry_name(self):
        return self.__industry_name

    @property
    def per_decimal(self):
        return self.__per_decimal

    @property
    def per_text(self):
        return self.__per_text

    @property
    def pbr_decimal(self):
        return self.__pbr_decimal

    @property
    def pbr_text(self):
        return self.__pbr_text

    @property
    def stock_code(self):
        return self.__code

    @property
    def existsCode(self):
        return self.__existsCode

    @property
    def isRegistedCode(self):
        return bool(Stock.objects.filter(code=int(self.__code)))

    # プロパティのsetterメソッドは、propertyの後に定義しないとエラーになる（プロパティ定義前にプロパティのメソッドは呼べない）
    # このクラスにsetterは不要だけど、お試しで実装。値を書き換えてほしくない場合は、以下のsetterメソッドを全て削除する事
    @industry_name.setter
    def industry_name(self, industry_name):
        self.__industry_name = industry_name

    @per_decimal.setter
    def per_decimal(self, per_decimal):
        self.__per_decimal = per_decimal

    @per_text.setter
    def per_text(self, per_text):
        self.__per_text = per_text

    @pbr_decimal.setter
    def pbr_decimal(self, pbr_decimal):
        self.__pbr_decimal = pbr_decimal

    @pbr_text.setter
    def pbr_text(self, pbr_text):
        self.__pbr_text = pbr_text

# コマンドプロンプトで直接ファイルを実行した場合、if文の中身を実行する（例：　c:\>py web_yahoo_stockcode.py）
# 但しコマンドラインから実行する前に、modelsのインポートとmodelsを使ったメソッドをコメントアウトすること
if __name__ == '__main__':
    web = WebYahooStockCode("3284")
    print(web.existsCode)

    if web.existsCode == True:
        # プロパティを直接呼び出す事で、getterと同じ動作となる。
        print(web.company_name)
        print(web.industry_name)
        print(web.per_decimal)
        print(web.per_text)
        print(web.pbr_decimal)
        print(web.pbr_text)
        web.industry_name = "セッターテスト"
        print(web.industry_name)
        print(web._getPer)
