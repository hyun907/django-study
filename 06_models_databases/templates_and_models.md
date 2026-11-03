# 템플릿과 데이터베이스 모델 연결하기

요약: **view에서 모델로 데이터를 꺼내 `context`에 담고, 템플릿에서 `{% for %}`로 꺼내 쓴다.**

```
/office/ 요청 ──▶ urls.py ──▶ views.list_patients ──▶ Patient.objects.all()
                                      │
                                      ▼
                         render(..., context={'patients': ...})
                                      │
                                      ▼
                          office/list.html 에서 {{ person.last_n }}
```

## 1. URL 연결

```python
# my_site/urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('office/', include('office.urls')),
]
```

```python
# office/urls.py (새로 만듦)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_patients, name='list_patients'),
]
```

`/office/`로 들어온 요청을 `office` 앱의 `urls.py`로 넘긴다. ([04. 뷰와 URL 라우팅](../04_views_routing_urls/README.md))

## 2. view: 모델에서 꺼내서 context로 전달

```python
# office/views.py
from django.shortcuts import render
from . import models

def list_patients(request):
    all_patients = models.Patient.objects.all()
    context_list = {
        'patients': all_patients
    }
    return render(request, 'office/list.html', context=context_list)
```

shell에서 하던 `Patient.objects.all()`을 view 안에서 그대로 쓴다. 딕셔너리의 키(`'patients'`)가 템플릿에서 쓰는 변수 이름이 된다.

`render()`의 인자 이름은 정확히 `context`다. 오타를 내면 바로 에러가 난다.

```
TypeError: render() got an unexpected keyword argument 'ccontent'
```

## 3. 템플릿: for문으로 출력

```html
<!-- office/templates/office/list.html -->
<body>
    {% for person in patients %}
    <p>{{ person.last_n }}</p>
    {% endfor %}
</body>
```

`patients`는 QuerySet이라서 `{% for %}`로 하나씩 꺼낼 수 있다. 꺼낸 각 객체의 필드는 파이썬처럼 `person.last_n`, `person.age`로 접근한다.

## 정리

| 위치 | 하는 일 |
|---|---|
| `my_site/urls.py` | `office/` 요청을 `office.urls`로 넘김 |
| `office/urls.py` | `''` → `list_patients` view 연결 |
| `office/views.py` | `Patient.objects.all()`로 꺼내서 `context`로 전달 |
| `office/templates/office/list.html` | `{% for %}`와 `{{ 객체.필드 }}`로 출력 |
