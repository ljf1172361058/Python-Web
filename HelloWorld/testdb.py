# -*- coding: utf-8 -*-

from django.http import HttpResponse

from TestModel.models import Test

# 数据库操作
def save(request):
	test = Test(name='admin')
	test.save()
	return HttpResponse("<p>数据添加成功！</p>")
