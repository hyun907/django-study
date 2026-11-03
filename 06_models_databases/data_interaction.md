# 데이터 인터렉션: 생성과 조회

## 0. shell 실행

데이터 인터렉션은 Django shell에서 실습한다. 일반 `python`과 달리 프로젝트 설정이 불러와진 상태로 실행된다.

```bash
python manage.py shell
```

```python
>>> from office.models import Patient
```

## 1. 생성과 삽입

**방법 1: 객체를 만들고 `save()`**

```python
>>> carl = Patient(first_n="carl", last_n="smith", age=30)
>>> carl.save()  # save()를 해야 DB에 저장된다
```

`Patient(...)`만 하면 파이썬 객체가 만들어질 뿐이고, **`save()`를 호출해야 DB에 들어간다.**

**방법 2: `objects.create()`**

```python
>>> Patient.objects.create(first_n="susan", last_n="smith", age=40)
```

객체 생성과 저장을 한 번에 한다.

**방법 3: 여러 개를 한 번에 `bulk_create()`**

```python
>>> Patient.objects.bulk_create([
...     Patient(first_n="adam", last_n="smith", age=40),
...     Patient(first_n="karl", last_n="marx", age=20),
... ])
```

저장하면 `id`가 자동으로 1, 2, 3... 순서로 붙는다.

## 2. `.all()`로 전체 조회

```python
>>> Patient.objects.all()
<QuerySet [<Patient: smith, carl, is 30 years old>, <Patient: smith, susan, is 40 years old>, <Patient: baek, seunghyun, is 25 years old>, <Patient: smith, adam, is 40 years old>, <Patient: marx, karl, is 20 years old>]>
```

결과는 **QuerySet**이다. 리스트와 비슷하게 다룰 수 있다.

```python
>>> patients = Patient.objects.all()
>>> patients[0]              # 인덱스로 꺼내기
<Patient: smith, carl, is 30 years old>
>>> patients[0].first_n      # 필드 값 꺼내기
'carl'
>>> patients.count()         # 개수
5
>>> for p in patients:       # 반복문
...     print(p.first_n, p.age)
```

각 항목이 `smith, carl, is 30 years old`처럼 보이는 건 모델에 정의한 `__str__` 덕분이다. ([모델과 필드](models_and_fields.md))

## 3. `filter()`와 `get()`으로 조건 조회

**`filter()`: 조건에 맞는 것 전부 → QuerySet**

```python
>>> Patient.objects.filter(last_n='smith')
<QuerySet [<Patient: smith, carl, is 30 years old>, <Patient: smith, susan, is 40 years old>, <Patient: smith, adam, is 40 years old>]>
```

결과가 없어도 에러가 나지 않고 빈 `<QuerySet []>`가 나온다. 뒤에 `.all()`을 붙여도 결과는 같으니 생략해도 된다.

**조건 여러 개 (AND)**

```python
>>> Patient.objects.filter(last_n='smith').filter(age=40)  # 체이닝
>>> Patient.objects.filter(last_n='smith', age=40)         # 쉼표, 가장 간단
<QuerySet [<Patient: smith, susan, is 40 years old>, <Patient: smith, adam, is 40 years old>]>
```

**`Q` 객체: OR / NOT 조건이 필요할 때**

```python
>>> from django.db.models import Q
>>> Patient.objects.filter(Q(last_n='smith') & Q(age=40))  # AND (쉼표와 같다)
>>> Patient.objects.filter(Q(last_n='smith') | Q(age=20))  # OR
>>> Patient.objects.filter(~Q(last_n='smith'))             # NOT
```

**`get()`: 딱 하나 → 객체**

```python
>>> Patient.objects.get(first_n='seunghyun')
<Patient: baek, seunghyun, is 25 years old>
```

QuerySet이 아니라 **객체 하나**를 돌려준다. 결과가 정확히 1개가 아니면 에러가 난다.

| 결과 개수 | 에러 |
|---|---|
| 0개 | `DoesNotExist` |
| 2개 이상 | `MultipleObjectsReturned` (`get(last_n='smith')` → 3개라서 에러) |

그래서 `get()`은 `id`/`pk`처럼 겹치지 않는 값으로 찾을 때 쓴다.

## 4. 필드 조회 (Field lookups)

`필드명__조건=값` 형태로 "같다" 말고 다른 조건을 건다. **밑줄은 두 개(`__`)**다.

```python
>>> Patient.objects.filter(last_n__startswith='s')   # 's'로 시작
<QuerySet [<Patient: smith, carl, is 30 years old>, <Patient: smith, susan, is 40 years old>, <Patient: smith, adam, is 40 years old>]>

>>> Patient.objects.filter(age__in=[20, 30, 40])     # 리스트 안에 있는 값
<QuerySet [<Patient: smith, carl, is 30 years old>, <Patient: smith, susan, is 40 years old>, <Patient: smith, adam, is 40 years old>, <Patient: marx, karl, is 20 years old>]>

>>> Patient.objects.filter(age__gte=39)              # 39 이상
<QuerySet [<Patient: smith, susan, is 40 years old>, <Patient: smith, adam, is 40 years old>]>
```

자주 쓰는 조건:

| lookup | 뜻 |
|---|---|
| `__gt` / `__gte` | 초과 / 이상 |
| `__lt` / `__lte` | 미만 / 이하 |
| `__in` | 리스트 안에 있음 |
| `__startswith` / `__endswith` | ~로 시작 / ~로 끝남 |
| `__contains` | ~를 포함 |

**`order_by()`: 정렬**

```python
>>> Patient.objects.order_by('age')    # 오름차순 (어린 순)
<QuerySet [<Patient: marx, karl, is 20 years old>, <Patient: baek, seunghyun, is 25 years old>, <Patient: smith, carl, is 30 years old>, <Patient: smith, susan, is 40 years old>, <Patient: smith, adam, is 40 years old>]>
>>> Patient.objects.order_by('-age')   # 앞에 -를 붙이면 내림차순
```

## 5. 모델 업데이트: 필드 추가와 validators

`Patient`에 `heartrate` 필드를 추가하고, `age`에 값 범위를 걸었다.

```python
# office/models.py
from django.core.validators import MaxValueValidator, MinValueValidator

class Patient(models.Model):
    first_n = models.CharField(max_length=30)
    last_n = models.CharField(max_length=30)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
    heartrate = models.IntegerField(default=60, validators=[MinValueValidator(1), MaxValueValidator(300)])
```

**데이터가 이미 있는 테이블에 필드를 추가하면**

처음에 `default` 없이 `heartrate`를 추가하고 `makemigrations`를 하면 이렇게 물어본다.

```
It is impossible to add a non-nullable field 'heartrate' to patient without specifying a default.
This is because the database needs something to populate existing rows.
 1) Provide a one-off default now
 2) Quit and manually define a default value in models.py.
```

이미 있는 환자 5명의 `heartrate` 칸을 뭘로 채울지 모르기 때문이다. 2번을 골라 빠져나온 뒤 `models.py`에 `default=60`을 넣으면 된다. 그러면 기존 데이터의 `heartrate`가 전부 60으로 채워진다. 값이 비어 있어도 된다면 `null=True`를 쓰는 방법도 있다.

**`makemigrations` 결과**

```
office/migrations/0002_patient_heartrate_alter_patient_age.py
    + Add field heartrate to patient
    ~ Alter field age on patient
```

`age`는 validators만 붙였는데도 `Alter field`가 생긴다. Django는 validators 변경까지 마이그레이션에 기록하기 때문이다. (실제 DB 테이블 구조는 바뀌지 않는다) 마지막으로 `python manage.py migrate`를 해야 DB에 반영된다. ([마이그레이션](migrations.md))

**validators 주의점**

validators는 `save()`나 `create()`를 할 때 **자동으로 검사되지 않는다.** `Patient.objects.create(..., age=200)`도 그대로 저장된다. 검사는 `full_clean()`을 호출하거나 폼(ModelForm, admin)을 통해 입력할 때 일어난다.

## 지금 DB에 들어 있는 데이터

| id | first_n | last_n | age |
|---|---|---|---|
| 1 | carl | smith | 30 |
| 2 | susan | smith | 40 |
| 3 | seunghyun | baek | 25 |
| 4 | adam | smith | 40 |
| 5 | karl | marx | 20 |

## 정리

| 하고 싶은 것 | 코드 |
|---|---|
| 하나 저장 | `Patient(...).save()` 또는 `Patient.objects.create(...)` |
| 여러 개 저장 | `Patient.objects.bulk_create([...])` |
| 전체 조회 | `Patient.objects.all()` → QuerySet |
| 조건 조회 | `Patient.objects.filter(...)` → QuerySet (없으면 빈 QuerySet) |
| OR / NOT 조건 | `filter(Q(...) \| Q(...))`, `filter(~Q(...))` |
| 딱 하나 조회 | `Patient.objects.get(...)` → 객체 (0개·2개 이상이면 에러) |
| 비교·포함 조건 | `filter(age__gte=39)`, `filter(last_n__startswith='s')` |
| 정렬 | `order_by('age')`, 내림차순은 `order_by('-age')` |
| 필드 추가 | 기존 데이터가 있으면 `default=` 또는 `null=True` 필요 |
