# reverse URL과 URL name

핵심: **URL에 `name`을 붙여두면, `reverse(이름)`으로 그 URL 주소를 만들어낼 수 있다.**

## 1. 주소를 직접 적으면 생기는 문제

```python
return HttpResponseRedirect(topic)                  # 지금 주소 기준이라 /가 붙으면 깨짐
return HttpResponseRedirect(f"/first_app/{topic}/") # 동작은 하지만 주소가 코드에 박혀 있음
```

`urls.py`에서 `first_app/`을 `news/`로 바꾸면, 주소를 적어둔 코드도 전부 찾아서 고쳐야 한다.

## 2. URL에 이름 붙이기

```python
# first_app/urls.py
urlpatterns = [
    path("<str:topic>/", views.news_view, name="topic-page"),
    path("<int:num_page>", views.num_page_view),
]
```

이름은 **이동할 목적지** URL에 붙인다. 여기서는 `news_view`가 목적지다.

## 3. reverse로 주소 만들기

```python
# first_app/views.py
from django.urls import reverse


def num_page_view(request, num_page):
    topics_list = list(articles.keys())
    topic = topics_list[num_page]

    return HttpResponseRedirect(reverse("topic-page", args=[topic]))
```

`reverse("topic-page", args=["sports"])` → `"/first_app/sports/"`

- `args`에 넣은 값이 URL의 `<topic>` 자리에 들어간다
- `/`로 시작하는 전체 주소가 만들어져서, 지금 주소에 상관없이 항상 같은 곳으로 간다
- 끝의 `/`까지 붙어서 나오기 때문에 Django가 `/`를 붙이는 301 이동도 생기지 않는다

```
/first_app/0  → 302 → /first_app/sports/  → 200 Sports Page
```

`urls.py`에서 주소를 바꿔도 이름만 그대로면 `reverse`가 바뀐 주소를 알아서 만든다.

## 4. 이름을 엉뚱한 곳에 붙이면

```python
path("<int:num_page>", views.num_page_view, name="topic-page"),  # ❌
```

```
NoReverseMatch: Reverse for 'topic-page' with arguments '('sports',)' not found.
1 pattern(s) tried: ['first_app/(?P<num_page>[0-9]+)\\Z']
```

`topic-page`가 숫자만 받는 URL을 가리키는데 `'sports'`를 넣어서 주소를 만들 수 없다는 뜻이다. `NoReverseMatch`가 나면 **이름이 어느 URL에 붙어 있는지**와 **`args` 값이 그 URL 타입에 맞는지**를 확인한다.

## 정리

URL에 `name`을 붙이고 `reverse(이름, args=[값])`로 주소를 만든다. 주소를 코드에 직접 적지 않아도 되고, URL이 바뀌어도 이름만 같으면 그대로 동작한다.
