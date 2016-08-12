# -*- coding: utf-8 -*-

#from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    context          = {}
    context['hello'] = '这是李智慧的Python服务器'
    return render(request, 'hello.html', context)
