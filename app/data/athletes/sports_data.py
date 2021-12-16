import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

from pandas.core.frame import DataFrame

class Data:
    '''This class is used to prepare dfs needed to generate athletes dataset.
    '''
    path_dict = {
        "group_sports": r"data/athletes/2020_gry_zespolowe.xlsx",
        "other": r'data/athletes/2020_pozostale.xlsx',
        "matrial_arts": r"data/athletes/2020_spoty_walki.xlsx",
        "water_sports": r"data/athletes/2020_spoty_wodne.xlsx",
        "winter_sports": r"data/athletes/2020_spoty_zimowe.xlsx"
    }
    
    @staticmethod
    def load_data() -> Tuple[DataFrame]:
        '''This method loads data from xlsx file to dataframe and removes unnecessary fields'''
        group_sports = pd.read_excel(__class__.path_dict['group_sports'],"TABLICA")
        other = pd.read_excel(__class__.path_dict["other"],"TABLICA")
        matrial_arts = pd.read_excel(__class__.path_dict["matrial_arts"],"TABLICA")
        water_sports = pd.read_excel(__class__.path_dict["water_sports"],"TABLICA")
        winter_sports = pd.read_excel(__class__.path_dict['winter_sports'],"TABLICA")
        
        new_group = group_sports[[x for x in group_sports.columns if "Unnamed" not in x]].copy().iloc[3:].drop(columns=["Kod"])
        new_other = other[[x for x in other.columns if "Unnamed" not in x]].copy().iloc[3:].drop(columns=["Kod"])
        new_matrial_arts = matrial_arts[[x for x in matrial_arts.columns if "Unnamed" not in x]].copy().iloc[3:].drop(columns=["Kod"])
        new_water = water_sports[[x for x in water_sports.columns if "Unnamed" not in x]].copy().iloc[3:].drop(columns=["Kod"])
        new_winter = winter_sports[[x for x in winter_sports.columns if "Unnamed" not in x]].copy().iloc[3:].drop(columns=["Kod"])
        
        return (new_group, new_other, new_matrial_arts, new_water, new_winter)


    @staticmethod
    def calculate_total_athletes() -> DataFrame:
        '''
        This method calculates the total number of athletes by province.
        '''
        data = __class__.load_data()
        names = data[0]["Nazwa"].to_frame()
        sum_group = names.join(data[0].drop(columns=["Nazwa"]).sum(axis = 1, skipna = True).to_frame()).rename(columns = {0:"Sporty grupowe"})
        sum_other = names.join(data[1].drop(columns=["Nazwa"]).sum(axis = 1, skipna = True).to_frame()).rename(columns = {0:"Pozostale"})
        sum_matrial_arts = names.join(data[2].drop(columns=["Nazwa"]).sum(axis = 1, skipna = True).to_frame()).rename(columns = {0:"Sporty walki"})
        sum_water = names.join(data[3].drop(columns=["Nazwa"]).sum(axis = 1, skipna = True).to_frame()).rename(columns = {0:"Sporty wodne"})
        sum_winter = names.join(data[4].drop(columns=["Nazwa"]).sum(axis = 1, skipna = True).to_frame()).rename(columns = {0:"Sporty zimowe"})
        total = sum_group.join(sum_other["Pozostale"]).join(sum_matrial_arts["Sporty walki"]).join(sum_water["Sporty wodne"]).join(sum_winter["Sporty zimowe"])
        total['Total'] = total.sum(axis=1)
        total.reset_index(inplace=True, drop=True)
        total.drop([0],inplace=True)
        total.reset_index(inplace=True, drop=True)
        provinces = total[["Nazwa","Total"]]
        return provinces
        
        
    @staticmethod
    def join_all_sports() -> DataFrame:
        ''' Join all sports table into one dataframe.'''
        
        data = __class__.load_data()
        names = data[0]["Nazwa"].to_frame()
        all_sports = names.join(data[0].drop(columns=["Nazwa"])).join(data[1].drop(columns=["Nazwa"])).join(data[2].drop(columns=["Nazwa"])).join(data[3].drop(columns=["Nazwa"])).join(data[4].drop(columns=["Nazwa"]))
        all_sports.reset_index(inplace=True, drop=True)
        all_sports.drop([0], inplace=True)
        all_sports.reset_index(inplace=True, drop=True)
        return all_sports
        