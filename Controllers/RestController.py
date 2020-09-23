from flask_restful import Resource,reqparse
from flask import Flask, render_template, jsonify, request
from fake_useragent import UserAgent

import requests
import os
import sys
#import pandas_datareader as pdr
import json
#from bs4 import BeautifulSoup
#import FinanceDataReader as fdr
#from selenium import webdriver
#import calendar
from datetime import datetime
import pymysql


#hii
#Response 임시 코드
RES_FAIL = 100 #실패
RES_FAIL_PARAM_ERR = 101 #필수 파라미터 에러
RES_SUCCESS = 200 #성공

# DB
HOST = "0.0.0.0"
USERNAME = "root"
PASSWORD = "app"
DB_NAME = "finance_db"


class RestController(Resource):

    # Get 요청에 대한 콜백함수
    def get(self, service_name):

        print("[RestController]get request received! service_name : {}".format(service_name))

        #배당 이력 구하기
        if service_name == "getDividendHistory":

            print("params : {}".format(request.args))

            #키 검사
            ticker = request.args.get('ticker')
            start_year = request.args.get('start_year')
            end_year = request.args.get('end_year')

            if ticker != None and start_year != None and end_year != None:

                print("[RestController]ticker : {}".format(ticker))
                print("[RestController]start_year : {}".format(start_year))
                print("[RestController]end_year : {}".format(end_year))
                return self.getDividendHistory(ticker, start_year, end_year)
            else:
                return self.makeResultJson(RES_FAIL_PARAM_ERR)

        #종가 이력 구하기
        elif service_name == "getClosePriceHistory":

            symbol = request.args.get('symbol')

            if symbol != None :
                return self.getClosePriceHistory(symbol)
            else:
                return self.makeResultJson(RES_FAIL_PARAM_ERR)

        #뉴스 구하기
        elif service_name == "getNewsByTicker":

            ticker = request.args.get('ticker')

            if ticker != None:
                return self.getNewsByTicker(ticker)
            else:
                return self.makeResultJson(RES_FAIL_PARAM_ERR)

        #재무정보 구하기
        elif service_name == "getFinanceInfo":

            ticker = request.args.get('ticker')

            if ticker != None:
                return self.getFinanceInfo(ticker)
            else:
                return self.makeResultJson(RES_FAIL_PARAM_ERR)

        #배당킹 구하기
        elif service_name == "getDividendKingTickerList":
            return self.getDividendKingListFromDB()

        #배당 귀족 구하기
        elif service_name == "getDividendAristocratsList":
            return self.getDividendAristocratListFromDB()

        # 원달러 환율
        elif service_name == "getKRWExchangeRate":
            return self.getKRWExchangeRate()

        # 키워드 완성
        elif service_name == "getRecommendKeyword":

            keyword = request.args.get('keyword')

            if keyword != None:
                return self.getRecommendKeyword(keyword)
            else:
                return self.makeResultJson(RES_FAIL_PARAM_ERR)

        # 기업 요약 정보
        elif service_name == "getCompanySummaryInfo":

            symbol = request.args.get('symbol')
            if symbol != None:
                return self.getCompanySummaryInfo(symbol)
            else:
                return self.makeResultJson(RES_FAIL_PARAM_ERR)

        elif service_name == "getMontlyDividendsData":
            from_year = request.args.get('from_year')
            from_month = request.args.get('from_month')
            to_year = request.args.get('to_year')
            to_month = request.args.get('to_month')

            if from_year != None and from_month != None and to_year != None and to_month != None:
                return self.getMontlyDividendsInfoFromDB(from_year, from_month, to_year, to_month)
            else :
                return self.makeResultJson(RES_FAIL_PARAM_ERR)

            #def getMontlyDividendsInfoFromDB(self, from_year : int, from_month : int, to_year : int, to_month : int):


            return self.getMontlyDividendsInfoFromDB()

        #최근 종가
        #http://15.164.248.209:20000/rest/getLatestClosePrice?symbol=ko
        elif service_name == "getLatestClosePrice":
            symbol = request.args.get('symbol')
            if symbol != None:
                return self.getLatestClosePrice(symbol)
            else:
                return self.makeResultJson(RES_FAIL_PARAM_ERR)


        # ex) http://15.164.248.209:20000/rest/getMultipleDividendsInfo?symbol_list=1,2
        elif service_name == "getMultipleDividendsInfo":
            symbol_list = request.args.get('symbol_list').split(',')

            if len(symbol_list) > 0 :
                return self.getMultipleDividendsInfoFromDB(symbol_list)
            else :
                return self.makeResultJson(RES_FAIL_PARAM_ERR)


    # 결과 json을 생성해주는 함수
    def makeResultJson(self, res_code : int, data : dict = dict()) -> dict:

        result_dict = dict()
        result_dict["resultCode"] = res_code
        result_dict["data"] = data

        if res_code is RES_FAIL :
            result_dict["description"] = "실패"
        elif res_code is RES_FAIL_PARAM_ERR :
            result_dict["description"] = "필수 파라미터를 확인해주세요"
        elif res_code is RES_SUCCESS :
            result_dict["description"] = "성공"

        print("makeResutJson result_dict : {}".format(result_dict))

        return jsonify(result_dict)


    # 배당이력 구하는 함수
    def getDividendHistory(self, ticker : str , startYear : int , endYear : int):
        print("@@@@")
        df = pdr.DataReader(ticker, 'yahoo-dividends','{}-01-01'.format(startYear), '{}-12-30'.format(endYear))
        res_json = json.loads(df.to_json())

        return self.makeResultJson(RES_SUCCESS,res_json["value"])


    # 종가이력 구하는 함수

    def getClosePriceHistory(self, symbol : str):

        apikey = "ZSFBXRCOCCY81AN5"
        req_url = "https://www.alphavantage.co/query"

        params = {
            "apikey" : apikey,
            "symbol" : symbol,
            "function" : "TIME_SERIES_DAILY_ADJUSTED",
            "outputsize" : "compact"
        }

        res = requests.get(req_url, params=params)
        res_json = res.json()

        return self.makeResultJson(RES_SUCCESS,res_json)

    # 뉴스 구하는 함수
    def getNewsByTicker(self, ticker : str):

        print("ticker : {}".format(ticker))

        ua = UserAgent()
        headers = {'User-Agent' : ua.random} #변경하고 싶은 user-agent 값

        res = requests.get("https://news.therich.io/api/stock/news?ticker={}".format(ticker), headers=headers)

        if(res.status_code != 200):
            result_dict = dict()
            result_dict["result_code"] = "100"
            result_dict["description"] = "Ticker is not invalid"
            return result_dict

        res_json = res.json()

        news = json.loads(res_json['articles'])

        result_dict = dict()
        result_dict["result_code"] = "200"
        result_dict["description"] = "success"

        data = dict()

        content_list = []

        for idx, content in enumerate(news):
            content_list.append(content)
            #data["news{}".format(idx+1)] = content

        result_dict["data"] = content_list

        return result_dict

    # 재무정보 구하는 함수
    def getFinanceInfo(self, ticker : str):

        apikey = "ZSFBXRCOCCY81AN5"
        req_url = "https://www.alphavantage.co/query"

        params = {
            "apikey" : apikey,
            "symbol" : ticker,
            "function" : "BALANCE_SHEET"
        }

        res = requests.get(req_url, params=params)
        res_json = res.json()

        return self.makeResultJson(RES_SUCCESS, res_json)

    # 배당킹 티커 리스트 구하기
    def getDividendKingTickerList(self) -> list:
        ua = UserAgent()
        headers = {'User-Agent' : ua.random} #변경하고 싶은 user-agent 값

        dividend_king_url = "https://dividendvaluebuilder.com/dividend-kings-list/"
        res = requests.get(dividend_king_url, headers=headers)
        dom = BeautifulSoup(res.content)

        dividend_kings_list_dom = dom.select('.et_pb_section_2 .et_pb_text_inner')[0]
        dividend_kings_list_dom_items = dividend_kings_list_dom.select("p")

        #이놈이 결과값이다.
        dividend_king_ticker_list = []

        for idx, item in enumerate(dividend_kings_list_dom_items):
            #print(item.text)
            #print("idx : {}, item :{}".format(idx, item.text))

            company_name_and_ticker_txt = item.text.split("–")[0]
            #print(item.text.split("–")[0]) #Parker Hannifin  (PH)  이 결과는 요런 형태가 나오게 된다
            #내용 없는거랑 실제 내용 아닌거 재끼고..
            if len(company_name_and_ticker_txt) is not 1 and company_name_and_ticker_txt[0] is not "("  :

                copmany_name = company_name_and_ticker_txt.split("(")[0] #회사 풀네임
                ticker = company_name_and_ticker_txt.split("(")[1].split(")")[0] # 티커만..

                dividend_king_ticker_list.append(ticker)

        return self.makeResultJson(RES_SUCCESS, dividend_king_ticker_list)

    def getDividendAristocratsList(self) -> list :
        ua = UserAgent()
        headers = {'User-Agent': ua.random}  # 변경하고 싶은 user-agent 값

        dividend_aristocrats_url = "https://dividendvaluebuilder.com/dividend-aristocrats-list/"
        res = requests.get(dividend_aristocrats_url, headers=headers)
        dom = BeautifulSoup(res.content)

        dividend_aristocrats_list_dom = dom.select('.et_pb_section_2 .et_pb_text_inner')[0]
        dividend_aristocrats_list_dom_items = dividend_aristocrats_list_dom.select("p")

        # 이놈이 결과값이다.
        dividend_aristocrats_ticker_list = []

        for idx, item in enumerate(dividend_aristocrats_list_dom_items):
            # print(item.text)
            # print("idx : {}, item :{}\n".format(idx, item.text))

            company_name_and_ticker_txt = item.text.split("–")[0]

            # print( "updated" not in company_name_and_ticker_txt)
            # print(item.text.split("–")[0]) #Parker Hannifin  (PH)  이 결과는 요런 형태가 나오게 된다
            # 내용 없는거랑 실제 내용 아닌거 재끼고..
            if len(company_name_and_ticker_txt) is not 1 and "updated" not in company_name_and_ticker_txt:

                company_name = company_name_and_ticker_txt.split("(")[0]

                if len(company_name_and_ticker_txt.split("(")) == 2:
                    ticker = company_name_and_ticker_txt.split("(")[1].split(")")[0]
                    dividend_aristocrats_ticker_list.append(ticker)

        return self.makeResultJson(RES_SUCCESS, dividend_aristocrats_ticker_list)

    def getKRWExchangeRate(self):
        apikey = "ZSFBXRCOCCY81AN5"
        from_currency = "USD"
        to_currency = "KRW"
        function = "CURRENCY_EXCHANGE_RATE"

        req_url = "https://www.alphavantage.co/query"

        params = {
            "apikey" : apikey,
            "from_currency" : from_currency,
            "to_currency" : to_currency,
            "function" : function
        }


        res = requests.get(req_url, params=params)
        res_json = res.json()['Realtime Currency Exchange Rate']

        return self.makeResultJson(RES_SUCCESS, res_json)

    #https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=BA&apikey=ZSFBXRCOCCY81AN5

    def getRecommendKeyword(self, keyword : str):

        apikey = "ZSFBXRCOCCY81AN5"
        req_url = "https://www.alphavantage.co/query"

        params = {
            "apikey" : apikey,
            "keywords" : keyword,
            "function" : "SYMBOL_SEARCH"
        }

        res = requests.get(req_url, params=params)
        res_json = res.json()['bestMatches']
        #HIsssssssss

        return self.makeResultJson(RES_SUCCESS, res_json)

    def getCompanySummaryInfo(self, symbol : str):
        apikey = "ZSFBXRCOCCY81AN5"
        req_url = "https://www.alphavantage.co/query"
        params = {
            "apikey" : apikey,
            "symbol" : symbol,
            "function" : "OVERVIEW"
        }

        res = requests.get(req_url, params=params)
        res_json = res.json()

        return self.makeResultJson(RES_SUCCESS, res_json)


    def getThisMonthDividendStock(self):
        chrome_driver_path = os.getcwd() + "/bin/chromedriver"
        dividend_calaner_url = "https://kr.investing.com/dividends-calendar/"


        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        # UserAgent값을 바꿔줍시다!
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")


        print("driver path : {}".format(chrome_driver_path))

        # 웹 드라이버 인스턴스를 얻는다.
        driver = webdriver.Chrome(chrome_driver_path, options=options)

        print("00000000")


        driver.implicitly_wait(3)

        # 배당 캘린더 url에 접근한다.
        driver.get(dividend_calaner_url)

        # 달력 버튼을 누르고,
        this_week_btn = driver.find_element_by_id("datePickerToggleBtn")
        this_week_btn.click()

        today = datetime.today()

        #시작 날짜 적고... (이달 첫날을 적는다.)
        start_date_edit_text = driver.find_element_by_id("startDate")
        start_date_edit_text.clear()
        start_date_edit_text.send_keys('{}/{}/01'.format(today.year,today.month))

        #끝 날짜 적고.. (이달 말일을 적는다..)
        end_date_edit_text = driver.find_element_by_id("endDate")
        end_date_edit_text.clear()
        end_date_edit_text.send_keys('{}/{}/{}'.format(today.year,today.month,calendar.monthrange(today.year,today.month)[1]))

        print("1111111111")

        #신청합니다 버튼 누른다.
        apply_btn = driver.find_element_by_id("applyBtn")
        apply_btn.click()

        for idx in range(5):

            #로딩해야되니까 3초정도 기다린다.
            #driver.implicitly_wait(5)

            #그리고 창을 맨 아래로 내린다.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-200);")

        #로딩이 다 되면 데이터들을 긁어온다.


        time.sleep(3)


        print("2222222222")


        dom = BeautifulSoup(driver.page_source, 'html.parser')

        #뭔 이상한 팝업이 뜨는데 포커스 없어져서, 이놈 제거
        driver.execute_script("document.getElementsByClassName('generalOverlay')[0].style.display = 'none';")
        dividends_table = dom.select('#dividendsCalendarData')
        items = dividends_table[0].select('tr')

        result_stocks_list = []

        for idx, item in enumerate(items):

            if item.find_all("td", {"class": "flag"}):
                #print(item.findAll("td")[0])

                item_data = item.findAll("td")
                ticker = item_data[1].text.split("(")[1].split(")")[0] #티커
                dividend_date = item_data[2].text #배당락일
                allocation = item_data[3].text  #배당액
                dividend_payment_date = item_data[5].text #배당지급일
                dividend_payment_rate = item_data[6].text

                single_item_dict = dict()
                single_item_dict["ticker"] = ticker
                single_item_dict["dividend_date"] = dividend_date
                single_item_dict["allocation"] = allocation
                single_item_dict["dividend_payment_date"] = dividend_payment_date
                single_item_dict["dividend_payment_rate"] = dividend_payment_rate

                print(single_item_dict)

                result_stocks_list.append(single_item_dict)

        return self.makeResultJson(RES_SUCCESS, result_stocks_list)

    # 월별 배당정보 DB에서 가져오는 함수
    def getMontlyDividendsInfoFromDB(self, from_year : int, from_month : int, to_year : int, to_month : int):

        conn = pymysql.connect(host=HOST, user= USERNAME, password=PASSWORD, db=DB_NAME,charset='utf8')
        cursor = conn.cursor()

        result_dict = dict()

        sql = "SELECT * FROM `finance_info` WHERE `dividends_date` BETWEEN '{}-{}-01' AND '{}-{}-31' LIMIT 0,1000;\
        ".format(from_year, from_month, to_year, to_month)

        cursor.execute(sql)
        result = cursor.fetchall()
        for row_data in result:

            #result_dict[row_data[0]] = "1"
            symbol = str(row_data[0])
            result_dict[symbol] = {
                "name" : row_data[1],
                "dividends" : row_data[2],
                "dividends_rate" : row_data[3],
                "dividends_date" : row_data[4],
                "payment_date" : row_data[5],
                "hot_dividends" : row_data[6],
                "type" : row_data[7]
            }
            #print(row_data[0])

        conn.close()

        return self.makeResultJson(RES_SUCCESS, result_dict)

    # 배당킹 리스트 가져오는 함수
    def getDividendKingListFromDB(self):

        conn = pymysql.connect(host=HOST, user= USERNAME, password=PASSWORD, db=DB_NAME,charset='utf8')
        cursor = conn.cursor()

        result_dict = []

        sql = "SELECT * FROM `finance_info` WHERE `hot_dividends` = '1' LIMIT 0,1000;"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        for row_data in result:
            #print(row_data)
            result_dict.append(row_data[0])
            #print(row_data[0])

        print(result_dict)

        conn.close()
        return self.makeResultJson(RES_SUCCESS, result_dict)

    # 배당귀족 리스트 가져오는 함수
    def getDividendAristocratListFromDB(self):

        conn = pymysql.connect(host=HOST, user= USERNAME, password=PASSWORD, db=DB_NAME,charset='utf8')
        cursor = conn.cursor()

        result_dict = []

        sql = "SELECT * FROM `finance_info` WHERE `hot_dividends` = '2' LIMIT 0,1000;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row_data in result:
            print(row_data)
            result_dict.append(row_data[0])
            #print(row_data[0])

        conn.close()

        return self.makeResultJson(RES_SUCCESS, result_dict)

    def getMultipleDividendsInfoFromDB(self, symbol_list : list):

        conn = pymysql.connect(host=HOST, user= USERNAME, password=PASSWORD, db=DB_NAME,charset='utf8')
        cursor = conn.cursor()

        result_dict = dict()

        sql = self.getQueryStringFromBySymbolList(symbol_list)

        print("sql : {}".format(sql))

        cursor.execute(sql)
        result = cursor.fetchall()

        for row_data in result:
            symbol = str(row_data[0])
            result_dict[symbol] = {
                "name" : row_data[1],
                "dividends" : row_data[2],
                "dividends_rate" : row_data[3],
                "dividends_date" : row_data[4],
                "payment_date" : row_data[5],
                "hot_dividends" : row_data[6],
                "type" : row_data[7]
            }

        print("result_dict : {}".format(result_dict))

        conn.close()

        return self.makeResultJson(RES_SUCCESS, result_dict)



    # list -> query string
    def getQueryStringFromBySymbolList(self, symbols : list) -> str :
        base_sql = "SELECT * FROM `finance_info` WHERE "
        result_sql = ""
        if(len(symbols) == 1):
            result_sql = base_sql + "`symbol` = '{}'".format(symbols[0])
        else:
            for idx, symbol in enumerate(symbols):
                if(idx == 0):
                    result_sql = base_sql + "(`symbol` = '{}'".format(symbols[0])
                else:
                    result_sql = result_sql + " OR `symbol` = '{}'".format(symbols[idx])

        result_sql = result_sql + ")"

        # NULL 체크 루틴 추가
        result_sql = result_sql + "AND `name` IS NOT NULL "
        result_sql = result_sql + "AND `dividends` IS NOT NULL "
        result_sql = result_sql + "AND `dividends_rate` IS NOT NULL "
        result_sql = result_sql + "AND `dividends_date` IS NOT NULL "
        result_sql = result_sql + "AND `payment_date` IS NOT NULL "


        return result_sql

    def getLatestClosePrice(self, symbol : str):

        apikey = "ZSFBXRCOCCY81AN5"
        req_url = "https://www.alphavantage.co/query"

        params = {
            "apikey" : apikey,
            "symbol" : symbol,
            "function" : "GLOBAL_QUOTE"
        }

        res = requests.get(req_url, params=params)
        res_json = res.json()
        close_price = res_json['Global Quote']['05. price']

        result_dict = dict()
        result_dict['close_price'] = close_price

        return self.makeResultJson(RES_SUCCESS, result_dict)
