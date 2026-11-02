# 모델과 필드

요약: **모델은 DB 테이블을 파이썬 클래스로 정의한 것이다. 클래스 하나가 테이블 하나, 필드 하나가 컬럼 하나가 된다.**

## 1. 모델 정의하기

```python
# office/models.py
from django.db import models


class Patient(models.Model):
    first_n = models.CharField(max_length=30)
    last_n = models.CharField(max_length=30)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.last_n}, {self.first_n}, is {self.age} years old"
```

- 모델은 `models.Model`을 상속받는다 (02의 [상속](../02_python_oop/inheritance.py))
- 클래스 속성 하나하나가 필드(테이블의 컬럼)가 된다

## 2. 모델 → 테이블

`Patient` 모델은 DB에서 `office_patient` 테이블이 된다. (`앱이름_모델이름` 소문자)

| 모델 | DB 테이블 |
|---|---|
| `class Patient` | `office_patient` 테이블 |
| `first_n = CharField(max_length=30)` | `first_n` 컬럼 (최대 30자 문자열) |
| `last_n = CharField(max_length=30)` | `last_n` 컬럼 (최대 30자 문자열) |
| `age = IntegerField()` | `age` 컬럼 (정수) |
| (적지 않음) | `id` 컬럼 (자동 생성) |

**`id`는 직접 만들지 않아도 Django가 자동으로 추가한다.** 데이터를 넣을 때마다 1, 2, 3... 순서로 번호가 붙는다. (`settings.py`의 `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'`)

## 3. 자주 쓰는 필드

| 필드 | 저장하는 값 | 비고 |
|---|---|---|
| `CharField` | 짧은 문자열 | `max_length` 필수 |
| `TextField` | 긴 문자열 | 길이 제한 없음 |
| `IntegerField` | 정수 | |
| `FloatField` | 실수 | |
| `BooleanField` | `True` / `False` | |
| `DateTimeField` | 날짜와 시간 | |

## 4. `__str__`을 정의하는 이유

02에서 배운 [특수 메서드](../02_python_oop/special_methods.py) `__str__`과 같다. 정의하지 않으면 shell이나 admin에서 객체가 이렇게 보인다.

```
<Patient: Patient object (1)>
```

정의하면 이렇게 보여서 어떤 데이터인지 바로 알 수 있다.

```
<Patient: smith, carl, is 30 years old>
```

## 정리

모델 클래스는 테이블, 필드는 컬럼이 된다. `id`는 자동으로 생기고, `__str__`을 정의해 두면 데이터를 확인하기 쉽다. 모델을 만들기만 해서는 DB에 테이블이 생기지 않는다. [마이그레이션](migrations.md)을 해야 한다.
