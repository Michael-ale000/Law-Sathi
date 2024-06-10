from django.shortcuts import render
import os,requests
from dotenv import load_dotenv

# Create your views here.
load_dotenv()

def landingpage(request):
    api_key = os.getenv("Newsportal_api")
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey={}'.format(api_key)
    news = requests.get(url).json()

    a = news['articles']
    desc =[]
    title =[]
    img =[]
    url=[]

    for i in range(len(a)):
        f = a[i]
        title.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])
        url.append(f['url'])
    mylist = zip(title, desc, img,url)
    # print(title)

    context = {'mylist': mylist}

    return render(request, 'newsportal.html', context)