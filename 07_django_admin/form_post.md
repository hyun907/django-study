# HTML form으로 데이터 받기 (POST)

요약: **form의 입력값은 `name` 속성을 키로 해서 서버에 전송되고, view에서는 `request.POST['name']`으로 꺼낸다.**

```
add.html form 제출 ──▶ POST /cars/add/ ──▶ views.add
                       brand=bmw&year=2020       │
                                                 ▼
                                request.POST['brand'] → 'bmw'
                                request.POST['year']  → '2020' (문자열)
                                                 │
                                                 ▼
                                Car.objects.create(...)로 DB에 저장
```

## 1. 템플릿: form 만들기

```html
<!-- cars/templates/cars/add.html -->
<form action="" method="POST">
    {% csrf_token %}
    <div>
        <label for="brand">Brand:</label>
        <input type="text" id="brand" name="brand">
    </div>
    <div>
        <label for="year">Year:</label>
        <input type="text" id="year" name="year">
    </div>
    <input type="submit">
</form>
```

- `method="POST"`: 데이터를 요청 본문에 담아 보낸다. 생략하면 GET이 되고 값이 주소창에 `?brand=bmw`처럼 붙는다
- `action=""`: 비워두면 지금 페이지 주소(`/cars/add/`)로 보낸다
- `{% csrf_token %}`: Django는 POST form에 이 토큰이 없으면 `403 Forbidden`으로 막는다. 다른 사이트가 몰래 요청을 보내는 공격(CSRF)을 막기 위한 장치다

## 2. 전송되는 건 `name`이 있는 input뿐

| 속성 | 역할 |
|---|---|
| `name` | **서버로 보낼 때의 키 이름.** `request.POST['year']`의 `'year'` |
| `id` | HTML 안에서 이 요소를 가리키는 이름 |
| `label for` | `input`의 `id`와 같은 값을 넣으면 둘이 연결돼서 라벨을 클릭해도 입력칸이 선택된다 |

**실수 사례: `name`을 label에 붙임**

```html
<label for="" id="year" name="year">Year:</label>   <!-- ❌ label은 전송 안 됨 -->
<input type="text">                                  <!-- ❌ name이 없음 -->
```

브라우저는 `input`, `select`, `textarea` 중에서 `name`이 있는 것만 보낸다. 이렇게 쓰면 `brand`만 전송되고 `year`는 빠진다.

## 3. view: GET과 POST 나누기

```python
# cars/views.py
def add(request):
    if request.POST:
        brand = request.POST['brand']
        year = int(request.POST['year'])
        models.Car.objects.create(brand=brand, year=year)
        return redirect(reverse('cars:list'))

    return render(request, 'cars/add.html')
```

하나의 view가 두 가지 요청을 처리한다.

| 요청 | 언제 | 하는 일 |
|---|---|---|
| GET | 주소창 입력, 링크 클릭 | `if`를 건너뛰고 빈 form 페이지를 보여줌 |
| POST | form 제출 | 값을 꺼내 DB에 저장하고 목록으로 이동 ([POST 처리 후 redirect](redirect_after_post.md)) |

- `request.POST`는 딕셔너리처럼 쓴다. 키가 없으면 `KeyError`가 나고 `request.POST.get('year')`로 꺼내면 에러 대신 `None`이 나온다
- `if request.POST:`는 POST 데이터가 비어 있으면 거짓이 된다. "POST 요청인가?"를 정확히 묻고 싶으면 `if request.method == 'POST':`라고 쓴다

## 4. form에서 온 값은 전부 문자열

```python
request.POST['year']        # '2020'  ← 문자열
int(request.POST['year'])   # 2020    ← 숫자
```

`Car.year`가 `IntegerField`라서 `int()`로 바꿔서 넣는다. 숫자가 아닌 값을 입력하면 `int()`에서 `ValueError`가 난다.

## 정리

| 위치 | 하는 일 |
|---|---|
| `add.html` | `<form method="POST">`, `{% csrf_token %}`, input마다 `name` |
| `views.add` | `if request.POST:`로 GET/POST 구분, `request.POST['name']`으로 꺼냄 |
| `views.add` | 숫자 필드는 `int()`로 변환 후 `create()` |
