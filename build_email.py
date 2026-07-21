###EMAIL CONTENT SCRIPT###

#STEP 0: IMPORT MODULES
from datetime import date                                   #import date. now datetime.date() is not required. 
from wx_email import build_wx
from state_gas import get_gas                               #import function that gets state gas price through api
from get_bible import get_verses                            #import function to get verses from google script
from pull_verse import get_display_verse                    
from config import * 
import pandas as pd
from get_snow import merge_dfs, calc_snowstoke              #import functions to get snow data
from pickle_calc import plot_pickle



def generate_daily_report():                                #generate a dict with plain text and html content


    #STEP 1: BUILD EMAIL SUBJECT VARIABLE
    today = date.today()
    # %B gives the full month name
    # %d gives the day of the month
    # %Y gives the four-digit year
    formatted_date = today.strftime("%B %d, %Y")            #strftime is string format time

    email_subject = (f"Tim's Daily Report: {formatted_date}"       #f string lets you use python expressions in {}
    )

    ###################### WX #################
    df_currentwx, df_weekwx = build_wx()


    #function for getting uv guidance
    def get_uv(df,uv_guide, city):
        df_city = df[df['CITY'] == city]
        return df_city[uv_guide].iloc[0] if not df_city.empty else "N/A"
    
    #styling for weather
    def highlight_night(row):
        styles = ['']* len(row)
        if row['DAY_NIGHT'] == 'night':
            styles = ['background-color: black; color: white'] * len(row)
        return styles
    
    df_currentwx.rename(columns={'wx_code_itp': 'SKY COND', 'wx_icon': 'ICON'}, inplace = True)
    df_weekwx.rename(columns={'SUNRISE':'SR', 'SUNSET':'SS','uv_index':'UV INDEX', 'uv_label':'UV LABEL','wx_code_itp': 'SKY COND', 'wx_icon': 'ICON' }, inplace= True)

        
    ######## GAS ###########
    df_gas = get_gas()

    #select columns
    df_gas = df_gas[['Date', 'State', 'Price', 'Date_str']]

    ############BIBLE############################
    verse_list, display_verse = get_verses()
    verse_html = "\n".join(f"{item}, " for item in verse_list)
    
    display_verse_html = get_display_verse(display_verse)

    #################SNOW#############################
    #call merge_dfs function to get dataframe with necessary data for the resorts
    df_mergedsnow = merge_dfs()
    #go through dataframe to calculate scores and extract more relevant data
    df_snowscores = calc_snowstoke(df_mergedsnow)
    print(df_snowscores)


    ###########PICKLE###########
    img_base64, pickle_scores = plot_pickle()


    ###################CONVERT TO HTML#################################
    wx_now_html = (
    df_currentwx[['CITY', 'DATE', 'LOCAL TIME', 'TEMP', 'DAY_NIGHT', 'SKY COND', 'ICON']]
    .style
    .background_gradient(axis=0, gmap=df_currentwx['TEMP'], cmap = 'coolwarm', vmin = 20, vmax = 110)
    .apply(highlight_night, axis=1)
    .to_html(escape=False)
    )

    wx_week_html = (df_weekwx[['CITY', 'DATE', 'MAX TEMP', 'MIN TEMP', 'SR','SS', 'UV INDEX', 'UV LABEL','SKY COND', 'ICON']]
    .style
    .background_gradient(axis=0, gmap=df_weekwx['MAX TEMP'], cmap = 'coolwarm', vmin = 20, vmax = 110)
    .format({
    'MAX TEMP': '{:.0f}',
    'MIN TEMP': '{:.0f}',
    'UV INDEX': '{:.1f}'})      
    .to_html(escape = False)
    )
    
    # Plain Text
    text_template = ("looks like the html broke and this plane text will have to suffice"
    )

    # HTML version
    html_template = f"""
    <!doctype html>
    <html lang="und" dir="auto" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
    <h3>Daily Report: {formatted_date}</h3>
    <p>This awesome daily newsletter will provide you an automated weather forecast, current state gas prices, and bible verses. </p>

    <h3>Weather Right Now</h3>
    {wx_now_html}
    <p>Should you put sunscreen on today?<br>
    Tacoma?: {get_uv(df_weekwx, 'uv_guide', 'Tacoma')}... El Paso?: {get_uv(df_weekwx,'uv_guide','El Paso')}
    ...Okinawa (tomorrow)?: {get_uv(df_weekwx,'uv_guide','Yomitan')}...Jordan?: {get_uv(df_weekwx,'uv_guide','Zarqa')}<br>
    </p>

    <h3>Local Gas Prices</h3>
    <p>
    WA AVG GAS: {df_gas['Price'].iloc[1]} $/GAL as of {df_gas['Date_str'].iloc[1]}<br>
    WA AVG GAS: {df_gas['Price'].iloc[3]} $/GAL as of {df_gas['Date_str'].iloc[3]}<br>
    TX AVG GAS: {df_gas['Price'].iloc[0]} $/GAL as of {df_gas['Date_str'].iloc[0]}<br>
    TX AVG GAS: {df_gas['Price'].iloc[2]} $/GAL as of {df_gas['Date_str'].iloc[2]}<br>
    </p>

    <h3>Weekly Bible Verses</h3>
    <p>{verse_html}<br><br>
      <strong>{display_verse} (NIV)</strong>
      {display_verse_html}</p>
    <p>To adjust the verses displayed: https://forms.gle/qQGYDkyALhoeXeH58</p>
    <h3>Weekly Weather</h3>
    {wx_week_html}

    <h3>Outdoor Activity Indices</h3>
    <p>Pickleball Index<br>
    <img src="data:image/png;base64,{img_base64}">
    Snowboard Index</p>
    <p>Steven's Pass Ski Guidance: {df_snowscores['stoke_guide'][0]}<br>
    Yesterday, it snowed {df_snowscores['snow_yest'][0]} inches<br>
    Tomorrow, exected to rain {df_snowscores['rain_tom'][0]} inches and snow {df_snowscores['snow_tom'][0]} inches</p>
    <p>White Pass Ski Guidance: {df_snowscores['stoke_guide'][1]}<br>
    Yesterday, it snowed {df_snowscores['snow_yest'][1]} inches<br>
    Tomorrow, exected to rain {df_snowscores['rain_tom'][1]} inches and snow {df_snowscores['snow_tom'][1]} inches</p>

    <h3>Useful Links</h3>
    <p>
    Fife Gas Station Price: https://www.gasbuddy.com/station/80969 <br>
    Fed Way Costco: https://www.gasbuddy.com/station/1692 <br> 
    Tahoma Express: https://www.gasbuddy.com/station/33563 <br>
    QFC: https://www.gasbuddy.com/station/154752 <br>
    320 Safeway: https://www.gasbuddy.com/station/142380 <br>
    320 Arco: https://www.gasbuddy.com/station/2156<br>
    </p>

    <h3>About</h3>
    <p>Just a fun project to practice some python code and API calls.</p>
    </html>



    """
    

    return {
        "subject": email_subject,             #email subject
        "text": text_template,                #plain text
        "html": html_template                 #html
    }

#generate_daily_report() for testing