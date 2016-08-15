from django.conf.urls import *
from HelloWorld.view import hello
from HelloWorld.testdb import save

urlpatterns = patterns("",
                       ('^hello/$', hello),
                       ('^save/$', save),
                       )
