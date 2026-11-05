# ModelForm

요약: **`ModelForm`은 모델을 보고 폼 필드를 자동으로 만들고, `form.save()` 한 줄로 입력값을 DB에 저장한다.**

```
models.py   Review (first_n, last_n, stars)
    │  Meta의 model로 연결
forms.py    ReviewForm → 필드 자동 생성
    │  form.is_valid() → form.save()
db.sqlite3  cars_review 테이블에 한 행 추가
```

## 1. 폼 클래스와 비교

| | `forms.Form` | `forms.ModelForm` |
|---|---|---|
| 필드 | 직접 하나씩 적는다 | 모델에서 자동으로 만든다 |
| 저장 | `cleaned_data`를 꺼내 직접 저장한다 | `form.save()` |
| 쓰는 경우 | 모델과 상관없는 입력을 받을 때 | 입력값을 모델에 저장할 때 |

`forms.Form`은 [Django 폼 클래스 기초](django_form_class.md) 참고.

## 2. 모델과 validator

```python
# cars/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    first_n = models.CharField(max_length=30)
    last_n = models.CharField(max_length=30)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
```

`validators`는 값이 규칙에 맞는지 검사한다. 위 코드에서 `stars`는 1~5만 통과한다.

메시지를 바꾸고 싶으면 `message`를 넘긴다.

```python
MaxValueValidator(5, message='별점은 5점 이하로 입력해 주세요.')
```

## 3. ModelForm 정의

```python
# cars/forms.py
from django.forms import ModelForm
from .models import Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = "__all__"

        labels = {
            'first_n': "YOUR FIRST NAME",
            'last_n': 'Last Name',
            'stars': "rating",
        }
```

| `Meta` 항목 | 역할 |
|---|---|
| `model` | 폼을 만들 때 기준이 되는 모델 |
| `fields` | 폼에 넣을 필드. `"__all__"`은 수정 가능한 필드 전부 |
| `labels` | 필드별 라벨 글자 |

`id`는 자동으로 만들어지는 값이라 `"__all__"`을 써도 폼에 나오지 않는다.

## 4. view

```python
# cars/views.py
def rental_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('cars:thank_you'))
    else:
        form = ReviewForm()
    return render(request, 'cars/rental_review.html', context={'form': form})
```

`form.save()`가 입력값으로 `Review`를 만들어 DB에 저장한다.

## 5. 에러 메시지가 자동으로 나오는 이유

`stars`에 `8`을 넣고 제출하면 `Ensure this value is less than or equal to 5.`가 뜬다. view에 에러 처리 코드를 따로 쓰지 않아도 아래 순서로 동작한다.

1. `ModelForm`의 `is_valid()`가 모델의 validator까지 검사한다
2. `MaxValueValidator(5)`에 걸려서 에러가 `form.errors`에 저장되고 `False`를 돌려준다
3. `if` 블록을 건너뛰어 `save()`와 `redirect()`가 실행되지 않는다
4. 맨 아래 `render()`가 입력값과 에러가 담긴 `form`을 템플릿에 넘긴다
5. 템플릿이 에러를 출력하고, 입력칸에는 `8`이 그대로 남는다

validator는 폼이나 `full_clean()`을 거칠 때만 실행된다. 아래처럼 바로 저장하면 검사 없이 들어간다.

```python
Review.objects.create(first_n='a', last_n='b', stars=8)  # 에러 없이 저장된다
```

## 6. 필드별 렌더링

`{{ form }}`은 라벨, 입력칸, 에러를 한 번에 출력한다. 따로 배치하고 싶으면 필드를 반복한다.

```html
<!-- cars/templates/cars/rental_review.html -->
<form method="POST" class="myform">
    {% csrf_token %}
    {% for field in form %}
        <div>
            {{ field.label_tag }}
            {{ field }}
            {{ field.errors }}
        </div>
    {% endfor %}
    <input type="submit">
</form>
```

| 코드 | 출력 |
|---|---|
| `{{ field.label_tag }}` | `<label>` 태그 (`rating:`) |
| `{{ field.label }}` | 라벨 글자만 (`rating`) |
| `{{ field }}` | 입력칸 |
| `{{ field.errors }}` | 그 필드의 에러. `<ul class="errorlist">`로 나온다 |

반복문은 특정 필드에 속하지 않는 폼 전체 에러는 출력하지 않는다. `clean()`으로 그런 검사를 추가했다면 반복문 위에 `{{ form.non_field_errors }}`를 넣는다.

## 7. 실수 사례

### admin에 라벨이 안 나온다

admin은 `ReviewForm`을 쓰지 않고 모델을 바탕으로 자기 폼을 따로 만든다. 그래서 `labels`를 넣어도 admin에는 `First n`, `Last n`, `Stars`로 나온다. admin에도 적용하려면 폼을 지정한다.

```python
# cars/admin.py
from .forms import ReviewForm

class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm

admin.site.register(Review, ReviewAdmin)
```

### 행이 있는 테이블에 필수 필드를 추가했다

`makemigrations`가 멈추고 기존 행에 넣을 값을 묻는다.

```
It is impossible to add a non-nullable field 'stars' to review without specifying a default.
 1) Provide a one-off default now
 2) Quit and manually define a default value in models.py.
```

- `1`을 고르고 값을 입력하면 기존 행에만 그 값이 들어간다. 모델에 `default`는 생기지 않는다
- `2`를 고르면 그대로 끝난다. 모델에 `default=5`를 적고 `makemigrations`를 다시 실행한다
- `1` 다음에 `>>>`에서 `exit`를 입력하면 파일이 만들어지지 않는다

### `no such column: cars_review.stars`

`makemigrations`만 하고 `migrate`를 안 했을 때 나온다. 파일은 있지만 DB에 컬럼이 없는 상태다. `python manage.py migrate`를 실행한다. ([마이그레이션](../06_models_databases/migrations.md))

`validators`만 추가해도 `makemigrations`가 변경으로 감지한다. DB 구조는 바뀌지 않지만 마이그레이션 파일은 만든다. (`0003_alter_review_stars.py`)

## 정리

| 하고 싶은 것 | 방법 |
|---|---|
| 모델로 폼 만들기 | `ModelForm` + `Meta`의 `model`, `fields` |
| 라벨 바꾸기 | `Meta`의 `labels` |
| 입력값 저장 | `form.is_valid()` 다음 `form.save()` |
| 값 범위 제한 | 모델 필드의 `validators=[MinValueValidator(1), MaxValueValidator(5)]` |
| 라벨, 입력칸, 에러 따로 출력 | `{% for field in form %}` + `field.label_tag`, `field`, `field.errors` |
| admin에도 폼 적용 | `ModelAdmin`의 `form = ReviewForm` |
