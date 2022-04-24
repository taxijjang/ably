# 에이블리 사전과제

## 목차
- [프로젝트 개요](#프로젝트-개요)
- [실행 방법](#실행-방법)
- [사용기술](#사용기술)
- [구현스펙 및 범위](#구현스펙-및-범위)
- [소개하고싶은부분](#소개하고싶은부분)


## 프로젝트 개요

- 에이블리 사전과제 기능설명서를 바탕으로 구현 진행
    - python django를 이용했습니다.
- 요구사항에서 제시하는 기능 구현
    - 문자발송   
    - 회원가입
    - 로그인기능
    - 내 정보 보기 및 수정
    - 비밀번호 찾기 (재설정) 기능
- swagger를 이용하여 api 문서 작성
- python black linter 적용
- 각 기능에 대한 테스트 코드 작성
    - 순수 기능 구현한 부분의 coverage 94% 달성
- 네이버 sns를 이용하여 실제 문자 발송 기능 구현


## 실행 방법

python3.7 기준

### 1. 가상환경생성 및 패키지 설치

1. python -m venv .env
2. source .env/bin/activate
3. pip install -r requirements.txt

### 2. DB 초기화

1. python [manage.py](http://manage.py) makemigrations
2. python [manage.py](http://manage.py) migrate

### 3. 프로젝트 실행

1. python [manage.py](http://manage.py) runserver

## 사용기술

- 언어 - python
- 프레임워크 - django, django-rest-framework
- API문서 - swagger (drf-spectacular)
- 테스트 - coverage


## 구현스펙 및 범위

- 문자 메시지 발송 및 인증
    - 네이버 sns를 이용하여 실제 문제 발송 기능 구현
    - 회원가입 또는 비밀번호 재설정을 하기 위한 필수 조건
    - 유효기간(5분)을 설정
- 회원가입
    - 문자인증과정 적용
    - 기능 설명서에서 요구한 내용을 기반으로 회원가입진행
    - 비밀번호 오입력을 방지하기 위해 비밀번호 검증단계 추가
- 비밀번호 재설정
    - 기존에 저장된 비밀번호를 찾는게 아닌 재설정 기능
    - 문자인증과정 적용
    - 비밀번호 오입력을 방지하기 위해 비밀번호 검증단계 추가
    - email과 phone_number를 이용하여 특정 유저의 비밀번호를 변경
- 로그인기능
    - email과 password를 이용
    - 로그인시 jwt token발급
- 내 정보 보기 및 수정 기능
    - 로그인시 발급되는 jwt token을 이용하여 현재 유저의 판단하여 정보 제공
    - jwt token을 이용하여 변경 가능한 데이터(name, nickname) 변경 가능


## 소개하고싶은부분

### API 문서 ( 주소 - {baseurl}/api/swagger )

- 작성한 API에 대한 문서를 작성하여 클라이언트 개발자가 문서를 보고 개발을 진행할 수 있도록함

### Testcode 작성

- 기능 구현된 로직에 대하여 testcode를 작성하여 코드의 안정성을 더함
- coverage를 이용하여 testcode의 범위를 측정
- 네이버 sns를 이용하여 실제 문자메시지 발송을 구현했는데, Mock을 이용하여 testcode 실행시 실제로 문자가 발송되지 않도록 구현
