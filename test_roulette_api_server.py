#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import requests
import subprocess
def get_requests(url):
    r = requests.get(url)
    if(r.status_code == 200):
        get_result_dict = json.loads(r.content)    
    else:
        aux_str= "REST Status {} inesperado".format(r.status_code)
        assert False, aux_str
    
    return get_result_dict
def post_request(url, body):
    r = requests.post(url = url, data = json.dumps(body))

    return r.text
def test_roulette():
    # --------- numeral a, punto 1, crear ruleta
    input("Enter key to create a new roulette.")
    result_content = post_request("http://127.0.0.1:5000/newRoulette", {"Content-Type": "application/json", "command": "create new roulette"})
    print("---crear una ruleta---\n{}".format(json.dumps(json.loads(result_content), indent=4, sort_keys=False)))
    newRouletteId = json.loads(result_content)["rouletteId"]
    # --------- numeral a, punto 2, Abrir ruleta
    input("Enter key to (authorize) open the roullte.")
    result_content = post_request("http://127.0.0.1:5000/openRoulette", {"Content-Type": "application/json", "command": "open roulette", "rouletteId":newRouletteId})
    print("---Abrir la nueva ruleta---\n{}".format(json.dumps(json.loads(result_content), indent=4, sort_keys=False)))
    # --------- numeral a, punto 3, apostar en ruleta
    userIdData = "wakaUser42"
    betData = {"12":{"betValue":100},"32":{"betValue":200},"black":{"betValue":1000}}
    result_content = post_request("http://127.0.0.1:5000/betInRoulette", {"Content-Type": "application/json", "command": "bet in roulette", "userId":userIdData, "rouletteId":newRouletteId, "userBet":betData})
    input("Enter key to bet {}".format(json.dumps(betData)))
    print("---Apostar en ruleta---\n{}".format(json.dumps(json.loads(result_content), indent=4, sort_keys=False)))
    # --------- numeral a, punto 4, cerrar la ruleta
    input("Enter to (authorize) close the roullete.")
    result_content = post_request("http://127.0.0.1:5000/executeNcloseRoulette", {"Content-Type": "application/json", "command": "close rulette", "rouletteId":newRouletteId})
    print("---Cerrar ruleta---\n{}".format(json.dumps(json.loads(result_content), indent=4, sort_keys=False)))
    # --------- numeral a, punto 5, listar las ruletas
    input("Enter to list all registered roulettes.")
    result_content = post_request("http://127.0.0.1:5000/listRoulettes", {"Content-Type": "application/json", "command": "list roulettes"})
    print("---Listar todas las ruletas---\n{}".format(json.dumps(json.loads(result_content), indent=4, sort_keys=False)))
    # ---------
if __name__ == "__main__":
    test_roulette()

