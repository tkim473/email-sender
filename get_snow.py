import requests
from config import *
import requests_cache
import pandas as pd
import openmeteo_requests
from retry_requests import retry
from datetime import datetime, timezone

def get_snow():
	    
    requests_cache.install_cache(       #check cache first
        "snow_cache",
        expire_after=3600  # seconds (1 hour)
    )

    try:
     
     response = requests.get(url = snow_url, params = snow_params)        #will check cache first though
     print("From snow cache:", response.from_cache)
     data_snow = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    except KeyError as e:
        print(f"Error parsing response data: {e}")
    return data_snow            #list of dictionaries 

#convert df_snow into an easier to use dataframe with SNDN, SNWD, and TMAX as columns. 

def convert_df(list):
    #iterate through each item of the list. Each item is a dictionary
    df_vals = pd.DataFrame()
    #nested for loops... oh well.
    loc = 0         #counter to merge dataframes
    for dict1 in list:
        stationTriplet = dict1['stationTriplet']
        list2 = dict1['data']
        df_val1 = pd.DataFrame({'date': []})
        for dict2 in list2:
            el_code = dict2['stationElement']['elementCode']
            df_val2 = pd.DataFrame(dict2['values'])
            df_val2.rename(columns = {'value': el_code}, inplace = True)
            df_val1 = pd.merge(df_val2, df_val1, on = 'date', how = 'left')
        df_val1['statTrip'] = stationTriplet
        df_val1['loc'] = loc
        loc +=1
        df_vals = pd.concat([df_vals, df_val1])
    return df_vals


def get_snowfall():
# Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    responses = openmeteo.weather_api(wx_url, params = snowfall_params)
    # Process first location. Add a for-loop for multiple locations or weather models

    df_snowfall = pd.DataFrame()
    for response in responses:
        
        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_snowfall_sum = daily.Variables(0).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(1).ValuesAsNumpy()
        daily_rain_sum = daily.Variables(2).ValuesAsNumpy()
        daily_wind_gusts_10m_mean = daily.Variables(3).ValuesAsNumpy()
        daily_visibility_mean = daily.Variables(4).ValuesAsNumpy()
        
        daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}

        daily_data["snowfall_sum"] = daily_snowfall_sum
        daily_data["precipitation_sum"] = daily_precipitation_sum
        daily_data["rain_sum"] = daily_rain_sum
        daily_data["wind_gusts_10m_mean"] = daily_wind_gusts_10m_mean
        daily_data["visibility_mean"] = daily_visibility_mean
        daily_data['lat'] = response.Latitude()
        daily_data['long'] = response.Longitude()
        daily_data['loc'] = response.LocationId()

        
        daily_dataframe = pd.DataFrame(data = daily_data)
        df_snowfall = pd.concat([df_snowfall, pd.DataFrame(daily_dataframe)], ignore_index=True)
    return df_snowfall

#combine the two dataframes across date and loc columns
def merge_dfs():
    data_snow = get_snow()
    #convert df_snow so its usable
    df_snow = convert_df(data_snow) 
    df_snow['date'] = pd.to_datetime(df_snow['date'], utc = True)
    df_snowfall = get_snowfall()
    #snowfall dataframe will have future values, so we will merge by left
    df_mergedsnow = pd.merge(df_snowfall,df_snow, on = ['date', 'loc'], how = 'left')            
    return df_mergedsnow



def calc_snowstoke(df):
    start_score = 20
    today = pd.Timestamp.now(tz="UTC").normalize()
    yest = today - pd.Timedelta(days =1)
    tomorrow = today + pd.Timedelta(days = 1)
    loc = df['loc'].unique()

    #create dataframe shell to capture scores for each resort
    df_snowstoke = pd.DataFrame({'resorts': df['statTrip'].dropna().unique()})
    stokescore_list = []
    snowtom_list = []
    snowyest_list = []
    raintom_list = []
    for i in loc:
        SNWD = df.loc[(df['date']==yest) & (df['loc'] ==i), 'SNWD'].iloc[0]     #returns scalar of snow depth from yesterday

        if SNWD > 42:
            SNWD_score = 30
        else:
            SNWD_score = 0

        
        snowfall_sum = df.loc[(df['date'] <= yest) & (df['loc'] == i), 'snowfall_sum'].sum()        #get cumulative snowfall for last 3 days

        if snowfall_sum > 15:
            snowfall_score = 30
        elif snowfall_sum > 10:
            snowfall_score = 20
        elif snowfall_sum > 6:
            snowfall_score = 10
        else:
            snowfall_score = 0

        rain_sum = df.loc[(df['date'] <= yest) & (df['loc'] == i), 'rain_sum'].sum()        #get cumulative snowfall for last 3 days
        
        if rain_sum > 5:
            rain_score = -10
        elif rain_sum > 0:
            rain_score = -5
        else:
            rain_score = 0

        #add points for immediate snowfall the day prior
        snow_yest = df.loc[(df['date'] == yest) & (df['loc'] == i), 'snowfall_sum'].iloc[0]

        if snow_yest > 6:
            snowyest_score = 20
        elif snow_yest >4:
            snowyest_score = 10
        elif snow_yest >2:
            snowyest_score = 5
        else:
            snowyest_score = 0

        #tomorrow scores
        rain_tomorrow = df.loc[(df['date'] == tomorrow) & (df['loc'] == i), 'rain_sum'].iloc[0]
        snow_tomorrow = df.loc[(df['date'] == tomorrow) & (df['loc'] == i), 'snowfall_sum'].iloc[0]
        vis_tomorrow = df.loc[(df['date'] == tomorrow) & (df['loc'] == i), 'visibility_mean'].iloc[0]
        temp_tomorrow = df.loc[(df['date'] == tomorrow) & (df['loc'] == i), 'TMAX'].iloc[0]

        #tomorrow rain
        if rain_tomorrow > 0:
            raintom_score = -15
        else:
            raintom_score = 0 

        #tomorrow snow
        if snow_tomorrow > 6:
            snowtom_score = 10
        elif snow_tomorrow > 4:
            snowtom_score = 5
        else:
            snowtom_score = 0 

        #visibility score
        if vis_tomorrow > 20000:
            vis_score = 5
        else:
            vis_score = 0

        #temp scores
        if temp_tomorrow < 32:
            temp_score = 5
        else:
            temp_score = 0 
        
        total_score = start_score + SNWD_score + snowfall_score + rain_score + snowyest_score + raintom_score + snowtom_score + vis_score + temp_score
        stokescore_list.append(total_score)
        snowtom_list.append(snow_tomorrow)
        raintom_list.append(rain_tomorrow)
        snowyest_list.append(snow_yest)

    #add tomorrows and yesterdays conditions to dataframe
    df_snowstoke['rain_tom'] = snowtom_list
    df_snowstoke['snow_tom'] = raintom_list
    df_snowstoke['snow_yest'] = snowyest_list
    df_snowstoke['stoke_score'] = stokescore_list

    df_snowstoke['stoke_guide'] = pd.cut(df_snowstoke['stoke_score'], bins = snow_bins, labels = snow_guidance)
    return df_snowstoke


