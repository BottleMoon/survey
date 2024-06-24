# 설문조사

앱/웹 기반 설문조사 애플리케이션입니다. 

## 환경

- django
- postgresql
- docker
- flutter

## TODO

- [ ]  api spec
- [x]  ERD
- [ ]  TDD

## 기능 (MVP)

- 회원
    - 회원가입
        - 전화번호 본인 인증
    - 로그인
    - OAuth2
- 설문조사
    - 회원가입, 로그인을 하지 않아도 볼 수 있음.(완료된 조사만)
    - 작성
        - 나이, 성별, 직업 등 대상 설정
        - 해당 설문조사가 종료되면  회원의 이메일로 알림메일 발송
    - 투표
        - 투표 대상에 적합한 회원에게만 투표권 부여
    - 추천
        - 투표가 저조한 설문조사 우선으로 추천 알고리즘
    - 연관된 주제 태그.
    - 댓글?
- 피드백, 문의 페이지
    - 폼 작성시 정해진 이메일로 발송
    

## ERD

![choice](https://github.com/BottleMoon/survey/assets/46589339/149e4f17-7842-4a42-bf6c-f63860d75299)

<details>
  
<summary>테이블 구조</summary> 


- user
    - id(pk)
    - person_id(fk)
    - password
    - created_date
    - username
- person
    - id(pk)
    - name
    - sex
    - age
    - job
- oauth
    - id(pk)
    - user_id(fk)
    - provider
    - email
- role
    - id(pk)
    - authority
- user_role
    - user_id(fk)
    - role_id(fk)
- survey
    - id(pk)
    - user_id(fk)
    - classfication_id(fk)
    - created_date
    - text
- classification
    - id(pk)
    - name
- question
    - id(pk)
    - survey_id(fk)
    - text
- choice
    - id(pk)
    - question_id(fk)
    - text
- choice_user
    - choice_id(fk)
    - user_id(fk)
- target_base
    - id(pk)
    - survey_id(fk)
    - min_age
    - max_age
    - sex
    - job
- target_extra
    - id(pk)
    - survey_id
    - text
</details>


