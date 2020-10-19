import requests

msg = 'Line Stock Notify'
token = '8YJaUK8zcO3GwEjJVeBWwsUwnhkxHRmfaBNj52VbjeL'  #權杖
headers = {
    "Authorization": "Bearer " + token, 
    "Content-Type" : "application/x-www-form-urlencoded"
}
payload = {'message': msg}
notify = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
if notify.status_code == 200:
    print('發送 LINE Notify 成功！')
else:
    print('發送 LINE Notify 失敗！')
    