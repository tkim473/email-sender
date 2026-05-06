###TODAYS WEATHER###

from config import *            #get wx api key and wx_params variable and wx_codes
import openmeteo_requests		#import python library 
import pandas as pd
import requests_cache
from retry_requests import retry
import requests					#for geocode
from datetime import datetime, timedelta, UTC	#adjust time for location


def get_wx():

	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	#urls in config file
	#Get lat/longs based on city name given through config file
	loc_data = pd.DataFrame({'names': wx_locs})
	wx_lat = []
	wx_lon = []
	wx_id = []

	geo_session = requests_cache.CachedSession('.geo_cache', expire_after=86400)


	for city in wx_locs:
		geo_response = geo_session.get(geo_url, params = {
			"name": city,
			"count": 1
		}).json()

		if "results" not in geo_response:
			print(f"Skipping {city} (not found)")
			continue

		result = geo_response["results"][0]
		wx_lat.append(round(result['latitude'],4))
		wx_lon.append(round(result['longitude'],4))
		wx_id.append(result['id'])
		
	loc_data['lat'] = wx_lat
	loc_data['lon'] = wx_lon
	loc_data['id'] = wx_id

	#will use lat long lists in parameter of the next API call
	wx_params['latitude'] = wx_lat
	wx_params['longitude'] = wx_lon

	#call API to get response
	responses = openmeteo.weather_api(wx_url, params = wx_params)              #from config. access weather api wrapper

	wx_week_data = pd.DataFrame()
	current_wx = pd.DataFrame()



	
	# Process 4 locations
	for response in responses:
		
		# Process daily data. The order of variables needs to be the same as requested.
		utc_offset = timedelta(seconds=response.UtcOffsetSeconds())
		daily = response.Daily()
		daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
		daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
		daily_weather_code = daily.Variables(2).ValuesAsNumpy()
		daily_sunrise = daily.Variables(3).ValuesInt64AsNumpy()
		daily_sunset = daily.Variables(4).ValuesInt64AsNumpy()
		daily_uv_index_max = daily.Variables(5).ValuesAsNumpy()
		daily_apparent_temperature_max = daily.Variables(6).ValuesAsNumpy()
		daily_apparent_temperature_min = daily.Variables(7).ValuesAsNumpy()
		daily_precipitation_probability_max = daily.Variables(8).ValuesAsNumpy()
		daily_wind_speed_10m_max = daily.Variables(9).ValuesAsNumpy()
		daily_wind_gusts_10m_max = daily.Variables(10).ValuesAsNumpy()

		
		dates = pd.date_range(
			start = pd.to_datetime(daily.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
			end =  pd.to_datetime(daily.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = daily.Interval()),
			inclusive = "left")
		
		daily_data = pd.DataFrame()
		daily_data['DATE'] = dates.tz_localize(None).date	
		daily_data['CITY'] = loc_data['names'][response.LocationId()]			#return city for respective data. Location ID corresponds to index
		daily_data['lat'] = loc_data['lat'][response.LocationId()]				#have lat data
		daily_data['lon'] = loc_data['lon'][response.LocationId()]				#have long data
		daily_data["MAX TEMP"] = daily_temperature_2m_max.round()
		daily_data["MIN TEMP"] = daily_temperature_2m_min.round()
		daily_data["WX_CODE"] = daily_weather_code

		daily_data['sr_utc'] = pd.to_datetime(daily_sunrise, unit='s', utc=True) + utc_offset
		daily_data['ss_utc'] = pd.to_datetime(daily_sunset, unit='s', utc=True) + utc_offset
		daily_data['SUNRISE'] = daily_data['sr_utc'].dt.strftime("%H:%M")
		daily_data['SUNSET'] = daily_data['ss_utc'].dt.strftime("%H:%M")
		daily_data["uv_index"] = daily_uv_index_max
		daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
		daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
		daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
		daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
		daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max

		#process current data. 
		current = response.Current()
		current_temperature_2m = round(current.Variables(0).Value())
		current_is_day = current.Variables(1).Value()
		current_weather_code = current.Variables(2).Value()

		now_utc = datetime.now(UTC)
		local_time = now_utc + utc_offset

		current_dict = {
			'CITY': loc_data['names'][response.LocationId()],
			'TIMESTAMP': local_time,
			'DATE': local_time.strftime("%Y-%m-%d"),
			'LOCAL TIME': local_time.strftime("%H:%M"),
			'TEMP':current_temperature_2m,
			'DAY': current_is_day,
			'WX_CODE': current_weather_code
				  }

		current_df = pd.DataFrame([current_dict])		#wrapping in list	
		wx_week_data = pd.concat([pd.DataFrame(daily_data), wx_week_data], ignore_index = True)
		current_wx = pd.concat([current_df, current_wx], ignore_index = True)

	#add interpreted weather codes and icons outside of for loop
	current_wx['wx_code_itp'] = current_wx['WX_CODE'].map(wx_code_map)
	wx_week_data['wx_code_itp'] = wx_week_data['WX_CODE'].map(wx_code_map)

	current_wx['wx_icon'] = current_wx['WX_CODE'].map(wx_icon_map)
	wx_week_data['wx_icon'] = wx_week_data['WX_CODE'].map(wx_icon_map)

	#day time or not outside of for loop
	current_wx['DAY_NIGHT'] = current_wx['DAY'].map(day_or_not)


	
	return current_wx, wx_week_data		#returns tuple



#put weeklong weather dataframe and return added columns with sunscreen checks
def add_sun_check(week_df, uv_index_col):
	#uv data from google
	week_df['uv_label']= pd.cut(week_df[uv_index_col], bins=bins, labels=labels, include_lowest=False)
	week_df['uv_guide'] = week_df['uv_label'].map(uv_guidance_map)		#uv_guidance map from config file
	
	return week_df

def build_wx():
	df_current, df_week = get_wx()
	df_week = add_sun_check(df_week, "uv_index")
	return df_current, df_week

