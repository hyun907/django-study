# Django 작동 방식

핵심: **Django는 요청(request)이 들어오면 URL을 보고 맞는 view 함수를 찾아 실행하고, 그 결과를 응답(response)으로 돌려준다.**

## 1. 요청과 응답

```
브라우저 ──요청(request)──▶ Django ──응답(response)──▶ 브라우저
```

Django에서 view 함수는 모두 같은 규칙을 따른다.

- 매개변수로 `request`(요청 정보)를 받는다
- `HttpResponse`(응답)를 반환한다

## 2. 코드로 보는 흐름

`/posts/`에 접속했을 때 실행되는 코드를 순서대로 보면 다음과 같다.

**① 프로젝트의 `urls.py`**: URL 앞부분을 보고 어느 앱으로 보낼지 정한다

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("posts/", include("posts.urls")),  # posts/로 시작하면 posts 앱으로
]
```

**② 앱의 `posts/urls.py`**: 나머지 URL을 보고 어떤 view를 실행할지 정한다

```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.post_list),  # posts/ 뒤에 아무것도 없으면 post_list 실행
]
```

**③ 앱의 `posts/views.py`**: 요청을 처리하고 응답을 반환한다

```python
from django.http import HttpResponse


def post_list(request):
    return HttpResponse("게시글 목록")
```

결과적으로 브라우저에는 `게시글 목록`이 표시된다.

## 3. DB와 템플릿까지 쓰면

실제로는 view에서 DB의 데이터를 꺼내 템플릿(HTML)에 넣어서 응답한다.

```python
from django.shortcuts import render

from .models import Post


def post_list(request):
    posts = Post.objects.all()                       # 1. Model: DB에서 데이터 조회
    return render(request, "posts/post_list.html",   # 2. Template: HTML에 데이터를 채워서
                  {"posts": posts})                  # 3. 응답으로 반환
```

```html
<!-- templates/posts/post_list.html -->
{% for post in posts %}
    <p>{{ post.title }}</p>
{% endfor %}
```

`render()`는 템플릿에 데이터를 채운 결과를 `HttpResponse`로 만들어 준다. 그래서 view가 응답을 반환한다는 규칙은 그대로다.

## 4. 주요 파일의 역할

| 파일 | 역할 |
|---|---|
| `manage.py` | 서버 실행, 앱 생성 등 명령어 실행 (`python manage.py runserver`) |
| `settings.py` | 프로젝트 설정 (설치된 앱 목록, DB, 템플릿 경로 등) |
| `urls.py` | URL과 view 연결 |
| `views.py` | 요청 처리, 응답 반환 |
| `models.py` | 데이터 구조 정의, DB와 연결 |
| `templates/` | 화면(HTML) |

## 정리

요청이 들어오면 Django는 `urls.py`에서 URL에 맞는 view를 찾아 실행한다. view는 필요하면 Model로 데이터를 가져오고 Template으로 HTML을 만든 뒤, 그 결과를 응답으로 돌려준다.
