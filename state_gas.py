# Import needed packages
import pandas as pd
from datetime import datetime, timedelta
import requests
import requests_cache
from config import *        #get api key and url

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x-pivot))

def get_gas():

    requests_cache.install_cache(       #check cache first
        "gas_cache",
        expire_after=3600  # seconds (1 hour)
    )

    try:
        # Make the API request for washington state parameters
        response = requests.get(gas_url, params=gas_params)             #will check cache first
        response.raise_for_status()  # Raise an exception for bad status codes
        print("From gas cache:", response.from_cache)

        data_gas = response.json()
        df_gas = pd.DataFrame(data_gas['response']['data'])
        # Convert period to datetime and PST(-8 hours from UTC)
        df_gas['period'] = pd.to_datetime(df_gas['period'])
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    except KeyError as e:
        print(f"Error parsing response data: {e}")


    today = datetime.now()      #todays date

    df_recent = df_gas[df_gas['period']==nearest(df_gas['period'], today)]

    gas_date = df_recent['period'].iloc[0]          #get first value of dataframe date
    last_week = gas_date - timedelta(days = 7)       #get last week relative to first date
    df_last = df_gas[df_gas['period']==nearest(df_gas['period'], last_week)]        #last weeks
    df_recent = pd.concat([df_recent, df_last])           #combine them

    df_recent.rename(columns = {"period": "Date", "area-name": "State", "value": "Price"}, inplace =True)

    df_recent['Date_str'] = df_recent['Date'].dt.strftime("%Y-%m-%d")
    print(df_recent)
    return df_recent