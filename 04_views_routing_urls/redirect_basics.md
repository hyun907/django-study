# 리디렉션 기초

핵심: **`HttpResponseRedirect(주소)`를 반환하면 브라우저가 그 주소로 다시 접속한다.**

## 1. 숫자 주소를 글자 주소로 보내기

`/first_app/0`으로 접속하면 `/first_app/sports/`로 이동시키는 예제다.

```python
# first_app/urls.py
urlpatterns = [
    path("<str:topic>/", views.news_view),
    path("<int:num_page>", views.num_page_view),
]
```

```python
# first_app/views.py
from django.http.response import HttpResponseRedirect


def num_page_view(request, num_page):
    topics_list = list(articles.keys())  # ['sports', 'finance', 'politics']
    topic = topics_list[num_page]        # 0 → 'sports'

    return HttpResponseRedirect(topic)
```

| 접속 URL | 이동하는 곳 |
|---|---|
| `/first_app/0` | `/first_app/sports/` |
| `/first_app/1` | `/first_app/finance/` |
| `/first_app/2` | `/first_app/politics/` |

- 딕셔너리의 키 목록은 `keys()`로 가져온다. `key()`라고 쓰면 `AttributeError`가 난다
- `/first_app/5`처럼 범위를 넘는 숫자를 넣으면 `IndexError`가 나서 500 페이지가 뜬다

## 2. 이동하는 과정

```
/first_app/0
  → 302 → /first_app/sports    (HttpResponseRedirect)
  → 301 → /first_app/sports/   (Django가 끝에 / 자동 추가)
  → 200 Sports Page
```

`<str:topic>/`처럼 패턴 끝에 `/`가 있는데 `/` 없이 접속하면, Django가 `/`를 붙인 주소로 자동으로 보내준다 (`APPEND_SLASH`).

## 3. 상대 주소와 절대 주소

`HttpResponseRedirect("sports")`처럼 `/` 없이 쓰면 **지금 주소 기준**으로 이동한다. 폴더 경로와 같다.

| 지금 주소 | `"sports"`로 이동하면 |
|---|---|
| `/first_app/0` | `/first_app/sports` ✅ |
| `/first_app/0/` | `/first_app/0/sports` ❌ 404 |

끝에 `/`가 붙으면 `0/`이 폴더처럼 취급돼서 그 안으로 들어간다.

`/`로 시작하는 **절대 주소**를 쓰면 지금 주소와 상관없이 항상 같은 곳으로 간다.

```python
return HttpResponseRedirect(f"/first_app/{topic}/")
```

주소를 직접 적는 대신 URL 이름으로 만드는 방법은 다음 강의(56강 reverse URL)에서 다룬다.

## 4. 301은 브라우저가 기억한다

| 코드 | 뜻 | 브라우저 |
|---|---|---|
| 302 | 임시 이동 | 매번 서버에 다시 물어본다 |
| 301 | 영구 이동 | 저장해 두고 다음부터 서버에 묻지 않고 바로 이동한다 |

`HttpResponseRedirect`는 302다. Django가 `/`를 자동으로 붙일 때는 301이다.

URL 패턴을 바꿨는데도 예전 주소로 이동한다면 브라우저에 저장된 301 때문일 수 있다. 시크릿 창으로 열거나 `localhost` 대신 `127.0.0.1`로 접속해서 확인한다.

## 정리

`HttpResponseRedirect`로 다른 주소로 보낼 수 있다. `/` 없이 쓴 주소는 지금 주소 기준으로 이동하므로, 지금 주소 끝의 `/`에 따라 이동하는 곳이 달라진다. 항상 같은 곳으로 보내려면 `/`로 시작하는 절대 주소를 쓴다.
