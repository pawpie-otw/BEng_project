from pandas.core.frame import DataFrame
from common_functions.custom_draws import draw_from_df
from data.athletes.sports_data import Data
import pandas as pd


class Athletes:
    
    '''Class for generating athletes dataset'''
    
    data = Data()
    
    @classmethod
    def create_provinces_dict(cls):
        all_sports = cls.data.join_all_sports()
        all_to_dict = all_sports.drop(columns=["Nazwa"])
        sport_names = []
        for col in all_to_dict.columns:
            sport_names.append(col)
        sport_names_series = pd.Series(sport_names)
        dfs_provinces_dict = {}
        for index, row in all_sports.iterrows():
            dfs_provinces_dict[row[0]] = pd.DataFrame({'Name': sport_names_series, 'People': row[1:].reset_index(drop=True)})

        return dfs_provinces_dict
        
    @staticmethod
    def generate_dataset(): 
        dataset = draw_from_df(__class__.data.calculate_total_athletes(),k=1)
        res = {}
        for province in dataset:
            res[province] = draw_from_df(__class__.create_provinces_dict()[province])
        return res
            
                
            
        

        
    
    