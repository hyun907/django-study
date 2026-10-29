# 03. Django 프레임워크 소개

## 강의 체크리스트
- [x] 44. Django 프레임워크에 대한 소개
- [x] 45. Django 작동 방식
- [x] 46. 첫 번째 Django 프로젝트
- [x] 47. 첫 번째 Django 애플리케이션

## 노트
- [Django 프레임워크 개요](django_intro.md)
- [Django 작동 방식](how_django_works.md)

## 실습 코드
[`my_site/`](my_site/): 46, 47강에서 만든 프로젝트(`my_site`)와 앱(`my_app`)

```bash
cd my_site
python manage.py runserver
```

http://127.0.0.1:8000/my_app/ 에 접속하면 `HELLO THIS IS A VIEW INSIDE MY_APP`이 표시된다.

| 파일 | 역할 |
|------|------|
| `my_site/urls.py` | `my_app/`으로 시작하는 요청을 `my_app.urls`로 보냄 (`include`) |
| `my_app/urls.py` | 나머지 경로가 비어 있으면 `views.index` 실행 |
| `my_app/views.py` | `HttpResponse`로 문자열 반환 |
