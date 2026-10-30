from django.shortcuts import render
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

articles = {
    'sports': 'Sports Page',
    'finance': 'Finance Page',
    'politics': 'Politics Page'
}

def simple_view(request):
    return render(request, 'first_app/example.html') # templates/ 다음 경로부터 적음

def news_view(request, topic):
    try:
        result = articles[topic]
        return HttpResponse(result)
    except KeyError:
        raise Http404("404 GENERIC ERROR")

def add_view(request, num1, num2):
    add_result = num1 + num2
    result = f"{num1} + {num2} = {add_result}"
    return HttpResponse(result)

def num_page_view(request, num_page):
    topics_list = list(articles.keys()) # ['sports', 'finance', 'politics']
    topic = topics_list[num_page]

    return HttpResponseRedirect(reverse('topic-page', args=[topic]))
