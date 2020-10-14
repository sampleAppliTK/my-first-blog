from django.conf import settings
from django.db import models
from django.utils import timezone
# バリデーションを実装するためにインポートが必要（未定義エラーが出たら大体インポートしてないのが原因）
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Stock(models.Model):
    # ユーザー名
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 株価コード　1000～9999までの登録可能とする
    code = models.PositiveSmallIntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])

    # 登録日付
    created_date = models.DateTimeField(default=timezone.now)

    def regist(self):
        self.created_date = timezone.now()
        self.save()

    class Meta:
        constraints = [
            # １ユーザーに同じコードを複数登録させない
            models.UniqueConstraint(fields=['author', 'code'], name='stock_code_booking'),
        ]

    def __str__(self):
        return str(self.code)
