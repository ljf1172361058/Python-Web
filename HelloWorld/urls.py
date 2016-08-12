from django.conf.urls import *
from HelloWorld.view import hello
from HelloWorld.testdb import save
from HelloWorld.wechat_python_sdk import checkout


urlpatterns = patterns("",
                       ('^hello/$', hello),
                       ('^save/$', save),
                       ("^checkout$", checkout),
                       )
