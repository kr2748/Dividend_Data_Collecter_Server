## 주린이 배당주 API 프로토콜

현재 주린이 프로젝트에서 크롤러 서버는 20000번 포트를 사용중입니다.  
예를 들어, 배당이력을 가져오고자 할때는 아래와 같은 형태로 요청하면 데이터를 전달받을 수 있습니다. 

http://15.164.248.209:20000/rest/getDividendHistory?start_year=1980&end_year=2020&ticker=ko

### TODO 리스트
- [ ] 재무정보 : 현재 크롤링 하도록 되어있음. 재무정보 API 찾아내기
- [ ] 뉴스 : 현재 크롤링 하도록 되어있음. API 찾아내기
- [ ] 배당 이력 : pandas_datareader 라이브러리 사용중인데, 내부적으로 크롤링을 하고 있어서 느림. API를 찾아내기.
- [ ] 그래프 라이브러리 적용 : https://github.com/PhilJay/MPAndroidChart

### API리스트 
- [x] 배당 이력 가져오기
- [x] 종가이력 구하기
- [x] 뉴스 구하기
- [ ] 이번주에 배당락 혹은 배당 주는 주식 구하기
- [x] 재무정보 구하기
- [x] 배당킹 리스트
- [x] 배당귀족 리스트
- [x] 원달러 환율
- [x] 검색 키워드 자동완성

***

### 배당 이력 가져오기
Test URL : http://15.164.248.209:20000/rest/getDividendHistory?ticker=ko&start_year=1980&end_year=2020

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

***

### 종가 이력 가져오기
Test URL : http://15.164.248.209:20000/rest/getClosePriceHistory?symbol=ko

```
GET /rest/getClosePriceHistory
```

- request 
```
{
  "symbol" : "ko"
}
```

- response 
```
SUCCESS
{
  "data": {
    "Meta Data": {
      "1. Information": "Daily Time Series with Splits and Dividend Events", 
      "2. Symbol": "KO", 
      "3. Last Refreshed": "2020-07-22", 
      "4. Output Size": "Full size", 
      "5. Time Zone": "US/Eastern"
    }, 
    "Time Series (Daily)": {
      "1999-11-01": {
        "1. open": "58.2500", 
        "2. high": "59.3800", 
        "3. low": "57.8800", 
        "4. close": "59.0000", 
        "5. adjusted close": "16.9269", 
        "6. volume": "4212600", 
        "7. dividend amount": "0.0000", 
        "8. split coefficient": "1.0000"
      }, 
      "1999-11-02": {
        "1. open": "58.6300", 
        "2. high": "58.9400", 
        "3. low": "57.3100", 
        "4. close": "57.7500", 
        "5. adjusted close": "16.5683", 
        "6. volume": "3226800", 
        "7. dividend amount": "0.0000", 
        "8. split coefficient": "1.0000"
      }, 
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

***

### 뉴스 가져오기 
Test URL : http://15.164.248.209:20000/rest/getNewsByTicker?ticker=ko

```
GET /rest/getNewsByTicker
```

- request 
```
{
  "ticker" : "ko",
}
```

- response 
```
SUCCESS
{
    "result_code": "200",
    "description": "success",
    "data": {
        "news1": {
            "news_url": "https://www.youtube.com/watch?v=achKqtU2FYU",
            "image_url": "https://cdn.snapi.dev/images/v1/r/4/technician-has-one-name-you-should-buy-and-one-you-should-sell-into-earnings.jpg",
            "title": "Technician has one name you should buy and one you should sell into earnings",
            "text": "Cornerstone Macro's Carter Worth has earnings winners and losers.",
            "source_name": "CNBC Television",
            "date": "Mon, 20 Jul 2020 18:14:45 -0400",
            "topics": [
                "tanalysis"
            ],
            "sentiment": "Neutral",
            "type": "Video",
            "tickers": [
                "KO",
                "SHW"
            ],
            "title_ko": "\uae30\uc220\uc790\ub294 \ud558\ub098\uc758 \uc774\ub984\uc744 \uc0ac\uc57c\ud558\uace0 \ub2e4\ub978 \ud558\ub098\ub294 \uc218\uc785\uc73c\ub85c \ud314\uc544\uc57c\ud569\ub2c8\ub2e4"
        },
        "news2": {
            "news_url": "https://www.fool.com/investing/2020/07/20/dow-jones-lags-as-microsoft-stock-surges-coca-cola.aspx",
            "image_url": "https://cdn.snapi.dev/images/v1/z/4/urlhttps3a2f2fgfoolcdncom2feditorial2fimages2f5292312fgettyimages-1153657433jpgw700opresize.jpg",
            "title": "Dow Jones Lags as Microsoft Stock Surges, Coca-Cola Stock Sinks Ahead of Earnings",
            "text": "Analysts expect solid results from Microsoft and awful results from Coca-Cola.",
            "source_name": "The Motley Fool",
            "date": "Mon, 20 Jul 2020 15:06:00 -0400",
            "topics": [],
            "sentiment": "Neutral",
            "type": "Article",
            "tickers": [
                "KO",
                "MSFT"
            ],
            "title_ko": "\ub2e4\uc6b0 \uc874\uc2a4, \ub9c8\uc774\ud06c\ub85c \uc18c\ud504\ud2b8 \uc99d\uad8c \uae09\ub4f1\uc73c\ub85c \ucf54\uce74\ucf5c\ub77c \uc99d\uad8c \uc2f1\ud06c\uac00 \uc55e\uc11c\uace0\uc788\ub2e4"
        },
        "news3": {
            "news_url": "https://www.forbes.com/sites/adamsarhan/2020/07/20/earnings-preview-what-to-expect-from-coke-on-tuesday/",
            "image_url": "https://cdn.snapi.dev/images/v1/8/f/earnings-preview-what-to-expect-from-coke-on-tuesday.jpg",
            "title": "Earnings Preview: What To Expect From Coke On Tuesday",
            "text": "Coke is expected to report $0.40/share on $8.69 billion in revenue. Meanwhile, the so-called Whisper number is $0.44.",
            "source_name": "Forbes",
            "date": "Mon, 20 Jul 2020 13:38:22 -0400",
            "topics": [
                "earnings"
            ],
            "sentiment": "Positive",
            "type": "Article",
            "tickers": [
                "KO"
            ],
            "title_ko": "\uc2e4\uc801 \ubbf8\ub9ac\ubcf4\uae30 : \ud654\uc694\uc77c \ucf5c\ub77c\uc5d0\uc11c \uc608\uc0c1\ub418\ub294 \uc0ac\ud56d"
        },
        "news4": {
            "news_url": "https://www.businesswire.com/news/home/20200720005144/en/Bradley-Gayton-Elected-Senior-Vice-President-General/",
            "image_url": "https://cdn.snapi.dev/images/v1/w/2/press17.jpg",
            "title": "Bradley Gayton Elected Senior Vice President and General Counsel of The Coca-Cola Company",
            "text": "ATLANTA--(BUSINESS WIRE)--The Coca-Cola Company today announced that Bradley Gayton has been elected senior vice president and general counsel. He will join the company Sept.",
            "source_name": "Business Wire",
            "date": "Mon, 20 Jul 2020 09:00:00 -0400",
            "topics": [
                "PressRelease"
            ],
            "sentiment": "Neutral",
            "type": "Article",
            "tickers": [
                "KO"
            ],
            "title_ko": "\ube0c\ub798\ub4e4\ub9ac \uac8c\uc774 \ud134, \ucf54\uce74\ucf5c\ub77c \ud68c\uc0ac\uc758 \uc218\uc11d \ubd80\uc0ac\uc7a5 \uacb8 \ubc95\ub960 \uace0\ubb38 \uc120\uc784"
        },
        "news5": {
            "news_url": "https://www.fool.com/investing/2020/07/19/3-things-to-watch-in-the-stock-market-this-week.aspx",
            "image_url": "https://cdn.snapi.dev/images/v1/5/p/etf39-5.jpg",
            "title": "3 Things to Watch in the Stock Market This Week",
            "text": "Tesla is one of several high-profile stocks set to announce earnings results over the next few trading days.",
            "source_name": "The Motley Fool",
            "date": "Sun, 19 Jul 2020 08:05:00 -0400",
            "topics": [],
            "sentiment": "Neutral",
            "type": "Article",
            "tickers": [
                "IRBT",
                "KO",
                "TSLA"
            ],
            "title_ko": "\uc774\ubc88 \uc8fc \uc8fc\uc2dd \uc2dc\uc7a5\uc5d0\uc11c \ubcfc 3 \uac00\uc9c0"
        }
    }
}

FAIL 
{
  "data":{},  
  "description":"필수 파라미터를 확인해주세요",  
  "resultCode":101  
}
```

***

### 재무정보 가져오기 
Test URL : http://15.164.248.209:20000/rest/getFinanceInfo?ticker=ko

```
GET /rest/getFinanceInfo
```

- request 
```
{
  "ticker" : "ko",
}
```

- response 
```
SUCCESS
{
    "result_code": "200",
    "reason": "success",
    "data": {
        "PER": "19.88",
        "EPS(ttm)": "2.32",
        "PBR": "10.90",
        "ROE": "54.10%",
        "ROA": "11.20%",
        "PCR": "11.05",
        "BETA": "0.54",
        "Employees": "86200",
        "RecentNewsTitle": "Jul-21-20 09:45AM\u00a0\u00a0Dow's 275-point rally highlighted by gains in shares of Exxon Mobil, Coca-Cola MarketWatch",
        "RecentNewsLink": "https://www.marketwatch.com/story/dows-275-point-rally-highlighted-by-gains-in-shares-of-exxon-mobil-coca-cola-2020-07-21?siteid=yhoof2"
    }
}

FAIL 
{
  "data":{},  
  "description":"필수 파라미터를 확인해주세요",  
  "resultCode":101  
}
```

***

### 배당킹 티커 리스트 가져오기 
Test URL : http://15.164.248.209:20000/rest/getDividendKingTickerList

```
GET /rest/getDividendKingTickerList
```

- request 
```
{

}
```

- response 
```
SUCCESS
{
  "data": [
    "AWR", 
    "DOV", 
    "NWN", 
    "EMR", 
    "GPC", 
    "PG", 
    "PH", 
    "MMM", 
    "CINF", 
    "JNJ", 
    "KO", 
    "LANC", 
    "LOW", 
    "FMCB", 
    "CL", 
    "NDSN", 
    "HRL", 
    "ABM", 
    "CWT", 
    "TR", 
    "FRT", 
    "SCL", 
    "SJW", 
    "SWK", 
    "TGT", 
    "CBSH", 
    "MO", 
    "SYY", 
    "FUL"
  ], 
  "description": "\uc131\uacf5", 
  "resultCode": 200
}

```

***

### 배당귀족 티커 리스트 가져오기 
Test URL : http://15.164.248.209:20000/rest/getDividendAristocratsList

```
GET /rest/getDividendAristocratsList
```

- request 
```
{

}
```

- response 
```
SUCCESS
{
  "data": [
    "GPC", 
    "DOV", 
    "EMR", 
    "PG", 
    "MMM", 
    "CINF", 
    "KO", 
    "JNJ", 
    "LOW", 
    "CL", 
    "HRL", 
    "TGT", 
    "SWK", 
    "SYY", 
    "BDX", 
    "LEG", 
    "PPG", 
    "GWW", 
    "KMB", 
    "PEP", 
    "VFC", 
    "ABBV", 
    "NUE", 
    "SPGI", 
    "ABT", 
    "WMT", 
    "ED", 
    "ITW", 
    "ADM", 
    "ADP", 
    "WBA", 
    "MCD", 
    "PNR", 
    "CLX", 
    "MDT", 
    "SHW", 
    "BEN", 
    "AFL", 
    "CTAS", 
    "XOM", 
    "BF.B", 
    "ATO", 
    "T", 
    "TROW", 
    "MKC", 
    "CAH", 
    "CVX", 
    "GD", 
    "ECL", 
    "LIN", 
    "PBCT", 
    "ROP", 
    "O", 
    "AOS", 
    "CAT", 
    "CB", 
    "RTX", 
    "OTIS", 
    "CARR", 
    "ESS", 
    "EXPD", 
    "ROST", 
    "ALB", 
    "AMCR"
  ], 
  "description": "\uc131\uacf5", 
  "resultCode": 200
}

```

***

### 원달러 환율가져오기 
Test URL : http://15.164.248.209:20000/rest/getKRWExchangeRate

```
GET /rest/getKRWExchangeRate
```

- request 
```

```

- response 
```
SUCCESS
{
  "data": {
    "1. From_Currency Code": "USD", 
    "2. From_Currency Name": "United States Dollar", 
    "3. To_Currency Code": "KRW", 
    "4. To_Currency Name": "South Korean Won", 
    "5. Exchange Rate": "1196.90000000", 
    "6. Last Refreshed": "2020-07-22 22:05:50", 
    "7. Time Zone": "UTC", 
    "8. Bid Price": "1196.90000000", 
    "9. Ask Price": "1197.90000000"
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

### 티커 검색 
Test URL : http://15.164.248.209:20000/rest/getRecommendKeyword?keyword=KO

```
GET /rest/getRecommendKeyword
```

- request 
```
{
  "keyword" : "KO"
}
```

- response 
```
SUCCESS{
  "data": [
    {
      "1. symbol": "KO", 
      "2. name": "The Coca-Cola Company", 
      "3. type": "Equity", 
      "4. region": "United States", 
      "5. marketOpen": "09:30", 
      "6. marketClose": "16:00", 
      "7. timezone": "UTC-05", 
      "8. currency": "USD", 
      "9. matchScore": "1.0000"
    }, 
    {
      "1. symbol": "KSS", 
      "2. name": "Kohl's Corporation", 
      "3. type": "Equity", 
      "4. region": "United States", 
      "5. marketOpen": "09:30", 
      "6. marketClose": "16:00", 
      "7. timezone": "UTC-05", 
      "8. currency": "USD", 
      "9. matchScore": "0.8000"
    }, 
    {
      "1. symbol": "KOS", 
      "2. name": "Kosmos Energy Ltd.", 
      "3. type": "Equity", 
      "4. region": "United States", 
      "5. marketOpen": "09:30", 
      "6. marketClose": "16:00", 
      "7. timezone": "UTC-05", 
      "8. currency": "USD", 
      "9. matchScore": "0.8000"
    }, 
    {
      "1. symbol": "KGKG", 
      "2. name": "Kona Gold Solutions Inc.", 
      "3. type": "Equity", 
      "4. region": "United States", 
      "5. marketOpen": "09:30", 
      "6. marketClose": "16:00", 
      "7. timezone": "UTC-05", 
      "8. currency": "USD", 
      "9. matchScore": "0.6667"
    }, 
    {
      "1. symbol": "PHG", 
      "2. name": "Koninklijke Philips N.V.", 
      "3. type": "Equity", 
      "4. region": "United States", 
      "5. marketOpen": "09:30", 
      "6. marketClose": "16:00", 
      "7. timezone": "UTC-05", 
      "8. currency": "USD", 
      "9. matchScore": "0.6667"
    }, 
    {
      "1. symbol": "KODK", 
      "2. name": "Eastman Kodak Company", 
      "3. type": "Equity", 
      "4. region": "United States", 
      "5. marketOpen": "09:30", 
      "6. marketClose": "16:00", 
      "7. timezone": "UTC-05", 
      "8. currency": "USD", 
      "9. matchScore": "0.4000"
    }, 
    {
      "1. symbol": "KOD", 
      "2. name": "Kodiak Sciences Inc.", 
      "3. type": "Equity", 
      "4. region": "United States", 
      "5. marketOpen": "09:30", 
      "6. marketClose": "16:00", 
      "7. timezone": "UTC-05", 
      "8. currency": "USD", 
      "9. matchScore": "0.4000"
    }, 
    {
      "1. symbol": "KTB", 
      "2. name": "Kontoor Brands Inc.", 
      "3. type": "Equity", 
      "4. region": "United States", 
      "5. marketOpen": "09:30", 
      "6. marketClose": "16:00", 
      "7. timezone": "UTC-05", 
      "8. currency": "USD", 
      "9. matchScore": "0.3333"
    }, 
    {
      "1. symbol": "KORU", 
      "2. name": "Direxion Daily South Korea Bull 3X Shares", 
      "3. type": "ETF", 
      "4. region": "United States", 
      "5. marketOpen": "09:30", 
      "6. marketClose": "16:00", 
      "7. timezone": "UTC-05", 
      "8. currency": "USD", 
      "9. matchScore": "0.1538"
    }
  ], 
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
