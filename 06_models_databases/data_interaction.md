# 데이터 인터렉션: 생성과 조회

핵심: **SQL을 직접 쓰지 않고 `Patient.objects`로 데이터를 넣고 꺼낸다. (ORM)**

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
