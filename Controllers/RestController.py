from flask_restful import Resource,reqparse
from flask import Flask, render_template, jsonify, request
from fake_useragent import UserAgent

import requests
import os
import sys
import pandas_datareader as pdr
import json
from bs4 import BeautifulSoup
import FinanceDataReader as fdr

#Response 임시 코드
RES_FAIL = 100 #실패
RES_FAIL_PARAM_ERR = 101 #필수 파라미터 에러
RES_SUCCESS = 200 #성공


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
            return self.getDividendKingTickerList()

        #배당 귀족 구하기
        elif service_name == "getDividendAristocratsList":
            return self.getDividendAristocratsList()

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
            "outputsize" : "full"
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

        for idx, content in enumerate(news):
            data["news{}".format(idx+1)] = content

        result_dict["data"] = data

        return result_dict

    # 재무정보 구하는 함수
    def getFinanceInfo(self, ticker : str):

        ua = UserAgent()
        headers = {'User-Agent' : ua.random} #변경하고 싶은 user-agent 값


        target_site_url = "https://finviz.com/quote.ashx?t={}".format(ticker)
        res = requests.get(target_site_url, headers=headers)

        dom = BeautifulSoup(res.content,'html.parser')

        #없는 티커 입력시 예외처리
        if(len(dom.select('.snapshot-td2')) < 10):
            return {"result_code":"100","reason":"Invalid Ticker"}

        #각종 지표 크롤링
        PER = dom.select('.snapshot-td2')[1].text
        EPS_ttm = dom.select('.snapshot-td2')[2].text
        PBR = dom.select('.snapshot-td2')[25].text
        ROE = dom.select('.snapshot-td2')[33].text
        ROA = dom.select('.snapshot-td2')[27].text
        PCR = dom.select('.snapshot-td2')[31].text
        BETA = dom.select('.snapshot-td2')[41].text
        Employees = dom.select('.snapshot-td2')[48].text

        #뉴스 가져오기
        recent_news_title = dom.select("#news-table")[0].select("tr")[0].text
        recent_news_link = dom.select("#news-table")[0].select("tr")[0].select('a')[0].attrs['href']

        result_data = dict()
        result_data["PER"] = PER
        result_data["EPS(ttm)"] = EPS_ttm
        result_data["PBR"] = PBR
        result_data["ROE"] = ROE
        result_data["ROA"] = ROA
        result_data["PCR"] = PCR
        result_data["BETA"] = BETA
        result_data["Employees"] = Employees
        result_data["RecentNewsTitle"] = recent_news_title
        result_data["RecentNewsLink"] = recent_news_link

        return self.makeResultJson(RES_SUCCESS, result_data)

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

        return self.makeResultJson(RES_SUCCESS, res_json)
