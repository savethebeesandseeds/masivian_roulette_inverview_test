#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
from flask import Flask, jsonify, request
from time import time, gmtime, strftime
import requests
import subprocess
import random
from datetime import datetime
import uuid

class RouletteClass:
    def __init__(self):
        self.rouletteId = str(uuid.uuid4())
        self.isOpen = False
        self.betsInPlay = []
        self.eventSummary = []
        self.totalEarnings = 0
        self.openInDate = None
        self.closeInDate = None
        self.whereIsBall = None
        self.randomSecure = random.SystemRandom()
        self.betFields = {
            '00':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '0':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '1':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '2':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '3':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '4':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '5':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '6':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '7':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '8':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '9':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '10':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '11':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '12':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '13':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '14':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '15':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '16':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '17':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '18':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '19':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '20':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '21':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '22':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '23':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '24':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '25':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '26':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '27':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '28':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '29':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '30':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '31':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '32':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '33':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '34':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            '35':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':True,'isFieldBlack':False,'winRate':36.0},
            '36':{'totalBetValue':0.0,'isRouletteField':True,'isFieldRed':False,'isFieldBlack':True,'winRate':36.0},
            'red':{'totalBetValue':0.0,'isRouletteField':False,'isFieldRed':None,'isFieldBlack':None,'winRate':2.0},
            'black':{'totalBetValue':0.0,'isRouletteField':False,'isFieldRed':None,'isFieldBlack':None,'winRate':2.0}
        }
    def roll_ball(self):
        self.whereIsBall = self.randomSecure.choice([a for a in self.betFields.keys() if self.betFields[a]['isRouletteField']])
    def getWinners(self):
        total_user_wins = 0.0
        self.eventSummary.append("The experiment result for rouletteId {} is {}. ".format(self.rouletteId, self.whereIsBall))
        if(self.whereIsBall is not None and len(self.betsInPlay)>0):
            for a in self.betsInPlay:
                for userOption in a["userBet"].keys():
                    userWins = 0.0
                    userWins += float(a["userBet"][userOption]["betValue"])*float(self.betFields[userOption]["winRate"]) if(self.betFields[self.whereIsBall]["isRouletteField"] and self.betFields[self.whereIsBall]["isFieldRed"] and str(userOption) == 'red') else 0.0
                    userWins += float(a["userBet"][userOption]["betValue"])*float(self.betFields[userOption]["winRate"]) if(self.betFields[self.whereIsBall]["isRouletteField"] and self.betFields[self.whereIsBall]["isFieldBlack"] and str(userOption) == 'black') else 0.0
                    userWins += float(a["userBet"][userOption]["betValue"])*float(self.betFields[userOption]["winRate"]) if(self.betFields[self.whereIsBall]["isRouletteField"] and str(userOption) != 'red' and str(userOption) != 'black' and self.whereIsBall == userOption) else 0.0
                    self.eventSummary.append("In rouletteId: <{}>, in result: <{}>; With betId: <{}>, user bet: <'{}':{}>. RESULT: user <{}>; wins: <{}>".format(
                        self.rouletteId,
                        self.whereIsBall,
                        a["betId"],
                        userOption,
                        a["userBet"][userOption]["betValue"],
                        a["userId"],
                        userWins
                    ))
                    total_user_wins += userWins
        house_wins = sum([self.betFields[a]["totalBetValue"] for a in self.betFields.keys()])-total_user_wins
        self.eventSummary.append("End of report for experiment in rouletteId {}; the house wins: {} ".format(self.rouletteId,house_wins))
    def open_roulette(self):
        self.isOpen = True
        self.openInDate = datetime.utcnow().replace(tzinfo=None).isoformat()
    def play_roulette(self):
        self.roll_ball()
        self.getWinners()
    def close_roulette(self):
        self.whereIsBall = None
        self.betsInPlay = []
        self.isOpen = False
        self.closeInDate = datetime.utcnow().replace(tzinfo=None).isoformat()
    def add_user_bet(self,bet):
        betId = str(uuid.uuid4())
        self.betsInPlay.append({'userId':bet['userId'], 'userBet':bet['userBet'], 'betId':betId})
        for Field in bet['userBet'].keys():
            self.betFields[Field]['totalBetValue'] += float(bet['userBet'][Field]['betValue'])
        
        return betId
def write_to_log(msg=None):
    if(msg is not None):
        with open(os.environ['roulette_api_logPath'],"a",encoding="utf-8") as f:
            f.write("{}".format(msg))
def inicialize_log(msg=None):
    with open(os.path.normpath(os.environ['roulette_api_logPath']), "a+",encoding="utf-8") as _:
        pass
    write_to_log(msg=msg)
def id_roulette_search(search_id):
    for p in allRoulettes:
        if str(p.rouletteId) == str(search_id):
            return p
    
    return None
app = Flask("Roulette REST web service")
@app.route("/newRoulette",methods=['POST'])
def new_roulette_api_fun():
    resolve_data = {}
    try:
        newRoulette = RouletteClass()
        allRoulettes.append(newRoulette)
        resolve_data['data'] = "status finish ::: state created ::: roulette id {}".format(newRoulette)
        resolve_data['rouletteId'] = newRoulette.rouletteId
    except:
        resolve_data = {'status_code':400, 'data':"ERROR", 'meaning':"bad query ERROR"}
    
    return jsonify(resolve_data)
@app.route("/openRoulette",methods=["POST"])
def open_roulette_api_fun():
    resolve_data = {}
    try:
        currentRoulette = id_roulette_search(json.loads(request.data)['rouletteId'])
        if(currentRoulette is None):
            resolve_data = {'status_code':400, 'data':"ERROR", 'meaning':"no roulette found with id {}".format(json.loads(request.data)["rouletteId"])}
        else:
            currentRoulette.open_roulette()
            resolve_data['data'] = "status finish ::: {}".format("state open ::: roulette {}".format(currentRoulette.rouletteId))
    except:
        resolve_data = {'status_code':400, 'data':"ERROR", 'meaning':"bad query ERROR, key value 'rouletteId' needed"}
    
    return jsonify(resolve_data)
@app.route("/betInRoulette",methods=["POST"])
def bet_in_roulette_api_fun():
    resolve_data = {}
    try:
        request_data = json.loads(request.data)
        if("userId" in request_data.keys() and "userBet" in request_data.keys() and "rouletteId" in request_data.keys()):
            currentRoulette = id_roulette_search(request_data['rouletteId'])
            if(currentRoulette is None):
                resolve_data = {'status_code':400, 'data':"ERROR", 'meaning':"no roulette found with id {}".format(json.loads(request.data)["rouletteId"])}
            else:
                if(any([float(request_data['userBet'][a]['betValue'])>float(os.environ['roulette_max_bet_value']) for a in request_data['userBet'].keys()])):
                    resolve_data = {'status_code':400, 'data':"ERROR", 'meaning':"bad query ERROR, impossible beat, too high"}
                else:
                    # print("---current roulette---\t{}".format(json.dumps(currentRoulette.betFields,default=lambda o: o.__dict__, indent=4, sort_keys=False)))
                    if(all([a in currentRoulette.betFields.keys() for a in request_data['userBet'].keys()])):
                        if(all(["betValue" in request_data['userBet'][Field].keys() for Field in request_data['userBet'].keys()])):
                            resolve_data['betId'] = currentRoulette.add_user_bet({"userId":request_data['userId'], "userBet":request_data['userBet']})
                            resolve_data['data'] = "status finish  ::: de puesta: <{}>".format("user: {}, in roulette: {}, and beted: {}".format(request_data['userId'],request_data['rouletteId'], request_data['userBet']))
                        else:
                            resolve_data = {'status_code':400, 'data':"ERROR", 'meaning':"bad query ERROR, unrecognized bet; Please rise a 'betValue' in all Fields"}
                    else:
                        resolve_data = {'status_code':400, 'data':"ERROR", 'meaning':"bad query ERROR, unrecognized bet Field"}
        else:
            resolve_data = {'status_code':400, 'data':"ERROR", 'meaning':"bad query ERROR, key value 'userId', 'userBet' and 'rouletteId' needed"}
    except:
        resolve_data = {'status_code':400, 'data':"ERROR", 'meaning':"bad query ERROR"}
    
    return jsonify(resolve_data)
@app.route("/executeNcloseRoulette",methods=["POST"])
def execute_n_close_roulette_api_fun():
    resolve_data = {}
    try:
        currentRoulette = id_roulette_search(json.loads(request.data)['rouletteId'])
        if(currentRoulette is None):
            resolve_data = {'status_code':400, 'data':"ERROR", 'meaning':"no roulette found with id {}".format(json.loads(request.data)["rouletteId"])}
        else:
            currentRoulette.play_roulette()
            resolve_data['data'] = "status finish ::: {}".format("close roulette {}".format(currentRoulette.rouletteId))
            resolve_data['eventSummary'] = currentRoulette.eventSummary
            resolve_data['Result_whereIsBall'] = currentRoulette.whereIsBall
            currentRoulette.close_roulette()
    except:
        resolve_data = {'status_code':400, 'data':"ERROR", 'meaning':"bad query ERROR, key value 'rouletteId' needed"}
    
    return jsonify(resolve_data)
@app.route("/listRoulettes",methods=["POST"])
def list_roulettes_api_fun():
    resolve_data = {}
    try:
        resolve_data['data'] = "status finish ::: {}".format("list all roulettes")
        resolve_data['all_roulettes'] = [{b:a.__dict__[b] for b in a.__dict__ if b in ["rouletteId", "isOpen"]} for a in allRoulettes]
    except:
        resolve_data = {'status_code':400, 'data':"ERROR", 'meaning':"bad query ERROR,"}
    
    return jsonify(resolve_data)
if __name__ == "__main__":
    os.environ['roulette_api_logPath'] = "Log_file__{}.txt".format(datetime.utcnow().replace(tzinfo=None, microsecond=0).isoformat())
    os.environ['roulette_api_port'] = "5000"
    os.environ['roulette_max_bet_value'] = "10000"
    inicialize_log(msg="Initiating log...")
    allRoulettes = []
    try:
        app.run(port=os.environ['roulette_api_port'])
    except OSError as e:
        if str(e) == "[Error 98] Address already in use":
            print("ERROR: (Address internet port {} already in use) ---please run: \n\t'killall -9 python3' on linux, \n\t'Taskkill /IM python3.exe /F' on Windows".format(os.environ['roulette_api_port']))
        else:
            raise
    write_to_log("no log procedure embedded.")
    write_to_log("Ending log.")