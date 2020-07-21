## 주린이 배당주 API 프로토콜

현재 주린이 프로젝트에서 크롤러 서버는 20000번 포트를 사용중입니다.
따라서, 배당이력을 가져오고자 할때는, 아래와 같이 요청하면 데이터를 전달받을 수 있습니다. 

http://15.164.248.209:20000/rest/getDividendHistory?start_year=1980&end_year=2020

### 배당 이력 가져오기

```
GET /rest/getDividendHistory
```

- request 
```
{
  "ticker" : "ko",
  "start_year" : "1980",
  "end_year" : "2020",
}
```

- response 
```
SUCCESS
{
  "data": {
    "1000252800000": 0.18, 
    "1000684800000": 0.09, 
    "1006905600000": 0.18, 
    "1015977600000": 0.2
  }, 
  "description": "\uc131\uacf5", 
  "resultCode": 200
}

FAIL 
{
  "data":{},  
  "description":"필수 파라미터를 확인해주세요",  
  "resultCode":101  
}
```
