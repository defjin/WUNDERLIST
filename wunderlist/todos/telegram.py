import requests

def getID():
    mes=requests.get('https://api.telegram.org/bot945387076:AAFFIwIUMDhmxDSn-0-cHrF8He14WpKFlLQ/getUpdates').json()
    return {i['message']['from']['id'] for i in mes['result']}

def sendMessage(msg, ids=getID()):
    for i in ids:
        requests.get(f'https://api.telegram.org/bot945387076:AAFFIwIUMDhmxDSn-0-cHrF8He14WpKFlLQ/sendMessage?text={msg}&chat_id={i}')