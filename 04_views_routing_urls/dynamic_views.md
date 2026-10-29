# 동적 뷰 - 라우팅 로직

핵심: **URL의 일부를 `<타입:이름>`으로 적으면, 그 자리에 들어온 값이 view 함수의 매개변수로 전달된다.**

## 1. URL에서 값 받기

URL마다 view를 하나씩 만들면 페이지가 늘어날 때마다 view도 늘어난다.

```python
path("sports/", views.sports_view),
path("finance/", views.finance_view),
path("politics/", views.politics_view),
```

URL의 바뀌는 부분을 `<>`로 감싸면 view 하나로 처리할 수 있다.

```python
# first_app/urls.py
urlpatterns = [
    path("<str:topic>/", views.news_view),
]
```

```python
# first_app/views.py
articles = {
    "sports": "Sports Page",
    "finance": "Finance Page",
    "politics": "Politics Page",
}


def news_view(request, topic):  # URL의 <topic> 값이 topic으로 들어온다
    return HttpResponse(articles[topic])
```

| 접속 URL | `topic` 값 | 화면 |
|---|---|---|
| `/first_app/sports/` | `"sports"` | `Sports Page` |
| `/first_app/finance/` | `"finance"` | `Finance Page` |

**URL의 `<topic>`과 view의 매개변수 이름 `topic`이 같아야 한다.** 다르면 오류가 난다.

## 2. 타입 변환 (Path Converter)

`<타입:이름>`의 타입은 어떤 값을 받을지, 어떤 자료형으로 넘길지를 정한다.

```python
path("<int:num1>/<int:num2>", views.add_view),
```

```python
def add_view(request, num1, num2):
    add_result = num1 + num2
    result = f"{num1} + {num2} = {add_result}"
    return HttpResponse(result)
```

`/first_app/3/4`에 접속하면 `3 + 4 = 7`이 표시된다.

`int`로 받았기 때문에 `num1`, `num2`는 **정수**다. `str`로 받았다면 문자열이라서 `"3" + "4"` = `"34"`가 된다.

| 타입 | 받는 값 | 예 |
|---|---|---|
| `str` | `/`를 제외한 모든 문자 (기본값) | `sports` |
| `int` | 0 이상의 정수 | `3` |
| `slug` | 영문, 숫자, `-`, `_` | `my-first-post` |
| `uuid` | UUID 형식 | `075194d3-6885-417e-a8a8-6c931e272f00` |
| `path` | `/`를 포함한 모든 문자 | `a/b/c` |

타입을 생략하고 `<topic>`만 적으면 `str`로 처리된다.

## 3. 위에서부터 순서대로 비교한다

Django는 `urlpatterns`를 **위에서부터** 비교해서 처음 일치하는 view를 실행한다.

```python
urlpatterns = [
    path("<str:topic>/", views.news_view),
    path("<int:num1>/<int:num2>", views.add_view),
]
```

- `/first_app/sports/` → 첫 번째와 일치 → `news_view`
- `/first_app/3/4` → `str`은 `/`를 받지 못해서 첫 번째와 일치하지 않음 → 두 번째와 일치 → `add_view`
- `/first_app/3/` → 첫 번째와 일치 → `news_view(topic="3")`

## 4. 없는 값이 들어오면?

```
/first_app/music/
```

`articles`에 `"music"` 키가 없어서 `articles[topic]`에서 **KeyError**가 나고, 서버 오류(500) 페이지가 표시된다.

없는 페이지는 서버 오류가 아니라 **404(페이지 없음)** 로 응답하는 게 맞다. 다음 강의(54강)에서 `HttpResponseNotFound`로 다룬다.

## 정리

`<타입:이름>`으로 URL의 일부를 변수처럼 받아 view 하나로 여러 페이지를 처리할 수 있다. 타입을 `int`로 지정하면 정수로 변환되어 전달되고, URL 패턴은 위에서부터 순서대로 비교된다.
