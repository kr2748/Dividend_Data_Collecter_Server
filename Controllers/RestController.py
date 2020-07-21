from flask_restful import Resource,reqparse
from flask import Flask, render_template, jsonify, request

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
