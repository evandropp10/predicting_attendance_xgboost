#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import datetime


# In[ ]:


# Feature Business Day
def business_day(df):
    busday = 0
    if df['weekday'] >= 5 or df['holiday'] == 1:
        busday = 1
    
    #vac = vacation(df['date_hour'])
    #if vac > 0:
    #    busday = 1
    
    return busday

# Classify rain intensity
def classify_rain(precip):
    if precip <= 2:
        rain = 0
    else:
        if precip <= 4:
            rain = 1
        else:
            if precip <= 6:
                rain = 2
            else:
                rain = 3
    return rain

def strike_day(df):
    if df['is_a_strike_ratp_day'] == 1 or df['is_a_strike_sncf_day'] == 1:
        strike = 1
    else:
        strike = 0
        
    return strike

def month_period(day):
    if day <= 10:
        mopr = 1
    elif day <= 20:
        mopr = 2
    else:
        mopr = 3
        
    return mopr

def week_part(df):
    if df['weekday'] <= 2:
        wp = 0
    elif df['weekday'] <= 4:
        wp = 1
    else:
        wp = 2
        
    if df['busday'] == 1:
        wp = 2
        
    return wp

def vacation(dt):
    vc = 0
    
    if dt.month == 8 and dt.day >= 3 and dt.day <= 25:
        vc = 1
    #6
    if dt >= datetime.date(2019, 12, 22) and dt <= datetime.date(2020, 1, 5):
        vc = 2
        
    return vc

def vacation_part(dt):
    vcp = 0
    if dt.month == 8 and dt.day <= 8:
        vcp = 1
    if dt.month == 8 and dt.day > 8 and dt.day <= 16:
        vcp = 2
    if dt.month == 8 and dt.day > 16 and dt.day <= 25:
        vcp = 3
    
    if dt >= datetime.date(2019, 12, 22) and dt <= datetime.date(2020, 1, 27):
        vcp = 1
    if dt >= datetime.date(2019, 12, 28) and dt <= datetime.date(2019, 12, 31):
        vcp = 2
    if dt >= datetime.date(2020, 1, 1) and dt <= datetime.date(2020, 1, 6):
        vcp = 3  
        
    return vcp

def def_type(df):
    if df['busday'] == 1 or df['bushour'] == 1:
        tp = 1
    else:
        tp = 0
    
    return tp

def split_week(x):
    if x <= 7:
        wc = 0
    if x >= 10 and x <= 17:
        wc = 1
    if x >= 15 and x <= 22:
        wc = 2
    if x >= 20 and x <= 27:
        wc = 3
    if x >= 25 and x <= 32:
        wc = 4
    if x >= 30 and x <= 37:
        wc = 5
    if x >= 35 and x <= 42:
        wc = 6
    if x >= 40 and x <= 47:
        wc = 7
    if x >= 45 and x <= 52:
        wc = 8
        
    return wc

def wkday(df):
    wkd = df['weekday']
    if df['busday'] == 1 or df['vacation'] != 0:
        wkd = 9
    
    return wkd

def enrich_number_of_rer_a(df):
    num = df['number_of_rer_a']
    if df['hour'] == 2:
          num = 9
    if df['hour'] == 3:
        num = 13
    if df['hour'] == 4:
        num = 18
        
    return num

def enrich_number_of_metro_1(df):
    num = df['number_of_metro_1']
    if df['hour'] == 3:
        num = 8
    if df['hour'] == 4:
        num = 15
        
    return num

def part_of_day(x):
    # nigth
    if x <= 7 or x >= 20:
        part = 0
    # morning
    if x >= 8 and x <= 12:
        part = 1
    # afternoon
    if x >= 13 and x <= 19:
        part = 2
    
    return part
    
def friday_after_holiday(df):
    if df['busday2'] == 1:
        busday = 1
    else:
        busday = df['busday']
    return busday

    
# In[ ]:


def data_prep(df_path):
    # Load
    print('Starting....')
    print('Running....')
    df_gbs = pd.read_csv(df_path)
    df_floor = pd.read_csv('GBS Building Attendance  - Meeting Room.csv')

    #converting object to datetime and adding separated columns and creating features 
    df_gbs['date_hour'] = pd.to_datetime(df_gbs['date_hour'])
    df_gbs['hour'] = df_gbs['date_hour'].dt.hour
    df_gbs['date'] = df_gbs['date_hour'].dt.date
    df_gbs['year'] = df_gbs['date_hour'].dt.year
    df_gbs['month'] = df_gbs['date_hour'].dt.month
    df_gbs['day'] = df_gbs['date_hour'].dt.day
    df_gbs['weekday'] = df_gbs['date_hour'].dt.weekday
    df_gbs['month_period'] = df_gbs['day'].apply(month_period)
    df_gbs['week_number'] = df_gbs['date_hour'].dt.week
    df_gbs['vacation'] = df_gbs['date_hour'].apply(vacation)
    df_gbs['vacation_part'] = df_gbs['date_hour'].apply(vacation_part)
    df_gbs['day_part'] = df_gbs['hour'].apply(part_of_day)
    
    # Factorizing Strike day attributes
    df_gbs['is_a_strike_ratp_day'] = df_gbs['is_a_strike_ratp_day'].apply(lambda x: 0 if x == 'NO' else 1)
    df_gbs['is_a_strike_sncf_day'] = df_gbs['is_a_strike_sncf_day'].apply(lambda x: 0 if x == 'NO' else 1)
    df_gbs['building_floor_number'] = df_gbs['building_floor'].apply(lambda x: int(x[2:]))

    # Feature Strike - 0 is not and 1 is
    df_gbs['strike_day'] = df_gbs.apply(strike_day, axis=1)
    
    # Merging with floor data
    df_gbs = df_gbs.merge(df_floor, on='building_floor', how='left')
    
    # Transforming NaN
    df_gbs['meeting_room_capacity'] = df_gbs['meeting_room_capacity'].fillna(int(df_gbs['meeting_room_capacity'].mean()))
    df_gbs['meeting_room_number'] = df_gbs['meeting_room_number'].fillna(int(df_gbs['meeting_room_number'].mean()))
    
    # Enrichment number_of_metro : Missing information fo the hours 2 ,3 and 4 of the day
    df_gbs['number_of_rer_a'] = df_gbs[['number_of_rer_a', 'hour']].apply(enrich_number_of_rer_a, axis=1)
    
    # Enrichment number_of_metro_1 : Missing information fo the hours 3 and 4 of the day
    df_gbs['number_of_metro_1'] = df_gbs[['number_of_metro_1', 'hour']].apply(enrich_number_of_metro_1, axis=1)
    

    # Holidays in France
    import holidays
    fr_holidays = holidays.CountryHoliday('FRA')
    df_gbs['holiday'] = df_gbs['date'].apply(lambda x: x in fr_holidays)
    df_gbs['holiday'] = df_gbs['holiday'].apply(lambda x: 0 if x == False else 1)

    # Feature Business Day if 0 is and 1 is not
    df_gbs['busday'] = df_gbs.apply(business_day, axis=1)
    
    # Friday between holiday and wekeend are claissified as not business day, because the attendance are near zero
    df_holiday = df_gbs[df_gbs['holiday'] == 1][['date', 'weekday']]
    df_hol = df_holiday.groupby(['date', 'weekday']).count().reset_index()
    i = 0
    dates=[]
    while i < len(df_hol):
        # Thursday
        if df_hol['weekday'].iloc[i] == 3:

            dates.append(df_hol['date'].iloc[i] + pd.Timedelta(days=1))
        i=i+1
    df_gbs['busday2'] = df_gbs['date'].apply(lambda dt: 1 if dt in dates else 0)
    df_gbs['busday'] = df_gbs[['busday', 'busday2']].apply(friday_after_holiday, axis=1)
    
    # Feature part of week
    df_gbs['week_part'] = df_gbs.apply(week_part, axis=1)
    
    df_gbs['week_class'] = df_gbs['week_number'].apply(split_week)
    
    df_gbs['bushour'] = df_gbs['hour'].apply(lambda x: 0 if x >= 8 and x <= 20 else 1)
    
    df_gbs['type'] = df_gbs[['busday', 'bushour']].apply(def_type, axis=1)
  

    df_gbs['weekday'] = df_gbs[['weekday', 'busday', 'vacation']].apply(wkday, axis=1)
    
    # Cleansing Outliers
    '''
    if 'attendance' in df_gbs:
        df_group = df_gbs.groupby(['fact_building_floor', 'building_floor', 'busday', 'hour'])['attendance'].count().reset_index()
        
        df_gbs2 = pd.DataFrame()
        for i in range(len(df_group)):

            df = df_gbs[(df_gbs['fact_building_floor'] == df_group['fact_building_floor'].iloc[i]) & \
                          (df_gbs['busday'] == df_group['busday'].iloc[i]) & (df_gbs['hour'] == df_group['hour'].iloc[i])]
            
            # Considering 80% in the middle of distribuction
            df = df[(df['attendance'] >= df['attendance'].quantile(0.1)) & (df['attendance'] <= df['attendance'].quantile(0.9))]

            df_gbs2 = df_gbs2.append(df)

        df_gbs = df_gbs2
    '''    
    
    if 'attendance' in df_gbs:
        # Some statistics per week and building floor
        df_group_floor_day = df_gbs.groupby(['building_floor_number', 'date']).count().reset_index()
    
        df_group_floor_day['mean_day'] = 0
        df_group_floor_day['median_day'] = 0
        df_group_floor_day['std_day'] = 0
        i = 0

        while i < len(df_group_floor_day):
            df1 = df_gbs[(df_gbs['building_floor_number'] == df_group_floor_day['building_floor_number'].iloc[i]) & \
                           (df_gbs['date'] == df_group_floor_day['date'].iloc[i])]

            mean = df1['attendance'].mean()
            median = df1['attendance'].median()
            std = df1['attendance'].std()

            df_group_floor_day['mean_day'].iloc[i] = mean
            df_group_floor_day['median_day'].iloc[i] = median
            df_group_floor_day['std_day'].iloc[i] = std

            i = i + 1
            
        df_group_floor_day = df_group_floor_day[['building_floor_number', 'date', 'mean_day', 'median_day', 'std_day']]
    
        df_gbs = df_gbs.merge(df_group_floor_day, on=['building_floor_number','date'], how='left')
        
        df_gbs['stops'] = df_gbs['std_day'].apply(lambda x: 0 if x > 10 else 1)
    
    # Nan in Weather features, enrich with mean of the same month, hour and building floor
    df_gbs = df_gbs.fillna(999)
    
    if 999 in df_gbs['temp_c'].unique():
        
        df_gbs['temp_c'] = df_gbs.apply(lambda df: df_gbs[(df_gbs['year'] == df['year']) & \
                                                          (df_gbs['month'] == df['month']) & \
                                                          (df_gbs['hour']== df['hour']) & \
                                                          (df_gbs['building_floor'] == df['building_floor'])]['temp_c'].mean() \
                                                    if df['temp_c'] == 999 else df['temp_c'], axis = 1)
        df_gbs['high_cloud_cover_per'] = df_gbs.apply(lambda df: df_gbs[(df_gbs['year'] == df['year']) & \
                                                                        (df_gbs['month'] == df['month']) & \
                                                                        (df_gbs['hour'] == df['hour']) & \
                                                                        (df_gbs['building_floor'] == \
                                                                         df['building_floor'])]['high_cloud_cover_per'].mean() \
                                                      if df['high_cloud_cover_per'] == 999 else df['high_cloud_cover_per'], axis = 1)
        df_gbs['medium_cloud_cover_per'] = df_gbs.apply(lambda df: df_gbs[(df_gbs['year'] == df['year']) & \
                                                                          (df_gbs['month'] == df['month']) & \
                                                                          (df_gbs['hour'] == df['hour']) & \
                                                                          (df_gbs['building_floor'] == \
                                                                           df['building_floor'])]['medium_cloud_cover_per'].mean() \
                                                        if df['medium_cloud_cover_per'] == 999 else df['medium_cloud_cover_per'], axis = 1)
        df_gbs['low_cloud_cover_per'] = df_gbs.apply(lambda df: df_gbs[(df_gbs['year'] == df['year']) & \
                                                                       (df_gbs['month'] == df['month']) & \
                                                                       (df_gbs['hour'] == df['hour']) & \
                                                                       (df_gbs['building_floor'] == \
                                                                        df['building_floor'])]['low_cloud_cover_per'].mean() \
                                                     if df['low_cloud_cover_per'] == 999 else df['low_cloud_cover_per'], axis = 1)
        df_gbs['precipitation_mm'] = df_gbs.apply(lambda df: df_gbs[(df_gbs['year'] == df['year']) & \
                                                                    (df_gbs['month'] == df['month']) & \
                                                                    (df_gbs['hour'] == df['hour']) & \
                                                                    (df_gbs['building_floor'] == \
                                                                     df['building_floor'])]['precipitation_mm'].mean() \
                                                  if df['precipitation_mm'] == 999 else df['precipitation_mm'], axis = 1)
        df_gbs['sunshine_duration_h'] = df_gbs.apply(lambda df: df_gbs[(df_gbs['year'] == df['year']) & \
                                                                       (df_gbs['month'] == df['month']) & \
                                                                       (df_gbs['hour'] == df['hour']) & \
                                                                       (df_gbs['building_floor'] == \
                                                                        df['building_floor'])]['sunshine_duration_h'].mean() \
                                                     if df['sunshine_duration_h'] == 999 else df['sunshine_duration_h'], axis = 1)
    
    df_gbs['rain_escale'] = df_gbs['precipitation_mm'].apply(classify_rain)
    
    print('Finished....')
    return df_gbs
    
    
    

