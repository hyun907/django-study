# ResponseNotFound와 404 페이지

핵심: **없는 페이지를 요청받으면 서버 오류(500)가 아니라 404로 응답한다.**

## 1. 404 = Not Found

`404`는 상태 코드(번호)이고 `Not Found`는 그 번호의 이름이다. 둘은 같은 뜻이다.

```
HTTP/1.1 404 Not Found
```

## 2. 404를 보내는 두 가지 방법

```python
# 방법 1: 응답을 직접 만들어서 return
from django.http import HttpResponseNotFound

def news_view(request, topic):
    try:
        return HttpResponse(articles[topic])
    except KeyError:
        return HttpResponseNotFound("페이지가 없습니다")
```

```python
# 방법 2: 예외를 raise해서 Django에게 맡김
from django.http import Http404

def news_view(request, topic):
    try:
        return HttpResponse(articles[topic])
    except KeyError:
        raise Http404("404 GENERIC ERROR")
```

| | `HttpResponseNotFound` | `Http404` |
|---|---|---|
| 쓰는 법 | `return` | `raise` |
| 화면 | 직접 넣은 내용 | Django의 404 페이지 (`404.html`) |

보통은 `raise Http404`를 쓴다. 사이트 전체에서 같은 404 페이지를 보여줄 수 있다.

## 3. 직접 만든 404.html은 DEBUG = False일 때만 보인다

`DEBUG = True`면 개발용 노란 디버그 페이지가 대신 뜬다.

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
```

`DEBUG = False`가 되면 Django는 실제 서비스 중이라고 보고, `ALLOWED_HOSTS`에 등록된 주소로 온 요청만 받는다. 가짜 Host로 들어오는 요청을 막기 위해서다. (`DEBUG = True`일 때는 localhost를 자동으로 허용한다.)

## 정리

없는 페이지에는 `raise Http404`로 404를 보낸다. 직접 만든 404 페이지를 확인하려면 `DEBUG = False`로 바꾸고 `ALLOWED_HOSTS`에 주소를 등록해야 한다.
