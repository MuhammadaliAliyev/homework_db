import random
import string
from django.shortcuts import render, redirect
from .models import UrlData
from .forms import Url
# Create your views here.
def urlShort(request):
    if request.method == 'POST':
        form = Url(request.POST)
        if form.is_valid():
            slug = ''.join(random.choice(string.ascii_letters) for x in range(10))
            url = form.cleaned_data['url']
            new_url = UrlData(url=url, slug=slug)
            new_url.save()

            return redirect('url:index')
    else:
        form = Url()
    data = UrlData.objects.last()
    context = {
        'form':form,
        'data':data,
    }
    return render(request, 'index.html', context)
        
def urlRedirect(request, slugs):
    data = UrlData.objects.get(slug = slugs)
    return redirect(data.url)