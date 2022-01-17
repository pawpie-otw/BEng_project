import pandas as pd

from typing import Any
from random import choices, choice

from common_functions import extra_funcs

class Education:
    
    number_of_lan_mapper = {
            "no_one": 0,
            "one":1,
            "two":2,
            "tree_or_more":3}
    
    education_mapper = {"Wyższe":"Tertiary",
        "Policealne":"Post-secondary",
        "Średnie zawodowe":"Technical secondary",
        "Średnie ogólnokształcące":"General secondary",
        "Zasadnicze zawodowe":"Basic vocational",
        "Gimnazjalne":"Lower secondary",
        "podstawowe":"primary" ,
        "bez formalnego wykształcenia":"incomplete primary"}

    path_dict = {
        "female_by_age":r"data\education\female_languages_by_age.xlsx",
        "female_by_edu":r"data\education\female_languages_education.xlsx",
        "male_by_age"  :r"data\education\male_languages_by_age.xlsx",
        "male_by_edu"  :r"data\education\male_languages_education.xlsx"}
    
    
    
    
    
    
    @classmethod
    def generate_dataset(cls
                         ,rows
                         ,base_df:pd.DataFrame
                         ,languages:dict
                         ,education:dict
                         )->pd.DataFrame:
                             
        by_age_df = {"female": pd.read_excel(cls.path_dict["female_by_age"], index_col="age"),
            "male": pd.read_excel(cls.path_dict["male_by_age"], index_col="age")}
        by_edu_df = {"male": pd.read_excel(cls.path_dict["male_by_edu"], index_col="edu_level"),
                 "female": pd.read_excel(cls.path_dict["female_by_edu"], index_col="edu_level")}
        
        result = pd.DataFrame()
        
        result["languages"] = pd.Series([cls.generate_number_of_langs(by_age_df[gender], age)
                                            for gender, age in zip(base_df.gender, base_df.age)],dtype=object)
        
        result["education"] = pd.Series([cls.generate_edu_level(by_edu_df[gender], number_of_lang
                                                      ,equal_weight = education["equal_weight"]
                                                      ,map_to_polish=True
                                                      )
                               for gender, number_of_lang in zip(base_df.gender, result["languages"])],dtype=object)
        
        return result
        
        
        
        
        
    @classmethod
    def generate_edu_level(cls
                           ,education_data:pd.DataFrame
                           ,number_of_langs
                           ,equal_weight = False
                           ,map_to_polish = False)-> str:
        
        if number_of_langs is None:
            edu = "Incomplete primary"
        else:    
            column = extra_funcs.find_by_value(cls.number_of_lan_mapper,
                                    number_of_langs)
            
            if equal_weight:
                edu = choice(education_data.index.to_list()) 
            
            else:
                edu = choices(education_data.index.to_list()
                    ,education_data[column].to_list())[0]
            
        if map_to_polish:
            return extra_funcs.find_by_value(cls.education_mapper,
                                      edu)
        return edu
    
    @classmethod
    def generate_number_of_langs(cls, 
                                 language_data:pd.DataFrame,
                                 age:int,
                                 equal_weight:bool = False,
                                 without_none:bool = False)->int:
        if age<18:
            if without_none:
                column = "18 - 24"
            elif age<18:
                return None
        else:
            column = language_data.index[-1] if age>69 else language_data.index[int((age-24)/5)]
        
        if equal_weight:
            return cls.number_of_lan_mapper[choice(language_data.loc[column].index)]
        
        return cls.number_of_lan_mapper[choices(language_data.loc[column].index,
                language_data.loc[column].to_list())[0]]
