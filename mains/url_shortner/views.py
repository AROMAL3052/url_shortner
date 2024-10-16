from django.shortcuts import render, redirect
from .forms import urlform
from .models import urldb 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout 
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from urlshortner.utils import shorten_url
from django.core.paginator import Paginator


def url_create(request):
    form =urlform()
    obj=urldb.objects.filter(author=request.user).values('id')
    c=0
    for i in obj:
        c=c+1
    if c<5:  
        if request.method == 'POST':
            surl=request.POST['url']   
           
            form = urlform(request.POST)
        
            if form.is_valid():
                data=form.save(commit=False)
                data.short_url=shorten_url(surl,is_permanent=False)
                data.author=request.user
                data.save()
              
                return redirect('retrieve')
    message="limit exceeded, can only add five objects."        
    context={'message':message,'form':form}        
    
    return render(request, 'create.html', context)

def home(request):
    return render(request, 'retrieve.html')

def url_read(request):
    
    product_list=urldb.objects.filter(author=request.user)
    paginator = Paginator(product_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    if request.method == "POST":
        titles=request.POST.get("title")
        if titles:
            product_list=urldb.objects.filter(title__istartswith=titles).filter(author=request.user)
        else:
            product_list=urldb.objects.none() 
        return render(request,'retrieve.html',{'page_obj':product_list})   
        
    return render(request,'retrieve.html',{'page_obj':page_obj})

def searchlist(request):
    if 'term' in request.GET:
        all=urldb.objects.filter(title__istartswith = request.GET.get("term")).filter(author=request.user)
        titles=list()
        for i in all:
            titles.append(i.title)
    return JsonResponse(titles,safe=False)    

def url_update(request, id):
    product = urldb.objects.get(pk=id)
    if request.method == 'POST':
        form = urlform(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('retrieve')
    else:
        form =urlform(instance=product)           
    return render(request, 'update.html', {'form': form})


def url_delete(request,id):
    product=urldb.objects.get(pk=id)  
    if request.method == 'POST':
        product.delete()
        return redirect('retrieve')
    
    return render(request,'delete.html',{'product':product})


def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def homepage(request):
    return render(request,'home.html')


@login_required(login_url='/login/')
def logouts(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    context = {
        'user': request.user
    }

    return render(request, 'logout.html', context)



