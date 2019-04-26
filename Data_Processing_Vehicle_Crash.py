# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 20:51:03 2019

@author: jdbul
"""

import pandas as pd
import numpy as np

#%%

file = "Data/Traffic_Crashes_-_Crashes.csv"

crash_data_raw = pd.read_csv(file)


#%%

crash_data_raw.info()


traffic_control_device_values = crash_data_raw['TRAFFIC_CONTROL_DEVICE'].unique()
device_condition_values = crash_data_raw['DEVICE_CONDITION'].unique()
weather_condition_values = crash_data_raw['WEATHER_CONDITION'].unique()
lighting_condition_values = crash_data_raw['LIGHTING_CONDITION'].unique()
trafficway_type_values = crash_data_raw['TRAFFICWAY_TYPE'].unique()
alignment_values = crash_data_raw['ALIGNMENT'].unique()
roadway_surface_condition_values = crash_data_raw['ROADWAY_SURFACE_COND'].unique()
road_defect_values = crash_data_raw['ROAD_DEFECT'].unique()

#%%
"""
Set target to binary
"""

binary_target = []
crash_type_character_vector = crash_data_raw['CRASH_TYPE']

for i in range(len(crash_type_character_vector)):
    if crash_type_character_vector[i] == 'INJURY AND / OR TOW DUE TO CRASH':
        binary_target.append(1)
    elif crash_type_character_vector[i] == 'NO INJURY / DRIVE AWAY':
        binary_target.append(0)
    else:
        binary_target.append('Ruh-Roh Raggy')

assert set(binary_target) == {0, 1}

crash_data = crash_data_raw.iloc[:, 3:14]
crash_data = crash_data.drop(columns = ['FIRST_CRASH_TYPE', 'LANE_CNT'])
crash_data['SEVERE_CRASH'] = binary_target

#%%

crash_data.describe()
np.median(crash_data['POSTED_SPEED_LIMIT'])

raw_speed_limits = list(crash_data['POSTED_SPEED_LIMIT'])
new_speeds = []

for i in range(len(raw_speed_limits)):
    if raw_speed_limits[i] < 15:
        new_speeds.append(15)
    elif raw_speed_limits[i] == 99:
        new_speeds.append(30)
    else:
        new_speeds.append(raw_speed_limits[i])

crash_data['POSTED_SPEED_LIMIT'] = new_speeds

crash_data.isnull().sum()

#%%
"""
Frequency Table for Target variable
"""

vals, counts = np.unique(crash_data['SEVERE_CRASH'], return_counts=True)
print(vals, counts)


#%%
"""
Create Dummies for Categorical Variables
"""

crash_data_w_all_dummies = pd.get_dummies(crash_data)

crash_data_w_all_dummies.columns = crash_data_w_all_dummies.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(',', '_').str.replace(")",'').str.replace("(",'').str.replace("-",'').str.replace('/', '_')

new_column_name_list = []


for i in range(len(crash_data_w_all_dummies.columns)):
    name = crash_data_w_all_dummies.columns[i]
    if len(name) >= 32:
        name = name[0:31]
    else:
        pass
    assert len(name) < 32
    new_column_name_list.append(name)

assert len(new_column_name_list) == len(crash_data_w_all_dummies.columns)
    
crash_data_SAS_ready = crash_data_w_all_dummies

crash_data_SAS_ready.columns = new_column_name_list
    
crash_data_SAS_ready.columns
    
#%%
"""
Write to CSV file for SAS import
"""

#crash_data_SAS_ready.to_csv("Data/crash_data.csv")

    
#%%
"""
Condense dummies based on theory and SAS stepwise results
"""

#%%
"""
Start condensing variables

Traffic control device and condition
"""

crash_data_reduced = crash_data


print(traffic_control_device_values)
print(device_condition_values)

traffic_control_pres_func = []
traffic_control_pres_nonfunc = []


for i in range(len(crash_data_reduced)):
    if crash_data_reduced.TRAFFIC_CONTROL_DEVICE[i] != 'NO CONTROLS' and crash_data_reduced.DEVICE_CONDITION[i] == 'FUNCTIONING PROPERLY':
        traffic_control_pres_func.append(1)
    else:
        traffic_control_pres_func.append(0)

for i in range(len(crash_data_reduced)):
    if crash_data_reduced.TRAFFIC_CONTROL_DEVICE[i] != 'NO CONTROLS' and crash_data_reduced.DEVICE_CONDITION[i] != 'FUNCTIONING PROPERLY':
        traffic_control_pres_nonfunc.append(1)
    else:
        traffic_control_pres_nonfunc.append(0)
        
crash_data_reduced['Traffic_Control_Present_Func'] = traffic_control_pres_func
crash_data_reduced['Traffic_Control_Present_NonFunc'] = traffic_control_pres_nonfunc
crash_data_reduced.drop(columns=['TRAFFIC_CONTROL_DEVICE', 'DEVICE_CONDITION'], inplace=True)

#%%
"""
weather condition
"""

print(weather_condition_values)

weather_condition_column = []

for i in range(len(crash_data_reduced)):
    if crash_data_reduced.WEATHER_CONDITION[i] == 'CLEAR':
        weather_condition_column.append(0)
    else:
        weather_condition_column.append(1)
        
crash_data_reduced['Weather_Cond_Present'] = weather_condition_column
crash_data_reduced.drop(columns=['WEATHER_CONDITION'], inplace=True)

#%%
"""
Lighting
"""

print(lighting_condition_values)

lighting_condition_column = []

for i in range(len(crash_data_reduced)):
    if crash_data_reduced.LIGHTING_CONDITION[i] == 'DAYLIGHT':
        lighting_condition_column.append(0)
    else:
        lighting_condition_column.append(1)
        
crash_data_reduced['Non_Daylight'] = lighting_condition_column
crash_data_reduced.drop(columns=['LIGHTING_CONDITION'], inplace=True)


#%%
"""
Trafficway type
"""

print(alignment_values)

alignment_column = []

for i in range(len(crash_data_reduced)):
    if crash_data_reduced.ALIGNMENT[i] == 'STRAIGHT AND LEVEL':
        alignment_column.append(1)
    else:
        alignment_column.append(0)
        
crash_data_reduced['Straight_Road'] = alignment_column
crash_data_reduced.drop(columns=['ALIGNMENT', 'TRAFFICWAY_TYPE'], inplace=True)

#%%
"""
roadway_surface_condition
"""

print(roadway_surface_condition_values)

roadway_surface_condition_column = []
poor_conditions = ['WET', 'SNOW OR SLUSH' , 'ICE', 'SAND, MUD, DIRT']

for i in range(len(crash_data_reduced)):
    if crash_data_reduced.ROADWAY_SURFACE_COND[i] in poor_conditions:
        roadway_surface_condition_column.append(1)
    else:
        roadway_surface_condition_column.append(0)
        
crash_data_reduced['Poor_Road_Cond'] = roadway_surface_condition_column
crash_data_reduced.drop(columns=['ROADWAY_SURFACE_COND'], inplace=True)


#%%
"""
roadway_surface_condition
"""

print(road_defect_values)

road_defect_column = []

for i in range(len(crash_data_reduced)):
    if crash_data_reduced.ROAD_DEFECT[i] == 'NO DEFECTS':
        road_defect_column.append(0)
    else:
        road_defect_column.append(1)
        
crash_data_reduced['Road_Defect_Pres'] = road_defect_column
crash_data_reduced.drop(columns=['ROAD_DEFECT'], inplace=True)


#%%
"""
Write to CSV file for SAS import
"""

#crash_data_reduced.to_csv("Data/crash_data_dummy_ready.csv")
#sum(crash_data_reduced['Traffic_Control_Present_Func'])
s#sum(crash_data_reduced['Traffic_Control_Present_NonFunc'])










