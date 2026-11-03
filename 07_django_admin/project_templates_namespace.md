# 프로젝트 공용 템플릿과 app_name

요약: **여러 앱이 같이 쓰는 `base.html`은 프로젝트 루트의 `templates/`에 두고 `DIRS`에 등록한다. URL 이름은 `app_name`으로 앱별로 구분한다.**

## 1. 폴더 구조

```
my_car_site/                 ← 프로젝트 루트 (BASE_DIR)
├── manage.py
├── templates/
│   └── base.html            ← 공용 템플릿 (DIRS로 찾음)
├── cars/
│   ├── urls.py              ← app_name = 'cars'
│   └── templates/cars/
│       ├── list.html        ← 앱 템플릿 (APP_DIRS로 찾음)
│       ├── add.html
│       └── delete.html
└── my_car_site/             ← 설정 폴더 (settings.py, urls.py)
```

안쪽 `my_car_site/`는 앱이 아니라 프로젝트 전체 설정을 담는 폴더다. 기능은 `cars` 같은 앱이 맡는다.

## 2. `BASE_DIR`과 `DIRS` 등록

```python
# my_car_site/settings.py
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # 여기 추가
        'APP_DIRS': True,
        ...
    },
]
```

`BASE_DIR`이 가리키는 곳:

```
__file__           → .../my_car_site/my_car_site/settings.py
.parent            → .../my_car_site/my_car_site/   (설정 폴더)
.parent.parent     → .../my_car_site/               (프로젝트 루트) = BASE_DIR
```

| 설정 | 찾는 곳 |
|---|---|
| `DIRS` | 직접 등록한 폴더 (여기선 루트의 `templates/`) |
| `APP_DIRS: True` | 각 앱 안의 `templates/` |

([템플릿에 뷰 연결하기](../04_views_routing_urls/connect_templates.md)에서는 `os.path.join`으로 등록했다. 결과는 같다.)

## 3. base.html 상속

```html
<!-- templates/base.html -->
<body>
    <a href="{% url 'cars:list' %}">list</a>
    <a href="{% url 'cars:add' %}">add</a>
    <a href="{% url 'cars:delete' %}">delete</a>

    {% block content %}
    {% endblock %}
</body>
```

```html
<!-- cars/templates/cars/list.html -->
{% extends "base.html" %}

{% block content %}
    <h1>List html</h1>
    ...
{% endblock %}
```

**실수 사례: 링크가 안 뜸**

`base.html`에 링크를 만들고 `DIRS`도 등록했는데 화면에 링크가 안 나왔다. 원인은 `list.html`이 `<!DOCTYPE html>`부터 시작하는 독립 HTML이었고 `extends`를 쓰지 않았기 때문이다.

- `DIRS` 등록은 Django가 `base.html`을 **찾을 수 있게** 해줄 뿐이고 자동으로 붙여주지 않는다
- 자식 템플릿에서 `{% extends "base.html" %}`를 **맨 첫 줄**에 써야 한다
- `base.html`에 `{% block content %}` 자리가 있어야 자식 내용이 들어간다

## 4. `app_name`으로 URL 이름 구분하기

```python
# cars/urls.py
app_name = 'cars'

urlpatterns = [
    path('list/', views.list, name='list'),
    path('add/', views.add, name='add'),
    path('delete/', views.delete, name='delete'),
]
```

```python
# my_car_site/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('cars/', include('cars.urls')),
]
```

`app_name`을 붙이면 URL 이름이 `앱이름:URL이름` 형태가 된다.

```
'cars:list'  →  'cars/' + 'list/'  →  /cars/list/
```

다른 앱에도 `name='list'`가 있을 수 있다. `app_name`이 없으면 이름이 겹쳐서 어느 `list`인지 알 수 없다. `cars:list`, `users:list`처럼 앞에 앱 이름을 붙여서 구분한다.

| 어디서 | 쓰는 법 |
|---|---|
| 템플릿 | `{% url 'cars:list' %}` |
| view | `reverse('cars:list')`, `redirect('cars:list')` |

## 정리

| 위치 | 하는 일 |
|---|---|
| `settings.py` | `'DIRS': [BASE_DIR / 'templates']`로 공용 템플릿 폴더 등록 |
| `templates/base.html` | 공통 링크 + `{% block content %}` 자리 |
| `cars/templates/cars/*.html` | 첫 줄 `{% extends "base.html" %}`, 내용은 `{% block content %}` 안에 |
| `cars/urls.py` | `app_name = 'cars'` → `'cars:list'`로 부름 |
