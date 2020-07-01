from django.shortcuts import render


def home(request):
    return render(request, 'base.html')


def search(request):
    search_query = request.POST.get('search')
    models.Search.objects.create(search=search_query)
