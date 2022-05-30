import time
import requests
import os

pwd = os.path.expanduser('~') + '/'
cert_path = pwd + 'Documents/CERT/Line_Notify_stock.txt'
fp = open(cert_path,"r")
zops = fp.readlines()
token = zops[0]  #權杖

def lineNotify(msg):
    cert_path = pwd + 'Documents/CERT/Line_Notify.txt'
    fp = open(cert_path,"r")
    zops = fp.readlines()
    token = zops[0]  #權杖

    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    notify = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return notify.status_code

def lineNotify_fw3_leader(msg):
    cert_path = pwd + 'Documents/CERT/Line_Notify_fw3_leader.txt'
    fp = open(cert_path,"r")
    zops = fp.readlines()
    token = zops[0]  #權杖
    
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    notify = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return notify.status_code


def lineNotify_r(msg):
    cert_path = pwd + 'Documents/CERT/Line_Notify.txt'
    fp = open(cert_path,"r")
    zops = fp.readlines()
    token = zops[0]  #權杖

    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    notify = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return notify.status_code