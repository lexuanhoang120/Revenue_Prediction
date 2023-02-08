import requests, json

## input to API
date1='2022-04-5'
date2='2022-05-27'
CH='1'

## url of API
url = 'http://127.0.0.1:5000/predict'

## send dict
myDict={
        'date1': date1,
        'date2': date2,
        'CH': CH
}

r = requests.post(url, data=json.dumps(myDict))
print(f'==> output: {r.text}')



