from django.conf.urls import *
from HelloWorld.view import hello
from HelloWorld.testdb import save
<<<<<<< HEAD
from HelloWorld.wechat_python_sdk import checkout
=======
>>>>>>> b798cb59ea60320c85ecfa754f63eeca32834ede


urlpatterns = patterns("",
                       ('^hello/$', hello),
                       ('^save/$', save),
<<<<<<< HEAD
                       ("^checkout$", checkout),
=======
>>>>>>> b798cb59ea60320c85ecfa754f63eeca32834ede
                       )
