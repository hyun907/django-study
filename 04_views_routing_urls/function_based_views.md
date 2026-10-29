# Function 기반 뷰

핵심: **view는 `request`를 받아 `HttpResponse`를 반환하는 함수이고, `urls.py`에서 URL과 연결해야 접속할 수 있다.**

## 1. Function 기반 뷰의 기본 형태

```python
# first_app/views.py
from django.http.response import HttpResponse


def simple_view(request):              # 1. request를 받아서
    return HttpResponse("SIMPLE VIEW")  # 2. HttpResponse를 반환
```

- 함수 이름은 자유롭게 정할 수 있다
- 첫 번째 매개변수는 항상 `request`다. Django가 요청 정보를 넣어서 호출한다
- `HttpResponse`는 `django.http`에서 가져와도 된다. `from django.http import HttpResponse`가 더 많이 쓰인다

## 2. 뷰는 프로젝트에도 둘 수 있다

보통 view는 앱의 `views.py`에 만들지만, 프로젝트 폴더에 `views.py`를 직접 만들어서 둘 수도 있다.

```python
# my_site/views.py (직접 만든 파일)
from django.http.response import HttpResponse


def home_view(request):
    return HttpResponse("HOME VIEW!")
```

```python
# my_site/urls.py
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("first_app/", include("first_app.urls")),
    path("", views.home_view),  # 메인 페이지(/)
]
```

메인 페이지처럼 특정 앱에 속하지 않는 화면은 이렇게 프로젝트에 둘 수 있다.

## 3. URL이 합쳐지는 방식

`include()`를 쓰면 프로젝트 `urls.py`의 경로 뒤에 앱 `urls.py`의 경로가 이어 붙는다.

```python
# first_app/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("simple_view", views.simple_view),
]
```

```
프로젝트 urls.py    "first_app/"
앱 urls.py       +  "simple_view"
                 =  /first_app/simple_view
```

앱 `urls.py`에는 `first_app/`을 다시 적지 않는다. **`first_app/` 뒤에 남은 부분**만 적는다.

| 접속 URL | 실행되는 view | 화면 |
|---|---|---|
| `/` | `home_view` | `HOME VIEW!` |
| `/first_app/simple_view` | `simple_view` | `SIMPLE VIEW` |

## 4. URL 끝의 `/`

`path()`에 적은 문자열과 **정확히 일치**해야 view가 실행된다.

```python
path("simple_view", views.simple_view)   # /first_app/simple_view 만 열림
                                         # /first_app/simple_view/ 는 404
path("simple_view/", views.simple_view)  # /first_app/simple_view/ 가 열림
```

Django에서는 `"simple_view/"`처럼 **끝에 `/`를 붙이는 것이 관례**다. 끝에 `/`를 붙여 두면 `/`를 빼고 접속해도 Django가 `/`를 붙인 주소로 자동으로 이동시켜 준다. (`settings.py`의 `APPEND_SLASH`, 기본값 `True`)

## 정리

view는 `request`를 받아 `HttpResponse`를 반환하는 함수다. 앱에도, 프로젝트에도 둘 수 있다. URL은 프로젝트 `urls.py`와 앱 `urls.py`의 경로가 이어 붙어서 만들어진다.
