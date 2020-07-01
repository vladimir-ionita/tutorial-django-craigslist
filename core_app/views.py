from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests

from . import models

CRAIGSLIST_BASE_SEARCH_URL = "https://chicago.craigslist.org/search/?query={}"
CRAIGSLIST_BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"


def home(request):
    return render(request, 'base.html')


def search(request):
    search_query = request.POST.get('search')
    models.Search.objects.create(search=search_query)

    craigslist_search_url = CRAIGSLIST_BASE_SEARCH_URL.format(quote_plus(search_query))
    response = requests.get(craigslist_search_url)
    data = response.text

    soup = BeautifulSoup(data, features='html.parser')
    craiglist_listings = soup.find_all('li', {'class': 'result-row'})
    final_listings = []
    for listing in craiglist_listings:
        post_title = listing.find(class_='result-title').text
        post_url = listing.find('a').get('href')

        if listing.find(class_='result-price'):
            post_price = listing.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if listing.find(class_='result-image').get('data-ids'):
            post_image_id = listing.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = CRAIGSLIST_BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_listings.append((post_title, post_url, post_price, post_image_url))


    view_context = {
        'search_query': search_query,
        'listings': final_listings
    }
    return render(request, 'core_app/search.html', view_context)
