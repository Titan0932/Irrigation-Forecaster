from django.shortcuts import render
from main_app.forms import getDetails
from django.http import HttpResponse
from main_app.process import get_data

def display_home(request):
    return render(request,'index.html',context=None)

def harvest_img(request):
    return render(request,'harvest.html',context=None)

def showForm(request):
    if request.method=='GET':
        form=getDetails()
        return render(request,'form.html', {'form':form} )

    if request.method=='POST':
        results=get_data(request.POST)
        
        return render(request, 'result.html',{'month':results[0], 'day':results[1]})