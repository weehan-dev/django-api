# django-api

장고 api서버

## Git

- 절대 마스터 브랜치에 push 하지 말 것.
- 브랜치 이름은 [id]/[기능]으로 짓기. (ex. changhoi/authenticate)
- 모였을 때 코드 리뷰 후 merge

## Code

- 변수, 함수 이름은 snake_case로 짓기
- 클래스 이름은 PascalCase로 짓기
- 함수는 한 번에 하나의 기능만 하도록 만들기
- 함수 네이밍은 기능을 드러내야 하고, 동사 형태로 만들 것
- 웬만하면 변수, 함수, 클래스 이름은 생략하거나 줄이지 말고 짓기
- REST 준수

## Pull 이후

- `pip install -r requirements.txt`
- yeonhadae/dbconfig.py 설정

```
db = {
    'NAME': 'DB이름',
    'USER': '계정 이름',
    'PASSWORD': 'DB 비밀번호',
    'HOST': '호스트',
    'PORT': '포트'
}
``` 

- `python manage.py migrate`

