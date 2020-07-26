from django.db import models
from django.core.files.storage import FileSystemStorage


# 抽象クラス（作成日時、更新日時を持つクラス）
class DatedModel(models.Model):
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


# 丁目マスタ（MST_CHOME）
class Chome(models.Model):
	id = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
	chome = models.TextField()


# 分類テーブル（TBL_CATEGORY）
class Category(models.Model):
	category_cd = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
	category = models.CharField(blank=True, max_length=64)

	def __str__(self):
		return self.category


# 会員テーブル（TBL_MEMBER）
class Member(models.Model):
	member_no = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
	member_name = models.CharField(blank=True, max_length=64)
	mail = models.CharField(blank=True, max_length=128)
	tel = models.CharField(blank=True, max_length=13)
	manager_flg = models.CharField(blank=True, max_length=1)
	password = models.CharField(blank=True, max_length=128)


# 冠水状況画像テーブル（TBL_PHOTO）
class Photo(models.Model):
	id = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
	code = models.DecimalField(null=True, max_digits=10, decimal_places=0)
	dtime = models.DecimalField(max_digits=12, decimal_places=0)
	chome = models.ForeignKey(Chome, on_delete=models.CASCADE, related_name='states')
	detail = models.CharField(blank=True, max_length=64)
	member_no = models.DecimalField(max_digits=10, decimal_places=0)
	category_cd = models.DecimalField(max_digits=10, decimal_places=0, default=0)
	photo = models.ImageField(storage=FileSystemStorage())

	@property
	def data_time(self):
		s0 = self.dtime
		yy = int(s0 // 100000000)
		s0 = s0 % 100000000
		mm = int(s0 // 1000000)
		s0 = s0 % 1000000
		dd = int(s0 // 10000)
		s0 = s0 % 10000
		hr = int(s0 // 100)
		mn = int(s0 % 100)
		print(type(yy))
		print("Photo.data_time - ", yy, mm, dd, hr, mn)
		s1 = '{:04d}/{:02d}/{:02d} {:02d}:{:02d}'.format(yy, mm, dd, hr, mn)
		return s1
