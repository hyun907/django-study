# 05. Django 템플릿

## 강의 체크리스트
- [x] 58. Django와 템플릿
- [x] 59. 템플릿 디렉토리
- [x] 60. 템플릿의 변수
- [x] 61. VS Code Django 확장 프로그램
- [x] 62. 필터
- [x] 63. 태그 - For 루프
- [x] 64. 태그 - If, Elif, Else
- [x] 65. 템플릿의 태그 및 URL 이름
- [x] 66. 템플릿 상속
- [x] 67. 사용자 정의 오류 템플릿
- [x] 68. 정적 파일

## 노트

## 실습 코드
[`my_site/`](my_site/): 58~68강에서 만든 프로젝트(`my_site`)와 앱(`my_app`)

```bash
cd my_site
python manage.py runserver
```

| URL | 내용 |
|-----|------|
| http://127.0.0.1:8000/my_app/ | 템플릿 상속(`base.html`)과 정적 파일 이미지 |
| http://127.0.0.1:8000/my_app/variable/ | 변수, 필터, 주석, for/if 태그 |

| 파일 | 역할 |
|------|------|
| `templates/base.html` | 상속용 부모 템플릿 (`{% block content %}`) |
| `templates/404.html` | `DEBUG = False`일 때 보여주는 사용자 정의 404 페이지 |
| `my_app/templates/my_app/` | 앱 템플릿 (`example.html`, `variable.html`) |
| `my_app/static/my_app/django.png` | `{% static %}`으로 불러오는 이미지 |
| `my_app/urls.py` | `app_name = 'my_app'`과 URL name(`example`, `variable`) |
