## 주린이 배당주 API 프로토콜

현재 주린이 프로젝트에서 크롤러 서버는 20000번 포트를 사용중입니다.  
예를 들어, 배당이력을 가져오고자 할때는 아래와 같은 형태로 요청하면 데이터를 전달받을 수 있습니다. 

http://15.164.248.209:20000/rest/getDividendHistory?start_year=1980&end_year=2020&ticker=ko

### 용어 정리 
- Ex-Dividend Date : 배당락일
- Preferred Stock : 우선주
- Current Yield : 현재 배당률
- Declare Date : 배당 발표일(이사회에서 배당금을 지급하기로 결정한 날)
- Payout Ratio : 배당성향
- 5 Year Growth Rate : 최근 5년 연평균 배당금 인상률
- Adj. Amount : 주식분할 조정 배당금. 주식분할까지 반영된 정확한 배당금을 말함. 최근에 주식분할이 없었다면 배당금(Amount)과 주식분할 조정 배당금(Adj. Amount)은 동일함
- Pay Date : 배당금 지급일
- Call Date : 매입권리 발생 기준일
- Record Date : 주주명부 확정일  
  
출처 : https://m.blog.naver.com/PostView.nhn?blogId=danny121227&logNo=221718369992&categoryNo=68&proxyReferer=https:%2F%2Fwww.google.com%2F

### TODO 리스트
- [x] 재무정보 : 현재 크롤링 하도록 되어있음. 재무정보 API 찾아내기 
- [ ] 뉴스 : 현재 크롤링 하도록 되어있음. API 찾아내기
- [ ] 배당 이력 : pandas_datareader 라이브러리 사용중인데, 내부적으로 크롤링을 하고 있어서 느림. API를 찾아내기.
- [x] 그래프 라이브러리 적용 : https://github.com/PhilJay/MPAndroidChart
- [x] https://documentation.tradier.com/brokerage-api/markets/fundamentals/get-dividends API 사용해보기 => 돈 내야 사용가능. 
- [ ] 논 블러킹으로 크롤링 서버 세팅
- [x] 배당정보 API 드디어 찾았다.. https://iexcloud.io/docs/api/#dividends => 이력나오는 API는 돈내야되고, 요약정보는 티커 변경해도 고정된값 나옴. 엉터리.

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
- [x] 기업 요약 정보

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
    "data": [
        {
            "news_url": "https://www.forbes.com/sites/greatspeculations/2020/07/24/can-coca-colas-stock-rise-any-further/",
            "image_url": "https://cdn.snapi.dev/images/v1/y/t/can-coca-colas-stock-rise-any-further.jpg",
            "title": "Can Coca-Cola\u2019s Stock Rise Any Further?",
            "text": "Despite almost a 30% rise since the March 23 lows of this year, at the current price of around $48 per share, we believe Coca-Cola stock has some upside left. KO stock has increased from $37 to $48 off the recent bottom, less than the S&P which increased by 46% from its recent bottom.",
            "source_name": "Forbes",
            "date": "Fri, 24 Jul 2020 08:30:00 -0400",
            "topics": [],
            "sentiment": "Positive",
            "type": "Article",
            "tickers": [
                "KO"
            ],
            "title_ko": "\ucf54\uce74\ucf5c\ub77c\uc758 \uc8fc\uac00\uac00 \ub354 \uc0c1\uc2b9 \ud560 \uc218 \uc788\ub294\uac00?"
        },
        {
            "news_url": "https://seekingalpha.com/article/4360370-coca-cola-femsa-s-b-de-c-v-kof-ceo-john-santa-maria-on-q2-2020-results-earnings-call",
            "image_url": "https://cdn.snapi.dev/images/v1/5/l/transcript50.jpg",
            "title": "Coca-Cola FEMSA, S.A.B. de C.V. (KOF) CEO John Santa Maria on Q2 2020 Results - Earnings Call Transcript",
            "text": "Coca-Cola FEMSA, S.A.B. de C.V. (KOF) CEO John Santa Maria on Q2 2020 Results - Earnings Call Transcript",
            "source_name": "Seeking Alpha",
            "date": "Thu, 23 Jul 2020 16:16:08 -0400",
            "topics": [
                "CallScript"
            ],
            "sentiment": "Neutral",
            "type": "Article",
            "tickers": [
                "KO"
            ],
            "title_ko": "\ucf54\uce74\ucf5c\ub77c FEMSA, S.A.B. \ub4dc C.V. (KOF) 2020 \ub144 2 \ubd84\uae30 \uacb0\uacfc\uc5d0 \ub300\ud55c CEO John Santa Maria-\uc2e4\uc801 \ubcf4\uace0\uc11c"
        },
        {
            "news_url": "https://www.fool.com/investing/2020/07/23/coca-cola-explains-why-a-full-recovery-could-take.aspx",
            "image_url": "https://cdn.snapi.dev/images/v1/h/m/coke-340446-1280.jpg",
            "title": "Coca-Cola Explains Why a Full Recovery Could Take Years",
            "text": "Consumers aren't moving around like they used to, according to details from Coke's second-quarter earnings report.",
            "source_name": "The Motley Fool",
            "date": "Thu, 23 Jul 2020 15:34:33 -0400",
            "topics": [],
            "sentiment": "Negative",
            "type": "Article",
            "tickers": [
                "KO"
            ],
            "title_ko": "\ucf54\uce74\ucf5c\ub77c\ub294 \uc804\uccb4 \ubcf5\uad6c\uc5d0 \uba87 \ub144\uc774 \uac78\ub9ac\ub294 \uc774\uc720\ub97c \uc124\uba85\ud569\ub2c8\ub2e4"
        },
        {
            "news_url": "https://seekingalpha.com/article/4360165-retirement-strategy-blue-skies-for-dividend-growth-investors-storms-ahead-for-savers?utm_source=feed_articles_dividends_dividend_strategy&utm_medium=referral",
            "image_url": "https://cdn.snapi.dev/images/v1/l/d/103334235-gettyimages-498338509.jpg",
            "title": "Retirement Strategy: Blue Skies For Dividend Growth Investors, More Storms Ahead For Savers",
            "text": "The Federal Reserve has given another clear signal that there is less risk for investors, especially in long term.",
            "source_name": "Seeking Alpha",
            "date": "Thu, 23 Jul 2020 09:00:00 -0400",
            "topics": [
                "dividend"
            ],
            "sentiment": "Positive",
            "type": "Article",
            "tickers": [
                "JNJ",
                "KO",
                "MO",
                "O"
            ],
            "title_ko": "\ud1f4\uc9c1 \uc804\ub7b5 : \ubc30\ub2f9 \uc131\uc7a5 \ud22c\uc790\uc790\ub97c\uc704\ud55c \ud478\ub978 \ud558\ub298, \ubcf4\ud638\uc790\ub97c\uc704\ud55c \ub354 \ub9ce\uc740 \ud3ed\ud48d"
        },
        {
            "news_url": "https://www.zacks.com/stock/news/1012407/will-cokes-plan-to-cut-its-zombie-brands-boost-revenues",
            "image_url": "https://cdn.snapi.dev/images/v1/r/r/coca-cola-462776-1280.jpg",
            "title": "Will Coke's Plan to Cut Its Zombie Brands Boost Revenues?",
            "text": "Coca-Cola is massively streamlining its businesses in a bid to push for a more efficient business plan. Let's see how feasible it could be.",
            "source_name": "Zacks Investment Research",
            "date": "Thu, 23 Jul 2020 08:17:00 -0400",
            "topics": [],
            "sentiment": "Neutral",
            "type": "Article",
            "tickers": [
                "KO"
            ],
            "title_ko": "\ucf54\uce74\uc778\uc758 \uc880\ube44 \ube0c\ub79c\ub4dc \uc778\ud558 \uacc4\ud68d\uc774 \uc218\uc775\uc744 \uc99d\ub300\uc2dc\ud0ac \uac83\uc778\uac00?"
        }
    ]
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
  "data": {
    "annualReports": [
      {
        "accountsPayable": "3804000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "None", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "17154000000", 
        "cash": "6480000000", 
        "cashAndShortTermInvestments": "7947000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4314000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "15247000000", 
        "deferredLongTermAssetCharges": "2412000000", 
        "deferredLongTermLiabilities": "2284000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2019-12-31", 
        "goodwill": "16764000000", 
        "intangibleAssets": "10002000000", 
        "inventory": "3379000000", 
        "liabilitiesAndShareholderEquity": "86381000000", 
        "longTermDebt": "27516000000", 
        "longTermInvestments": "19879000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3971000000", 
        "netTangibleAssets": "-7785000000", 
        "otherAssets": "5264000000", 
        "otherCurrentAssets": "1886000000", 
        "otherCurrentLiabilities": "565000000", 
        "otherLiabilities": "9662000000", 
        "otherNonCurrentLiabilities": "8510000000", 
        "otherNonCurrrentAssets": "6075000000", 
        "otherShareholderEquity": "-13544000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "None", 
        "propertyPlantEquipment": "12210000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "65855000000", 
        "retainedEarningsTotalEquity": "65855000000", 
        "shortTermDebt": "15247000000", 
        "shortTermInvestments": "4695000000", 
        "totalAssets": "86381000000", 
        "totalCurrentAssets": "20411000000", 
        "totalCurrentLiabilities": "26973000000", 
        "totalLiabilities": "65283000000", 
        "totalLongTermDebt": "27516000000", 
        "totalNonCurrentAssets": "65970000000", 
        "totalNonCurrentLiabilities": "38310000000", 
        "totalPermanentEquity": "None", 
        "totalShareholderEquity": "18981000000", 
        "treasuryStock": "-52244000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "2498000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "None", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "16520000000", 
        "cash": "8926000000", 
        "cashAndShortTermInvestments": "10951000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4299000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "18191000000", 
        "deferredLongTermAssetCharges": "2667000000", 
        "deferredLongTermLiabilities": "1933000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2018-12-31", 
        "goodwill": "10263000000", 
        "intangibleAssets": "7007000000", 
        "inventory": "2766000000", 
        "liabilitiesAndShareholderEquity": "83216000000", 
        "longTermDebt": "25364000000", 
        "longTermInvestments": "20274000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3396000000", 
        "netTangibleAssets": "-4606000000", 
        "otherAssets": "5563000000", 
        "otherCurrentAssets": "8508000000", 
        "otherCurrentLiabilities": "1722000000", 
        "otherLiabilities": "9960000000", 
        "otherNonCurrentLiabilities": "7638000000", 
        "otherNonCurrrentAssets": "4139000000", 
        "otherShareholderEquity": "-12814000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "None", 
        "propertyPlantEquipment": "9598000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "63234000000", 
        "retainedEarningsTotalEquity": "63234000000", 
        "shortTermDebt": "18191000000", 
        "shortTermInvestments": "7038000000", 
        "totalAssets": "83216000000", 
        "totalCurrentAssets": "30634000000", 
        "totalCurrentLiabilities": "29223000000", 
        "totalLiabilities": "64158000000", 
        "totalLongTermDebt": "25376000000", 
        "totalNonCurrentAssets": "52582000000", 
        "totalNonCurrentLiabilities": "34935000000", 
        "totalPermanentEquity": "None", 
        "totalShareholderEquity": "16981000000", 
        "treasuryStock": "-51719000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "2288000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "15864000000", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "15864000000", 
        "cash": "6006000000", 
        "cashAndShortTermInvestments": "15358000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4324000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "16503000000", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "2522000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2017-12-31", 
        "goodwill": "9401000000", 
        "intangibleAssets": "7235000000", 
        "inventory": "2655000000", 
        "liabilitiesAndShareholderEquity": "87896000000", 
        "longTermDebt": "31182000000", 
        "longTermInvestments": "21952000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3667000000", 
        "netTangibleAssets": "436000000", 
        "otherAssets": "3231000000", 
        "otherCurrentAssets": "9548000000", 
        "otherCurrentLiabilities": "1533000000", 
        "otherLiabilities": "10504000000", 
        "otherNonCurrentLiabilities": "8021000000", 
        "otherNonCurrrentAssets": "4560000000", 
        "otherShareholderEquity": "-10305000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "8203000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "60430000000", 
        "retainedEarningsTotalEquity": "60430000000", 
        "shortTermDebt": "3298000000", 
        "shortTermInvestments": "14669000000", 
        "totalAssets": "87896000000", 
        "totalCurrentAssets": "36545000000", 
        "totalCurrentLiabilities": "27194000000", 
        "totalLiabilities": "68919000000", 
        "totalLongTermDebt": "31182000000", 
        "totalNonCurrentAssets": "51351000000", 
        "totalNonCurrentLiabilities": "41725000000", 
        "totalPermanentEquity": "18977000000", 
        "totalShareholderEquity": "17072000000", 
        "treasuryStock": "-50677000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "2682000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "14993000000", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "14993000000", 
        "cash": "8555000000", 
        "cashAndShortTermInvestments": "18150000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4367000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "16025000000", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "3753000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2016-12-31", 
        "goodwill": "10629000000", 
        "intangibleAssets": "10499000000", 
        "inventory": "2675000000", 
        "liabilitiesAndShareholderEquity": "87270000000", 
        "longTermDebt": "29684000000", 
        "longTermInvestments": "17249000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3856000000", 
        "netTangibleAssets": "1934000000", 
        "otherAssets": "2928000000", 
        "otherCurrentAssets": "5278000000", 
        "otherCurrentLiabilities": "710000000", 
        "otherLiabilities": "7786000000", 
        "otherNonCurrentLiabilities": "4081000000", 
        "otherNonCurrrentAssets": "4248000000", 
        "otherShareholderEquity": "-11205000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "10635000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "65502000000", 
        "retainedEarningsTotalEquity": "65502000000", 
        "shortTermDebt": "3527000000", 
        "shortTermInvestments": "13646000000", 
        "totalAssets": "87270000000", 
        "totalCurrentAssets": "34010000000", 
        "totalCurrentLiabilities": "26532000000", 
        "totalLiabilities": "64050000000", 
        "totalLongTermDebt": "29684000000", 
        "totalNonCurrentAssets": "53260000000", 
        "totalNonCurrentLiabilities": "37518000000", 
        "totalPermanentEquity": "23220000000", 
        "totalShareholderEquity": "23062000000", 
        "treasuryStock": "-47988000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "9991000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "0", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "14016000000", 
        "cash": "7309000000", 
        "cashAndShortTermInvestments": "15631000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4405000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "2729000000", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "4691000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2015-12-31", 
        "goodwill": "11289000000", 
        "intangibleAssets": "12843000000", 
        "inventory": "2902000000", 
        "liabilitiesAndShareholderEquity": "90093000000", 
        "longTermDebt": "28543000000", 
        "longTermInvestments": "12318000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3941000000", 
        "netTangibleAssets": "2276000000", 
        "otherAssets": "3030000000", 
        "otherCurrentAssets": "6652000000", 
        "otherCurrentLiabilities": "14262000000", 
        "otherLiabilities": "8760000000", 
        "otherNonCurrentLiabilities": "4301000000", 
        "otherNonCurrrentAssets": "8531000000", 
        "otherShareholderEquity": "-10174000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "12571000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "65018000000", 
        "retainedEarningsTotalEquity": "65018000000", 
        "shortTermDebt": "2729000000", 
        "shortTermInvestments": "12591000000", 
        "totalAssets": "89996000000", 
        "totalCurrentAssets": "33395000000", 
        "totalCurrentLiabilities": "26929000000", 
        "totalLiabilities": "64232000000", 
        "totalLongTermDebt": "28311000000", 
        "totalNonCurrentAssets": "56698000000", 
        "totalNonCurrentLiabilities": "37399000000", 
        "totalPermanentEquity": "0", 
        "totalShareholderEquity": "25554000000", 
        "treasuryStock": "-45066000000", 
        "warrants": "None"
      }
    ], 
    "quarterlyReports": [
      {
        "accountsPayable": "12640000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "None", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "17312000000", 
        "cash": "13561000000", 
        "cashAndShortTermInvestments": "15274000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4325000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "19299000000", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "1856000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2020-03-31", 
        "goodwill": "16673000000", 
        "intangibleAssets": "11165000000", 
        "inventory": "3558000000", 
        "liabilitiesAndShareholderEquity": "94013000000", 
        "longTermDebt": "31094000000", 
        "longTermInvestments": "18672000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "4430000000", 
        "netTangibleAssets": "-9680000000", 
        "otherAssets": "8276000000", 
        "otherCurrentAssets": "2580000000", 
        "otherCurrentLiabilities": "None", 
        "otherLiabilities": "10688000000", 
        "otherNonCurrentLiabilities": "8832000000", 
        "otherNonCurrrentAssets": "6001000000", 
        "otherShareholderEquity": "-15696000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "None", 
        "propertyPlantEquipment": "10993000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "66870000000", 
        "retainedEarningsTotalEquity": "66870000000", 
        "shortTermDebt": "19299000000", 
        "shortTermInvestments": "4105000000", 
        "totalAssets": "94013000000", 
        "totalCurrentAssets": "28234000000", 
        "totalCurrentLiabilities": "32397000000", 
        "totalLiabilities": "74179000000", 
        "totalLongTermDebt": "31094000000", 
        "totalNonCurrentAssets": "65779000000", 
        "totalNonCurrentLiabilities": "41782000000", 
        "totalPermanentEquity": "None", 
        "totalShareholderEquity": "18158000000", 
        "treasuryStock": "-52088000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "3804000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "None", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "17154000000", 
        "cash": "6480000000", 
        "cashAndShortTermInvestments": "7947000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4314000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "15247000000", 
        "deferredLongTermAssetCharges": "2412000000", 
        "deferredLongTermLiabilities": "2284000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2019-12-31", 
        "goodwill": "16764000000", 
        "intangibleAssets": "10002000000", 
        "inventory": "3379000000", 
        "liabilitiesAndShareholderEquity": "86381000000", 
        "longTermDebt": "27516000000", 
        "longTermInvestments": "19879000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3971000000", 
        "netTangibleAssets": "-7785000000", 
        "otherAssets": "5264000000", 
        "otherCurrentAssets": "1886000000", 
        "otherCurrentLiabilities": "565000000", 
        "otherLiabilities": "9662000000", 
        "otherNonCurrentLiabilities": "8510000000", 
        "otherNonCurrrentAssets": "6075000000", 
        "otherShareholderEquity": "-13544000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "None", 
        "propertyPlantEquipment": "12210000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "65855000000", 
        "retainedEarningsTotalEquity": "65855000000", 
        "shortTermDebt": "15247000000", 
        "shortTermInvestments": "4695000000", 
        "totalAssets": "86381000000", 
        "totalCurrentAssets": "20411000000", 
        "totalCurrentLiabilities": "26973000000", 
        "totalLiabilities": "65283000000", 
        "totalLongTermDebt": "27516000000", 
        "totalNonCurrentAssets": "65970000000", 
        "totalNonCurrentLiabilities": "38310000000", 
        "totalPermanentEquity": "None", 
        "totalShareholderEquity": "18981000000", 
        "treasuryStock": "-52244000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "12474000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "8267000000", 
        "additionalPaidInCapital": "None", 
        "capitalLeaseObligations": "1329000000", 
        "capitalSurplus": "17039000000", 
        "cash": "7531000000", 
        "cashAndShortTermInvestments": "9532000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4321000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "11464000000", 
        "deferredLongTermAssetCharges": "2452000000", 
        "deferredLongTermLiabilities": "2581000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2019-09-30", 
        "goodwill": "16465000000", 
        "intangibleAssets": "9865000000", 
        "inventory": "3266000000", 
        "liabilitiesAndShareholderEquity": "87433000000", 
        "longTermDebt": "31012000000", 
        "longTermInvestments": "19567000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "4353000000", 
        "netTangibleAssets": "-7617000000", 
        "otherAssets": "4870000000", 
        "otherCurrentAssets": "2510000000", 
        "otherCurrentLiabilities": "1040000000", 
        "otherLiabilities": "9562000000", 
        "otherNonCurrentLiabilities": "6981000000", 
        "otherNonCurrrentAssets": "4440000000", 
        "otherShareholderEquity": "-13706000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "None", 
        "propertyPlantEquipment": "10217000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "65481000000", 
        "retainedEarningsTotalEquity": "65481000000", 
        "shortTermDebt": "11464000000", 
        "shortTermInvestments": "5457000000", 
        "totalAssets": "87433000000", 
        "totalCurrentAssets": "23117000000", 
        "totalCurrentLiabilities": "25100000000", 
        "totalLiabilities": "66750000000", 
        "totalLongTermDebt": "31012000000", 
        "totalNonCurrentAssets": "64316000000", 
        "totalNonCurrentLiabilities": "41650000000", 
        "totalPermanentEquity": "None", 
        "totalShareholderEquity": "18713000000", 
        "treasuryStock": "-51861000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "12537000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "8222000000", 
        "additionalPaidInCapital": "None", 
        "capitalLeaseObligations": "1353000000", 
        "capitalSurplus": "16833000000", 
        "cash": "6731000000", 
        "cashAndShortTermInvestments": "9303000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4305000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "15779000000", 
        "deferredLongTermAssetCharges": "2559000000", 
        "deferredLongTermLiabilities": "2687000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2019-06-30", 
        "goodwill": "16840000000", 
        "intangibleAssets": "10075000000", 
        "inventory": "3453000000", 
        "liabilitiesAndShareholderEquity": "89996000000", 
        "longTermDebt": "29296000000", 
        "longTermInvestments": "20312000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "4888000000", 
        "netTangibleAssets": "-8734000000", 
        "otherAssets": "5064000000", 
        "otherCurrentAssets": "2658000000", 
        "otherCurrentLiabilities": "941000000", 
        "otherLiabilities": "9941000000", 
        "otherNonCurrentLiabilities": "7265000000", 
        "otherNonCurrrentAssets": "4266000000", 
        "otherShareholderEquity": "-12981000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "None", 
        "propertyPlantEquipment": "10254000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "64602000000", 
        "retainedEarningsTotalEquity": "64602000000", 
        "shortTermDebt": "15779000000", 
        "shortTermInvestments": "6630000000", 
        "totalAssets": "89996000000", 
        "totalCurrentAssets": "24360000000", 
        "totalCurrentLiabilities": "29382000000", 
        "totalLiabilities": "69701000000", 
        "totalLongTermDebt": "29296000000", 
        "totalNonCurrentAssets": "65636000000", 
        "totalNonCurrentLiabilities": "40319000000", 
        "totalPermanentEquity": "None", 
        "totalShareholderEquity": "18181000000", 
        "treasuryStock": "-52033000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "10735000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "8032000000", 
        "additionalPaidInCapital": "None", 
        "capitalLeaseObligations": "1268000000", 
        "capitalSurplus": "16577000000", 
        "cash": "5645000000", 
        "cashAndShortTermInvestments": "7183000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4306000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "14867000000", 
        "deferredLongTermAssetCharges": "2617000000", 
        "deferredLongTermLiabilities": "2602000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2019-03-31", 
        "goodwill": "12964000000", 
        "intangibleAssets": "9780000000", 
        "inventory": "3178000000", 
        "liabilitiesAndShareholderEquity": "88347000000", 
        "longTermDebt": "29400000000", 
        "longTermInvestments": "20198000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3852000000", 
        "netTangibleAssets": "-5009000000", 
        "otherAssets": "5188000000", 
        "otherCurrentAssets": "9562000000", 
        "otherCurrentLiabilities": "1835000000", 
        "otherLiabilities": "10155000000", 
        "otherNonCurrentLiabilities": "7581000000", 
        "otherNonCurrrentAssets": "4140000000", 
        "otherShareholderEquity": "-12325000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "None", 
        "propertyPlantEquipment": "8866000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "63704000000", 
        "retainedEarningsTotalEquity": "63704000000", 
        "shortTermDebt": "14867000000", 
        "shortTermInvestments": "6303000000", 
        "totalAssets": "88347000000", 
        "totalCurrentAssets": "28540000000", 
        "totalCurrentLiabilities": "27943000000", 
        "totalLiabilities": "68543000000", 
        "totalLongTermDebt": "29400000000", 
        "totalNonCurrentAssets": "59807000000", 
        "totalNonCurrentLiabilities": "40600000000", 
        "totalPermanentEquity": "None", 
        "totalShareholderEquity": "17735000000", 
        "treasuryStock": "-51981000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "9310000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "None", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "16520000000", 
        "cash": "8926000000", 
        "cashAndShortTermInvestments": "10951000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4299000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "4997000000", 
        "deferredLongTermAssetCharges": "2667000000", 
        "deferredLongTermLiabilities": "1933000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2018-12-31", 
        "goodwill": "10263000000", 
        "intangibleAssets": "7007000000", 
        "inventory": "2766000000", 
        "liabilitiesAndShareholderEquity": "83216000000", 
        "longTermDebt": "25404000000", 
        "longTermInvestments": "19407000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3396000000", 
        "netTangibleAssets": "-15000000", 
        "otherAssets": "5547000000", 
        "otherCurrentAssets": "8508000000", 
        "otherCurrentLiabilities": "1722000000", 
        "otherLiabilities": "9531000000", 
        "otherNonCurrentLiabilities": "7638000000", 
        "otherNonCurrrentAssets": "5280000000", 
        "otherShareholderEquity": "-12814000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "None", 
        "propertyPlantEquipment": "8232000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "63234000000", 
        "retainedEarningsTotalEquity": "63234000000", 
        "shortTermDebt": "18191000000", 
        "shortTermInvestments": "7038000000", 
        "totalAssets": "83216000000", 
        "totalCurrentAssets": "30634000000", 
        "totalCurrentLiabilities": "29223000000", 
        "totalLiabilities": "64158000000", 
        "totalLongTermDebt": "25364000000", 
        "totalNonCurrentAssets": "52582000000", 
        "totalNonCurrentLiabilities": "34935000000", 
        "totalPermanentEquity": "None", 
        "totalShareholderEquity": "16981000000", 
        "treasuryStock": "-51719000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "10253000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "8011000000", 
        "additionalPaidInCapital": "16266000000", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "16266000000", 
        "cash": "9065000000", 
        "cashAndShortTermInvestments": "13792000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4295000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "6341000000", 
        "deferredLongTermAssetCharges": "2720000000", 
        "deferredLongTermLiabilities": "2500000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2018-09-28", 
        "goodwill": "9856000000", 
        "intangibleAssets": "6999000000", 
        "inventory": "2627000000", 
        "liabilitiesAndShareholderEquity": "86877000000", 
        "longTermDebt": "25591000000", 
        "longTermInvestments": "20899000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3702000000", 
        "netTangibleAssets": "1689000000", 
        "otherAssets": "4827000000", 
        "otherCurrentAssets": "8237000000", 
        "otherCurrentLiabilities": "1486000000", 
        "otherLiabilities": "9678000000", 
        "otherNonCurrentLiabilities": "7246000000", 
        "otherNonCurrrentAssets": "5866000000", 
        "otherShareholderEquity": "-12070000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "7404000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "64028000000", 
        "retainedEarningsTotalEquity": "63808000000", 
        "shortTermDebt": "19314000000", 
        "shortTermInvestments": "9782000000", 
        "totalAssets": "86877000000", 
        "totalCurrentAssets": "33413000000", 
        "totalCurrentLiabilities": "31430000000", 
        "totalLiabilities": "66699000000", 
        "totalLongTermDebt": "25523000000", 
        "totalNonCurrentAssets": "53464000000", 
        "totalNonCurrentLiabilities": "35269000000", 
        "totalPermanentEquity": "20178000000", 
        "totalShareholderEquity": "18264000000", 
        "treasuryStock": "-51720000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "10777000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "8284000000", 
        "additionalPaidInCapital": "16117000000", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "16117000000", 
        "cash": "7975000000", 
        "cashAndShortTermInvestments": "13818000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4290000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "4023000000", 
        "deferredLongTermAssetCharges": "2999000000", 
        "deferredLongTermLiabilities": "2589000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2018-06-29", 
        "goodwill": "9863000000", 
        "intangibleAssets": "6999000000", 
        "inventory": "2881000000", 
        "liabilitiesAndShareholderEquity": "89593000000", 
        "longTermDebt": "28114000000", 
        "longTermInvestments": "20604000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "4565000000", 
        "netTangibleAssets": "1753000000", 
        "otherAssets": "4829000000", 
        "otherCurrentAssets": "9224000000", 
        "otherCurrentLiabilities": "16171000000", 
        "otherLiabilities": "9905000000", 
        "otherNonCurrentLiabilities": "7367000000", 
        "otherNonCurrrentAssets": "5708000000", 
        "otherShareholderEquity": "-11774000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "7688000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "63808000000", 
        "retainedEarningsTotalEquity": "60430000000", 
        "shortTermDebt": "4023000000", 
        "shortTermInvestments": "11379000000", 
        "totalAssets": "89593000000", 
        "totalCurrentAssets": "36024000000", 
        "totalCurrentLiabilities": "31398000000", 
        "totalLiabilities": "69417000000", 
        "totalLongTermDebt": "28063000000", 
        "totalNonCurrentAssets": "53569000000", 
        "totalNonCurrentLiabilities": "38019000000", 
        "totalPermanentEquity": "20176000000", 
        "totalShareholderEquity": "18323000000", 
        "treasuryStock": "-51588000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "10218000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "8370000000", 
        "additionalPaidInCapital": "16006000000", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "16006000000", 
        "cash": "8291000000", 
        "cashAndShortTermInvestments": "15809000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4306000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "4377000000", 
        "deferredLongTermAssetCharges": "3298000000", 
        "deferredLongTermLiabilities": "2314000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2018-03-30", 
        "goodwill": "9908000000", 
        "intangibleAssets": "6806000000", 
        "inventory": "2937000000", 
        "liabilitiesAndShareholderEquity": "93282000000", 
        "longTermDebt": "29792000000", 
        "longTermInvestments": "21478000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3904000000", 
        "netTangibleAssets": "2896000000", 
        "otherAssets": "47263000000", 
        "otherCurrentAssets": "9828000000", 
        "otherCurrentLiabilities": "16313000000", 
        "otherLiabilities": "8079000000", 
        "otherNonCurrentLiabilities": "8079000000", 
        "otherNonCurrrentAssets": "5773000000", 
        "otherShareholderEquity": "-10038000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "7977000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "63150000000", 
        "retainedEarningsTotalEquity": "60430000000", 
        "shortTermDebt": "4370000000", 
        "shortTermInvestments": "13082000000", 
        "totalAssets": "93282000000", 
        "totalCurrentAssets": "38042000000", 
        "totalCurrentLiabilities": "31480000000", 
        "totalLiabilities": "71665000000", 
        "totalLongTermDebt": "29792000000", 
        "totalNonCurrentAssets": "55240000000", 
        "totalNonCurrentLiabilities": "40185000000", 
        "totalPermanentEquity": "21617000000", 
        "totalShareholderEquity": "19610000000", 
        "treasuryStock": "-51268000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "9158000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "15864000000", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "15864000000", 
        "cash": "6006000000", 
        "cashAndShortTermInvestments": "15358000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4324000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "3328000000", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "2522000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2017-12-31", 
        "goodwill": "9401000000", 
        "intangibleAssets": "6867000000", 
        "inventory": "2655000000", 
        "liabilitiesAndShareholderEquity": "87896000000", 
        "longTermDebt": "31182000000", 
        "longTermInvestments": "20856000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3667000000", 
        "netTangibleAssets": "804000000", 
        "otherAssets": "43148000000", 
        "otherCurrentAssets": "9548000000", 
        "otherCurrentLiabilities": "14738000000", 
        "otherLiabilities": "8021000000", 
        "otherNonCurrentLiabilities": "8021000000", 
        "otherNonCurrrentAssets": "6024000000", 
        "otherShareholderEquity": "-10305000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "8203000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "60430000000", 
        "retainedEarningsTotalEquity": "60430000000", 
        "shortTermDebt": "3298000000", 
        "shortTermInvestments": "14669000000", 
        "totalAssets": "87896000000", 
        "totalCurrentAssets": "36545000000", 
        "totalCurrentLiabilities": "27194000000", 
        "totalLiabilities": "68919000000", 
        "totalLongTermDebt": "31182000000", 
        "totalNonCurrentAssets": "51351000000", 
        "totalNonCurrentLiabilities": "41725000000", 
        "totalPermanentEquity": "18977000000", 
        "totalShareholderEquity": "17072000000", 
        "treasuryStock": "-50677000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "10212000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "15699000000", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "15699000000", 
        "cash": "12528000000", 
        "cashAndShortTermInvestments": "22219000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4320000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "3264000000", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "4313000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2017-09-29", 
        "goodwill": "9473000000", 
        "intangibleAssets": "6713000000", 
        "inventory": "2608000000", 
        "liabilitiesAndShareholderEquity": "90515000000", 
        "longTermDebt": "32471000000", 
        "longTermInvestments": "21644000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3664000000", 
        "netTangibleAssets": "5555000000", 
        "otherAssets": "43805000000", 
        "otherCurrentAssets": "4775000000", 
        "otherCurrentLiabilities": "13835000000", 
        "otherLiabilities": "3946000000", 
        "otherNonCurrentLiabilities": "3946000000", 
        "otherNonCurrrentAssets": "5975000000", 
        "otherShareholderEquity": "-9843000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "8306000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "64759000000", 
        "retainedEarningsTotalEquity": "64759000000", 
        "shortTermDebt": "3231000000", 
        "shortTermInvestments": "14829000000", 
        "totalAssets": "90515000000", 
        "totalCurrentAssets": "38404000000", 
        "totalCurrentLiabilities": "27633000000", 
        "totalLiabilities": "68363000000", 
        "totalLongTermDebt": "32471000000", 
        "totalNonCurrentAssets": "52111000000", 
        "totalNonCurrentLiabilities": "40730000000", 
        "totalPermanentEquity": "22152000000", 
        "totalShareholderEquity": "22119000000", 
        "treasuryStock": "-50256000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "10363000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "15473000000", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "15473000000", 
        "cash": "11718000000", 
        "cashAndShortTermInvestments": "22734000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4327000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "49720000000", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "4330000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2017-06-30", 
        "goodwill": "9449000000", 
        "intangibleAssets": "7299000000", 
        "inventory": "2790000000", 
        "liabilitiesAndShareholderEquity": "91146000000", 
        "longTermDebt": "31805000000", 
        "longTermInvestments": "20845000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "4024000000", 
        "netTangibleAssets": "4809000000", 
        "otherAssets": "43513000000", 
        "otherCurrentAssets": "4923000000", 
        "otherCurrentLiabilities": "14638000000", 
        "otherLiabilities": "4092000000", 
        "otherNonCurrentLiabilities": "4092000000", 
        "otherNonCurrrentAssets": "5920000000", 
        "otherShareholderEquity": "-10489000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "8672000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "64890000000", 
        "retainedEarningsTotalEquity": "64890000000", 
        "shortTermDebt": "3478000000", 
        "shortTermInvestments": "15506000000", 
        "totalAssets": "91146000000", 
        "totalCurrentAssets": "38961000000", 
        "totalCurrentLiabilities": "28830000000", 
        "totalLiabilities": "69057000000", 
        "totalLongTermDebt": "31805000000", 
        "totalNonCurrentAssets": "52185000000", 
        "totalNonCurrentLiabilities": "40227000000", 
        "totalPermanentEquity": "22089000000", 
        "totalShareholderEquity": "22001000000", 
        "treasuryStock": "-49633000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "10251000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "15197000000", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "15197000000", 
        "cash": "12120000000", 
        "cashAndShortTermInvestments": "21911000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4334000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "15911000000", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "3899000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2017-03-31", 
        "goodwill": "10008000000", 
        "intangibleAssets": "8247000000", 
        "inventory": "2885000000", 
        "liabilitiesAndShareholderEquity": "91201000000", 
        "longTermDebt": "31538000000", 
        "longTermInvestments": "16753000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3702000000", 
        "netTangibleAssets": "4621000000", 
        "otherAssets": "41204000000", 
        "otherCurrentAssets": "8459000000", 
        "otherCurrentLiabilities": "15952000000", 
        "otherLiabilities": "4041000000", 
        "otherNonCurrentLiabilities": "4041000000", 
        "otherNonCurrrentAssets": "6196000000", 
        "otherShareholderEquity": "-10206000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "9746000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "65099000000", 
        "retainedEarningsTotalEquity": "65099000000", 
        "shortTermDebt": "2185000000", 
        "shortTermInvestments": "13085000000", 
        "totalAssets": "91201000000", 
        "totalCurrentAssets": "40251000000", 
        "totalCurrentLiabilities": "28656000000", 
        "totalLiabilities": "68134000000", 
        "totalLongTermDebt": "31538000000", 
        "totalNonCurrentAssets": "50950000000", 
        "totalNonCurrentLiabilities": "39478000000", 
        "totalPermanentEquity": "23067000000", 
        "totalShareholderEquity": "22876000000", 
        "treasuryStock": "-48974000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "9797000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "14993000000", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "14993000000", 
        "cash": "8555000000", 
        "cashAndShortTermInvestments": "18150000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4367000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "3571000000", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "3753000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2016-12-31", 
        "goodwill": "10629000000", 
        "intangibleAssets": "9773000000", 
        "inventory": "2675000000", 
        "liabilitiesAndShareholderEquity": "87270000000", 
        "longTermDebt": "29684000000", 
        "longTermInvestments": "16260000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3856000000", 
        "netTangibleAssets": "2660000000", 
        "otherAssets": "42625000000", 
        "otherCurrentAssets": "5278000000", 
        "otherCurrentLiabilities": "13208000000", 
        "otherLiabilities": "4081000000", 
        "otherNonCurrentLiabilities": "4081000000", 
        "otherNonCurrrentAssets": "5963000000", 
        "otherShareholderEquity": "-11205000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "10635000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "65502000000", 
        "retainedEarningsTotalEquity": "65502000000", 
        "shortTermDebt": "3527000000", 
        "shortTermInvestments": "13646000000", 
        "totalAssets": "87270000000", 
        "totalCurrentAssets": "34010000000", 
        "totalCurrentLiabilities": "26532000000", 
        "totalLiabilities": "64050000000", 
        "totalLongTermDebt": "29684000000", 
        "totalNonCurrentAssets": "53260000000", 
        "totalNonCurrentLiabilities": "37518000000", 
        "totalPermanentEquity": "23220000000", 
        "totalShareholderEquity": "23062000000", 
        "treasuryStock": "-47988000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "11153000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "14882000000", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "14882000000", 
        "cash": "11147000000", 
        "cashAndShortTermInvestments": "22412000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4364000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "15561000000", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "4243000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2016-09-30", 
        "goodwill": "10865000000", 
        "intangibleAssets": "10621000000", 
        "inventory": "2751000000", 
        "liabilitiesAndShareholderEquity": "93927000000", 
        "longTermDebt": "31663000000", 
        "longTermInvestments": "16917000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "4082000000", 
        "netTangibleAssets": "4590000000", 
        "otherAssets": "44799000000", 
        "otherCurrentAssets": "5554000000", 
        "otherCurrentLiabilities": "12770000000", 
        "otherLiabilities": "3984000000", 
        "otherNonCurrentLiabilities": "3984000000", 
        "otherNonCurrrentAssets": "6396000000", 
        "otherShareholderEquity": "-10209000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "11172000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "66457000000", 
        "retainedEarningsTotalEquity": "66457000000", 
        "shortTermDebt": "3473000000", 
        "shortTermInvestments": "14422000000", 
        "totalAssets": "93927000000", 
        "totalCurrentAssets": "37956000000", 
        "totalCurrentLiabilities": "27792000000", 
        "totalLiabilities": "67682000000", 
        "totalLongTermDebt": "31663000000", 
        "totalNonCurrentAssets": "55971000000", 
        "totalNonCurrentLiabilities": "39890000000", 
        "totalPermanentEquity": "26245000000", 
        "totalShareholderEquity": "26076000000", 
        "treasuryStock": "-46814000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "10235000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "14710000000", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "14710000000", 
        "cash": "9647000000", 
        "cashAndShortTermInvestments": "21402000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4377000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "18796000000", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "4497000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2016-06-30", 
        "goodwill": "11204000000", 
        "intangibleAssets": "11654000000", 
        "inventory": "3005000000", 
        "liabilitiesAndShareholderEquity": "94094000000", 
        "longTermDebt": "29252000000", 
        "longTermInvestments": "16215000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "4768000000", 
        "netTangibleAssets": "3779000000", 
        "otherAssets": "45558000000", 
        "otherCurrentAssets": "4025000000", 
        "otherCurrentLiabilities": "14039000000", 
        "otherLiabilities": "3963000000", 
        "otherNonCurrentLiabilities": "3963000000", 
        "otherNonCurrrentAssets": "6485000000", 
        "otherShareholderEquity": "-10153000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "12663000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "66921000000", 
        "retainedEarningsTotalEquity": "66921000000", 
        "shortTermDebt": "4895000000", 
        "shortTermInvestments": "14428000000", 
        "totalAssets": "94094000000", 
        "totalCurrentAssets": "35873000000", 
        "totalCurrentLiabilities": "29544000000", 
        "totalLiabilities": "67256000000", 
        "totalLongTermDebt": "29252000000", 
        "totalNonCurrentAssets": "58221000000", 
        "totalNonCurrentLiabilities": "37712000000", 
        "totalPermanentEquity": "26838000000", 
        "totalShareholderEquity": "26637000000", 
        "treasuryStock": "-46601000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "9626000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "0", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "14507000000", 
        "cash": "8748000000", 
        "cashAndShortTermInvestments": "18751000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4382000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "None", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "4337000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2016-03-31", 
        "goodwill": "11396000000", 
        "intangibleAssets": "11728000000", 
        "inventory": "3052000000", 
        "liabilitiesAndShareholderEquity": "91263000000", 
        "longTermDebt": "26990000000", 
        "longTermInvestments": "12610000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "4147000000", 
        "netTangibleAssets": "1790000000", 
        "otherAssets": "42140000000", 
        "otherCurrentAssets": "7100000000", 
        "otherCurrentLiabilities": "16130000000", 
        "otherLiabilities": "3820000000", 
        "otherNonCurrentLiabilities": "3820000000", 
        "otherNonCurrrentAssets": "6406000000", 
        "otherShareholderEquity": "-10789000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "12613000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "64985000000", 
        "retainedEarningsTotalEquity": "64985000000", 
        "shortTermDebt": "4956000000", 
        "shortTermInvestments": "13463000000", 
        "totalAssets": "91263000000", 
        "totalCurrentAssets": "36510000000", 
        "totalCurrentLiabilities": "30987000000", 
        "totalLiabilities": "66134000000", 
        "totalLongTermDebt": "26990000000", 
        "totalNonCurrentAssets": "54753000000", 
        "totalNonCurrentLiabilities": "35147000000", 
        "totalPermanentEquity": "0", 
        "totalShareholderEquity": "24914000000", 
        "treasuryStock": "-45549000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "9991000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "0", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "14016000000", 
        "cash": "7309000000", 
        "cashAndShortTermInvestments": "15631000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "4405000000", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "2729000000", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "4691000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2015-12-31", 
        "goodwill": "11289000000", 
        "intangibleAssets": "11989000000", 
        "inventory": "2902000000", 
        "liabilitiesAndShareholderEquity": "90093000000", 
        "longTermDebt": "28407000000", 
        "longTermInvestments": "12318000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "3941000000", 
        "netTangibleAssets": "2276000000", 
        "otherAssets": "44127000000", 
        "otherCurrentAssets": "6652000000", 
        "otherCurrentLiabilities": "14262000000", 
        "otherLiabilities": "4301000000", 
        "otherNonCurrentLiabilities": "4301000000", 
        "otherNonCurrrentAssets": "8531000000", 
        "otherShareholderEquity": "-10174000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "12571000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "65018000000", 
        "retainedEarningsTotalEquity": "65018000000", 
        "shortTermDebt": "2677000000", 
        "shortTermInvestments": "12591000000", 
        "totalAssets": "90093000000", 
        "totalCurrentAssets": "33395000000", 
        "totalCurrentLiabilities": "26930000000", 
        "totalLiabilities": "64329000000", 
        "totalLongTermDebt": "28407000000", 
        "totalNonCurrentAssets": "56698000000", 
        "totalNonCurrentLiabilities": "37399000000", 
        "totalPermanentEquity": "0", 
        "totalShareholderEquity": "25554000000", 
        "treasuryStock": "-45066000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "9877000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "0", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "13715000000", 
        "cash": "9983000000", 
        "cashAndShortTermInvestments": "19160000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "None", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "None", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "5053000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2015-10-02", 
        "goodwill": "11357000000", 
        "intangibleAssets": "12165000000", 
        "inventory": "2910000000", 
        "liabilitiesAndShareholderEquity": "93008000000", 
        "longTermDebt": "25949000000", 
        "longTermInvestments": "12504000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "4028000000", 
        "netTangibleAssets": "2527000000", 
        "otherAssets": "43799000000", 
        "otherCurrentAssets": "6882000000", 
        "otherCurrentLiabilities": "18593000000", 
        "otherLiabilities": "4194000000", 
        "otherNonCurrentLiabilities": "4194000000", 
        "otherNonCurrrentAssets": "7773000000", 
        "otherShareholderEquity": "-10813000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "12615000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "65209000000", 
        "retainedEarningsTotalEquity": "65209000000", 
        "shortTermDebt": "2692000000", 
        "shortTermInvestments": "12791000000", 
        "totalAssets": "93008000000", 
        "totalCurrentAssets": "36594000000", 
        "totalCurrentLiabilities": "31545000000", 
        "totalLiabilities": "66741000000", 
        "totalLongTermDebt": "25949000000", 
        "totalNonCurrentAssets": "56414000000", 
        "totalNonCurrentLiabilities": "35196000000", 
        "totalPermanentEquity": "0", 
        "totalShareholderEquity": "26049000000", 
        "treasuryStock": "-43822000000", 
        "warrants": "None"
      }, 
      {
        "accountsPayable": "9997000000", 
        "accumulatedAmortization": "None", 
        "accumulatedDepreciation": "None", 
        "additionalPaidInCapital": "0", 
        "capitalLeaseObligations": "None", 
        "capitalSurplus": "13486000000", 
        "cash": "8805000000", 
        "cashAndShortTermInvestments": "17514000000", 
        "commonStock": "1760000000", 
        "commonStockSharesOutstanding": "None", 
        "commonStockTotalEquity": "1760000000", 
        "currentLongTermDebt": "None", 
        "deferredLongTermAssetCharges": "None", 
        "deferredLongTermLiabilities": "5785000000", 
        "earningAssets": "None", 
        "fiscalDateEnding": "2015-07-03", 
        "goodwill": "11706000000", 
        "intangibleAssets": "13398000000", 
        "inventory": "3224000000", 
        "liabilitiesAndShareholderEquity": "93538000000", 
        "longTermDebt": "25977000000", 
        "longTermInvestments": "12771000000", 
        "negativeGoodwill": "None", 
        "netReceivables": "4976000000", 
        "netTangibleAssets": "3314000000", 
        "otherAssets": "46370000000", 
        "otherCurrentAssets": "3656000000", 
        "otherCurrentLiabilities": "16387000000", 
        "otherLiabilities": "4283000000", 
        "otherNonCurrentLiabilities": "4283000000", 
        "otherNonCurrrentAssets": "8495000000", 
        "otherShareholderEquity": "-8736000000", 
        "preferredStockRedeemable": "None", 
        "preferredStockTotalEquity": "0", 
        "propertyPlantEquipment": "14365000000", 
        "reportedCurrency": "USD", 
        "retainedEarnings": "65196000000", 
        "retainedEarningsTotalEquity": "65196000000", 
        "shortTermDebt": "2031000000", 
        "shortTermInvestments": "12142000000", 
        "totalAssets": "93538000000", 
        "totalCurrentAssets": "32803000000", 
        "totalCurrentLiabilities": "28852000000", 
        "totalLiabilities": "64897000000", 
        "totalLongTermDebt": "25977000000", 
        "totalNonCurrentAssets": "60735000000", 
        "totalNonCurrentLiabilities": "36045000000", 
        "totalPermanentEquity": "0", 
        "totalShareholderEquity": "28418000000", 
        "treasuryStock": "-43288000000", 
        "warrants": "None"
      }
    ], 
    "symbol": "KO"
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


### 기업 요약 정보
Test URL : http://15.164.248.209:20000/rest/getCompanySummaryInfo?symbol=KO

```
GET /rest/getCompanySummaryInfo
```

- request 
```
{
  "symbol" : "KO"
}
```

- response 
```
SUCCESS

{
  "data": {
    "200DayMovingAverage": "49.464", 
    "50DayMovingAverage": "46.1911", 
    "52WeekHigh": "60.13", 
    "52WeekLow": "36.27", 
    "Address": "One Coca-Cola Plaza, Atlanta, GA, United States, 30301", 
    "AnalystTargetPrice": "53.45", 
    "AssetType": "Common Stock", 
    "Beta": "0.544", 
    "BookValue": "4.071", 
    "Country": "USA", 
    "Currency": "USD", 
    "Description": "The Coca-Cola Company, a beverage company, manufactures, markets, and sells various nonalcoholic beverages worldwide. The company provides sparkling soft drinks; water, enhanced water, and sports drinks; juice, dairy, and plantbased beverages; tea and coffee; and energy drinks. It also offers beverage concentrates and syrups, as well as fountain syrups to fountain retailers, such as restaurants and convenience stores. The company sells its products under the Coca-Cola, Diet Coke/Coca-Cola Light, Coca-Cola Zero Sugar, Fanta, Fresca, Schweppes, Sprite, Thums Up, Aquarius, Ciel, Dasani, glacau smartwater, glacau vitaminwater, Ice Dew, I LOHAS, Powerade, Topo Chico, AdeS, Del Valle, fairlife, innocent, Minute Maid, Minute Maid Pulpy, Simply, ZICO, Ayataka, Costa, dogadan, FUZE TEA, Georgia, Gold Peak, HONEST TEA, and Kochakaden brands. It operates through a network of company-owned or controlled bottling and distribution operators, as well as through independent bottling partners, distributors, wholesalers, and retailers. The company was founded in 1886 and is headquartered in Atlanta, Georgia.", 
    "DilutedEPSTTM": "2.12", 
    "DividendDate": "2020-10-01", 
    "DividendPerShare": "1.64", 
    "DividendYield": "0.034", 
    "EBITDA": "11226999808", 
    "EPS": "2.12", 
    "EVToEBITDA": "18.2904", 
    "EVToRevenue": "7.0133", 
    "ExDividendDate": "2020-09-14", 
    "Exchange": "NYSE", 
    "FiscalYearEnd": "December", 
    "ForwardAnnualDividendRate": "1.64", 
    "ForwardAnnualDividendYield": "0.034", 
    "ForwardPE": "25.5102", 
    "FullTimeEmployees": "86200", 
    "GrossProfitTTM": "22647000000", 
    "Industry": "BeveragesNon-Alcoholic", 
    "LastSplitDate": "2012-08-13", 
    "LastSplitFactor": "2:1", 
    "LatestQuarter": "2020-03-31", 
    "MarketCapitalization": "209230872576", 
    "Name": "The Coca-Cola Company", 
    "OperatingMarginTTM": "0.2831", 
    "PEGRatio": "4.2422", 
    "PERatio": "22.8679", 
    "PayoutRatio": "0.7642", 
    "PercentInsiders": "0.696", 
    "PercentInstitutions": "69.997", 
    "PriceToBookRatio": "11.9093", 
    "PriceToSalesRatioTTM": "6.1041", 
    "ProfitMargin": "0.2677", 
    "QuarterlyEarningsGrowthYOY": "-0.328", 
    "QuarterlyRevenueGrowthYOY": "-0.285", 
    "ReturnOnAssetsTTM": "0.0658", 
    "ReturnOnEquityTTM": "0.4664", 
    "RevenuePerShareTTM": "8.007", 
    "RevenueTTM": "34325999616", 
    "Sector": "Consumer Defensive", 
    "SharesFloat": "4261370150", 
    "SharesOutstanding": "4295439872", 
    "SharesShort": "24221422", 
    "SharesShortPriorMonth": "26507099", 
    "ShortPercentFloat": "0.0057", 
    "ShortPercentOutstanding": "0.01", 
    "ShortRatio": "1.33", 
    "Symbol": "KO", 
    "TrailingPE": "22.8679"
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
