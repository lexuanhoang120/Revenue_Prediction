from flask import Flask, request, make_response
import pandas as pd
import random
from params import *
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# cors = CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def get_date(date1, date2, CH):
    # CH=4
    print(f'==> store: {CH}')
    data=pd.read_csv(f'output/{CH}_{export_date}.csv')
    data=data[(data['ngay']>=date1) & (data['ngay']<=date2)]

    output={}
    for x in data.index:
        output[data.loc[x, 'ngay']]=data.loc[x, 'doanhthu']
    return output
    
# def get_date(date1, date2, CH):
#     print(f'==> store: {CH}')
#     dates=[str(x).split()[0] for x in pd.date_range(date1, date2, freq='D')]
#     output={}
#     for x in dates:
#         output[x]=random.randint(20, 200)
#     return output

@app.route('/predict', methods=['POST'])
def welcome():
    data = eval(eval(request.data)['body'])
    print(f'==> data: {data}')

    date1=data['date1']
    date2=data['date2']
    CH=data['CH']

    return get_date(date1, date2, CH)

@app.route('/download', methods=['POST'])
def test():
    data = eval(eval(request.data)['body'])
    print('=====', request.data, type(request.data))
    # data = eval(eval(request.data))
    print(f'==> data: {data}')

    date1=data['date1']
    date2=data['date2']
    CH=data['CH']

    data = get_date(date1, date2, CH);

    print(f'==> {data}')

    # resp = pd.DataFrame(data)
    ## convert to dataframe
    date=[]
    val=[]
    for k,v in data.items():
        date.append(k)
        val.append(v)

    df=pd.DataFrame(date)
    df.columns=['ngay']
    df['doanhthu']=val

    resp=make_response(df.to_csv(index=False))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    
    return resp


if __name__ == '__main__':
    app.run()


