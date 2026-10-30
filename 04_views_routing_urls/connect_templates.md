# 템플릿에 뷰 연결하기

핵심: **HTML 파일을 `templates` 폴더에 두고, `settings.py`에 위치를 알려준 뒤, view에서 `render()`로 반환한다.**

## 1. 폴더 구조

```
my_site/
├── manage.py
├── my_site/
│   └── settings.py
├── first_app/
│   ├── urls.py
│   └── views.py
└── templates/              ← 직접 만든 폴더 (manage.py와 같은 위치)
    └── first_app/          ← 앱 이름으로 한 번 더 나눔
        └── example.html
```

`templates/` 안에 앱 이름 폴더를 한 번 더 만드는 이유: 여러 앱에 같은 이름의 `index.html`이 있어도 `first_app/index.html`, `blog/index.html`처럼 구분할 수 있다.

## 2. settings.py에 templates 위치 등록

```python
# my_site/settings.py
import os

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates/")],  # 여기 추가
        "APP_DIRS": True,
        ...
    },
]
```

- `BASE_DIR`은 `manage.py`가 있는 폴더다
- `DIRS`: Django가 템플릿을 찾을 폴더 목록이다. 여기에 등록하지 않으면 `TemplateDoesNotExist` 오류가 난다
- `APP_DIRS: True`: 각 앱 안의 `templates/` 폴더도 찾아본다
- `os.path.join` 대신 `BASE_DIR / "templates"`로 써도 된다 (`BASE_DIR`이 `Path` 객체라서)

## 3. view에서 render로 반환

```python
# first_app/views.py
from django.shortcuts import render


def simple_view(request):
    return render(request, "first_app/example.html")
```

```python
# first_app/urls.py
urlpatterns = [
    path("", views.simple_view),  # /first_app/
]
```

- `render(request, 템플릿 경로)`: HTML 파일을 읽어서 `HttpResponse`로 만들어 준다
- 템플릿 경로는 `templates/` **다음부터** 적는다 (`templates/first_app/example.html` → `"first_app/example.html"`)
- `.html` 확장자까지 적어야 한다

`/first_app/`에 접속하면 `example.html` 내용이 표시된다.

## 4. HttpResponse vs render

| | `HttpResponse("글자")` | `render(request, "파일.html")` |
|---|---|---|
| 내용 | 코드에 직접 쓴 문자열 | HTML 파일 |
| 가져오는 곳 | `django.http` | `django.shortcuts` |
| 용도 | 간단한 테스트 | 실제 페이지 |

## 정리

`templates/앱이름/파일.html`에 HTML을 만들고, `settings.py`의 `DIRS`에 `templates` 폴더를 등록한 뒤, view에서 `render(request, "앱이름/파일.html")`을 반환하면 HTML 페이지가 보인다.
