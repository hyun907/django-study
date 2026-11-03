# 마이그레이션

요약: **`makemigrations`로 모델의 변경 사항을 파일로 기록하고, `migrate`로 그 파일을 DB에 적용한다.**

## 1. 앱 등록

마이그레이션을 하려면 먼저 앱이 `settings.py`의 `INSTALLED_APPS`에 등록되어 있어야 한다.

```python
# my_site/settings.py
INSTALLED_APPS = [
    "office.apps.OfficeConfig",  # 또는 "office"
    "django.contrib.admin",
    ...
]
```

등록하지 않으면 Django가 `office` 앱의 모델을 찾지 못한다. `makemigrations`를 해도 `No changes detected`가 나오고, `makemigrations office`처럼 앱 이름을 적으면 `App 'office' could not be found` 오류가 난다.

## 2. makemigrations와 migrate

```bash
python manage.py makemigrations office  # 1. 변경 사항을 파일로 기록
python manage.py migrate                # 2. DB에 적용
```

```
models.py ──makemigrations──▶ migrations/0001_initial.py ──migrate──▶ db.sqlite3
 (모델 정의)                      (변경 사항 기록)                         (실제 테이블)
```

**① `makemigrations`**: `models.py`를 보고 무엇이 바뀌었는지 파일로 만든다

```python
# office/migrations/0001_initial.py (자동 생성)
operations = [
    migrations.CreateModel(
        name="Patient",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("first_n", models.CharField(max_length=30)),
            ("last_n", models.CharField(max_length=30)),
            ("age", models.IntegerField()),
        ],
    ),
]
```

직접 적지 않은 `id` 필드가 자동으로 들어가 있다.

**② `migrate`**: 아직 적용하지 않은 마이그레이션 파일을 DB에 실행한다. 여기서 `office_patient` 테이블이 실제로 만들어진다.

처음 `migrate`를 하면 `admin`, `auth`, `sessions` 같은 기본 앱의 테이블도 함께 만들어진다.

## 3. 모델을 바꾸면

모델에 필드를 추가하거나 수정하면 다시 두 단계를 거친다.

```bash
python manage.py makemigrations office  # 0002_....py 가 새로 생김
python manage.py migrate
```

마이그레이션 파일은 `0001`, `0002`... 순서로 쌓인다. **어떤 파일까지 적용했는지는 DB의 `django_migrations` 테이블에 기록된다.** 그래서 `migrate`는 아직 적용하지 않은 파일만 실행한다.

## 4. 모델 업데이트: 필드 추가와 validators

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

`age`는 validators만 붙였는데도 `Alter field`가 생긴다. Django는 validators 변경까지 마이그레이션에 기록하기 때문이다. (실제 DB 테이블 구조는 바뀌지 않는다)

**validators 주의점**

validators는 `save()`나 `create()`를 할 때 **자동으로 검사되지 않는다.** `Patient.objects.create(..., age=200)`도 그대로 저장된다. 검사는 `full_clean()`을 호출하거나 폼(ModelForm, admin)을 통해 입력할 때 일어난다.

마지막으로 `python manage.py migrate`를 해야 DB에 반영된다.

## 정리

| 명령어 | 하는 일 | 결과 |
|---|---|---|
| `makemigrations` | 모델 변경 사항을 파일로 기록 | `migrations/000N_...py` |
| `migrate` | 기록된 변경 사항을 DB에 적용 | DB 테이블 생성, 수정 |

마이그레이션 파일은 DB 구조의 변경 이력이라서 Git에 함께 올린다. (`db.sqlite3`는 올리지 않는다)
