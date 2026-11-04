# CSS 연결(static)과 폼 위젯

요약: **CSS 파일은 `앱/static/앱이름/`에 두고 템플릿에서 `{% static %}`으로 연결한다. 폼 입력칸의 종류를 바꿀 때는 필드에 `widget`을 지정한다.**

```
cars/static/cars/custom.css   ← 실제 파일
          │
{% static 'cars/custom.css' %}   ← 템플릿에 쓰는 경로
          │
<link href="/static/cars/custom.css">   ← 브라우저가 받는 HTML
```

## 1. 파일 위치

```
cars/
├── static/
│   └── cars/
│       └── custom.css
└── templates/
    └── cars/
        └── rental_review.html
```

`static/` 아래에 앱 이름 폴더를 한 번 더 둔다. 다른 앱에도 같은 이름의 파일이 있을 때 겹치지 않게 하려는 것으로, `templates/` 구조와 같은 이유다. ([프로젝트 공용 템플릿과 app_name](../07_django_admin/project_templates_namespace.md))

`django.contrib.staticfiles`가 `INSTALLED_APPS`에 있고 `STATIC_URL`이 설정돼 있으면 `settings.py`는 수정할 필요가 없다. 둘 다 프로젝트를 만들 때 기본으로 들어 있다.

## 2. 템플릿에 연결

```css
/* cars/static/cars/custom.css */
.myform {
    color: red;
}
```

```html
<!-- cars/templates/cars/rental_review.html -->
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <link rel="stylesheet" href="{% static 'cars/custom.css' %}">
</head>
<body>
    <h1>RENTAL REVIEW FORM</h1>
    <form method="POST" class="myform">
        {% csrf_token %}
        {{ form }}
        <input type="submit">
    </form>
</body>
</html>
```

| 코드 | 역할 |
|---|---|
| `{% load static %}` | `static` 태그를 불러온다. 파일 맨 위에 한 번 쓴다 |
| `{% static 'cars/custom.css' %}` | `static/` 다음 경로를 쓰면 `/static/cars/custom.css` 주소를 만들어준다 |
| `class="myform"` | CSS의 `.myform`과 연결한다 |

`color`는 `<form>` 안의 라벨 글자에 물려받아져서 라벨이 빨개진다. `<input>`은 브라우저 기본 스타일이 있어서 입력칸 안의 글자는 그대로다.

## 3. 위젯: 입력칸 종류 바꾸기

필드는 데이터를 어떻게 검사할지 정하고, 위젯은 화면에 어떤 HTML로 보여줄지 정한다. `CharField`의 기본 위젯은 한 줄짜리 `<input type="text">`다. 긴 글을 받을 때는 `Textarea`로 바꾼다.

```python
# cars/forms.py
review = forms.CharField(label='Please write your review here', widget=forms.Textarea())
```

```html
<textarea name="review" cols="40" rows="10" required id="id_review"></textarea>
```

입력칸에 직접 HTML 속성을 넣고 싶으면 `attrs`를 쓴다.

```python
review = forms.CharField(widget=forms.Textarea(attrs={'class': 'myform', 'rows': 3}))
```

```html
<textarea name="review" cols="40" rows="3" class="myform" required id="id_review"></textarea>
```

## 4. CSS가 적용되지 않을 때

1. 개발자 도구 Network 탭에서 `custom.css`가 200인지 확인한다
2. 404라면 파일 위치와 `{% static %}` 경로를 확인한다
3. `static` 폴더를 서버가 켜진 뒤에 만들었다면 `runserver`를 껐다 켠다
4. 200인데 예전 CSS가 보이면 브라우저 캐시 때문일 수 있다. 강력 새로고침(`Cmd + Shift + R`)을 한다

## 정리

| 하고 싶은 것 | 방법 |
|---|---|
| CSS 파일 두기 | `앱/static/앱이름/파일.css` |
| 템플릿에 연결 | `{% load static %}` + `<link href="{% static '앱이름/파일.css' %}">` |
| 입력칸 종류 변경 | `widget=forms.Textarea()` |
| 입력칸에 HTML 속성 추가 | `forms.Textarea(attrs={'class': 'myform'})` |
