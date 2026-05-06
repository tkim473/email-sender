from config import *
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
import io
import base64



def get_pickle():
    pickle_params['latitude'] = pickle_locs['lat']
    pickle_params['longitude'] = pickle_locs['long']
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)


    responses = openmeteo.weather_api(wx_url, params = pickle_params)         #url and params in config file
    # Process first location. Add a for-loop for multiple locations or weather models
    i = 0           #index to iterate through pickle_loc names
    pickledf_list = []

    for response in responses:
        
        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_wind_speed_10m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
        hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()
        hourly_temperature_2m = hourly.Variables(3).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(5).ValuesAsNumpy()
        hourly_is_day = hourly.Variables(6).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
	        start = pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
	        end =  pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
	        freq = pd.Timedelta(seconds = hourly.Interval()),
	        inclusive = "left"
        )}

        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
        hourly_data["precipitation_probability"] = hourly_precipitation_probability
        hourly_data["apparent_temperature"] = hourly_apparent_temperature
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["precipitation"] = hourly_precipitation
        hourly_data["weather_code"] = hourly_weather_code
        hourly_data["is_day"] = hourly_is_day
        hourly_data['court'] = pickle_locs['court'][i]
        hourly_data['lights'] = pickle_locs['lights'][i]
        
        
        #scoring for each variable: wind, precip, temp, day
        hourly_data['wind_score'] = pd.cut(hourly_data['wind_speed_10m'], bins = wind_bins, labels = wind_scores, include_lowest=True).astype(float)
        hourly_data['temp_score'] = pd.cut(hourly_data['temperature_2m'], bins = temp_bins, labels = temp_scores, include_lowest=True).astype(float)
        hourly_data['precip_score'] = pd.cut(hourly_data['precipitation_probability'], bins = precip_bins, labels = precip_scores, include_lowest=True).astype(float)


        hourly_dataframe = pd.DataFrame(data = hourly_data)
        hourly_dataframe.set_index('date', inplace = True)
        hourly_dataframe.loc[hourly_dataframe.between_time("22:00", "06:00").index, 'lights'] = 0
        hourly_dataframe = hourly_dataframe.reset_index()       #resetting it to numerical cause I'm dumb and having issues
        
        hourly_dataframe['light_score'] = hourly_dataframe['is_day'] + hourly_dataframe['lights']
        hourly_dataframe['light_multiplier'] = np.where(hourly_dataframe['light_score'] > 0, 1, 0)
        hourly_dataframe['pickle_score'] = (hourly_dataframe['wind_score'] + hourly_dataframe['temp_score'] + hourly_dataframe['precip_score'])*hourly_dataframe['light_multiplier']

        i += 1 #for court names
        pickledf_list.append(hourly_dataframe)


   
    return pickledf_list





def plot_pickle():
    df_list = get_pickle()
    print(df_list)
    score_list= []
    col_list = []
    for df in df_list:
        court = df['court'].iloc[0]
        new_col = court + '_score'
        df.rename(columns = {'pickle_score': new_col}, inplace = True)
        score_list.append(df[['date', new_col]])
        col_list.append(new_col)

    score_df = reduce(lambda a, b: pd.merge(a, b, on='date', how='left'), score_list)
    
    #for my visualization

    print(f'Lets see all the scores for each court {score_df}')

   
  #  x = np.arange(len(score_df['date']))
   # width = .2
   # multiplier = 0
  #  fig, ax = plt.subplots(layout = 'constrained')

   # print(x)

   # for row in score_df.itertuples():
  #      offset = width * multiplier
  #      print(row[2:6])
  #      rects = ax.bar(x + offset, row[2:6], label = row[1])
  #      ax.bar_label(rects, padding = 3)
  #      multiplier += 1

  #  plt.show()




    ax = score_df.plot(x = 'date', y= col_list, title ='Local Pickle Ball Scores')
    ax.axhspan(80, 100, color = 'green', alpha=.2)
    ax.axhspan(50, 80, color = 'yellow', alpha=.3)
    ax.axhspan(00, 50, color = 'red', alpha=.1)

    #plt.show() #nice to see

    #thanks chat
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64, score_df

plot_pickle()
