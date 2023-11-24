import os
import pandas as pd
import numpy as np
from tkinter import messagebox 
from data_processing import *

def mapping_idx(df_mea, df_sim):
    """
        Function: mapping 2 dataframe with different sensor naming order 
         - key: the index of sensor from measurement
         - value: the index of sensor from simulation
        Return: a dictionary of index mapping with the same exact name
        e.g:
        sensor_mea = ['M1_4_01', 'M2_2_01', 'M2_4_01', 'M3_1_09', 'M3_1_11', 'M3_1_14', 'M3_2_10']
        sensor_sim = ['M1_4_01', 'M2_2_01', 'M3_2_10', 'M3_1_14', 'M3_1_11', 'M3_1_09', 'M2_4_01']
    
        return {1: 1, 
                2: 6, 
                3: 5, 
                4: 4, 
                5: 3, 
                6: 2}
    """
    #create a list of sensors name
    sensor_sim = find_sensor(list(df_sim.columns))
    sensor_mea = find_sensor(list(df_mea.columns))
    #######
    list_idx_sim, list_idx_mea = [], []
    indices = [i for i in range(len(sensor_sim))]
    dict_sim = dict(zip(sensor_sim, indices))
    sensor_sim_s = sensor_sim.copy()
    n = len(sensor_sim_s)
    for j in range(1,len(sensor_mea)):
        i = 1
        list_idx_mea.append(j)
        while i<n:
            if sensor_mea[j] == sensor_sim_s[i]:
                list_idx_sim.append(dict_sim[sensor_sim_s[i]])
                sensor_sim_s.pop(i)
                n-=1
                break
            i+=1
    return dict(zip(list_idx_mea, list_idx_sim))

def KPI2_fn(measure_path, 
            sim_paths, 
            saved_folder, 
            initital_f=100, 
            end_f=2000):
    """
        Function: calculate KPI2 based on FRAC formula
        Return: 
        - a .csv file with FRAC value of each sensor
        - an updated sim .csv file which re-orders the columns to be the same with the one of measurement file
        if .csv file has the same column order --> not update
    """
    if initital_f >=100 and end_f<=2000:
        if end_f>initital_f:
            df_mea = pd.read_csv(measure_path)
            df_mea = df_mea.drop(columns=[col for col in df_mea.columns if 'Unnamed' in col])
            paths_sim = [sim_paths.split(' ')[i] for i in range(len(sim_paths.split(' ')))]
            for filepath in paths_sim:
                filename = filepath.split('/')[-1].split('.csv')[0]
                df_sim = pd.read_csv(filepath)
                df_sim = df_sim.drop(columns=[col for col in df_sim.columns if 'Unnamed' in col])
                if len(df_mea)!=len(df_sim) and len(df_mea.columns)!=len(df_sim.columns):
                    raise Exception
                else:
                    frac_sensor = []
                    frac_value = []
                    for col in range(1,len(df_mea.columns)):
                        frac_sensor.append(df_mea.columns[col])
                        upper = sum(df_mea[df_mea.columns[col]]*df_sim[df_sim.columns[mapping_idx(df_mea, df_sim)[col]]])
                        lower_left = sum(pow(df_mea[df_mea.columns[col]],2))
                        lower_right = sum(pow(df_sim[df_sim.columns[mapping_idx(df_mea, df_sim)[col]]],2))

                        frac_value.append(pow(upper,2)/(lower_left*lower_right))
                mean_frac = np.mean(frac_value)
                frac_sensor.append('Average')
                frac_value.append(mean_frac)
                df_final = pd.DataFrame(list(zip(frac_sensor, frac_value)), columns=['Sensor name', 'FRAC value'])
                
                try:
                    df_final.to_csv(os.path.join(saved_folder,filename + '_'+ str(initital_f)+'_'+str(end_f)+'_KPI2.csv'), index=False)
                except:
                    messagebox.showerror(title='Error', message='Please close file ' + filename + '_'+ str(initital_f)+'_'+str(end_f)+'_KPI2.csv')
                
                """Create a new simulation file if columns between mea and sim are not the same order"""
                #create a new list with specific order
                specific_order = list(df_mea.columns[1:])
                order = {key: i for i, key in enumerate(specific_order)}
                
                new_column_order = sorted(df_sim.columns[1:], 
                                          key=lambda a: order['_'.join(find_sensor(a))])
                #insert f[Hz] to the first column
                new_column_order.insert(0,'f[Hz]')
                if list(df_sim.columns) != new_column_order:
                    try:
                        df_sim[new_column_order].to_csv(filepath.split('.csv')[0] + '_updated.csv', index=False)
                        messagebox.showinfo(title='Info', message='File ' + filepath + ' is updated due to different order')
                    except:
                        messagebox.showerror(title='Error', message='Please close file ' + filepath.split('.csv')[0] + '_updated.csv')
                ###------

            messagebox.showinfo(title='Result', message='Finish calculation')
        else:
            messagebox.showerror(title='Error', message='End frequency must be higher than initial frequency')
            raise Exception
    else:
        messagebox.showerror(title='Error', message='Initial frequency must be higher than and equal to 100Hz\n End frequency must be lower than and equal to 2000Hz')
        raise Exception
        

def KPI3_fn(measure_path, 
            sim_paths, 
            saved_folder,
            k_SNCurve: int, 
            initital_f=100, 
            end_f=2000):
    """
        Function: calculate KPI3* 
        Return: 
        - a .csv file with KPI3* value of each sensor
        - an updated sim .csv file which re-orders the columns to be the same with the one of measurement file
        if .csv file has the same column order --> not update
    """
    if initital_f >=100 and end_f<=2000:
        if end_f>initital_f:
            df_mea = pd.read_csv(measure_path)
            df_mea = df_mea.drop(columns=[col for col in df_mea.columns if 'Unnamed' in col])
            paths_sim = [sim_paths.split(' ')[i] for i in range(len(sim_paths.split(' ')))]
            for filepath in paths_sim:
                filename = filepath.split('/')[-1].split('.csv')[0]
                df_sim = pd.read_csv(filepath)
                df_sim = df_sim.drop(columns=[col for col in df_sim.columns if 'Unnamed' in col])
                # print(df_sim.head())
                if len(df_mea)!=len(df_sim) and len(df_mea.columns)!=len(df_sim.columns):
                    raise Exception
                else:
                    kpi3_sensor = []
                    kpi3_value = []
                    idx_start = df_sim.index[df_sim['f[Hz]']==initital_f].tolist()[0]
                    idx_end = df_sim.index[df_sim['f[Hz]']==end_f].tolist()[0]
                    for col in range(1,len(df_mea.columns)):
                        # print(mapping_idx(df_mea, df_sim))
                        kpi3_sensor.append(df_mea.columns[col])
                        upper = sum(df_sim.iloc[idx_start:idx_end+1]['f[Hz]']\
                                    *df_sim.iloc[idx_start:idx_end+1][df_sim.columns[mapping_idx(df_mea, df_sim)[col]]].pow(k_SNCurve))
                        lower = sum(df_mea.iloc[idx_start:idx_end+1]['f[Hz]']\
                                    *df_mea.iloc[idx_start:idx_end+1][df_mea.columns[col]].pow(k_SNCurve))

                        kpi3_value.append(upper/lower)
                mean_kpi3 = np.mean(kpi3_value)
                kpi3_sensor.append('Average')
                kpi3_value.append(mean_kpi3)
                df_final = pd.DataFrame(list(zip(kpi3_sensor, kpi3_value)), columns=['Sensor name', 'KPI3* value'])
                
                try:
                    df_final.to_csv(os.path.join(saved_folder,filename + '_'+ str(initital_f)+'_'+str(end_f)+'_KPI3.csv'), index=False)
                except:
                    messagebox.showerror(title='Error', message='Please close file ' + filename + '_'+ str(initital_f)+'_'+str(end_f)+'_KPI3.csv')
                
                """Create a new simulation file if columns between mea and sim are not the same order"""
                #create a new list with specific order
                specific_order = list(df_mea.columns[1:])
                order = {key: i for i, key in enumerate(specific_order)}
                
                new_column_order = sorted(df_sim.columns[1:], 
                                          key=lambda a: order['_'.join(find_sensor(a))])
                #insert f[Hz] to the first column
                new_column_order.insert(0,'f[Hz]')
                if list(df_sim.columns) != new_column_order:
                    try:
                        df_sim[new_column_order].to_csv(filepath.split('.csv')[0] + '_updated.csv', index=False)
                        messagebox.showinfo(title='Info', message='File ' + filepath + ' is updated due to different order')
                    except:
                        messagebox.showerror(title='Error', message='Please close file ' + filepath.split('.csv')[0] + '_updated.csv')
                ###------

            messagebox.showinfo(title='Result', message='Finish calculation')
        else:
            messagebox.showerror(title='Error', message='End frequency must be higher than initial frequency')
            raise Exception
    else:
        messagebox.showerror(title='Error', message='Initial frequency must be higher than and equal to 100Hz\n End frequency must be lower than and equal to 2000Hz')
        raise Exception
