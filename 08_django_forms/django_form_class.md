# Django 폼 클래스 기초

요약: **`forms.Form`을 상속해 폼을 정의하면 Django가 입력칸 생성, 값 검증, 타입 변환을 대신 해준다. view에서는 `is_valid()`로 검증하고 `cleaned_data`로 값을 꺼낸다.**

```
GET  /cars/rental_review/ ──▶ ReviewForm()             ──▶ 빈 폼 표시

POST /cars/rental_review/ ──▶ ReviewForm(request.POST)
                                       │
                                  is_valid()?
                                 │          │
                               True        False
                                 ▼          ▼
                 redirect(thank_you)      에러가 담긴 폼을 다시 표시
```

## 1. 직접 만든 form과 비교

07에서는 HTML을 직접 쓰고 view에서 값을 하나씩 꺼냈다. ([HTML form으로 데이터 받기](../07_django_admin/form_post.md))

| | 직접 만든 form | `forms.Form` |
|---|---|---|
| 입력칸 | `<input>`을 직접 작성 | `{{ form }}`이 생성 |
| 값 꺼내기 | `request.POST['year']` | `form.cleaned_data['year']` |
| 검증 | 직접 작성 | `is_valid()` |
| 타입 | 전부 문자열이라 `int()`로 변환 | 필드 타입에 맞게 변환 |
| 잘못된 입력 | `int()`에서 `ValueError` | 에러가 담긴 폼을 다시 표시 |

## 2. 폼 클래스 정의

```python
# cars/forms.py
from django import forms


class ReviewForm(forms.Form):
    first_n = forms.CharField(label='First Name', max_length=100)
    last_n = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email')
    review = forms.CharField(label='Please write your review here')
```

- 파일 이름은 관례대로 `forms.py`로 쓴다. import할 때 `from .forms import ReviewForm`처럼 `s`까지 맞춰야 한다
- `label`: 입력칸 앞에 보이는 글자
- `max_length`: 최대 글자 수. HTML에도 `maxlength="100"`으로 들어가고 서버에서도 다시 검사한다
- `EmailField`: 이메일 형식인지 검사한다
- 필드는 기본이 필수 입력이다. HTML에 `required`가 붙는다

**필드 변수 이름이 곧 HTML의 `name`이다.**

```python
first_n = forms.CharField(label='First Name', max_length=100)
```

```html
<input type="text" name="first_n" maxlength="100" required id="id_first_n">
```

## 3. 템플릿

```html
<!-- cars/templates/cars/rental_review.html -->
<form method="POST">
    {% csrf_token %}
    {{ form }}
    <input type="submit">
</form>
```

`{{ form }}`은 라벨과 입력칸만 만든다. `<form>` 태그, `{% csrf_token %}`, 제출 버튼은 직접 써야 한다.

## 4. view

```python
# cars/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ReviewForm


def rental_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)          # 입력값이 담긴 폼
        if form.is_valid():
            print(form.cleaned_data)
            return redirect(reverse('cars:thank_you'))
    else:
        form = ReviewForm()                      # 빈 폼

    return render(request, 'cars/rental_review.html', context={'form': form})
```

| 요청 | `form` | 결과 |
|---|---|---|
| GET | 빈 폼 | 맨 아래 `render` → 200 |
| POST, 검증 성공 | 입력값이 담긴 폼 | `redirect` → 302 |
| POST, 검증 실패 | 입력값과 에러가 담긴 폼 | 맨 아래 `render` → 200 |

**`render`가 `if`/`else` 밖에 있는 이유:** 검증에 실패하면 `redirect`를 건너뛰고 맨 아래로 내려온다. 이때 `form`에는 입력값과 에러가 들어 있어서, 사용자가 쓴 내용이 남은 채로 에러 메시지가 보인다. `render`를 `else` 안에 넣으면 검증 실패 때 응답을 돌려주지 못한다.

성공 뒤에 `redirect`로 끝내는 이유는 [POST 처리 후 redirect](../07_django_admin/redirect_after_post.md) 참고.

## 5. `is_valid()`와 `cleaned_data`

`is_valid()`를 호출하면 검증이 돌아가고 결과가 `True`/`False`로 나온다.

```python
form = ReviewForm({'first_n': 'A', 'last_n': 'B', 'email': 'a@b.com', 'review': 'hi'})
form.is_valid()         # True
form.cleaned_data       # {'first_n': 'A', 'last_n': 'B', 'email': 'a@b.com', 'review': 'hi'}
```

검증에 실패하면 어떤 필드가 왜 틀렸는지 `form.errors`에 들어가고, `cleaned_data`에는 통과한 필드만 남는다.

```python
form = ReviewForm({'first_n': 'A', 'last_n': '', 'email': 'nope', 'review': 'hi'})
form.is_valid()         # False
form.errors             # last_n: This field is required. / email: Enter a valid email address.
form.cleaned_data       # {'first_n': 'A', 'review': 'hi'}
```

- `request.POST`: 브라우저가 보낸 값 그대로. 검증 전이고 전부 문자열이다
- `cleaned_data`: 검증을 통과하고 타입까지 변환된 값
- `cleaned_data`는 `is_valid()`를 호출한 뒤에 생긴다. 먼저 쓰면 `AttributeError`가 난다

## 6. CSRF

CSRF는 사용자가 로그인한 상태를 악용해서, 다른 사이트가 사용자 몰래 우리 사이트로 요청을 보내는 공격이다. 브라우저는 요청을 보낼 때 그 사이트의 쿠키를 자동으로 붙이기 때문에, 서버는 쿠키만으로는 사용자가 직접 보낸 요청인지 구분할 수 없다.

`{% csrf_token %}`은 form 안에 다른 사이트가 알 수 없는 값을 숨겨서 넣는다. Django는 POST를 받을 때 이 값을 확인하고, 없거나 맞지 않으면 `403 Forbidden`으로 막는다. 숨겨진 입력칸이라 화면에는 안 보인다.

GET은 값이 주소에 붙어서 브라우저 기록과 서버 로그에 그대로 남는다. 데이터를 보내거나 바꾸는 form은 POST로 만든다.

## 7. 실수 사례

**`method`에 오타가 있으면 조용히 GET으로 전송된다**

```html
<form method="'POST">   <!-- ❌ 따옴표가 하나 더 들어감 -->
```

브라우저는 모르는 `method` 값을 만나면 에러 없이 기본값인 GET으로 보낸다. 제출해도 빈 폼만 다시 나오고 redirect가 안 된다. 서버 로그를 보면 바로 알 수 있다.

```
"GET /cars/rental_review/?csrfmiddlewaretoken=...&first_n=...&review=hello HTTP/1.1" 200
```

POST로 보냈는데 로그에 `GET`이 찍히고 주소 뒤에 `?`로 값이 붙어 있으면 `<form>`의 `method`부터 확인한다.

**include 경로에 `/`가 빠지면 주소가 그대로 이어 붙는다**

```python
path('cars', include('cars.urls'))    # ❌ /carsrental_review/
path('cars/', include('cars.urls'))   # ⭕ /cars/rental_review/
```

Django는 앞뒤 경로를 문자열처럼 이어 붙인다. 알려준 주소로 들어가도 404가 나고, 오타가 난 주소로 들어가면 오히려 열린다.

**`if` 안이 비어 있으면 `IndentationError`**

```python
if request.method == 'POST':
                                  # ❌ 나중에 쓰려고 비워둠
else:
    form = ReviewForm()
```

비워두려면 `pass`를 넣어야 한다. 다만 `pass`만 두면 POST 요청 때 `form`이 만들어지지 않아서 맨 아래 `render`에서 `UnboundLocalError`가 난다.

## 정리

| 위치 | 하는 일 |
|---|---|
| `forms.py` | `forms.Form`을 상속하고 필드를 정의 |
| 템플릿 | `<form method="POST">`, `{% csrf_token %}`, `{{ form }}`, 제출 버튼 |
| view (GET) | `ReviewForm()`으로 빈 폼 전달 |
| view (POST) | `ReviewForm(request.POST)` → `is_valid()` → `cleaned_data` → `redirect` |
| view (검증 실패) | 에러가 담긴 폼을 그대로 `render` |
