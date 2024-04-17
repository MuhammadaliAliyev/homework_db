from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User

# Create your views here.
def urls(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        url = request.POST.get('url')
        User.objects.create(name=name, url=url)
        return redirect('/')
    queryset = User.objects.all()

    if request.GET.get('search'):
        queryset = User.objects.filter(name__icontains=request.GET.get('search'))
    
    context = {'urls': queryset}
    return render(request, 'urls.html', context)

def delete_url(request, id):
    User.objects.get(id=id).delete()
    return redirect('/')

def update_url(request, id):
    queryset = User.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        url = data.get('url')

        queryset.name = name
        queryset.url = url
        queryset.save()
        return redirect('/')
    context = {'url': queryset}
    return render(request, 'update_url.html', context)