from flask_restful import Resource,reqparse
from flask import Flask, render_template, jsonify, request
from fake_useragent import UserAgent

import requests
import os
import sys
import pandas_datareader as pdr
import json


#Response 임시 코드
RES_FAIL = 100 #실패
RES_FAIL_PARAM_ERR = 101 #필수 파라미터 에러
RES_SUCCESS = 200 #성공

class RestController(Resource):

    # Get 요청에 대한 콜백함수
    def get(self, service_name):
        print("[RestController]get request received! service_name : {}".format(service_name))

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

        elif service_name == "getClosePriceHistory":

            ticker = request.args.get('ticker')
            start_year = request.args.get('start_year')
            end_year = request.args.get('end_year')

            if ticker != None and start_year != None and end_year != None:
                return self.getClosePriceHistory(ticker, start_year, end_year)
            else:
                return self.makeResultJson(RES_FAIL_PARAM_ERR)

        elif service_name == "getNewsByTicker":

            ticker = request.args.get('ticker')

            if ticker != None:
                return self.getNewsByTicker(ticker)
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
    def getClosePriceHistory(self, ticker : str , startYear : int , endYear : int):
        df = pdr.DataReader(ticker, 'yahoo','{}-01-01'.format(startYear), '{}-12-30'.format(endYear))
        return self.makeResultJson(RES_SUCCESS,json.loads(df['Close'].to_json()))

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
