# view에서 삭제하기: 없는 pk 처리

요약: **사용자가 입력한 pk는 DB에 없을 수도 있다. `get` + `try/except` 또는 `filter().first()` + `if/else`로 처리한다.**

shell에서 `get()`과 `delete()`를 쓰는 법은 [데이터 인터렉션](../06_models_databases/data_interaction.md)에 있다. 여기서는 사용자가 form으로 보낸 값을 view에서 처리한다.

## 1. 템플릿: pk를 입력받는 form

```html
<!-- cars/templates/cars/delete.html -->
<form action="" method="POST">
    {% csrf_token %}
    <div>
        <label for="pk">PK:</label>
        <input type="number" id="pk" name="pk">
    </div>
    <input type="submit" value="Delete">
</form>
```

## 2. 방법 1: `get` + `try/except` (강의 방식)

```python
# cars/views.py
def delete(request):
    if request.POST:
        pk = request.POST['pk']
        try:
            models.Car.objects.get(pk=pk).delete()
            return redirect(reverse('cars:list'))
        except models.Car.DoesNotExist:
            print('해당 pk의 차가 없습니다')
            return redirect(reverse('cars:list'))

    return render(request, 'cars/delete.html')
```

- `get(pk=pk)`는 그 pk의 차가 없으면 `DoesNotExist` 에러를 낸다
- 에러를 잡지 않으면 서버 에러 페이지가 뜨기 때문에 `try/except`로 받는다
- `DoesNotExist`는 모델마다 있는 에러라서 `models.Car.DoesNotExist`처럼 모델 이름을 붙여서 쓴다
- `pk`는 문자열(`'3'`)로 오지만 `get(pk='3')`처럼 넣어도 Django가 숫자로 바꿔서 찾는다

## 3. 방법 2: `filter().first()` + `if/else`

```python
def delete(request):
    if request.POST:
        pk = request.POST['pk']
        car = models.Car.objects.filter(pk=pk).first()

        if car:
            car.delete()
            return redirect(reverse('cars:list'))
        else:
            context = {'error': f'{pk}번 차는 없습니다'}
            return render(request, 'cars/delete.html', context)

    return render(request, 'cars/delete.html')
```

- `filter()`는 결과가 없으면 에러 대신 빈 QuerySet을 준다
- `.first()`는 첫 번째 객체를 주고 비어 있으면 `None`을 준다
- 그래서 `if car:`로 바로 있는지 검사할 수 있다

## 4. 두 방법 비교

| | `get` + `try/except` | `filter().first()` + `if/else` |
|---|---|---|
| 없을 때 | `DoesNotExist` 에러 → `except`에서 처리 | `None` → `else`에서 처리 |
| 어울리는 상황 | "정확히 하나 있어야 한다"는 게 기본일 때 | "있으면 하고 없으면 말고"일 때 |
| Django에서 | 더 흔한 방식 | 이것도 자주 쓴다 |

둘 다 결과는 같다. 강의에서는 `get` + `try/except`를 쓴다.

## 5. 빈 값을 제출하면?

pk 칸을 비우고 제출하면 `pk = ''`가 된다. 이때는 `DoesNotExist`가 아니라 `ValueError`가 나서 두 방법 모두 잡지 못한다.

```
ValueError: Field 'id' expected a number but got ''.
```

막으려면 `except (models.Car.DoesNotExist, ValueError):`처럼 같이 잡거나, input에 `required`를 붙여 빈 값 제출을 막는다.

## 정리

| 하고 싶은 것 | 코드 |
|---|---|
| form 값으로 하나 찾아서 삭제 | `models.Car.objects.get(pk=pk).delete()` |
| 없는 pk 처리 (에러로) | `try` ... `except models.Car.DoesNotExist:` |
| 없는 pk 처리 (None으로) | `car = filter(pk=pk).first()` → `if car:` |
| 빈 값까지 처리 | `except (models.Car.DoesNotExist, ValueError):` |
