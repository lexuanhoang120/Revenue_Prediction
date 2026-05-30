import plotly.express as px
import datetime as dt
import pandas as pd
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
from pandas_profiling import ProfileReport

import itertools
import datetime as dt
from sklearn.metrics import mean_squared_log_error, mean_squared_error

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', -1)
pd.options.mode.chained_assignment = None  # default='warn'


# %%capture
from tqdm import tqdm_notebook as tqdm
tqdm().pandas()


import pandas as pd
import plotly.express as px

import numpy as np
import pandas as pd
from fbprophet import Prophet
import datetime as dt
from sklearn import metrics
import math
import itertools
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from fbprophet.diagnostics import performance_metrics
from fbprophet.diagnostics import cross_validation


def nfl_sunday(ds):
    date = ds
    if (date.weekday() == 5):
        return 1
    else:
        return 0


def nfl_satday(ds):
    date = ds
    if  (date.weekday() == 4):
        return 1
    else:
        return 0

def nfl_monday(ds):
    date = ds
    if  (date.weekday() == 6):
        return 1
    else:
        return 0
    
def visualize_hist_list(x_axis=20, 
                        y_axis=10, 
                        n_bins=100, 
                        data_points=None,
                        display=False):
    """this functions is to visualize histogram of a list to char
    INPUT:  data_points
            x_axis: width of char
            y_axis: height char
            n_bins: number sampling to present for entire list
    OUTPUT: show image to current notebook"""
    # data_points=[x/1000000 for x in data_points]
    # a=[]
    # for x in data_points:
    #     if x<20:
    #         a.append(x)

    # data_points=a
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import figure

    figure(figsize=(x_axis, y_axis), dpi=80)
    (n, bins, patches) = plt.hist(data_points, bins=n_bins)
    #print(n, bins, patches)
    if display:
        plt.show() 
    return n, bins, patches 



independent = pd.DataFrame({
  'holiday': 'independent',
  'ds': pd.to_datetime(['2017-09-02',
                        '2018-09-02', 
                        '2019-09-02',
                        '2020-09-02',
                        '2021-09-02',
                        '2022-09-02',
                       ]),
  'lower_window':-1,
  'upper_window': 0,
})

women = pd.DataFrame({
  'holiday': 'women',
  'ds': pd.to_datetime(['2017-03-08', '2017-10-20', '2017-11-20',
                        '2018-03-08', '2018-10-20', '2018-11-20',
                        '2019-03-08', '2019-10-20', '2019-11-20', 
                        '2020-03-08', '2020-10-20','2020-11-20',
                        '2021-03-08', '2021-10-20','2021-11-20',
                        '2022-03-08', '2022-10-20','2022-11-20',
                        ]),
  'lower_window':-2,
  'upper_window': 0,
})

labor = pd.DataFrame({
  'holiday': 'labor',
  'ds': pd.to_datetime(['2017-04-30', '2017-05-01', 
                        '2018-04-30', '2018-05-01',
                        '2019-04-30', '2019-05-01',
                        '2020-04-30', '2020-05-01',
                        '2021-04-30', '2021-05-01',
                        '2022-04-30', '2022-05-01',
                       ]),
  'lower_window':-3,
  'upper_window': 0,
})

xmas = pd.DataFrame({
  'holiday': 'xmas',
  'ds': pd.to_datetime(['2017-12-24', '2017-12-25', 
                        '2018-12-24', '2018-12-25', 
                        '2019-01-01', '2019-12-24', '2019-12-25',
                        '2020-01-01', '2020-12-24', '2020-12-25', 
                        '2021-01-01', '2021-12-24', '2021-12-25', 
                        '2022-01-01', '2022-12-24', '2022-12-25', 
                        ]),
  'lower_window':-3,
  'upper_window': 0,
})

tet = pd.DataFrame({
  'holiday': 'tet',
  'ds': pd.to_datetime(['2017-01-28', 
                        '2018-02-16', 
                        '2019-02-05', 
                        '2020-01-25', 
                        '2021-02-12', 
                        '2022-02-01', 
                        ]),
  'lower_window':-15,
  'upper_window':0,
})

holidays = pd.concat((independent,
                      women, 
                      labor, 
                      xmas, 
#                       tet,
                     ))

param_grid = {  
    'wseas':[2,3,5,10,25,30,40,50],
    'mseas':[2],
    'yseas':[2,3,5,10,25,30,40,50],
    'seasonality_prior_scale': [0.01, 0.1, 0.3, 0.5, 1.0, 10.0],
    'holiday_prior_scale': [0.01, 0.1, 0.3, 0.5, 1.0, 10.0],
    'changepoint_prior_scale': [0.001, 0.01,0.05,0.1, 0.2, 0.3, 0.5],
    
    
}
all_params = [list(v) for v in itertools.product(*param_grid.values())]


## build grid search
params = [[3, 5, 10, 0.5, 10, 0.5],
          [25, 25, 50, 0.1, 10, 0.1],
          [50, 30, 60, 0.3, 10, 0.3],
          [2, 4, 8, 0.8, 10, 0.8],
          [2, 2, 4, 0.8, 10, 0.8], 
          [2, 3, 25, 0.1, 10, 0.1],
          [5, 2, 2, 0.5, 0.3, 0.01]]

# param_grid = {  
#     'wseas':[2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50],
#     'mseas':[2,3,4,5],
#     'yseas':[2,3,4,5,6,7,8,9,10,15,20,25,30,40,50],
#     'seasonality_prior_scale': [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,10.0],
#     'holiday_prior_scale'    : [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,10.0],
#     'changepoint_prior_scale': [x/100 for x in range(1,1001, 10)],
# }

# all_params = [list(v) for v in itertools.product(*param_grid.values())]

# len(all_params)



def build_model(pars):
    wseas, mseas, yseas, s_prior, h_prior,c_prior= pars
    m = Prophet(growth = 'linear',
#                 seasonality_mode='multiplicative',
                holidays=holidays,
                changepoint_range = 0.9,
                daily_seasonality = False,
                weekly_seasonality = True,
                yearly_seasonality = False,
                holidays_prior_scale =h_prior,
                seasonality_prior_scale = s_prior,
                changepoint_prior_scale = c_prior
                    
                   )
        
    m = m.add_seasonality(
        name = 'weekly',
        period=7,
        fourier_order = wseas)


    m = m.add_seasonality(
        name = 'yearly',
        period=365.25,
        fourier_order = yseas)
    m.add_regressor('nfl_sunday')
    return m


def onecolfcst(current_col, params):  
    
    best_error = np.inf
    best_params = ()
    best_val_forecast = 0
    
    current_data = pd.DataFrame({
        'ds' : train.ngay,
        'y' : train[current_col],
        "nfl_sunday": train['nfl_sunday'],
        "nfl_monday": train['nfl_monday']
    })
    rmses = []
    for pars in tqdm(params):
        m = build_model(pars)  
        m.fit(current_data)
        df_cv = cross_validation(m, cutoffs=cutoffs, initial=500, horizon='30 days', parallel="processes")
        curerror = performance_metrics(df_cv, rolling_window=1)['mape'].values[0]
        print(pars, curerror)
        rmses.append(curerror)
    result = pd.DataFrame()
    result["params"] = params
    result["rmse"] = rmses
    return result

def predict_model(train, test, params, current_col):
    m = build_model(params)   
    current_data = pd.DataFrame({
        'ds' : list(train.ngay),
        'y' : list(train[current_col]),
        'nfl_sunday' : list(train["nfl_sunday"]),
        'nfl_monday' : list(train["nfl_monday"])})
    
    m.fit(current_data)
    
    predict_feature = pd.DataFrame({
            'ds': test.ngay,
            "nfl_sunday": test['nfl_sunday'],
            "nfl_monday": test['nfl_monday']
        })
    realforecast = m.predict(predict_feature)
    return list(realforecast['yhat'])


def predict_next(train, params, current_col, day = 30):
    m = build_model(params)   
    current_data = pd.DataFrame({
        'ds' : list(train.ngay),
        'y' : list(train[current_col]),
        'nfl_sunday' : list(train["nfl_sunday"]),
        'nfl_monday' : list(train["nfl_monday"])})
    
    m.fit(current_data)
    future = m.make_future_dataframe(periods = day,include_history =False)
    future["nfl_sunday"] = future.ds.apply(nfl_sunday)
    future["nfl_monday"] = future.ds.apply(nfl_monday)
    predict_feature = pd.DataFrame({
            'ds': future.ds,
            "nfl_sunday": future['nfl_sunday'],
            "nfl_monday": future['nfl_monday']
        })
    realforecast = m.predict(predict_feature)
    future["predict"] = list(realforecast['yhat'])
    return future


def roundx(x):
    return round(x/1000000,2)


def draw(df):
    fig = px.line(df,x="ngay", y="doanhthu")
    fig.show()

cutoffs = pd.to_datetime(['2020-07-31'])