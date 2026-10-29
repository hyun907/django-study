# Django 프레임워크 개요

핵심: **Django는 웹 서비스에 필요한 기능(URL 연결, DB, 관리자 페이지, 로그인 등)을 기본으로 갖추고 있는 파이썬 웹 프레임워크다.**

## 1. Django란?

파이썬으로 웹 사이트를 만들 때 쓰는 프레임워크다.
"Batteries included"(배터리 포함)라는 말처럼 웹 개발에 자주 필요한 기능이 처음부터 들어 있다.

- **ORM**: SQL 대신 파이썬 클래스로 DB를 다룬다
- **Admin**: 데이터를 관리하는 관리자 페이지를 자동으로 만들어 준다
- **인증**: 회원가입, 로그인, 권한 기능
- **템플릿**: HTML 안에 파이썬 데이터를 넣어 화면을 만든다
- **보안**: CSRF, XSS, SQL 인젝션 같은 공격을 기본으로 막아 준다

> 강의는 Django 4 기준이고, 설치한 버전은 5.2.18이다. 이 노트에서 다루는 기본 구조는 두 버전이 같다.

## 2. MTV 패턴

Django는 역할을 세 부분으로 나눈다.

| 구성 | 파일 | 역할 |
|---|---|---|
| **M**odel | `models.py` | 데이터 구조 정의, DB와 연결 |
| **T**emplate | `templates/*.html` | 사용자에게 보여 줄 화면 |
| **V**iew | `views.py` | 요청을 받아 데이터를 가져오고, 어떤 화면을 보여 줄지 결정 |

흔히 말하는 MVC 패턴과 같은 구조인데 이름만 다르다.

| MVC | Django (MTV) |
|---|---|
| Model | Model |
| View (화면) | **Template** |
| Controller (처리 로직) | **View** |

Django의 View는 화면이 아니라 **처리 로직**이라는 점이 헷갈리기 쉽다.

## 3. 요청이 처리되는 흐름

브라우저에서 `/posts/`에 접속하면 다음 순서로 처리된다.

```
브라우저 요청 (/posts/)
    ↓
urls.py      ── 이 URL은 어떤 view가 처리할지 찾는다
    ↓
views.py     ── 요청을 처리한다
    ↓  ↑
models.py    ── 필요하면 DB에서 데이터를 가져온다
    ↓
template     ── 데이터를 HTML에 채워 넣는다
    ↓
브라우저 응답 (완성된 HTML)
```

## 4. 프로젝트와 앱

Django에서는 **프로젝트**와 **앱**을 구분한다.

- **프로젝트**: 웹 사이트 전체. 설정(`settings.py`)과 최상위 URL(`urls.py`)을 가진다
- **앱**: 기능 단위 묶음. 예를 들어 블로그 사이트라면 `posts`, `accounts` 같은 앱을 만든다

하나의 프로젝트는 여러 개의 앱을 가질 수 있고, 잘 만든 앱은 다른 프로젝트에 가져가서 재사용할 수도 있다.

```bash
django-admin startproject mysite   # 프로젝트 생성
cd mysite
python manage.py startapp posts     # 앱 생성
python manage.py runserver          # 개발 서버 실행 (http://127.0.0.1:8000)
```

## 정리

Django는 웹 개발에 필요한 기능을 기본으로 갖춘 프레임워크다. 요청이 들어오면 `urls.py` → `views.py` → (`models.py`) → template 순서로 처리하며, 사이트 전체(프로젝트)를 기능 단위(앱)로 나눠서 만든다.
