# pylint: disable-all

from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'index.html')
 
def result(request):
    n1 = int(request.POST['a'])
    n2 = int(request.POST['b'])
    res = n1 + n2
    return render(request, 'result.html', {'result':res})