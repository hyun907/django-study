# Django 관리자(Admin)와 모델

요약: **`createsuperuser`로 관리자 계정을 만들고, `admin.py`에 모델을 등록하면 `/admin/`에서 데이터를 추가, 수정, 삭제할 수 있다.**

## 1. 관리자 페이지 들어가기

`urls.py`에 처음부터 `admin/` 경로가 들어 있다.

```python
# my_car_site/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('cars/', include('cars.urls')),
]
```

로그인하려면 관리자 계정이 필요하다.

```bash
python manage.py migrate            # auth 테이블이 있어야 계정을 만들 수 있다
python manage.py createsuperuser    # 아이디, 이메일, 비밀번호 입력
python manage.py runserver
```

`http://127.0.0.1:8000/admin/`에 로그인하면 기본으로 **Users**와 **Groups**가 보인다. `INSTALLED_APPS`의 `django.contrib.auth` 앱이 만든 모델이다.

## 2. 모델 등록

내가 만든 모델은 `admin.py`에 등록해야 관리자 페이지에 나타난다.

```python
# cars/admin.py
from django.contrib import admin
from cars.models import Car

admin.site.register(Car)
```

등록하면 `Cars` 메뉴가 생기고, 화면에서 바로 추가, 수정, 삭제를 할 수 있다. shell에서 `create()`, `save()`, `delete()`로 하던 일을 화면으로 하는 것이다.

목록에 `Car is bmw 2020`처럼 보이는 건 모델의 `__str__` 덕분이다.

## 3. `ModelAdmin`으로 수정 화면 바꾸기

`ModelAdmin`을 상속한 클래스를 만들어 `register()`의 두 번째 인자로 넘긴다.

**`fields`: 보여줄 필드와 순서**

```python
class CarAdmin(admin.ModelAdmin):
    fields = ['year', 'brand']   # year가 먼저 나온다
```

**`fieldsets`: 필드를 묶어서 제목 붙이기**

```python
class CarAdmin(admin.ModelAdmin):
    fieldsets = [
        ('TIME INFORMATION', {'fields': ['year']}),
        ('CAR INFORMATION', {'fields': ['brand']}),
    ]

admin.site.register(Car, CarAdmin)
```

`(묶음 제목, {'fields': [필드 목록]})` 형태의 튜플을 나열한다. `fields`와 `fieldsets`는 둘 중 하나만 쓴다. 같이 쓰면 에러가 난다.

## 정리

| 하고 싶은 것 | 방법 |
|---|---|
| 관리자 계정 만들기 | `python manage.py createsuperuser` |
| 관리자 페이지 | `/admin/` |
| 모델 보이게 하기 | `admin.py`에서 `admin.site.register(Car)` |
| 필드 순서 바꾸기 | `ModelAdmin`의 `fields` |
| 필드 묶어서 보여주기 | `ModelAdmin`의 `fieldsets` |
