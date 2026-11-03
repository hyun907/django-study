# POST 처리 후 redirect

요약: **POST로 데이터를 저장하거나 지운 뒤에는 `render`가 아니라 `redirect`로 다른 페이지에 보낸다.**

## 1. 코드

```python
# cars/views.py
from django.shortcuts import render, redirect
from django.urls import reverse


def add(request):
    if request.POST:
        ...
        models.Car.objects.create(brand=brand, year=year)
        return redirect(reverse('cars:list'))   # 저장 끝나면 목록으로

    return render(request, 'cars/add.html')
```

## 2. 왜 render가 아니라 redirect인가

**render로 끝내면**

```
POST /cars/add/ ──▶ 저장 ──▶ 200 (같은 주소에서 페이지 표시)
                              │
                         새로고침(F5)
                              ▼
                   POST /cars/add/ 를 한 번 더 보냄 ──▶ 같은 차가 또 저장됨
```

브라우저는 새로고침할 때 마지막 요청을 그대로 다시 보낸다. 마지막 요청이 POST면 form이 또 제출된다. 브라우저가 "양식을 다시 제출하시겠습니까?"라고 묻는 게 이 경우다.

**redirect로 끝내면**

```
POST /cars/add/ ──▶ 저장 ──▶ 302 /cars/list/
                                   │
                          GET /cars/list/ ──▶ 200 목록 페이지
                                                 │
                                            새로고침(F5)
                                                 ▼
                                   GET /cars/list/ (목록만 다시 봄)
```

마지막 요청이 GET이라서 새로고침해도 목록만 다시 불러온다. 이 흐름을 **PRG 패턴**(Post → Redirect → Get)이라고 부른다.

## 3. `reverse`와 `redirect`

```python
reverse('cars:list')                   # → '/cars/list/' (주소 문자열을 만듦)
redirect('/cars/list/')                # → 302 응답 (그 주소로 이동시킴)
redirect(reverse('cars:list'))         # 이름으로 주소를 만들어 이동
redirect('cars:list')                  # 이름만 줘도 redirect가 알아서 reverse 해준다
```

`reverse`는 URL 이름을 주소로 바꾸는 함수다. ([reverse URL과 URL name](../04_views_routing_urls/reverse_url_name.md)) `'cars:list'`의 `cars:` 부분은 [앱 네임스페이스](project_templates_namespace.md)다.

`redirect`는 04에서 쓴 `HttpResponseRedirect`를 짧게 쓰는 함수다. ([리디렉션 기초](../04_views_routing_urls/redirect_basics.md))

## 정리

| 상황 | 끝내는 방법 |
|---|---|
| GET: 페이지 보여주기 | `render(request, '템플릿')` |
| POST: 저장·삭제 성공 | `redirect('앱:이름')` → 새로고침해도 중복 제출 안 됨 |
