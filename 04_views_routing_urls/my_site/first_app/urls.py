from django.urls import path
from . import views

# first_app/이 붙어서 나가기 때문에 아래는 공백임
urlpatterns = [
    path('', views.simple_view), # domain.com/first_app/
    path('<int:num_page>', views.num_page_view),
    path('<str:topic>/', views.news_view, name='topic-page'),
    path('<int:num1>/<int:num2>', views.add_view),
]
