# Store Management Service

제품 쇼핑몰을 관리할 수 있는 **관리 페이지 서비스**

</br>

## 목차

  * [개발 기간](#개발-기간)
  * [프로젝트 개요](#프로젝트-개요)
      - [프로젝트 주체](#프로젝트-주체)
      - [💭 프로젝트 설명](#-프로젝트-설명)
      - [🛠 개발 조건](#-개발-조건)
      - [🧹 사용 기술](#-사용-기술)
      - [📰 모델링](#-모델링)
      - [🛠 API Test](#-api-test)
  * [프로젝트 분석](#프로젝트-분석)
  * [API ENDPOINT](#api-endpoint)
  * [Troubleshooting](#troubleshooting)


</br>

## 개발 기간
**2022.09.08 ~ 2022.09.15** 

(추석 연휴 포함 4일 ) : 기능 구현 및 테스트 코드 작성

</br>
</br>
  
## 프로젝트 개요


#### 프로젝트 주체 

![image](https://user-images.githubusercontent.com/83492367/190282679-1dc5d94a-b8f2-4f58-9b48-8de7da7bd760.png)



[I.M.LAB](https://imlabworld.com/)

</br>

#### 💭 프로젝트 설명

아래의 기능을 바탕으로 한 **제품 쇼핑몰 관리 페이지**의 **backend**를 작성

</br>

#### 🛠 개발 조건



> * **데이터**
> 	* 데이터는 실제 데이터 중 필터링 및 수정을 거친 데이터입니다.
> 	* Price는 KR인 경우 원 단위, 그 외의 경우 달러 단위입니다. 
> 	* 구매 건에 대한 데이터 입니다.
> 	* 배송비 테이블은 원단위 입니다.

> * 제품 주문 내역 열람
> 	* 주문 내역 검색
> 		* 주문 상태, 시작일자, 종료일자에 따른 필터 주문자명으로 검색
> 	* 주문건에 대하여 발송 처리
> * 쿠폰 관리
> 	* 새로운 쿠폰 타입 신설
> 	* 쿠폰은 다음의 방식이 있음 
> 		* 배송비 할인
> 		* % 할인
> 		* 정액 할인
> 	* 특정 신규 쿠폰 코드 발급
> 	* 발급된 쿠폰의 사용 내역 열람
> 	* 쿠폰 타입 별 사용 횟수, 총 할인액
> * 제품 배송 상태 업데이트
> 	* 제품의 배송 상태를 배송 중, 배송 완료 등으로 수정 가능
> * 간단히 구매 내역을 추가 할 수 있도록 구매하기 테스트 코드
> 	*  쿠폰 사용에 따른 사용 할인 적용
> 	* 구매 국가, 구매 갯수에 따른 배송비 적용
> 	* 달러단위 배송비인 경우 일괄 1200원 = 1달러 적용하여 배송비 추가
> 		* 일괄 적용이 아닌 현재 원-달러 환율을 가져와서 배송비 적용시 가산점 부여

</br>

#### 🧹 사용 기술 

- **Back-End** : Python, Django, Django REST framework
- **ETC** : Git, Github

</br>

#### 📰 모델링

![image](https://user-images.githubusercontent.com/83492367/190284149-fe22f5da-c799-4a63-8207-627949b17692.png)
</br>

#### 🛠 API Test

- 쿠폰의 CRUD API 테스트

- 쿠폰 할인 적용 및 구매 국가, 구매 갯수에 따른 배송비 적용 API 테스트

![image](https://user-images.githubusercontent.com/83492367/190426440-785df0c1-f6df-4633-bf15-8bf52855dbee.png)




</br>

## 프로젝트 분석
- 개발 조건을 바탕으로 중심 기능인 `coupons`, `deliveries`, `orders`의 3개의 앱으로 분리
- 해당 서비스의 흐름에 맞게 기업에서 제공한 데이터 가공
	- `DeliveryCost`에 `South Korea` 배송비 추가( 3개마다 3,000원 )
	-   주문 내역 검색을 위해 `시작일자(start_at)`, `종료일자(end_at)`, `주문자명(buyr_name)` 추가 정의

- 주문
	-  구매 국가와 수량에 따라 원화 또는 달러로 `상품가격(product_prcie)` , `쿠폰할인금액(coupon_discount),` `총 가격(total_price)` 자동 계산
		- 한국수출입은행의 실시간 원-달러 환율  OPEN API 이용
			- 비영업일의 데이터, 혹은 영업당일 11시 이전에 해당일의 데이터를 요청할 경우 null 값이 반환되므로  이 경우 일괄 1200원으로 처리
			- 일일 호출 가능 횟수가 1000회로 제한되어 있음
		- `DeliveryCost`에 없는 국가의 경우 `KeyError`를 이용하여 예외 처리
			- 한국이 아닐 경우 달러로 자동계산
			- 한국일 경우 원화로 자동계산 

		
- 쿠폰
	- 쿠폰 생성시 쿠폰의 타입에 따른 유효성 검증 추가
		- % 할인시 할인율이 100%를 초과할 수 없음
	-  쿠폰의 타입( 배송비, 정액, % 할인 )에 따라 다른 할인율이 적용
	-  쿠폰 사용 처리를 위해 put 방식의 @action decorator 이용
	- `Django ORM Aggregate`를 이용하여 쿠폰 타입별 사용 횟수, 총 할인액 계산

	
</br>

## API ENDPOINT

### coupons-types
URL|Method|Action|Description|
|------|---|---|---|
|"api/coupons-types"|GET|List|coupon type 전체 목록 조회|
|"api/coupons-types"|POST|Create|coupon type 생성
|"api/coupons-types/int:pk"|GET|Retrieve|coupon type 세부내역 조회
|"api/coupons-types/int:pk"|PUT|Update|coupon type 세부내역 업데이트|
|"api/coupons-types/int:pk"|PATCH|Partial_Update|coupon type 세부내역 업데이트|

### coupons

URL|Method|Action|Description|
|------|---|---|---|
|"api/coupons"|GET|List|coupon 전체 목록 조회|
|"api/coupons"|POST|Create|coupon 생성
|"api/coupons"/int:pk"|GET|Retrieve|coupon 세부내역 조회
|"api/coupons/int:pk"|PUT|Update|coupon 세부내역 업데이트|
|"api/coupons/int:pk"|PATCH|Partial_Update|coupon 세부내역 업데이트|
|"api/coupons/int:pk"|DELETE|Delete|coupon 삭제|
|"api/coupons/int:pk/redeem"|PUT|@action|coupon 사용처리|



### claimed coupons
URL|Method|Action|Description|
|------|---|---|---|
|"api/claimed-coupons"|GET|List|coupon type 전체 목록 조회|
|"api/claimed-coupons-types"|GET|List|coupon type별 사용 횟수와 총 할인액 조회|
- 쿠폰 사용 내역을 조회할 뿐으로 GET Method 외에는 사용 불가 

### orders


URL|Method|Action|Description|
|------|---|---|---|
|"api/orders"|GET|List|order 전체 목록 조회|
|"api/orders"|POST|Create|order 생성
|"api/orders/int:pk"|GET|Retrieve|order 세부내역 조회
|"api/orders/int:pk"|PUT|Update|order 세부내역 업데이트|
|"api/orders/int:pk"|PATCH|Partial_Update|order 세부내역 업데이트|
|"api/orders/int:pk"|DELETE|Delete|order 삭제|



</br>

## Troubleshooting


<details>
<summary>`ORM`에 대한 부족한 이해</summary>

<!-- summary 아래 한칸 공백 두어야함 -->

- 이번 프로젝트는 여러 테이블이 관계를 맺고 있었고, 외래키를 이용해 다른 테이블의 값을 가져올 필요가 많았음
-   `get`, `filter`의 return값에 대한 정확한 이해가 없었기 때문에 원하는 값을 원하는 타입으로 가져오는 것이 제일 어렵게 느껴졌고 이로 인한 많은 에러를 접함
 ![TypeError at apicoupons](https://user-images.githubusercontent.com/83492367/190439543-e8bdffb0-775d-4a24-8b38-2e8783b8e32c.jpg)
- console에 print할 수가 없는 단점을 보완하기 위해  `Django shell`을 이용하여 데이터베이스에 저장된 값을 이용하도록 노력
- 외래키 관계에 있는 filed를 가져오기 위해서는 __를 이용할 수 있다는 점을 배움

</details>

<details>
<summary>`모델링`과 `branch`의 중요성</summary>

<!-- summary 아래 한칸 공백 두어야함 -->

- 여유로운 마감기한을 위해 여러사항들을 오랫동안 고민하기 보다는 기능들을 만들면서 모델들을 계속해서 수정해나가는 방식으로 진행
-  완성도를 높이기 위한 고도화 작업들의 경우 잘못된 모델링으로 인한 설계의 문제가 많아 해결하는데 많은 시간을 소요
-  모델링의 경우 완벽하게 구현하기도, 구현할 수도 없으나 모델링에 많은 시간을 투자하는 것이 후에 대가를 줄일 수 있다는 점을 배움
-  ` git branch` 사용에 익숙하지 않아 여러 branch들을 checkout했더니 변경사항이 적용되지 않아 에러를 많이 접해 `git pull`를 습관화 할 필요 체감

</details>



