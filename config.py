###CONFIG FILE###

sender_email = 'timkim.emailbot@gmail.com'
app_password = "qzmwzsqestoctfjk"
receiver_email = ['kimtimt@gmail.com']
# ,'jaskim91@gmail.com', 'naeganayo@yahoo.com', 'naeganayo@gmail.com', 'j3nnipark@gmail.com','timkim.emailbot@gmail.com'

#api keys
wx_api_key = 'd5592d86a4e19a8e0e6ba345ca9cd54f'				#wait... might not need this
gas_api_key = 'dUGdlnW2MF7ydZSPMNLlpZoLNNtwgLdEeu3qb6ho'
bible_api_key = 'BBIZvVIzH2TdKOd3aOTTZ'

#google sheet variables
sheet_id = "1GQFneqAhbudUI542uyb6Nc2XDWtnIdakJLh53lyh3o4"
gs_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
bible_id = "78a9f6124f344018-01"

#other variables

#URLs
wx_url = "https://api.open-meteo.com/v1/forecast"
geo_url = "https://geocoding-api.open-meteo.com/v1/search"
gas_url = "https://api.eia.gov/v2/petroleum/pri/gnd/data"
snow_url = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data"

#locations
wx_locs = ["Tacoma", "Yomitan", "El Paso", "Zarqa"]

#pickle locations
pickle_locs = {'court': ['Sahalie', 'BP Elem', 'BP', 'GameFarm'], 'lights': [1,0,0,1], 'lat': [47.299, 47.302, 47.302, 47.281], 'long': [-122.352, -122.427, -122.440, -122.207]}

#light

#weather codes
wx_code_map = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle (light)",
    53: "Drizzle (moderate)",
    55: "Drizzle (dense)",
    56: "Freezing drizzle (light)",
    57: "Freezing drizzle (dense)",
    61: "Rain (slight)",
    63: "Rain (moderate)",
    65: "Rain (heavy)",
    66: "Freezing rain (light)",
    67: "Freezing rain (heavy)",
    71: "Snow fall (slight)",
    73: "Snow fall (moderate)",
    75: "Snow fall (heavy)",
    77: "Snow grains",
    80: "Rain showers (slight)",
    81: "Rain showers (moderate)",
    82: "Rain showers (violent)",
    85: "Snow showers (slight)",
    86: "Snow showers (heavy)",
    95: "Thunderstorm (slight/moderate)",
    96: "Thunderstorm with hail (slight)",
    99: "Thunderstorm with hail (heavy)",
}

#thanks chat. you the real mvp
wx_icon_map = {
    0: '<img src="https://openweathermap.org/img/wn/01d@2x.png" alt="clear sky">',

    1: '<img src="https://openweathermap.org/img/wn/02d@2x.png" alt="mainly clear">',
    2: '<img src="https://openweathermap.org/img/wn/02d@2x.png" alt="partly cloudy">',
    3: '<img src="https://openweathermap.org/img/wn/03d@2x.png" alt="overcast">',

    45: '<img src="https://openweathermap.org/img/wn/50d@2x.png" alt="fog">',
    48: '<img src="https://openweathermap.org/img/wn/50d@2x.png" alt="fog">',

    51: '<img src="https://openweathermap.org/img/wn/09d@2x.png" alt="drizzle">',
    53: '<img src="https://openweathermap.org/img/wn/09d@2x.png" alt="drizzle">',
    55: '<img src="https://openweathermap.org/img/wn/09d@2x.png" alt="drizzle">',

    56: '<img src="https://openweathermap.org/img/wn/13d@2x.png" alt="freezing drizzle">',
    57: '<img src="https://openweathermap.org/img/wn/13d@2x.png" alt="freezing drizzle">',

    61: '<img src="https://openweathermap.org/img/wn/10d@2x.png" alt="rain">',
    63: '<img src="https://openweathermap.org/img/wn/10d@2x.png" alt="rain">',
    65: '<img src="https://openweathermap.org/img/wn/10d@2x.png" alt="heavy rain">',

    66: '<img src="https://openweathermap.org/img/wn/13d@2x.png" alt="freezing rain">',
    67: '<img src="https://openweathermap.org/img/wn/13d@2x.png" alt="freezing rain">',

    71: '<img src="https://openweathermap.org/img/wn/13d@2x.png" alt="snow">',
    73: '<img src="https://openweathermap.org/img/wn/13d@2x.png" alt="snow">',
    75: '<img src="https://openweathermap.org/img/wn/13d@2x.png" alt="heavy snow">',

    77: '<img src="https://openweathermap.org/img/wn/13d@2x.png" alt="snow grains">',

    80: '<img src="https://openweathermap.org/img/wn/09d@2x.png" alt="rain showers">',
    81: '<img src="https://openweathermap.org/img/wn/09d@2x.png" alt="rain showers">',
    82: '<img src="https://openweathermap.org/img/wn/09d@2x.png" alt="heavy rain showers">',

    85: '<img src="https://openweathermap.org/img/wn/13d@2x.png" alt="snow showers">',
    86: '<img src="https://openweathermap.org/img/wn/13d@2x.png" alt="heavy snow showers">',

    95: '<img src="https://openweathermap.org/img/wn/11d@2x.png" alt="thunderstorm">',
    96: '<img src="https://openweathermap.org/img/wn/11d@2x.png" alt="thunderstorm with hail">',
    99: '<img src="https://openweathermap.org/img/wn/11d@2x.png" alt="heavy thunderstorm with hail">',
}

day_or_not = {
    0: "night",
    1: "day"
}

#UV INDEX
bins = [-1,2, 5, 7, 11, 100]
labels = ['Low', 'Mod', 'High', 'Very High', 'Extreme']
guidance = ['No', 'yes', 'yes!', 'YES!', 'STAY INSIDE']
uv_guidance_map = dict(zip(labels,guidance))



#pickle ball index
wind_bins = [0, 3, 5, 10, 100]
wind_scores = [20, 5, 3, 0]

temp_bins = [-30, 32, 50, 65, 75, 85, 100, 150]
temp_scores = [5, 10, 15, 20, 16, 8, 2]

precip_bins = [0, 3, 25, 50, 75, 100]
precip_scores = [60, 40, 30, 10, 5]


######### PARAMETERS #################
#https://open-meteo.com/en/docs?daily=temperature_2m_max,temperature_2m_min,weather_code,sunrise,sunset,uv_index_max,apparent_temperature_max,apparent_temperature_min,precipitation_probability_max&hourly=&timezone=America%2FLos_Angeles&temperature_unit=fahrenheit&wind_speed_unit=kn&precipitation_unit=inch&latitude=47.2529,26.3358,31.7587,31,NaN&longitude=-122.4443,127.8014,-106.4869,36,NaN
wx_params = {
    'latitude' : [],
    'longitude' : [],
	"daily": ["temperature_2m_max", "temperature_2m_min", "weather_code", "sunrise", "sunset", "uv_index_max", "apparent_temperature_max", "apparent_temperature_min", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max"],
	"current": ["temperature_2m", "is_day", "weather_code"],    
	"timezone": "auto",
	"wind_speed_unit": "kn",
	"temperature_unit": "fahrenheit",
	"precipitation_unit": "inch",
    "forecast_days": 3,
    "wind_speed_unit": "kn"
}

pickle_params = {
	"latitude": [],
	"longitude": [],
	"hourly": ["wind_speed_10m", "precipitation_probability", "apparent_temperature", "temperature_2m", "precipitation", "weather_code", "is_day"],
	"timezone": "America/Los_Angeles",
    "past_days": 0,
	"forecast_days": 1,
	"wind_speed_unit": "kn",
    "temperature_unit": "fahrenheit"
}

gas_params = {
    'frequency': 'weekly',
    'data[0]': 'value',
    'facets[duoarea][]': ['SWA', 'STX'],
    'facets[product][]': 'EPMR',
    'facets[process][]':'PTE',
    'api_key': gas_api_key
}

snow_params = {
	'stationTriplets': ['791:WA:SNTL', '863:WA:SNTL'],
	'elements': ['SNWD', 'SNDN', 'TMAX', 'SNOW'],
    'beginDate': -3,
    'endDate': 0
}

snowfall_params = {
	"latitude": [47.746, 46.638],
	"longitude": [-121.0928, -121.39],
	"daily": ["snowfall_sum", "precipitation_sum", "rain_sum", "wind_gusts_10m_mean", "visibility_mean"],
	"past_days": 3,
	"forecast_days": 2,
}

#snow scoring bins

snow_bins = [-50,60, 70, 80, 90, 110, 150]
snow_guidance = ['dont go', 'might be worth it', 'try it out', 'solid!', 'shred!', 'gnarfest']
#uv_guidance_map = dict(zip(labels,guidance))
